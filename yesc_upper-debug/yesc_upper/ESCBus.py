'''ESC bus protocol by python '''
from builtins import range
from builtins import object
import struct, array, sys

#MAX_CHANNEL_SUPPORT = 8
MAX_CHANNEL_SUPPORT = 6

#msg lenth
ESCBUS_MAX_DATA_LEN = 64
ESCBUS_NUM_CRC_BYTES = 1
ESCBUS_DATA_CRC_LEN = ESCBUS_MAX_DATA_LEN + ESCBUS_NUM_CRC_BYTES

ESCBUS_MESSAGE_LENGTH_CONFIG_BASIC = 7 + MAX_CHANNEL_SUPPORT
ESCBUS_MESSAGE_LENGTH_CONFIG_FULL = 33 + MAX_CHANNEL_SUPPORT
ESCBUS_MESSAGE_LENGTH_RUN = 2 * MAX_CHANNEL_SUPPORT
ESCBUS_MESSAGE_LENGTH_TUNE = 5
ESCBUS_MESSAGE_LENGTH_DO_CMD = 3
ESCBUS_MESSAGE_LENGTH_REQUEST_INFO = 2
ESCBUS_MESSAGE_LENGTH_CONFIG_INFO_BASIC = 8 + MAX_CHANNEL_SUPPORT
ESCBUS_MESSAGE_LENGTH_CONFIG_INFO_FULL = 28 + MAX_CHANNEL_SUPPORT
ESCBUS_MESSAGE_LENGTH_RUN_INFO = 4 + 2 * 2
ESCBUS_MESSAGE_LENGTH_STUDY_INFO = 5
ESCBUS_MESSAGE_LENGTH_COMM_INFO = 3
ESCBUS_MESSAGE_LENGTH_DEVICE_INFO = 13
ESCBUS_MESSAGE_LENGTH_ASSIGNED_ID = 1
ESCBUS_MESSAGE_LENGTH_BOOT_SYNC = 1

# message IDs (types)
ESCBus_MSG_ID_BAD_DATA = -1
ESCBUS_MSG_ID_CONFIG_BASIC = 0
ESCBUS_MSG_ID_CONFIG_FULL = 1
ESCBUS_MSG_ID_RUN = 2
ESCBUS_MSG_ID_TUNE = 3
ESCBUS_MSG_ID_DO_CMD = 4
##messages from ESC
ESCBUS_MSG_ID_REQUEST_INFO = 5
ESCBUS_MSG_ID_CONFIG_INFO_BASIC = 6	# simple configuration info for request from flight controller
ESCBUS_MSG_ID_CONFIG_INFO_FULL = 7 # full configuration info for request from host such as computer
ESCBUS_MSG_ID_RUN_INFO = 8  #feedback message in RUN mode
ESCBUS_MSG_ID_STUDY_INFO = 9	# studied parameters in STUDY mode
ESCBUS_MSG_ID_COMM_INFO = 10	# communication method info
ESCBUS_MSG_ID_DEVICE_INFO = 11# ESC device info
ESCBUS_MSG_ID_ASSIGNED_ID = 12	# never touch ESCBUS_MSG_ID_MAX_NUM
ESCBUS_MSG_ID_RUN_TEST_INFO = 13 # Production mode 
ESCBUS_MSG_ID_DEBUG_INFO=0x0F #debug message
##message request option
REQUEST_INFO_CONFIG_BASIC = 0
REQUEST_INFO_CONFIG_FULL = 1
REQUEST_INFO_RUN = 2
REQUEST_INFO_STUDY = 3
REQUEST_INFO_COMM = 4
REQUEST_INFO_DEVICE = 5

#boot loader used
PROTO_DEVICE_BL_REV = 1
PROTO_DEVICE_BOARD_ID = 2
PROTO_DEVICE_BOARD_REV = 3
PROTO_DEVICE_FW_SIZE = 4
PROTO_DEVICE_VEC_AREA = 5
PROTO_DEVICE_FW_REV = 6
###can be used as msg id with escbus protocol
PROTO_OK=0x10 # INSYNC/OK - 'ok' response
PROTO_FAILED=0x11 # INSYNC/FAILED - 'fail' response
PROTO_CMD_ERR=0x12
PROTO_INVALID = 0x13
ESCBUS_COMMUNIC_FAILED = 0x14 #EscBus communication used

PROTO_MSG_FEEDBACK = 0x15
PROTO_DEVICE_FEEDBACK = 0x16
PROTO_CRC_FEEDBACK = 0x17

ESCBUS_MSG_ID_BOOT_SYNC=0x21 # boot loader used
PROTO_GET_DEVICE=0x22 # get device ID bytes
PROTO_CHIP_ERASE=0x23 # erase program area and reset program address
PROTO_PROG_MULTI=0x27 # write bytes at program address and increment
PROTO_GET_CRC=0x29 # compute & return a CRC
PROTO_GET_OTP=0x2a # read a byte from OTP at the given address
PROTO_GET_SN=0x2b # read a word from UDID area ( Serial) at the given address
PROTO_BOOT=0x30 # boot the application
PROTO_DEBUG = 0x31 # emit debug information - format not defined
ESCBUS_MSG_ID_MAX_NUM = 0x32

# message const
PROTOCOL_ESCBUS = 0xFE
ESCBUS_UPDATE_SINGLE_SIZE = 128 #single update packet data size

crcTable = [
	0x00, 0xE7, 0x29, 0xCE, 0x52, 0xB5, 0x7B, 0x9C, 0xA4, 0x43, 0x8D, 0x6A,
	0xF6, 0x11, 0xDF, 0x38, 0xAF, 0x48, 0x86, 0x61, 0xFD, 0x1A, 0xD4, 0x33,
	0x0B, 0xEC, 0x22, 0xC5, 0x59, 0xBE, 0x70, 0x97, 0xB9, 0x5E, 0x90, 0x77,
	0xEB, 0x0C, 0xC2, 0x25, 0x1D, 0xFA, 0x34, 0xD3, 0x4F, 0xA8, 0x66, 0x81,
	0x16, 0xF1, 0x3F, 0xD8, 0x44, 0xA3, 0x6D, 0x8A, 0xB2, 0x55, 0x9B, 0x7C,
	0xE0, 0x07, 0xC9, 0x2E, 0x95, 0x72, 0xBC, 0x5B, 0xC7, 0x20, 0xEE, 0x09,
	0x31, 0xD6, 0x18, 0xFF, 0x63, 0x84, 0x4A, 0xAD, 0x3A, 0xDD, 0x13, 0xF4,
	0x68, 0x8F, 0x41, 0xA6, 0x9E, 0x79, 0xB7, 0x50, 0xCC, 0x2B, 0xE5, 0x02,
	0x2C, 0xCB, 0x05, 0xE2, 0x7E, 0x99, 0x57, 0xB0, 0x88, 0x6F, 0xA1, 0x46,
	0xDA, 0x3D, 0xF3, 0x14, 0x83, 0x64, 0xAA, 0x4D, 0xD1, 0x36, 0xF8, 0x1F,
	0x27, 0xC0, 0x0E, 0xE9, 0x75, 0x92, 0x5C, 0xBB, 0xCD, 0x2A, 0xE4, 0x03,
	0x9F, 0x78, 0xB6, 0x51, 0x69, 0x8E, 0x40, 0xA7, 0x3B, 0xDC, 0x12, 0xF5,
	0x62, 0x85, 0x4B, 0xAC, 0x30, 0xD7, 0x19, 0xFE, 0xC6, 0x21, 0xEF, 0x08,
	0x94, 0x73, 0xBD, 0x5A, 0x74, 0x93, 0x5D, 0xBA, 0x26, 0xC1, 0x0F, 0xE8,
	0xD0, 0x37, 0xF9, 0x1E, 0x82, 0x65, 0xAB, 0x4C, 0xDB, 0x3C, 0xF2, 0x15,
	0x89, 0x6E, 0xA0, 0x47, 0x7F, 0x98, 0x56, 0xB1, 0x2D, 0xCA, 0x04, 0xE3,
	0x58, 0xBF, 0x71, 0x96, 0x0A, 0xED, 0x23, 0xC4, 0xFC, 0x1B, 0xD5, 0x32,
	0xAE, 0x49, 0x87, 0x60, 0xF7, 0x10, 0xDE, 0x39, 0xA5, 0x42, 0x8C, 0x6B,
	0x53, 0xB4, 0x7A, 0x9D, 0x01, 0xE6, 0x28, 0xCF, 0xE1, 0x06, 0xC8, 0x2F,
	0xB3, 0x54, 0x9A, 0x7D, 0x45, 0xA2, 0x6C, 0x8B, 0x17, 0xF0, 0x3E, 0xD9,
	0x4E, 0xA9, 0x67, 0x80, 0x1C, 0xFB, 0x35, 0xD2, 0xEA, 0x0D, 0xC3, 0x24,
	0xB8, 0x5F, 0x91, 0x76]

