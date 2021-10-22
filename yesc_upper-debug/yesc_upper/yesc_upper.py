#!/usr/bin/env python3
'''yesc_upper main program'''

# -- coding: utf-8 -- for Chinaese comment

# use python3 print fromat
from __future__ import print_function

import sys, os
import binascii
import serial
import serial.tools.list_ports
import time
from time import sleep
import socket
import struct

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QStatusBar, QComboBox, QFileDialog

from ESCBus import ESCBus as esc
import ESCBus

from ui import Ui_MainWindow


SOCKET_HOST = "192.168.42.1"
GB_SOCKET_PORT = 49186
ESC_SPEED_MIN = 1100
ESC_SPEED_MAX = 1900

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    '''main window'''

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle("yesc upper")
        self.setFixedSize(self.width(), self.height())

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.radioButton_udp.setChecked(True)
        self.radioButton_udp.toggled.connect(self.use_udp)
        self.radioButton_uart.setChecked(False)
        self.radioButton_uart.toggled.connect(self.use_uart)
        self.baudrate_CB.setEnabled(False)

        self.comboBox_udp.insertItem(0,"192.168.42.1")
        self.comboBox_udp.insertItem(1,"192.168.42.6")
        self.comboBox_udp.insertItem(2,"0")
        self.comboBox_udp.setCurrentText("192.168.42.1")

        self.udp_port.insertItem(0, "49186")
        self.udp_port.insertItem(1, "14551")
        self.udp_port.setCurrentText("49186")

        self.comboBox_uart = port_combobox(self.comboBox_uart)
        self.comboBox_uart.insertItem(0, "Choose port...")

        self.baudrate_CB.insertItem(0, "9600")
        self.baudrate_CB.insertItem(1, "19200")
        self.baudrate_CB.insertItem(2, "38400")
        self.baudrate_CB.insertItem(3, "57600")
        self.baudrate_CB.insertItem(4, "115200")
        self.baudrate_CB.insertItem(5, "250000")
        self.baudrate_CB.insertItem(6, "500000")
        self.baudrate_CB.insertItem(7, "921600")
        self.baudrate_CB.setCurrentText("250000")

        self.escid_set.insertItem(0, "0")
        self.escid_set.insertItem(1, "1")
        self.escid_set.insertItem(2, "2")
        self.escid_set.insertItem(3, "3")
        self.escid_set.insertItem(4, "4")
        self.escid_set.insertItem(5, "5")
        self.escid_set.insertItem(6, "6")
        self.escid_set.insertItem(7, "7")
        self.escid_set.setCurrentText("0")
        self.esc_id = int(self.escid_set.currentText())

        self.statusBar.showMessage("python version: "+str(sys.version))

        self.button_reserve.clicked.connect(self.reserve_clicked)
        self.button_conn.clicked.connect(self.conn_clicked)
        self.button_clean.clicked.connect(self.clean_clicked)
        self.button_update.clicked.connect(self.update_clicked)
        self.button_tune.clicked.connect(self.tune_clicked)
        self.button_data_escid_set.clicked.connect(self.escid_set_clicked)

        self.widget_enable_control(False)
        self.yesc_connect_flag = False
        self.uart_on_status = False
        self.udp_on_status = False

        self.timer_getdata = QTimer(self)
        self.timer_getdata.timeout.connect(self.get_data)

        self.yesc = esc()
        self.yesc.set_send_callback(self.send_to_yesc)

        self.udp_select_flag = True
        self.udp_flag = False

        # run packet the frist value must be 1100
        self.once_flag = False

        # update file read
        self.update_file_name = None
        self.update_file_size = 0
        self.update_data_pos = 0

        self.speed_set = ESC_SPEED_MIN

        # QSlider's parameters are int type, and range in (0~100)
        self.QSlider_speed_control.valueChanged.connect(self.qslider_val_change_speed)
        self.label_data_speed_set.setNum(self.speed_set)
        self.label_data_speed_control_max.setNum(ESC_SPEED_MAX)

    def widget_enable_control(self,bool_value):
        '''control widget togater'''
        if bool_value:
            self.statusBar.showMessage("yesc connect!")
        else:
            self.statusBar.showMessage("yesc disconnect!")

        self.QSlider_speed_control.setEnabled(bool_value)
        self.button_update.setEnabled(bool_value)
        self.button_tune.setEnabled(bool_value)
        self.escid_set.setEnabled(bool_value)

    def conn_clicked(self):
        if self.udp_select_flag == True:
            self.udp_conn()
        else:
            self.uart_conn()
      
    def reserve_clicked(self):
        if self.udp_select_flag == True:
            self.udp_reserve()
        else:
            self.uart_reserve()
        
    def use_udp(self):
        self.udp_select_flag = True
        self.comboBox_udp.setEnabled(True)
        self.udp_port.setEnabled(True)
        self.comboBox_uart.setEnabled(False)
        self.baudrate_CB.setEnabled(False)
        if self.uart_on_status:
            self.port_state_end()

    def use_uart(self):
        self.udp_select_flag = False
        self.comboBox_udp.setEnabled(False)
        self.udp_port.setEnabled(False)
        self.comboBox_uart.setEnabled(True)
        self.baudrate_CB.setEnabled(True)
        if self.udp_on_status:
            self.port_state_end()

    def send_to_yesc(self,yesc_msg):
        if self.udp_flag == True:
            self.__send_udp_gb(yesc_msg.get_msgbuf())
        else:
            self.port.write(yesc_msg.get_msgbuf())

    def __send_udp_gb(self, c):
        try:
            self.gb_socket_udp.sendto(
                c, (self.gb_socket_host, self.gb_socket_port))
        except Exception as e:
            print("udp send error")
            print(e)

    def __recv_gb(self):
        # UDP each read get the whole of the package.  Read size must cover the maximum package size.
        c = self.gb_socket_udp.recv(512)
        if len(c) > 0:
            return c
    
    def uart_reserve(self):
        '''define click active on open botton (reserve)'''
        if self.uart_on_status:
            try:
                self.timer_getdata.stop()
                self.port.close()
                self.port_state_end()
                return
            except:
                self.statusBar.showMessage('Port operation FAIL')
                self.timer_getdata.stop()
                return
             
        if self.comboBox_uart.currentText() != '':
            port_name = self.comboBox_uart.currentText().split()[0]
        else:
            self.statusBar.showMessage('')
            return

        if (
                self.baudrate_CB.currentText().isdigit() is False
                or int(self.baudrate_CB.currentText()) < 1200
                or int(self.baudrate_CB.currentText()) > 921600
        ):
            self.statusBar.showMessage(
                'Bad baudrate.Baudrate rang: 1200 ~ 921600')
            return
        try:
            self.port = serial.Serial(port_name, int(self.baudrate_CB.currentText()),
                                      stopbits=1, bytesize=8,
                                      parity=serial.PARITY_NONE,
                                      timeout=None, xonxoff=False,
                                      rtscts=False, dsrdtr=False)
            if self.port.is_open:
                self.statusBar.showMessage(
                    "Open  <"+self.port.name+">  Successful.  Format: "
                    + str(self.port.baudrate)+"-8bit-None-1stop")
                self.uart_on_status = True
                self.button_reserve.setText("Disreserve")
                self.widget_enable_control(True)
                self.timer_getdata.start(5)
                self.soft_timer = timer_thread()
                self.soft_timer.start()
                self.soft_timer.signal_flush_data.connect(self.flush_data_label)
                self.soft_timer.signal_msg_request_info.connect(self.send_msg_request_info)
                self.soft_timer.signal_msg_run.connect(self.send_msg_run)

        except:
            self.statusBar.showMessage('Port operation FAIL')
    
    
    
    
    
    
    

    def uart_conn(self):
        '''define click active on open botton'''
        if self.uart_on_status:
            try:
                self.timer_getdata.stop()
                self.port.close()
                self.port_state_end()
                return
            except:
                self.statusBar.showMessage('Port operation FAIL')
                self.timer_getdata.stop()
                return

        if self.comboBox_uart.currentText() != '':
            port_name = self.comboBox_uart.currentText().split()[0]
        else:
            self.statusBar.showMessage('')
            return

        if (
                self.baudrate_CB.currentText().isdigit() is False
                or int(self.baudrate_CB.currentText()) < 1200
                or int(self.baudrate_CB.currentText()) > 921600
        ):
            self.statusBar.showMessage(
                'Bad baudrate.Baudrate rang: 1200 ~ 921600')
            return
        try:
            self.port = serial.Serial(port_name, int(self.baudrate_CB.currentText()),
                                      stopbits=1, bytesize=8,
                                      parity=serial.PARITY_NONE,
                                      timeout=None, xonxoff=False,
                                      rtscts=False, dsrdtr=False)
            if self.port.is_open:
                self.statusBar.showMessage(
                    "Open  <"+self.port.name+">  Successful.  Format: "
                    + str(self.port.baudrate)+"-8bit-None-1stop")
                self.uart_on_status = True
                self.button_conn.setText("Disconn")
                self.widget_enable_control(True)
                self.timer_getdata.start(5)
                self.soft_timer = timer_thread()
                self.soft_timer.start()
                self.soft_timer.signal_flush_data.connect(self.flush_data_label)
                self.soft_timer.signal_msg_request_info.connect(self.send_msg_request_info)
                self.soft_timer.signal_msg_run.connect(self.send_msg_run)

        except:
            self.statusBar.showMessage('Port operation FAIL')
            
    def udp_reserve(self):
        if self.udp_on_status:
            try:
                self.timer_getdata.stop()
                # close udp
                self.port_state_end()
                return
            except:
                self.statusBar.showMessage('Port operation FAIL')
                self.timer_getdata.stop()
                return

        self.gb_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        udp_host_value = self.comboBox_udp.currentText()
        if self.judge_legal_ip(udp_host_value):
            self.gb_socket_host = udp_host_value
        else:
            self.statusBar.showMessage(
                'Bad host ip address,it should be: 192.168.x.x (x>=0)')
            return

        udp_port_value = self.udp_port.currentText()
        if (
                udp_port_value.isdigit() is False
                or int(udp_port_value) < 0
                or int(udp_port_value) > 65535
        ):
            self.statusBar.showMessage(
                'Bad udp port rang: 0 ~ 65535')
            return
        self.gb_socket_port = int(udp_port_value)

        self.gb_socket_udp.settimeout(0.5)
        self.udp_flag = True
        self.statusBar.showMessage('udp connetting')

        print("using udp network")
        self.udp_on_status = True
        self.button_reserve.setText("Disreserve")
        self.widget_enable_control(True)
        self.timer_getdata.start(5)
        self.soft_timer = timer_thread()
        self.soft_timer.start()
        self.soft_timer.signal_flush_data.connect(self.flush_data_label)

    def udp_conn(self):
        if self.udp_on_status:
            try:
                self.timer_getdata.stop()
                # close udp
                self.port_state_end()
                return
            except:
                self.statusBar.showMessage('Port operation FAIL')
                self.timer_getdata.stop()
                return

        self.gb_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        udp_host_value = self.comboBox_udp.currentText()
        if self.judge_legal_ip(udp_host_value):
            self.gb_socket_host = udp_host_value
        else:
            self.statusBar.showMessage(
                'Bad host ip address,it should be: 192.168.x.x (x>=0)')
            return

        udp_port_value = self.udp_port.currentText()
        if (
                udp_port_value.isdigit() is False
                or int(udp_port_value) < 0
                or int(udp_port_value) > 65535
        ):
            self.statusBar.showMessage(
                'Bad udp port rang: 0 ~ 65535')
            return
        self.gb_socket_port = int(udp_port_value)

        self.gb_socket_udp.settimeout(0.5)
        self.udp_flag = True
        self.statusBar.showMessage('udp connetting')

        print("using udp network")
        self.udp_on_status = True
        self.button_conn.setText("Disconn")
        self.widget_enable_control(True)
        self.timer_getdata.start(5)
        self.soft_timer = timer_thread()
        self.soft_timer.start()
        self.soft_timer.signal_flush_data.connect(self.flush_data_label)

    def judge_legal_ip(self,ip_str):
        if '.' not in ip_str:
            return False
        elif ip_str.count('.')!=3:
            return False
        else:
            ip_list = ip_str.split('.')
            if ip_list[0] != "192":
                return False
            if ip_list[1] != "168":
                return False
            if int(ip_list[2]) < 0:
                return False
            if int(ip_list[3]) < 0:
                return False
            return True

    def send_msg_run(self):
        value = [0,0,0,0,0,0]
        value[self.esc_id] = self.speed_set
        try:
            self.yesc.run_send(value)
        except Exception as e:
            print(e)

    def send_msg_tune(self):
        try:
            self.yesc.tune_send(600, 50, 50)
        except Exception as e:
            print(e)

    def send_msg_request_info(self):
        try:
            self.yesc.request_info_send(self.esc_id, 2)
        except Exception as e:
            print(e)

    def qslider_val_change_speed(self, move_value):
        speed_value = (move_value / 100) * (ESC_SPEED_MAX - ESC_SPEED_MIN) + ESC_SPEED_MIN
        self.speed_set = int(speed_value)
        self.label_data_speed_set.setNum(self.speed_set)

    def flush_data_label(self):
        self.qslider_val_change_speed(self.QSlider_speed_control.value())

    def flush_data_qslider(self):
        self.label_data_speed_control_max.setNum(ESC_SPEED_MAX)

    def yesc_msg_handle(self,msg):
        '''handle received yesc msg'''
        # updata process
        if msg.feedback_status == ESCBus.PROTO_OK:
            if msg._type == "MSG_FEEDBACK":
                if msg.command == ESCBus.ESCBUS_MSG_ID_BOOT_SYNC:
                    self.print_to_Tedit("get device \n")
                    self.yesc.get_device_info_send(self.esc_id, ESCBus.PROTO_DEVICE_BL_REV)
                if msg.command == ESCBus.PROTO_CHIP_ERASE:
                    update_data = self.get_update_file_data(self.update_file_name)
                    self.yesc.prog_multi_send(self.esc_id,update_data)
                    self.print_to_Tedit("start to update \n")
                if msg.command == ESCBus.PROTO_PROG_MULTI:
                    if self.update_data_pos != 0:
                        update_data = self.get_update_file_data(self.update_file_name)
                        self.yesc.prog_multi_send(self.esc_id,update_data)
                        if self.update_data_pos != 0:
                            self.print_to_Tedit("process of update : %.3f %% \n" %(self.update_data_pos/self.update_file_size * 100))
                    else:
                        self.yesc.get_crc_send(self.esc_id)
                        self.print_to_Tedit("process of update : 100% \n")
            if msg._type == "DEVICE_FEEDBACK":
                if msg.info <= 5*100:
                    self.yesc.chip_erase_send(self.esc_id)
                    self.print_to_Tedit("erase chip! \n")
            if msg._type == "CRC_FEEDBACK":
                if msg.command == ESCBus.PROTO_GET_CRC:
                    self.yesc.boot_send(self.esc_id)
                    self.print_to_Tedit("reboot! \n")
                    self.print_to_Tedit("update done! \n")
                    self.print_to_Tedit("reconnect! \n")
                    self.conn_clicked()
                    time.sleep(0.5)
                    self.conn_clicked()

        # data parse
        if msg._type == "RUN_INFO":
            self.label_data_esc_id.setNum(round(msg.channelID))
            self.label_data_run_speed.setNum(round(msg.speed))
            self.label_data_run_current.setNum(round(msg.current))

    def get_data(self):
        #get COM data
        if self.udp_flag == False and self.port.is_open:
            try:
                # check buff length
                len = self.port.inWaiting()
                if len:
                    data_bytes = self.port.read(len)
                    # filter the received msgs
                    try:
                        yesc_msg = self.yesc.parse_buffer(data_bytes)
                    except Exception as e:
                        print(e)
                        #pass
                    else:
                        if yesc_msg is not None:
                            self.yesc_connect_flag = True
                            for msg in yesc_msg:
                                self.yesc_msg_handle(msg)
                        else:
                            self.yesc_connect_flag = False
            except Exception as e:
                print(e)
                print("get invaild data. flush data.")
                self.port.flushInput()
                # push 1s statusBar info.
                self.statusBar.showMessage(
                    'Get invaild data. Check your setting.', 1000)
        
        #get UDP data
        if self.udp_flag == True:
            try:
                yesc_msg = self.yesc.parse_buffer(self.__recv_gb())
            except Exception as e:
                #  print(e)
                pass
            else:
                if yesc_msg is not None:
                    self.yesc_connect_flag = True
                    self.statusBar.showMessage("udp connecte success!")
                    self.yesc_msg_handle(msg)
                else:
                    self.yesc_connect_flag = False

    def print_to_Tedit(self, str):
        '''print in text module'''
        # make sure insert to the end.
        cursor = self.text_output.textCursor()
        pos = len(self.text_output.toPlainText())
        cursor.setPosition(pos)
        self.text_output.ensureCursorVisible()
        self.text_output.setTextCursor(cursor)
        # append() will adding a new line. insert to cursor is fine.
        self.text_output.insertPlainText(str)
        # make sure view test button.set cursor to the end of the text.
        cursor = self.text_output.textCursor()
        pos = len(self.text_output.toPlainText())
        cursor.setPosition(pos)
        self.text_output.ensureCursorVisible()
        self.text_output.setTextCursor(cursor)
        # force reflash display.
        app.processEvents()

    def clean_clicked(self):
        '''define click activation of clean button'''
        self.text_output.setPlainText("")
        cursor = self.text_output.textCursor()
        cursor.setPosition(0)
        self.text_output.ensureCursorVisible()
        self.text_output.setTextCursor(cursor)
        # force reflash display.
        app.processEvents()

    def escid_set_clicked(self):
        self.esc_id = int(self.escid_set.currentText())
        self.print_to_Tedit("select ESC ID to %d\n" % (self.esc_id))

    def tune_clicked(self):
        self.send_msg_tune()

    def port_state_end(self):
        '''make port state at end'''
        self.timer_getdata.stop()
        self.soft_timer.delete_timer()
        self.button_conn.setText("CONN")
        self.uart_on_status = False
        self.udp_on_status = False
        self.udp_flag = False
        self.statusBar.showMessage('Port Closed.')
        self.widget_enable_control(False)
        self.yesc_connect_flag = False
    
    def port_state_end(self):
        '''make port state at end'''
        self.timer_getdata.stop()
        self.soft_timer.delete_timer()
        self.button_reserve.setText("Reserve")
        self.uart_on_status = False
        self.udp_on_status = False
        self.udp_flag = False
        self.statusBar.showMessage('Port Closed.')
        self.widget_enable_control(False)
        self.yesc_connect_flag = False


    def read_file_data_len(self, file_name, pos, data_len):
        '''read bin file at pos with data_len, return bytes type data'''
        data_file = open(file_name,"rb")
        data_file.seek(pos,0)
        data_bytes = data_file.read(data_len)
        pos += data_len
        data_file.close()
        return pos, data_bytes

    def get_update_file_data(self, file_name):
        '''get update data from bin file per package'''
        self.update_data_pos, data_bytes = self.read_file_data_len(file_name,self.update_data_pos, ESCBus.ESCBUS_UPDATE_SINGLE_SIZE)
        if len(data_bytes) < ESCBus.ESCBUS_UPDATE_SINGLE_SIZE:
            for i in range(ESCBus.ESCBUS_UPDATE_SINGLE_SIZE - len(data_bytes)):
                data_bytes += 0xFF.to_bytes(length=1,byteorder='little',signed=False)
                self.update_file_read_finished_flag = True
                self.update_data_pos = 0
        return data_bytes

    def update_clicked(self):
        '''choose the update file'''
        self.print_to_Tedit("Choose the update file  ... \n")
        f_name, f_type = QFileDialog.getOpenFileName(
            self, "文件选择", "./", "*.bin;;*")
        if f_name == "":
            self.text_output.clear()
            return
        if f_type != "*.bin":
            self.print_to_Tedit("update file should be bin file, exit! \n")
            return
        else:
            self.update_file_name = f_name
            self.update_file_size = os.path.getsize(f_name)
            self.print_to_Tedit("%s as the bin file,size is %.3f K\n" % (f_name,self.update_file_size * 0.001))
        self.soft_timer.delete_timer()
        self.yesc.boot_sync_send(self.esc_id)
        time.sleep(0.5)
        self.yesc.boot_sync_send(self.esc_id)

