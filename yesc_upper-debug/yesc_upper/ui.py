# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(451, 488)
        MainWindow.setAcceptDrops(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.text_output = QtWidgets.QTextEdit(self.centralwidget)
        self.text_output.setGeometry(QtCore.QRect(10, 80, 341, 251))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.text_output.setFont(font)
        self.text_output.setObjectName("text_output")
        self.comboBox_uart = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_uart.setGeometry(QtCore.QRect(50, 40, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_uart.setFont(font)
        self.comboBox_uart.setEditable(False)
        self.comboBox_uart.setObjectName("comboBox_uart")
        self.button_clean = QtWidgets.QPushButton(self.centralwidget)
        self.button_clean.setGeometry(QtCore.QRect(360, 140, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.button_clean.setFont(font)
        self.button_clean.setObjectName("button_clean")
        self.baudrate_CB = QtWidgets.QComboBox(self.centralwidget)
        self.baudrate_CB.setEnabled(True)
        self.baudrate_CB.setGeometry(QtCore.QRect(250, 40, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.baudrate_CB.setFont(font)
        self.baudrate_CB.setEditable(True)
        self.baudrate_CB.setObjectName("baudrate_CB")
        self.comboBox_udp = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_udp.setGeometry(QtCore.QRect(50, 0, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_udp.setFont(font)
        self.comboBox_udp.setEditable(True)
        self.comboBox_udp.setObjectName("comboBox_udp")
        self.udp_port = QtWidgets.QComboBox(self.centralwidget)
        self.udp_port.setEnabled(True)
        self.udp_port.setGeometry(QtCore.QRect(250, 0, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.udp_port.setFont(font)
        self.udp_port.setEditable(True)
        self.udp_port.setObjectName("udp_port")
        self.radioButton_udp = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_udp.setGeometry(QtCore.QRect(20, 10, 16, 20))
        self.radioButton_udp.setText("")
        self.radioButton_udp.setObjectName("radioButton_udp")
        self.radioButton_uart = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_uart.setGeometry(QtCore.QRect(20, 40, 16, 30))
        self.radioButton_uart.setText("")
        self.radioButton_uart.setObjectName("radioButton_uart")
        self.QSlider_speed_control = QtWidgets.QSlider(self.centralwidget)
        self.QSlider_speed_control.setGeometry(QtCore.QRect(190, 370, 160, 16))
        self.QSlider_speed_control.setOrientation(QtCore.Qt.Horizontal)
        self.QSlider_speed_control.setObjectName("QSlider_speed_control")
        self.label_pitch_speed_Kp = QtWidgets.QLabel(self.centralwidget)
        self.label_pitch_speed_Kp.setGeometry(QtCore.QRect(10, 370, 31, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_pitch_speed_Kp.setFont(font)
        self.label_pitch_speed_Kp.setObjectName("label_pitch_speed_Kp")
        self.label_data_speed_set = QtWidgets.QLabel(self.centralwidget)
        self.label_data_speed_set.setGeometry(QtCore.QRect(80, 370, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_data_speed_set.setFont(font)
        self.label_data_speed_set.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.label_data_speed_set.setObjectName("label_data_speed_set")
        self.label_data_speed_control_max = QtWidgets.QLabel(self.centralwidget)
        self.label_data_speed_control_max.setGeometry(QtCore.QRect(370, 370, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_data_speed_control_max.setFont(font)
        self.label_data_speed_control_max.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextEditable|QtCore.Qt.TextEditorInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.label_data_speed_control_max.setObjectName("label_data_speed_control_max")
        self.label_speed_control = QtWidgets.QLabel(self.centralwidget)
        self.label_speed_control.setGeometry(QtCore.QRect(0, 340, 141, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_speed_control.setFont(font)
        self.label_speed_control.setObjectName("label_speed_control")
        self.button_conn = QtWidgets.QPushButton(self.centralwidget)
        self.button_conn.setGeometry(QtCore.QRect(360, 0, 81, 61))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.button_conn.setFont(font)
        self.button_conn.setObjectName("button_conn")
        self.label_escid_0 = QtWidgets.QLabel(self.centralwidget)
        self.label_escid_0.setGeometry(QtCore.QRect(270, 336, 81, 30))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_escid_0.setFont(font)
        self.label_escid_0.setObjectName("label_escid_0")
        self.label_data_esc_id = QtWidgets.QLabel(self.centralwidget)
        self.label_data_esc_id.setGeometry(QtCore.QRect(350, 336, 81, 30))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_data_esc_id.setFont(font)
        self.label_data_esc_id.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.label_data_esc_id.setObjectName("label_data_esc_id")
        self.label_data_run_current = QtWidgets.QLabel(self.centralwidget)
        self.label_data_run_current.setGeometry(QtCore.QRect(350, 408, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_data_run_current.setFont(font)
        self.label_data_run_current.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.label_data_run_current.setObjectName("label_data_run_current")
        self.label_run_current = QtWidgets.QLabel(self.centralwidget)
        self.label_run_current.setGeometry(QtCore.QRect(230, 408, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_run_current.setFont(font)
        self.label_run_current.setObjectName("label_run_current")
        self.label_data_run_speed = QtWidgets.QLabel(self.centralwidget)
        self.label_data_run_speed.setGeometry(QtCore.QRect(130, 410, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_data_run_speed.setFont(font)
        self.label_data_run_speed.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.label_data_run_speed.setObjectName("label_data_run_speed")
        self.label_run_speed = QtWidgets.QLabel(self.centralwidget)
        self.label_run_speed.setGeometry(QtCore.QRect(10, 410, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_run_speed.setFont(font)
        self.label_run_speed.setObjectName("label_run_speed")
        self.button_update = QtWidgets.QPushButton(self.centralwidget)
        self.button_update.setGeometry(QtCore.QRect(360, 180, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.button_update.setFont(font)
        self.button_update.setObjectName("button_update")
        self.button_tune = QtWidgets.QPushButton(self.centralwidget)
        self.button_tune.setGeometry(QtCore.QRect(360, 220, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.button_tune.setFont(font)
        self.button_tune.setObjectName("button_tune")
        self.button_data_escid_set = QtWidgets.QPushButton(self.centralwidget)
        self.button_data_escid_set.setGeometry(QtCore.QRect(360, 300, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.button_data_escid_set.setFont(font)
        self.button_data_escid_set.setObjectName("button_data_escid_set")
        self.escid_set = QtWidgets.QComboBox(self.centralwidget)
        self.escid_set.setEnabled(True)
        self.escid_set.setGeometry(QtCore.QRect(360, 260, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.escid_set.setFont(font)
        self.escid_set.setEditable(True)
        self.escid_set.setObjectName("escid_set")
        self.button_reserve = QtWidgets.QPushButton(self.centralwidget)
        self.button_reserve.setGeometry(QtCore.QRect(360, 70, 81, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(13)
        self.button_reserve.setFont(font)
        self.button_reserve.setObjectName("button_reserve")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 451, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button_clean.setText(_translate("MainWindow", "Clean"))
        self.baudrate_CB.setCurrentText(_translate("MainWindow", "115200"))
        self.udp_port.setCurrentText(_translate("MainWindow", "49186"))
        self.label_pitch_speed_Kp.setText(_translate("MainWindow", "set"))
        self.label_data_speed_set.setText(_translate("MainWindow", "0"))
        self.label_data_speed_control_max.setText(_translate("MainWindow", "0"))
        self.label_speed_control.setText(_translate("MainWindow", "Speed Control:"))
        self.button_conn.setText(_translate("MainWindow", "CONN"))
        self.label_escid_0.setText(_translate("MainWindow", "ESC_ID :"))
        self.label_data_esc_id.setText(_translate("MainWindow", "0"))
        self.label_data_run_current.setText(_translate("MainWindow", "0"))
        self.label_run_current.setText(_translate("MainWindow", "run_current :"))
        self.label_data_run_speed.setText(_translate("MainWindow", "0"))
        self.label_run_speed.setText(_translate("MainWindow", "run_speed :"))
        self.button_update.setText(_translate("MainWindow", "Update"))
        self.button_tune.setText(_translate("MainWindow", "Tune"))
        self.button_data_escid_set.setText(_translate("MainWindow", "ESCID Set"))
        self.escid_set.setCurrentText(_translate("MainWindow", "0"))
        self.button_reserve.setText(_translate("MainWindow", "Reserve"))