class ESCBus(object):
    '''ESC bus protocol handling class
        msg = start + length + id + data + crc
        msg_heater = start + length + id
        crc_buf = length + id + data
    '''

    def __init__(self):
        self.send_callback = None
        self.send_callback_args = None
        self.send_callback_kwargs = None
        self.msg_header_unpacker = struct.Struct('<BBB')
        self.msg_crc_unpacker = struct.Struct('<B')
        self.buf = bytearray()
        self.buf_index = 0
        self.expected_length = 0
        self.header_len = 3
        self.crc_len = 1
        self.have_prefix_error = False
        self.rval = 0
        self.updata_flag = 0

    def set_send_callback(self, callback, *args, **kwargs):
        '''msg send function interface'''
        self.send_callback = callback
        self.send_callback_args = args
        self.send_callback_kwargs = kwargs

    def send(self, ESCBus_msg):
        '''send a ESCBus message'''
        ESCBus_msg.pack()
        if self.send_callback:
            self.send_callback(ESCBus_msg, *self.send_callback_args, **self.send_callback_kwargs)

    def buf_len(self):
        return len(self.buf) - self.buf_index

    def __parse_chars(self):
        '''judge whether it is a ESCBus_message'''
        if self.buf_len() >= 1 and self.buf[self.buf_index] != PROTOCOL_ESCBUS:
            start = self.buf[self.buf_index]
            self.buf_index += 1
            if self.have_prefix_error:
                return None
            self.have_prefix_error = True
            raise ESCBus_Error("invalid ESCBus prefix '%s'" % start)

        self.have_prefix_error = False

        if self.buf_len() >= 3:
            sbuf = self.buf[self.buf_index:3+self.buf_index]
            (start, self.expected_length, msgId) = self.msg_header_unpacker.unpack(sbuf)
            self.expected_length += self.header_len + self.crc_len

        if self.expected_length >= self.header_len and self.buf_len() >= self.expected_length:
            mbuf = array.array('B', self.buf[self.buf_index:self.buf_index+self.expected_length])
            self.buf_index += self.expected_length
            self.expected_length = 0
            m = self.decode(mbuf)
            return m

        return None

    def parse_chars(self, cs):
        '''input some data bytes, possibly returning a new message'''
        self.buf.extend(cs)
        m = self.__parse_chars()
        if m is None:
            # XXX The idea here is if we've read something and there's nothing left in
            # the buffer, reset it to 0 which frees the memory
            if self.buf_len() == 0 and self.buf_index != 0:
                self.buf = bytearray()
                self.buf_index = 0
        return m

    def parse_buffer(self, s):
        '''input some data bytes, judge whether it is a list of new messages'''
        m = self.parse_chars(s)
        if m is None:
            return None
        ret = [m]
        while True:
            m = self.parse_chars("")
            if m is None:
                return ret
            ret.append(m)
        return ret

    def decode(self, msgbuf):
        '''decode a buffer as a ESCBus message'''
        # decode the header
        try:
            start, mlen, msgId = self.msg_header_unpacker.unpack(msgbuf[:self.header_len])
        except struct.error as emsg:
            raise ESCBus_Error('Unable to unpack ESCBus header: %s' % emsg)
        mapkey = msgId
        #if ord(start) != PROTOCOL_ESCBUS:
        if start != PROTOCOL_ESCBUS:
            raise ESCBus_Error("invalid ESCBus prefix '%s'" % start)
        if mlen != len(msgbuf)-(self.header_len + self.crc_len):
            raise ESCBus_Error('invalid ESCBus message length. Got %u expected %u, msgId=%u header_len=%u' % (len(msgbuf)-(self.header_len+self.crc_len), mlen, msgId, self.header_len))
        if not mapkey in ESCBus_map:
            raise ESCBus_Error('unknown ESCBus message ID %s' % str(mapkey))

        # decode the checksum
        try:
            crc, = self.msg_crc_unpacker.unpack(msgbuf[-1:])
        except struct.error as emsg:
            raise ESCBus_Error('Unable to unpack ESCBus CRC: %s' % emsg)
        crcbuf = msgbuf[1:-1]
        crc2 = self.crc_calc(crcbuf)
        if crc != crc2:
            raise ESCBus_Error('invalid ESCBus CRC in msgID %u 0x%04x should be 0x%04x' % (msgId, crc, crc2))

        # decode the payload(message class)
        if mapkey == PROTO_OK or mapkey == PROTO_FAILED or mapkey == PROTO_INVALID:
            if mlen == 2:
                msg_parsed = ESCBus_map[PROTO_MSG_FEEDBACK]
            if mlen == 5:
                msg_parsed = ESCBus_map[PROTO_DEVICE_FEEDBACK]
            if mlen == 6:
                msg_parsed = ESCBus_map[PROTO_CRC_FEEDBACK]
            msg_parsed.feedback_status = mapkey
            fd_status = msg_parsed.feedback_status
        else:
            msg_parsed = ESCBus_map[mapkey]

        fmt =msg_parsed.format
        order_map = msg_parsed.orders
        len_map = msg_parsed.lengths

        csize = msg_parsed.unpacker.size
        mbuf = msgbuf[self.header_len:-1]
        if len(mbuf) < csize:
            # zero pad to give right size
            mbuf.extend([0]*(csize - len(mbuf)))
        if len(mbuf) < csize:
            raise ESCBus_Error('Bad message of type %s length %u needs %s' % (
                msg_parsed, len(mbuf), csize))
        mbuf = mbuf[:csize]

        try:
            t = msg_parsed.unpacker.unpack(mbuf)
        except struct.error as emsg:
            raise ESCBus_Error('Unable to unpack ESCBus payload type=%s fmt=%s payloadLength=%u: %s' % (
                msg_parsed, fmt, len(mbuf), emsg))

        tlist = list(t)
        ## handle sorted fields
        if True:
            t = tlist[:]
            if sum(len_map) == len(len_map):
                # message has no arrays in it
                for i in range(0, len(tlist)):
                    tlist[i] = t[order_map[i]]
            else:
                # message has some arrays
                tlist = []
                for i in range(0, len(order_map)):
                    order = order_map[i]
                    L = len_map[order]
                    tip = sum(len_map[:order])
                    field = t[tip]
                    if L == 1 or isinstance(field, str):
                        tlist.append(field)
                    else:
                        tlist.append(t[tip:(tip + L)])

        ## terminate any strings
        for i in range(0, len(tlist)):
            if msg_parsed.fieldtypes[i] == 'char':
                if sys.version_info.major >= 3:
                    tlist[i] = tlist[i].decode('utf-8')
                tlist[i] = str(ESCBus_String(tlist[i]))
        t = tuple(tlist)

        ## construct the message object
        try:
            m = msg_parsed(*t)
        except Exception as emsg:
            raise ESCBus_Error('Unable to instantiate ESCBus message of type %s : %s' % (msg_parsed, emsg))
        m._length = mlen
        m._payload = msgbuf[self.header_len:-1]
        m._crc = crc
        m._msgbuf = msgbuf

        return m

    def crc_calc(self, crc_buf):
        '''crc_buf = length + id + data'''
        self.rval = 0
        for i in crc_buf:
            self.rval = crcTable[self.rval ^ i]
        return self.rval