#timer handle
class timer_thread(QtCore.QThread):
    signal_msg_request_info = pyqtSignal()
    signal_msg_run = pyqtSignal()
    signal_flush_data = pyqtSignal()
    delete_flag = False

    def __init__(self, parent=None):
        super(timer_thread,self).__init__(parent)
        self._1s_tick = int(time.time())
        self._10ms_tick = int(time.time() * 1000)
        self._100ms_tick = int(time.time() * 1000)

    def run(self):
        print("msg send timer start.")
        #  while True:
        while self.delete_flag == False:
            # limit thread loop 200HZ
            time.sleep(0.005)

            # Sent request_info msg Loop 10Hz
            if int(time.time()*1000) - self._100ms_tick > 100:
                self._100ms_tick = int(time.time()*1000)
                try:
                    self.signal_msg_request_info.emit()
                except Exception as e:
                    print("[Timer_thread] yesc disconnect.")
                    print(e)

            # Sent run msg Loop 100Hz
            if int(time.time()*1000) - self._10ms_tick > 10:
                self._10ms_tick = int(time.time()*1000)
                try:
                    self.signal_msg_run.emit()
                except Exception as e:
                    print("[Timer_thread] yesc disconnect.")
                    print(e)
                    
            # flash data Loop 1Hz
            if int(time.time()) - self._1s_tick > 1:
                self._1s_tick = int(time.time())
                try:
                    self.signal_flush_data.emit()
                except Exception as e:
                    print("[Timer_thread] yesc disconnect.")
                    print(e)

    def delete_timer(self):
        self.delete_flag = True
        print("msg send timer stop.")

# combobox did not had click event，inhert from combobox，and add some function
class port_combobox(QComboBox):
    def __init__(self, parent=None):
        super(port_combobox, self).__init__(parent)
        self.setGeometry(QtCore.QRect(0, 0, 351, 31))

    # Triggered when clicked
    def showPopup(self):
        self.clear()
        index = 0
        # obtain all serial ports accessed, insert into combobox options 
        portlist = self.get_port_list()
        if portlist is not None:
            for i in portlist:
                self.insertItem(index, i)
                index += 1
        QComboBox.showPopup(self)   # pop up option box

    def get_port_list(self):
        ''' obtain all serial ports accessed '''
        try:
            port_list = list(serial.tools.list_ports.comports())
            for port in port_list:
                yield str(port)
        except Exception as e:
            print("Scan Error："+str(e))


def get_byte(data):
    '''compatible PY2/3. Bytes type is str in PY2，need handle after ord() for caculate.'''
    if sys.version_info < (3, 0):
        return ord(data)
    return data


# Main function, generate mainWindow
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