################## bootloader ##########################
#    def get_sync_encode(self, myID):
#        return ESCBus_get_sync_message(myID)
#
#    def get_sync_send(self, myID):
#        return self.send(self.get_sync_encode(myID))

    def msg_feedback_encode(self, myID, command):
        return ESCBus_msg_feedback_message(myID, command)

    def msg_feedback_send(self, myID, command):
        return self.send(self.msg_feedback_encode(myID, command))

    def device_feedback_encode(self, myID, info):
        return ESCBus_device_feedback_message(myID, info)

    def device_feedback_send(self, myID, info):
        return self.send(self.device_feedback_encode(myID, info))

    def crc_feedback_encode(self, myID, crc, command):
        return ESCBus_crc_feedback_message(myID, crc, command)

    def crc_feedback_send(self, myID, crc, command):
        return self.send(self.crc_feedback_encode(myID, crc, command))

    def get_device_info_encode(self, myID, DeviceInfo):
        return ESCBus_get_device_info_message(myID, DeviceInfo)

    def get_device_info_send(self, myID, DeviceInfo):
        return self.send(self.get_device_info_encode(myID, DeviceInfo))

    def get_device_bl_rev_encode(self, myID, blRev):
        return ESCBus_get_device_bl_rev_message(myID, blRev)

    def get_device_bl_rev_send(self, myID, blRev):
        return self.send(self.get_device_bl_rev_encode(myID, blRev))

    def get_device_board_id_encode(self, myID, boardID):
        return ESCBus_get_device_board_id_message(myID, boardID)

    def get_device_board_id_send(self, myID, boardID):
        return self.send(self.get_device_board_id_encode(myID, boardID))

    def get_device_board_rev_encode(self, myID, boardRev):
        return ESCBus_get_device_board_rev_message(myID, boardRev)

    def get_device_board_rev_send(self, myID, boardRev):
        return self.send(self.get_device_board_rev_encode(myID, boardRev))

    def get_device_fw_size_encode(self, myID, fwSize):
        return ESCBus_get_device_fw_size_message(myID, fwSize)

    def get_device_fw_size_send(self, myID, fwSize):
        return self.send(self.get_device_fw_size_encode(myID, fwSize))

    def get_device_fw_rev_encode(self, myID, fwRev):
        return ESCBus_get_device_fw_rev_message(myID, fwRev)

    def get_device_fw_rev_send(self, myID, fwRev):
        return self.send(self.get_device_fw_rev_encode(myID, fwRev))

    def chip_erase_encode(self, myID):
        return ESCBus_chip_erase_message(myID)

    def chip_erase_send(self, myID):
        return self.send(self.chip_erase_encode(myID))

    def prog_multi_encode(self, myID, data):
        return ESCBus_prog_multi_message(myID, data)

    def prog_multi_send(self, myID, data):
        return self.send(self.prog_multi_encode(myID, data))

    def get_crc_encode(self, myID):
        return ESCBus_get_crc_message(myID)

    def get_crc_send(self, myID):
        return self.send(self.get_crc_encode(myID))

    def boot_encode(self, myID):
        return ESCBus_boot_message(myID)

    def boot_send(self, myID):
        return self.send(self.boot_encode(myID))

    def invalid_encode(self, myID):
        return ESCBus_invalid_message(myID)

    def invalid_send(self, myID):
        return self.send(self.invalid_encode(myID))



################## app ################################
    def config_basic_encode(self, maxChannelInUse, channelMapTable, monitorMsgType, controlMode, minChannelValue, maxChannelValue):
        return ESCBus_config_basic_message(maxChannelInUse, channelMapTable, monitorMsgType, controlMode, minChannelValue, maxChannelValue)

    def config_basic_send(self, maxChannelInUse, channelMapTable, monitorMsgType, controlMode, minChannelValue, maxChannelValue):
        return self.send(self.config_basic_encode(maxChannelInUse, channelMapTable, monitorMsgType, controlMode, minChannelValue, maxChannelValue))

    def config_full_encode(self, header, myId, basicConfig, minSpeedSet, maxSpeedSet, breakLevel, cutVoltage, limitCurrent, advanceAngle, freqOfPWM, polesNum, PID_P, PID_I, ConfigCrc32):
        return ESCBus_config_full_message(header, myId, basicConfig, minSpeedSet, maxSpeedSet, breakLevel, cutVoltage, limitCurrent, advanceAngle, freqOfPWM, polesNum, PID_P, PID_I, ConfigCrc32)

    def config_full_send(self, header, myId, basicConfig, minSpeedSet, maxSpeedSet, breakLevel, cutVoltage, limitCurrent, advanceAngle, freqOfPWM, polesNum, PID_P, PID_I, ConfigCrc32):
        return self.send(self.config_full_encode(header, myId, basicConfig, minSpeedSet, maxSpeedSet, breakLevel, cutVoltage, limitCurrent, advanceAngle, freqOfPWM, polesNum, PID_P, PID_I, ConfigCrc32))

    def run_encode(self, value):
        return ESCBus_run_message(value)

    def run_send(self, value):
        return self.send(self.run_encode(value))

    def tune_encode(self, frequency, duration_ms, strength):
        return ESCBus_tune_message(frequency, duration_ms, strength)

    def tune_send(self, frequency, duration_ms, strength):
        return self.send(self.tune_encode(frequency, duration_ms, strength))

    def do_cmd_encode(self, channelIDMask, command, escID):
        return ESCBus_do_cmd_message(channelIDMask, command, escID)

    def do_cmd_send(self, channelIDMask, command, escID):
        return self.send(self.do_cmd_encode(channelIDMask, command, escID))

    def request_info_encode(self, channelID, requestInfoType):
        return ESCBus_request_info_message(channelID, requestInfoType)

    def request_info_send(self, channelID, requestInfoType):
        return self.send(self.request_info_encode(channelID, requestInfoType))

    def config_info_basic_encode(self, channelID, maxChannelInUse, channelMapTable, monitorMsgType, controlMode, minChannelValue, maxChannelValue):
        return ESCBus_config_info_basic_message(channelID, maxChannelInUse, channelMapTable, monitorMsgType, controlMode, minChannelValue, maxChannelValue)

    def config_info_basic_send(self, channelID, maxChannelInUse, channelMapTable, monitorMsgType, controlMode, minChannelValue, maxChannelValue):
        return self.send(self.config_info_basic_encode(channelID, maxChannelInUse, channelMapTable, monitorMsgType, controlMode, minChannelValue, maxChannelValue))

    def config_info_full_encode(self, configInfoBasic, minSpeedSet, maxSpeedSet, breakLevel, cutVoltage, limitCurrent, advanceAngle, freqOfPWM, polesNum, PID_P, PID_I):
        return ESCBus_config_info_full_message(configInfoBasic, minSpeedSet, maxSpeedSet, breakLevel, cutVoltage, limitCurrent, advanceAngle, freqOfPWM, polesNum, PID_P, PID_I)

    def config_info_full_send(self, configInfoBasic, minSpeedSet, maxSpeedSet, breakLevel, cutVoltage, limitCurrent, advanceAngle, freqOfPWM, polesNum, PID_P, PID_I):
        return self.send(self.config_info_full_encode(configInfoBasic, minSpeedSet, maxSpeedSet, breakLevel, cutVoltage, limitCurrent, advanceAngle, freqOfPWM, polesNum, PID_P, PID_I))

    def run_info_encode(self, channelID, ESCStatus, speed, current, temperature):
        return ESCBus_run_info_message(channelID, ESCStatus, speed, current, temperature)

    def run_info_send(self, channelID, ESCStatus, speed, current, temperature):
        return self.send(self.run_info_encode(channelID, ESCStatus, speed, current, temperature))

    def study_info_encode(self, channelID,  motorMinSpeed, motorMaxSpeed):
        return ESCBus_study_info_message(channelID,  motorMinSpeed, motorMaxSpeed)

    def study_info_send(self, channelID,  motorMinSpeed, motorMaxSpeed):
        return self.send(self.study_info_encode(channelID,  motorMinSpeed, motorMaxSpeed))

    def comm_info_encode(self, channelID,  inputMode, baudRate):
        return ESCBus_comm_info_message(channelID,  inputMode, baudRate)

    def comm_info_send(self, channelID,  inputMode, baudRate):
        return self.send(self.comm_info_encode(channelID,  inputMode, baudRate))

    def device_info_encode(self, channelID, FwRev, HwRev, BlRev):
        return ESCBus_device_info_message(channelID, FwRev, HwRev, BlRev)

    def device_info_send(self, channelID, FwRev, HwRev, BlRev):
        return self.send(self.device_info_encode(channelID, FwRev, HwRev, BlRev))

    def assigned_id_encode(self, escID):
        return ESCBus_assigned_id_message(escID)

    def assigned_id_send(self, escID):
        return self.send(self.assigned_id_encode(escID))

    def boot_sync_encode(self, myID):
        return ESCBus_boot_sync_message(myID)

    def boot_sync_send(self, myID):
        return self.send(self.boot_sync_encode(myID))

    def run_test_info_encode(self, channelID, ESCStatus, current_a, current_b, current_c, data_cnt):
        return ESCBus_run_test_info_message(channelID, ESCStatus, current_a, current_b, current_c, data_cnt)

    def run_test_info_send(self, channelID, ESCStatus, current_a, current_b, current_c, data_cnt):
        return self.send(self.run_test_info_encode(channelID, ESCStatus, current_a, current_b, current_c, data_cnt))


class ESCBus_message(object):
    '''base ESCBus message class'''

    def __init__(self, msgId, name):
        self._start = PROTOCOL_ESCBUS
        self._length = None
        self._id = msgId
        # payload is the data
        self._payload = None
        self._crc = None
        self._msgbuf = None
        self._fieldnames = []
        self._type = name
        self.rval = 0

    def crc_calc(self, crc_buf):
        '''crc_buf = length + id + data'''
        for i in crc_buf:
            self.rval = crcTable[self.rval ^ i]
        self._crc = self.rval
        return self._crc

    def pack(self,payload):
        msg_body = struct.pack('<BB',len(payload),self._id) + payload
        self._msgbuf = struct.pack('<B',self._start) + msg_body + struct.pack('<B',self.crc_calc(msg_body))
        return self._msgbuf

    def get_msgbuf(self):
        if isinstance(self._msgbuf, bytearray):
            return self._msgbuf
        return bytearray(self._msgbuf)

    def get_payload(self):
        return self._payload

    def get_crc(self):
        return self._crc

    def get_fieldnames(self):
        return self._fieldnames

    def get_type(self):
        return self._type

    def get_msgId(self):
        return self._id


################## bootloader ##########################
#class ESCBus_get_sync_message(ESCBus_message):
#    '''get sync message class'''
#    id = PROTO_GET_SYNC
#    name = 'GET_SYNC'
#    fieldnames = ['myID']
#    fieldtypes = ['uint8_t']
#    ordered_fieldnames = ['myID']
#    format = '<B'
#    orders = [0]
#    lengths = [1]
#    array_lengths = [0]
#    unpacker = struct.Struct(format)
#
#    def __init__(self, myID):
#        ESCBus_message.__init__(self,ESCBus_get_sync_message.id, ESCBus_get_sync_message.name)
#        self._fieldnames = ESCBus_get_sync_message.fieldnames
#        self.myID = myID
#
#    def pack(self):
#        return ESCBus_message.pack(self,struct.pack(self.format,self.myID))

class ESCBus_msg_feedback_message(ESCBus_message):
    '''msg feecback message class'''
    id = PROTO_MSG_FEEDBACK
    name = 'MSG_FEEDBACK'
    fieldnames = ['myID', 'command']
    fieldtypes = ['uint8_t', 'uint8_t']
    ordered_fieldnames = ['myID', 'command']
    format = '<BB'
    orders = [0,1]
    lengths = [1,1]
    array_lengths = [0,0]
    feedback_status = None
    unpacker = struct.Struct(format)

    def __init__(self, myID, command):
        ESCBus_message.__init__(self,ESCBus_msg_feedback_message.id, ESCBus_msg_feedback_message.name)
        self._fieldnames = ESCBus_msg_feedback_message.fieldnames
        self.myID = myID
        self.command = command

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format,self.myID, self.command))

class ESCBus_device_feedback_message(ESCBus_message):
    '''device_info feecback message class'''
    id = PROTO_DEVICE_FEEDBACK
    name = 'DEVICE_FEEDBACK'
    fieldnames = ['myID', 'info']
    fieldtypes = ['uint8_t', 'uint32_t']
    ordered_fieldnames = ['myID', 'info']
    format = '<BI'
    orders = [0,1]
    lengths = [1,1]
    array_lengths = [0,0]
    feedback_status = None
    unpacker = struct.Struct(format)

    def __init__(self, myID, info):
        ESCBus_message.__init__(self,ESCBus_device_feedback_message.id, ESCBus_device_feedback_message.name)
        self._fieldnames = ESCBus_device_feedback_message.fieldnames
        self.myID = myID
        self.info = info

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format,self.myID, self.info))

class ESCBus_crc_feedback_message(ESCBus_message):
    '''crc_info feecback message class'''
    id = PROTO_CRC_FEEDBACK
    name = 'CRC_FEEDBACK'
    fieldnames = ['myID', 'crc', 'command']
    fieldtypes = ['uint8_t', 'uint32_t', 'uint8_t']
    ordered_fieldnames = ['myID', 'crc', 'command']
    format = '<BIB'
    orders = [0,1,2]
    lengths = [1,1,1]
    array_lengths = [0,0,0]
    feedback_status = None
    unpacker = struct.Struct(format)

    def __init__(self, myID, crc, command):
        ESCBus_message.__init__(self,ESCBus_crc_feedback_message.id, ESCBus_crc_feedback_message.name)
        self._fieldnames = ESCBus_crc_feedback_message.fieldnames
        self.myID = myID
        self.crc = crc
        self.command = command

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format,self.myID, self.crc, self.command))

class ESCBus_get_device_info_message(ESCBus_message):
    '''get device_info message class'''
    id = PROTO_GET_DEVICE
    name = 'GET_DEVICE'
    fieldnames = ['myID', 'DeviceInfo']
    fieldtypes = ['uint8_t', 'uint8_t']
    ordered_fieldnames = ['myID', 'DeviceInfo']
    format = '<BB'
    orders = [0,1]
    lengths = [1,1]
    array_lengths = [0,0]
    unpacker = struct.Struct(format)

    def __init__(self, myID, DeviceInfo):
        ESCBus_message.__init__(self,ESCBus_get_device_info_message.id, ESCBus_get_device_info_message.name)
        self._fieldnames = ESCBus_get_device_info_message.fieldnames
        self.myID = myID
        self.DeviceInfo = DeviceInfo

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format,self.myID, self.DeviceInfo))

class ESCBus_get_device_bl_rev_message(ESCBus_message):
    '''get device_bl_rev message class'''
    id = PROTO_DEVICE_BL_REV
    name = 'DEVICE_BL_REV'
    fieldnames = ['myID', 'blRev']
    fieldtypes = ['uint8_t', 'uint32_t']
    ordered_fieldnames = ['myID', 'blRev']
    format = '<BI'
    orders = [0,1]
    lengths = [1,1]
    array_lengths = [0,0]
    unpacker = struct.Struct(format)

    def __init__(self, myID, blRev):
        ESCBus_message.__init__(self,ESCBus_get_device_bl_rev_message.id, ESCBus_get_device_bl_rev_message.name)
        self._fieldnames = ESCBus_get_device_bl_rev_message.fieldnames
        self.myID = myID
        self.blRev= blRev

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format,self.myID, self.blRev))

class ESCBus_get_device_board_id_message(ESCBus_message):
    '''get device_board_id message class'''
    id = PROTO_DEVICE_BOARD_ID
    name = 'DEVICE_BOARD_ID'
    fieldnames = ['myID', 'boardID']
    fieldtypes = ['uint8_t', 'uint32_t']
    ordered_fieldnames = ['myID', 'boardID']
    format = '<BI'
    orders = [0,1]
    lengths = [1,1]
    array_lengths = [0,0]
    unpacker = struct.Struct(format)

    def __init__(self, myID, boardID):
        ESCBus_message.__init__(self,ESCBus_get_device_board_id_message.id, ESCBus_get_device_board_id_message.name)
        self._fieldnames = ESCBus_get_device_board_id_message.fieldnames
        self.myID = myID
        self.boardID= boardID

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format,self.myID, self.boardID))

class ESCBus_get_device_board_rev_message(ESCBus_message):
    '''get device_board_rev message class'''
    id = PROTO_DEVICE_BOARD_REV
    name = 'DEVICE_BOARD_REV'
    fieldnames = ['myID', 'boardRev']
    fieldtypes = ['uint8_t', 'uint32_t']
    ordered_fieldnames = ['myID', 'boardRev']
    format = '<BI'
    orders = [0,1]
    lengths = [1,1]
    array_lengths = [0,0]
    unpacker = struct.Struct(format)

    def __init__(self, myID, boardRev):
        ESCBus_message.__init__(self,ESCBus_get_device_board_rev_message.id, ESCBus_get_device_board_rev_message.name)
        self._fieldnames = ESCBus_get_device_board_rev_message.fieldnames
        self.myID = myID
        self.boardRev= boardRev

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format,self.myID, self.boardRev))

class ESCBus_get_device_fw_size_message(ESCBus_message):
    '''get device_fw_size message class'''
    id = PROTO_DEVICE_FW_SIZE
    name = 'DEVICE_FW_SIZE'
    fieldnames = ['myID', 'fwSize']
    fieldtypes = ['uint8_t', 'uint32_t']
    ordered_fieldnames = ['myID', 'fwSize']
    format = '<BI'
    orders = [0,1]
    lengths = [1,1]
    array_lengths = [0,0]
    unpacker = struct.Struct(format)

    def __init__(self, myID, fwSize):
        ESCBus_message.__init__(self,ESCBus_get_device_fw_size_message.id, ESCBus_get_device_fw_size_message.name)
        self._fieldnames = ESCBus_get_device_fw_size_message.fieldnames
        self.myID = myID
        self.fwSize= fwSize

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format,self.myID, self.fwSize))

class ESCBus_get_device_fw_rev_message(ESCBus_message):
    '''get device_fw_rev message class'''
    id = PROTO_DEVICE_FW_REV
    name = 'DEVICE_FW_REV'
    fieldnames = ['myID', 'fwRev']
    fieldtypes = ['uint8_t', 'uint32_t']
    ordered_fieldnames = ['myID', 'fwRev']
    format = '<BI'
    orders = [0,1]
    lengths = [1,1]
    array_lengths = [0,0]
    unpacker = struct.Struct(format)

    def __init__(self, myID, fwRev):
        ESCBus_message.__init__(self,ESCBus_get_device_fw_rev_message.id, ESCBus_get_device_fw_rev_message.name)
        self._fieldnames = ESCBus_get_device_fw_rev_message.fieldnames
        self.myID = myID
        self.fwRev= fwRev

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format,self.myID, self.fwRev))

class ESCBus_chip_erase_message(ESCBus_message):
    '''chip erase message class'''
    id = PROTO_CHIP_ERASE
    name = 'CHIP_ERASE'
    fieldnames = ['myID']
    fieldtypes = ['uint8_t']
    ordered_fieldnames = ['myID']
    format = '<B'
    orders = [0]
    lengths = [1]
    array_lengths = [0]
    unpacker = struct.Struct(format)

    def __init__(self, myID):
        ESCBus_message.__init__(self,ESCBus_chip_erase_message.id, ESCBus_chip_erase_message.name)
        self._fieldnames = ESCBus_chip_erase_message.fieldnames
        self.myID = myID

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format,self.myID))

class ESCBus_prog_multi_message(ESCBus_message):
    '''program multi message class'''
    id = PROTO_PROG_MULTI
    name = 'PROG_MULTI'
    fieldnames = ['myID', 'data']
    fieldtypes = ['uint8_t', 'uint8_t']
    ordered_fieldnames = ['myID', 'data']
    format = '<B' + str(ESCBUS_UPDATE_SINGLE_SIZE)+ 'B'
    orders = [0,1]
    lengths = [1,1]
    array_lengths = [0,ESCBUS_UPDATE_SINGLE_SIZE]
    unpacker = struct.Struct(format)

    def __init__(self, myID, data):
        ESCBus_message.__init__(self,ESCBus_prog_multi_message.id, ESCBus_prog_multi_message.name)
        self._fieldnames = ESCBus_prog_multi_message.fieldnames
        self.myID = myID
        self.data = data

    def pack(self):
        return ESCBus_message.pack(self,struct.pack('<B',self.myID) + self.data)

class ESCBus_get_crc_message(ESCBus_message):
    '''get crc message class'''
    id = PROTO_GET_CRC
    name = 'GET_CRC'
    fieldnames = ['myID']
    fieldtypes = ['uint8_t']
    ordered_fieldnames = ['myID']
    format = '<B'
    orders = [0]
    lengths = [1]
    array_lengths = [0]
    unpacker = struct.Struct(format)

    def __init__(self, myID):
        ESCBus_message.__init__(self,ESCBus_get_crc_message.id, ESCBus_get_crc_message.name)
        self._fieldnames = ESCBus_get_crc_message.fieldnames
        self.myID = myID

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format,self.myID))

class ESCBus_boot_message(ESCBus_message):
    '''reboot message class'''
    id = PROTO_BOOT
    name = 'BOOT'
    fieldnames = ['myID']
    fieldtypes = ['uint8_t']
    ordered_fieldnames = ['myID']
    format = '<B'
    orders = [0]
    lengths = [1]
    array_lengths = [0]
    unpacker = struct.Struct(format)

    def __init__(self, myID):
        ESCBus_message.__init__(self,ESCBus_boot_message.id, ESCBus_boot_message.name)
        self._fieldnames = ESCBus_boot_message.fieldnames
        self.myID = myID

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format,self.myID))

class ESCBus_invalid_message(ESCBus_message):
    '''invalid message class'''
    id = PROTO_INVALID
    name = 'INVAILD'
    fieldnames = ['myID']
    fieldtypes = ['uint8_t']
    ordered_fieldnames = ['myID']
    format = '<B'
    orders = [0]
    lengths = [1]
    array_lengths = [0]
    unpacker = struct.Struct(format)

    def __init__(self, myID):
        ESCBus_message.__init__(self,ESCBus_invalid_message.id, ESCBus_invalid_message.name)
        self._fieldnames = ESCBus_invalid_message.fieldnames
        self.myID = myID

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format,self.myID))


################## app ################################
class ESCBus_config_basic_message(ESCBus_message):
    '''basic config message class'''
    id = ESCBUS_MSG_ID_CONFIG_BASIC
    name = 'CONFIG_BASIC'
    fieldnames = ['maxChannelInUse', 'channelMapTable','monitorMsgType','controlMode','minChannelValue','maxChannelValue']
    fieldtypes = ['uint8_t', 'int8_t', 'uint8_t', 'uint8_t', 'uint16_t', 'uint16_t',]
    ordered_fieldnames = ['maxChannelInUse', 'channelMapTable','monitorMsgType','controlMode','minChannelValue','maxChannelValue']
    format = '<B' + str(MAX_CHANNEL_SUPPORT) +'bBBHH'
    orders = [0,1,2,3,4,5]
    lengths = [1,1,1,1,1,1]
    array_lengths = [0, MAX_CHANNEL_SUPPORT,0, 0, 0, 0]
    unpacker = struct.Struct(format)

    def __init__(self, maxChannelInUse, channelMapTable, monitorMsgType, controlMode, minChannelValue, maxChannelValue):
        ESCBus_message.__init__(self,ESCBus_config_basic_message.id,ESCBus_config_basic_message.name)
        self._fieldnames = ESCBus_config_basic_message.fieldnames
        self.maxChannelInUse = maxChannelInUse
        self.channelMapTable = channelMapTable
        self.monitorMsgType = monitorMsgType
        self.controlMode = controlMode
        self.minChannelValue = minChannelValue
        self.maxChannelValue = maxChannelValue

    def pack(self):
        return ESCBus_message.pack(self,struct.pack('<B8bBBHH',self.maxChannelInUse, *self.channel_map_table, self.monitorMsgType, self.minChannelValue, self.maxChannelValue))

class ESCBus_config_full_message(ESCBus_message):
    '''full config message class'''
    id = ESCBUS_MSG_ID_CONFIG_FULL
    name = 'CONFIG_FULL'
    fieldnames = ['header','myId', 'basicConfig', 'minSpeedSet', 'maxSpeedSet', 'breakLevel', 'cutVoltage','limitCurrent','advanceAngle','freqOfPWM','polesNum','PID_P','PID_I','ConfigCrc32']
    fieldtypes = ['int8_t','int8_t','EscbusConfigBasicPacket','int16_t','int16_t','uint8_t','uint8_t','uint16_t','uint8_t','uint8_t','uint16_t','uint8_t','float','float','uint32_t']
    ordered_fieldnames = ['header','myId', 'basicConfig', 'minSpeedSet', 'maxSpeedSet', 'breakLevel', 'cutVoltage','limitCurrent','advanceAngle','freqOfPWM','polesNum','PID_P','PID_I','ConfigCrc32']
    format = '<bb' + 'B' + str(MAX_CHANNEL_SUPPORT) +'bBBHH' +'hhBHBBHBffI'
    orders = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
    lengths = [1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    array_lengths = [0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    unpacker = struct.Struct(format)

    def __init__(self,header,myId, basicConfig, minSpeedSet, maxSpeedSet, breakLevel, cutVoltage,limitCurrent,advanceAngle,freqOfPWM,polesNum,PID_P,PID_I,ConfigCrc32):
        ESCBus_message.__init__(self,ESCBus_config_full_message.id,ESCBus_config_full_message.name)
        self._fieldnames = ESCBus_config_full_message.fieldnames
        self.header = header
        self.myId = myId
        self.basicConfig = basicConfig
        self.minSpeedSet = minSpeedSet
        self.maxSpeedSet = maxSpeedSet
        self.breakLevel = breakLevel
        self.cutVoltage = cutVoltage
        self.limitCurrent = limitCurrent
        self.advanceAngle = advanceAngle
        self.freqOfPWM = freqOfPWM
        self.polesNum = polesNum
        self.PID_P = PID_P
        self.PID_I = PID_I
        self.ConfigCrc32 = ConfigCrc32

    def pack(self):
        return ESCBus_message.pack(self, self.struct.pack(self.format, self.header, self.myId, self.basicConfig, self.minSpeedSet, self.maxSpeedSet, self.breakLevel, self.cutVoltage, self.limitCurrent, self.advanceAngle, self.freqOfPWM, self.polesNum, self.PID_P, self.PID_I, self.ConfigCrc32))

class ESCBus_run_message(ESCBus_message):
    '''running message class'''
    id = ESCBUS_MSG_ID_RUN
    name = 'RUN'
    fieldnames = ['value']
    fieldtypes = ['int16_t']
    ordered_fieldnames = ['value']
    format = '<' + str(MAX_CHANNEL_SUPPORT) +'h'
    orders = [0]
    lengths = [1]
    array_lengths = [MAX_CHANNEL_SUPPORT]
    unpacker = struct.Struct(format)

    def __init__(self, value):
        ESCBus_message.__init__(self,ESCBus_run_message.id, ESCBus_run_message.name)
        self._fieldnames = ESCBus_run_message.fieldnames
        self.value = value

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format, *self.value))

class ESCBus_tune_message(ESCBus_message):
    '''tune message class'''
    id = ESCBUS_MSG_ID_TUNE
    name = 'TUNE'
    fieldnames = ['frequency', 'duration_ms','strength']
    fieldtypes = ['uint16_t', 'uint16_t', 'uint8_t']
    ordered_fieldnames = ['frequency', 'duration_ms','strength']
    format = '<HHB'
    orders = [0,1,2]
    lengths = [1, 1, 1]
    array_lengths = [0, 0, 0]
    unpacker = struct.Struct(format)

    def __init__(self, frequency, duration_ms, strength):
        ESCBus_message.__init__(self,ESCBus_tune_message.id, ESCBus_tune_message.name)
        self._fieldnames = ESCBus_tune_message.fieldnames
        self.frequency = frequency
        self.duration_ms = duration_ms
        self.strength = strength

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format, self.frequency, self.duration_ms, self.strength))

class ESCBus_do_cmd_message(ESCBus_message):
    '''do cmd message class'''
    id = ESCBUS_MSG_ID_DO_CMD
    name = 'DO_CMD'
    fieldnames = ['channelIDMask','command','escID']
    fieldtypes = ['uint8_t', 'uint8_t', 'uint8_t']
    ordered_fieldnames = ['channelIDMask','command','escID']
    format = '<BBB'
    orders = [0,1,2]
    lengths = [1, 1, 1]
    array_lengths = [0, 0, 0]
    unpacker = struct.Struct(format)

    def __init__(self,channelIDMask,command,escID):
        ESCBus_message.__init__(self,ESCBus_do_cmd_message.id, ESCBus_do_cmd_message.name)
        self._fieldnames = ESCBus_do_cmd_message.fieldnames
        self.channelIDMask = channelIDMask
        self.command = command
        self.escID = escID

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format, self.channelIDMask, self.command, self.escID))

class ESCBus_request_info_message(ESCBus_message):
    '''info request message class'''
    id = ESCBUS_MSG_ID_REQUEST_INFO
    name = 'REQUEST_INFO'
    fieldnames = ['channelID', 'requestInfoType']
    fieldtypes = ['uint8_t', 'uint8_t']
    ordered_fieldnames = ['channelID', 'requestInfoType']
    format = '<BB'
    orders = [0,1]
    lengths = [1, 1]
    array_lengths = [0, 0]
    unpacker = struct.Struct(format)

    def __init__(self, channelID, requestInfoType):
        ESCBus_message.__init__(self,ESCBus_request_info_message.id, ESCBus_request_info_message.name)
        self._fieldnames = ESCBus_request_info_message.fieldnames
        self.channelID = channelID
        self.requestInfoType = requestInfoType

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format,self.channelID, self.requestInfoType))

class ESCBus_config_info_basic_message(ESCBus_message):
    '''basic config info message class'''
    id = ESCBUS_MSG_ID_CONFIG_INFO_BASIC
    name = 'CONFIG_INFO_BASIC'
    fieldnames = ['channelID', 'maxChannelInUse', 'channelMapTable','monitorMsgType','controlMode','minChannelValue','maxChannelValue']
    fieldtypes = ['uint8_t', 'uint8_t', 'int8_t', 'uint8_t', 'uint8_t', 'uint16_t', 'uint16_t',]
    ordered_fieldnames = [ 'channelID', 'maxChannelInUse', 'channelMapTable','monitorMsgType','controlMode','minChannelValue','maxChannelValue']
    format = '<BB' + str(MAX_CHANNEL_SUPPORT) +'bBBHH'
    orders = [0,1,2,3,4,5,6]
    lengths = [1,1,1,1,1,1,1]
    array_lengths = [0, 0, MAX_CHANNEL_SUPPORT,0, 0, 0, 0]
    unpacker = struct.Struct(format)

    def __init__(self, channelID, maxChannelInUse, channelMapTable, monitorMsgType, controlMode, minChannelValue, maxChannelValue):
        ESCBus_message.__init__(self,ESCBus_config_info_basic_message.id,ESCBus_config_info_basic_message.name)
        self._fieldnames = ESCBus_config_info_basic_message.fieldnames
        self.channelID = channelID
        self.maxChannelInUse = maxChannelInUse
        self.channelMapTable = channelMapTable
        self.monitorMsgType = monitorMsgType
        self.controlMode = controlMode
        self.minChannelValue = minChannelValue
        self.maxChannelValue = maxChannelValue

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format, self.channelID, self.maxChannelInUse, *self.channel_map_table, self.monitorMsgType, self.minChannelValue, self.maxChannelValue))

class ESCBus_config_info_full_message(ESCBus_message):
    '''full config info message class'''
    id = ESCBUS_MSG_ID_CONFIG_INFO_FULL
    name = 'CONFIG_INFO_FULL'
    fieldnames = ['configInfoBasic', 'minSpeedSet', 'maxSpeedSet', 'breakLevel', 'cutVoltage','limitCurrent','advanceAngle','freqOfPWM','polesNum','PID_P','PID_I']
    fieldtypes = ['EscbusConfigInfoBasicPacket','int16_t','int16_t','uint8_t','uint8_t','uint16_t','uint8_t','uint8_t','uint16_t','uint8_t','float','float']
    ordered_fieldnames =  ['configInfoBasic', 'minSpeedSet', 'maxSpeedSet', 'breakLevel', 'cutVoltage','limitCurrent','advanceAngle','freqOfPWM','polesNum','PID_P','PID_I']
    format = '<' + 'B' + str(MAX_CHANNEL_SUPPORT) +'bBBHH' +'hhBHBBHBff'
    orders = [0,1,2,3,4,5,6,7,8,9,10]
    lengths = [1,1,1,1,1,1,1,1,1,1,1]
    array_lengths = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    unpacker = struct.Struct(format)

    def __init__(self, configInfoBasic, minSpeedSet, maxSpeedSet, breakLevel, cutVoltage,limitCurrent,advanceAngle,freqOfPWM,polesNum,PID_P,PID_I):
        ESCBus_message.__init__(self,ESCBus_config_info_full_message.id,ESCBus_config_info_full_message.name)
        self._fieldnames = ESCBus_config_info_full_message.fieldnames
        self.configInfoBasic = configInfoBasic
        self.minSpeedSet = minSpeedSet
        self.maxSpeedSet = maxSpeedSet
        self.breakLevel = breakLevel
        self.cutVoltage = cutVoltage
        self.limitCurrent = limitCurrent
        self.advanceAngle = advanceAngle
        self.freqOfPWM = freqOfPWM
        self.polesNum = polesNum
        self.PID_P = PID_P
        self.PID_I = PID_I

    def pack(self):
        return ESCBus_message.pack(self, self.struct.pack(self.format, self.configInfoBasic, self.minSpeedSet, self.maxSpeedSet, self.breakLevel, self.cutVoltage, self.limitCurrent, self.advanceAngle, self.freqOfPWM, self.polesNum, self.PID_P, self.PID_I))

class ESCBus_run_info_message(ESCBus_message):
    '''running info message class'''
    id = ESCBUS_MSG_ID_RUN_INFO
    name = 'RUN_INFO'
    fieldnames = ['channelID', 'ESCStatus','speed','current','temperature']
    fieldtypes = ['uint8_t', 'uint8_t', 'int16_t', 'uint16_t', 'uint8_t']
    ordered_fieldnames = ['channelID', 'ESCStatus','speed','current','temperature']
    format = '<BBhHB'
    orders = [0,1,2,3,4]
    lengths = [1, 1, 1, 1, 1]
    array_lengths = [0, 0, 0, 0 ,0]
    feedback_status = None
    unpacker = struct.Struct(format)

    def __init__(self, channelID, ESCStatus, speed, current, temperature):
        ESCBus_message.__init__(self,ESCBus_run_info_message.id, ESCBus_run_info_message.name)
        self._fieldnames = ESCBus_run_info_message.fieldnames
        self.channelID = channelID
        self.ESCStatus = ESCStatus
        self.speed = speed
        self.current = current
        self.temperature = temperature

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format, self.channelID, self.ESCStatus, self.speed, self.current, self.temperature))

class ESCBus_study_info_message(ESCBus_message):
    '''stydy info message class'''
    id = ESCBUS_MSG_ID_STUDY_INFO
    name = 'STUDY_INFO'
    fieldnames = ['channelID', 'motorMinSpeed','motorMaxSpeed']
    fieldtypes = ['uint8_t', 'int16_t','int16_t']
    ordered_fieldnames = ['channelID', 'motorMinSpeed','motorMaxSpeed']
    format = '<Bhh'
    orders = [0,1,2]
    lengths = [1, 1, 1]
    array_lengths = [0, 0, 0]
    unpacker = struct.Struct(format)

    def __init__(self, channelID,  motorMinSpeed, motorMaxSpeed):
        ESCBus_message.__init__(self,ESCBus_study_info_message.id, ESCBus_study_info_message.name)
        self._fieldnames = ESCBus_study_info_message.fieldnames
        self.channelID = channelID
        self.motorMinSpeed = motorMinSpeed
        self.motorMaxSpeed = motorMaxSpeed

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format,self.channelID, self.motorMinSpeed , self.motorMaxSpeed))

class ESCBus_comm_info_message(ESCBus_message):
    '''comm info message class'''
    id = ESCBUS_MSG_ID_COMM_INFO
    name = 'COMM_INFO'
    fieldnames = ['channelID', 'inputMode','baudRate']
    fieldtypes = ['uint8_t', 'uint8_t', 'uint8_t']
    ordered_fieldnames = ['channelID', 'inputMode','baudRate']
    format = '<BBB'
    orders = [0,1,2]
    lengths = [1, 1, 1]
    array_lengths = [0, 0, 0]
    unpacker = struct.Struct(format)

    def __init__(self, channelID,  inputMode, baudRate):
        ESCBus_message.__init__(self,ESCBus_comm_info_message.id, ESCBus_comm_info_message.name)
        self._fieldnames = ESCBus_comm_info_message.fieldnames
        self.channelID = channelID
        self.inputMode = inputMode
        self.baudRate = baudRate

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format,self.channelID, self.inputMode , self.baudRate))

class ESCBus_device_info_message(ESCBus_message):
    '''device info message class'''
    id = ESCBUS_MSG_ID_DEVICE_INFO
    name = 'DEVICE_INFO'
    fieldnames = ['channelID', 'FwRev', 'HwRev', 'BlRev']
    fieldtypes = ['uint8_t', 'uint32_t', 'uint32_t', 'uint32_t']
    ordered_fieldnames =  ['channelID', 'FwRev', 'HwRev', 'BlRev']
    format = '<BIII'
    orders = [0,1,2,3]
    lengths = [1, 1, 1, 1]
    array_lengths = [0, 0, 0, 0]
    unpacker = struct.Struct(format)

    def __init__(self, channelID, FwRev, HwRev, BlRev):
        ESCBus_message.__init__(self,ESCBus_device_info_message.id, ESCBus_device_info_message.name)
        self._fieldnames = ESCBus_device_info_message.fieldnames
        self.channelID = channelID
        self.FwRev = FwRev
        self.HwRev = HwRev
        self.BlRev = BlRev

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format, self.channelID, self.FwRev, self.HwRev, self.BlRev))

class ESCBus_assigned_id_message(ESCBus_message):
    '''assigned id message class'''
    id = ESCBUS_MSG_ID_ASSIGNED_ID
    name = 'ASSIGNED_ID'
    fieldnames = ['escID']
    fieldtypes = ['uint8_t']
    ordered_fieldnames = ['escID']
    format = '<B'
    orders = [0]
    lengths = [1]
    array_lengths = [0]
    unpacker = struct.Struct(format)

    def __init__(self, escID):
        ESCBus_message.__init__(self,ESCBus_assigned_id_message.id, ESCBus_assigned_id_message.name)
        self._fieldnames = ESCBus_assigned_id_message.fieldnames
        self.escID = escID

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format,self.escID))

class ESCBus_boot_sync_message(ESCBus_message):
    '''boot sync message class'''
    id = ESCBUS_MSG_ID_BOOT_SYNC
    name = 'BOOT_SYNC'
    fieldnames = ['myID']
    fieldtypes = ['uint8_t']
    ordered_fieldnames = ['myID']
    format = '<B'
    orders = [0]
    lengths = [1]
    array_lengths = [0]
    unpacker = struct.Struct(format)

    def __init__(self, myID):
        ESCBus_message.__init__(self,ESCBus_boot_sync_message.id, ESCBus_boot_sync_message.name)
        self._fieldnames = ESCBus_boot_sync_message.fieldnames
        self.myID = myID

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format,self.myID))

class ESCBus_run_test_info_message(ESCBus_message):
    '''running test info message class'''
    id = ESCBUS_MSG_ID_RUN_TEST_INFO
    name = 'RUN_TEST_INFO'
    fieldnames = ['channelID', 'ESCStatus','current_a', 'current_b', 'current_c', 'data_cnt']
    fieldtypes = ['uint8_t', 'uint8_t', 'int16_t', 'int16_t', 'int16_t', 'uint8_t']
    ordered_fieldnames = ['channelID', 'ESCStatus','current_a', 'current_b', 'current_c', 'data_cnt']
    format = '<BBhhhB'
    orders = [0,1,2,3,4,5]
    lengths = [1, 1, 1, 1, 1, 1]
    array_lengths = [0, 0, 0, 0 ,0, 0]
    unpacker = struct.Struct(format)

    def __init__(self, channelID, ESCStatus, current_a, current_b, current_c, data_cnt):
        ESCBus_message.__init__(self,ESCBus_run_test_info_message.id, ESCBus_run_test_info_message.name)
        self._fieldnames = ESCBus_run_test_info_message.fieldnames
        self.channelID = channelID
        self.ESCStatus = ESCStatus
        self.current_a = current_a
        self.current_b = current_b
        self.current_c = current_c
        self.data_cnt = data_cnt

    def pack(self):
        return ESCBus_message.pack(self,struct.pack(self.format, self.channelID, self.ESCStatus, self.current_a, self.current_b, self.current_c, self.data_cnt))

class ESCBus_Error(Exception):
        '''ESCBus error class'''
        def __init__(self, msg):
            Exception.__init__(self, msg)
            self.message = msg

class ESCBus_String(str):
        '''NUL terminated string'''
        def __init__(self, s):
                str.__init__(self)
        def __str__(self):
            i = self.find(chr(0))
            if i == -1:
                return self[:]
            return self[0:i]

ESCBus_map = {
################## bootloader ##########################
    PROTO_OK : ESCBus_msg_feedback_message,
    PROTO_FAILED : ESCBus_msg_feedback_message,
    PROTO_INVALID : ESCBus_msg_feedback_message,

    PROTO_MSG_FEEDBACK : ESCBus_msg_feedback_message,
    PROTO_DEVICE_FEEDBACK : ESCBus_device_feedback_message,
    PROTO_CRC_FEEDBACK : ESCBus_crc_feedback_message,

#    PROTO_GET_SYNC : ESCBus_get_sync_message,
    PROTO_GET_DEVICE : ESCBus_get_device_info_message,
    PROTO_DEVICE_BL_REV : ESCBus_get_device_bl_rev_message,
    PROTO_DEVICE_BOARD_ID : ESCBus_get_device_board_id_message,
    PROTO_DEVICE_BOARD_REV : ESCBus_get_device_board_rev_message,
    PROTO_DEVICE_FW_SIZE : ESCBus_get_device_fw_size_message,
#    PROTO_DEVICE_VEC_AREA : ESCBus_get_device_vec_area_message,
    PROTO_DEVICE_FW_REV : ESCBus_get_device_fw_rev_message,
    PROTO_CHIP_ERASE : ESCBus_chip_erase_message,
    PROTO_PROG_MULTI : ESCBus_prog_multi_message,
    PROTO_GET_CRC : ESCBus_get_crc_message,
    PROTO_BOOT : ESCBus_boot_message,
    PROTO_INVALID : ESCBus_invalid_message,

################## app ################################
    ESCBUS_MSG_ID_CONFIG_BASIC : ESCBus_config_basic_message,
    ESCBUS_MSG_ID_CONFIG_FULL : ESCBus_config_full_message,
    ESCBUS_MSG_ID_RUN : ESCBus_run_message,
    ESCBUS_MSG_ID_TUNE : ESCBus_tune_message,
    ESCBUS_MSG_ID_DO_CMD : ESCBus_do_cmd_message,
    ESCBUS_MSG_ID_REQUEST_INFO : ESCBus_request_info_message,
    ESCBUS_MSG_ID_CONFIG_INFO_BASIC : ESCBus_config_info_basic_message,
    ESCBUS_MSG_ID_CONFIG_INFO_FULL : ESCBus_config_info_full_message,
    ESCBUS_MSG_ID_RUN_INFO : ESCBus_run_info_message,
    ESCBUS_MSG_ID_STUDY_INFO: ESCBus_study_info_message,
    ESCBUS_MSG_ID_COMM_INFO : ESCBus_comm_info_message,
    ESCBUS_MSG_ID_DEVICE_INFO : ESCBus_device_info_message,
    ESCBUS_MSG_ID_ASSIGNED_ID : ESCBus_assigned_id_message,
    ESCBUS_MSG_ID_BOOT_SYNC : ESCBus_boot_sync_message,
    ESCBUS_MSG_ID_RUN_TEST_INFO : ESCBus_run_test_info_message,
#    ESCBus_MSG_ID_BAD_DATA
#    ESCBUS_MSG_ID_DEBUG_INFO
}

