import time
import struct
import io
from IMU383_Uart import UART_Dev
from Test_Logger import TestLogger
from Test_Case import Test_Section
from Test_Case import Test_Case
from Test_Case import Code
from Test_Case import Condition_Check
from math import pi


ping = [0x50, 0x4B, 0x00]
echo = [0x41]

upper_limit_accel = 32767 * ((20.0)/65536)
lower_limit_accel = -32766 * ((20.0)/65536)
upper_limit_rate = 32767 * (1260.0/65536)
lower_limit_rate = -32766 * (1260.0/65536)

PK = [0x50, 0x4B]
CH = [0x43, 0x48]
GP = [0x47, 0x50]
NAK= [0x15, 0x15]
ID = [0x49, 0x44]
VR = [0x56, 0x52]
T0 = [0x54, 0x30]
S0 = [0x53, 0x30]
S1 = [0x53, 0x31]
WF = [0x57, 0x47]
SF = [0x53, 0x46]
RF = [0x52, 0x46]
GF = [0x47, 0x46]

packet_rate_div_f               = [0x00,0x01]
unit_baud_f                     = [0x00,0x02]
continuous_packet_type_f        = [0x00,0x03]
gyro_filter_setting_f           = [0x00,0x05]
accel_filter_setting_f          = [0x00,0x06]
orientation_f                   = [0x00,0x07]
sensor_enable_f                 = [0x00,0x42]
output_select_f                 = [0x00,0x43]
fault_detct_chip1_f             = [0x00,0x4C]
fault_detct_chip2_f             = [0x00,0x4D]
fault_detct_chip3_f             = [0x00,0x4E]
accel_consistency_en_f          = [0x00,0x61]
rate_sensor_consistency_en_f    = [0x00,0x62]

'''
class Evaluate:

    def __init__(self):
        self.expetced = None
        self.actual = None

    def onEvaluate(self, expcted_data, actual_data):
        raise NotImplementedError("Subclass must implement abstract method")

class Match(Evaluate):

    def onEvaluate(self, expected_data, actual_data):
        if(expected_data == actual_data):
            return True
        else:
            return False

class Range(Evaluate):

    def onEvaluate(self, )

'''
# Add test scripts here
class Test_Scripts:
    uut = None

    def __init__(self, device):
        Test_Scripts.uut = device

    def echo_test(self):
        #Test_Scripts.uut.send_message(echo)
        #pt,pll,pl = Test_Scripts.uut.unpacked_response()
        response = Test_Scripts.uut.imu383_command("CH",[0x41])
        if(int(response,16) == 0x41):
            return True, int(response,16), 0x41
        else:
            return False, int(response,16), 0x41

    def default_baudrate_test(self):
        return self.echo_test()

    def communication_test(self):
        return self.echo_test()

    def header_test(self):
        return self.echo_test()

    def payload_length_test(self):
        return self.echo_test()

    def payload_test(self):
        return self.echo_test()

    def CRC_test(self):
        return self.echo_test()

    def polled_mode_test(self):
        response = Test_Scripts.uut.imu383_command("GP", S0)
        if(response[0] == 'S0'):
            return True, response[0], 'S0'
        else:
            return False, response[0], 'S0'

    def continuouse_mode_test(self):
        data = Test_Scripts.uut.imu383_command("SF", continuous_packet_type_f + S0)
        data = Test_Scripts.uut.imu383_command("SF", packet_rate_div_f + [0x00,0x32])

        t0 = time.time()
        count = 0
        while(time.time() - t0 < 10.00):
            count = count+1
            response = Test_Scripts.uut.read_response()

        # verify that UUT reads data 20 times in 10 seconds,
        # more ofthen than not it reads 21 times due to time it takes to read
        if(count == 20 or count == 21):
            return True, count, [20,21]
        else:
            return False, count, [20,21]

    def packet_type_test(self, packet_type):

        ptype = ''.join(hex(val)[2:] for val in packet_type)

        response = Test_Scripts.uut.imu383_command("GP", packet_type)
        if(response[0] == ptype.decode("hex")):
            return True, response[0], ptype.decode("hex")
        else:
            return False, response[0], ptype.decode("hex")

    def get_field_test(self, field):
        response = Test_Scripts.uut.imu383_command("GF", field)
        if not response:
            return False, response, 'response'
        else:
            return True, response, 'response'

    def read_field_test(self, field):
        response = Test_Scripts.uut.imu383_command("RF", field)
        if not response:
            return False, response, 'response'
        else:
            return True, response, 'response'

    def set_field_test(self, field ,val):
        response = Test_Scripts.uut.imu383_command("SF", field + val)
        if not response:
            return False, response, 'response'
        else:
            return True, response, 'response'

    def write_field_test(self, field, val):
        data = Test_Scripts.uut.imu383_command("RF", field)
        orig_field_val = []
        orig_field_val= orig_field_val + field
        # store original field value before changing
        orig_field_val.append(int(data[-4:-2],16))# MSB
        orig_field_val.append(int(data[-2:],16))  # LSB

        response = Test_Scripts.uut.imu383_command("WF", field + [0x00, 0x00])

        # reset back to original
        Test_Scripts.uut.imu383_command("WF", orig_field_val)

        if not response:
            return False, response, 'response'
        else:
            return True, response, 'response'

    def verify_ID_packet_type(self):
        return self.packet_type_test(ID)
    def verify_VR_packet_type(self):
        return self.packet_type_test(VR)
    def verify_T0_packet_type(self):
        return self.packet_type_test(T0)
    def verify_S0_packet_type(self):
        return self.packet_type_test(S0)
    def verify_S1_packet_type(self):
        return self.packet_type_test(S1)
    def verify_RF_packet_type(self):
        return self.read_field_test(packet_rate_div_f)
    def verify_WF_packet_type(self):
        return self.write_field_test(packet_rate_div_f, [0x00, 0x00])
    def verify_GF_packet_type(self):
        return self.get_field_test(packet_rate_div_f)
    def verify_SF_packet_type(self):
        return self.set_field_test(packet_rate_div_f, [0x00, 0x00])

    def rf_default_test(self, cmd, expected_val):
        response = Test_Scripts.uut.imu383_command("RF", cmd)

        if(int(response[6:],16) == expected_val):
            return True, int(response[6:],16), expected_val
        else:
            return False, int(response[6:],16), expected_val

    def gf_default_test(self, field, expected_val):
        Test_Scripts.uut.restart_device();
        Test_Scripts.uut.silence_device();
        response = Test_Scripts.uut.imu383_command("GF", field)

        if(int(response[6:],16) == expected_val):
            return True, int(response[6:],16), expected_val
        else:
            return False, int(response[6:],16), expected_val

    # rate_val is packet_rate_value in list, eg:[0x00, 0x05]
    # rateHz is rate at which packets are expected
    def packet_rate_div(self, rate, rateHz):

        '''Setup'''
        # Set S0 as continuous packet type
        data = Test_Scripts.uut.imu383_command("SF", continuous_packet_type_f + S0)
        test_time = 1

        resp = Test_Scripts.uut.imu383_command("SF", packet_rate_div_f + rate)

        if not resp:
            #print "ERORR: Dint receive data"
            return False, "Response", "No Response"
        #print data

        '''Execute'''
        count = 0
        t0 = time.time()
        while(time.time() - t0 < test_time):
            response = Test_Scripts.uut.read_response()
            # Count up when S0 packet recceived
            if response and response[0] == "S0":
                #print time.time()
                count = count+1

        Test_Scripts.uut.silence_device()

        '''Result'''
        if(rateHz == 0):
            return True, count, 0 if(count == 0) else False, count , 0
        elif(((rateHz * test_time - 1) <= count) and (count <= (rateHz * test_time + 2))):
            return True, count , [(rateHz * test_time - 1), (rateHz * test_time + 2)]
        else:
            return False, count , [(rateHz * test_time - 1), (rateHz * test_time + 2)]


    def _combine_reg_short(self,lsb,msb):
            lsb = struct.pack('B',lsb)
            msb = struct.pack('B',msb)
            return struct.unpack('h',msb+lsb)[0]

    def _combine_reg_ushort(self,lsb,msb):
            lsb = struct.pack('B',lsb)
            msb = struct.pack('B',msb)
            return struct.unpack('H',msb+lsb)[0]

    def continuous_packet_type_S0(self):
        '''Setup'''
        data = Test_Scripts.uut.imu383_command("SF", continuous_packet_type_f + S0)
        data = Test_Scripts.uut.imu383_command("SF", packet_rate_div_f + [0x00,0x01])

        # convert list of hex value to string
        pt = ''.join(hex(val)[2:] for val in S0)
        # use pt.decode("hex") to conver pt ro ASCII

        '''Execute'''
        for each in range(100):
            response = Test_Scripts.uut.read_response()
            #print "S0",response
            if response and response[0] == pt.decode("hex"):
                len = int(response[1],16)
                msg = bytearray.fromhex(response[2])

                x_accel = self._combine_reg_short(msg[0],msg[1]) * (20.0/65536)
                y_accel = self._combine_reg_short(msg[2],msg[3]) * (20.0/65536)
                z_accel = self._combine_reg_short(msg[4],msg[5]) * (20.0/65536)
                x_rate = self._combine_reg_short(msg[6],msg[7]) * (1260.0/65536)
                y_rate = self._combine_reg_short(msg[8],msg[9]) * (1260.0/65536)
                z_rate = self._combine_reg_short(msg[10],msg[11]) * (1260.0/65536)
                x_temp = self._combine_reg_short(msg[18],msg[19]) * (200.0/65536)
                y_temp = self._combine_reg_short(msg[20],msg[21]) * (200.0/65536)
                z_temp = self._combine_reg_short(msg[22],msg[23]) * (200.0/65536)
                board_temp = self._combine_reg_short(msg[24],msg[25]) * (200.0/65536)
                timer = self._combine_reg_ushort(msg[26],msg[27]) * 15.259022
                BIT = self._combine_reg_ushort(msg[28],msg[29])

                '''Result'''
                # check data is within expected range
                if( not (lower_limit_accel < x_accel and x_accel < upper_limit_accel) and\
                    (lower_limit_accel < y_accel and y_accel < upper_limit_accel) and\
                    (lower_limit_accel < z_accel and z_accel < upper_limit_accel) and\
                    (lower_limit_accel < x_accel and x_accel < upper_limit_accel) and\
                    (lower_limit_accel < y_accel and y_accel < upper_limit_accel) and\
                    (lower_limit_accel < z_accel and z_accel < upper_limit_accel)    \
                   ) :
                   Test_Scripts.uut.silence_device()
                   return False, 'Not within limits', 'Within limit'
            else:
                Test_Scripts.uut.silence_device()
                return False, response, 'response'
        Test_Scripts.uut.silence_device()
        return True, 'Within limits', 'Within limits'

    def continuous_packet_type_S1(self):
        '''Setup'''
        data = Test_Scripts.uut.imu383_command("SF", continuous_packet_type_f + S1)
        data = Test_Scripts.uut.imu383_command("SF", packet_rate_div_f + [0x00,0x01])

        # conver list of hex value to string
        pt = ''.join(hex(val)[2:] for val in S1)
        # use pt.decode("hex") to conver pt ro ASCII

        '''Execute'''
        for each in range(10):
            response = Test_Scripts.uut.read_response()
            #print "S1",response
            if response and response[0] == pt.decode("hex"):
                len = int(response[1],16)
                msg = bytearray.fromhex(response[2])

                x_accel = self._combine_reg_short(msg[0],msg[1]) * (20.0/65536)
                y_accel = self._combine_reg_short(msg[2],msg[3]) * (20.0/65536)
                z_accel = self._combine_reg_short(msg[4],msg[5]) * (20.0/65536)
                x_rate = self._combine_reg_short(msg[6],msg[7]) * (1260.0/65536)
                y_rate = self._combine_reg_short(msg[8],msg[9]) * (1260.0/65536)
                z_rate = self._combine_reg_short(msg[10],msg[11]) * (1260.0/65536)
                x_temp = self._combine_reg_short(msg[12],msg[13]) * (200.0/65536)
                y_temp = self._combine_reg_short(msg[14],msg[15]) * (200.0/65536)
                z_temp = self._combine_reg_short(msg[16],msg[17]) * (200.0/65536)
                board_temp = self._combine_reg_short(msg[18],msg[19]) * (200.0/65536)
                timer = self._combine_reg_ushort(msg[20],msg[21]) * 15.259022
                BIT = self._combine_reg_ushort(msg[22],msg[23])

                '''Result'''
                if( not (lower_limit_accel < x_accel and x_accel < upper_limit_accel) and\
                    (lower_limit_accel < y_accel and y_accel < upper_limit_accel) and\
                    (lower_limit_accel < z_accel and z_accel < upper_limit_accel) and\
                    (lower_limit_accel < x_accel and x_accel < upper_limit_accel) and\
                    (lower_limit_accel < y_accel and y_accel < upper_limit_accel) and\
                    (lower_limit_accel < z_accel and z_accel < upper_limit_accel)    \
                   ) :
                   Test_Scripts.uut.silence_device()
                   return False, 'Not within limits', 'Within limit'
            else:
                Test_Scripts.uut.silence_device()
                return False, response, 'response'
        Test_Scripts.uut.silence_device()
        return True, 'Within limits', 'Within limits'

    def orientation(self, config, void):
        '''Setup'''
        data = Test_Scripts.uut.imu383_command("SF", orientation_f + config)
        Test_Scripts.uut.silence_device()
        orientation_config = ''.join(hex(val)[2:] for val in config)

        '''Execute'''
        data = Test_Scripts.uut.imu383_command("GF", orientation_f)

        '''Result'''
        if(int(data[6:], 16) == int(orientation_config, 16)):
            return True, int(data[6:], 16), int(orientation_config, 16)
        else:
            return False, int(data[6:], 16), int(orientation_config, 16)

    def check_bad_commands(self, field, val):
        '''Setup'''
        Test_Scripts.uut.silence_device()
        nak = ''.join(hex(val)[2:] for val in NAK)

        '''Execute'''
        data = Test_Scripts.uut.imu383_command("SF", field + val)
        if (type(data) != list):
            return False, 'Command Worked', "Negative Response"

        if( int(data[0].encode("hex"),16) == int(nak,16)):
            return True, int(data[0].encode("hex"),16), int(nak,16)
        else:
            #data = Test_Scripts.uut.sensor_command("GF", field)
            return False, int(data[0].encode("hex"),16), int(nak,16)


    def read_only_test(self, field, val):
        '''Setup'''
        data = Test_Scripts.uut.imu383_command("SF", field + val)
        data = Test_Scripts.uut.imu383_command("GF", field)

        '''Execute'''
        actual = int(data[-4:], 16)
        expected = int(''.join(hex(i)[2:] for i in val), 16)

        '''Result'''
        if(actual == expected):
            return False, actual, expected
        else:
            return True, actual, expected

    def print_default_eprom(self):
        data = Test_Scripts.uut.imu383_command("RF", [0x00,0x01])
        orig_field_val = []
        orig_field_val= orig_field_val + [0x00,0x01]
        # store original field value before changing
        orig_field_val.append(int(data[-4:-2],16))  # MSB
        orig_field_val.append(int(data[-2:],16))    # LSB

    def write_field_retention_test(self, field, val):
        '''Setup'''
        Test_Scripts.uut.silence_device()
        data = Test_Scripts.uut.imu383_command("RF", field)
        orig_field_val = []
        orig_field_val= orig_field_val + field
        # store original field value before changing
        orig_field_val.append(int(data[-4:-2],16))# MSB
        orig_field_val.append(int(data[-2:],16))  # LSB

        '''Execute'''
        data = Test_Scripts.uut.imu383_command("WF", field + val)
        Test_Scripts.uut.restart_device()
        Test_Scripts.uut.silence_device()
        data = Test_Scripts.uut.imu383_command("RF", field)

        '''Reset to Original'''
        data0 = Test_Scripts.uut.imu383_command("WF", orig_field_val)
        Test_Scripts.uut.restart_device()
        Test_Scripts.uut.silence_device()
        data0 = Test_Scripts.uut.imu383_command("RF", field)

        '''Result'''

        if(int(data[-4:],16) == int(''.join(hex(i)[2:] for i in val),16)):
            return True, int(data[-4:],16), int(''.join(hex(i)[2:] for i in val),16)
        else:
            return False, int(data[-4:],16), int(''.join(hex(i)[2:] for i in val),16)

    def _get_packet_rate(self, packet_type):
        # Convert from Hex list to ASCII
        type = ''.join(hex(val)[2:] for val in packet_type)

        nbytes = Test_Scripts.uut.UUT.inWaiting()
        if nbytes > 0:
            indata = Test_Scripts.uut.UUT.read(nbytes)
            #print indata

        t0 = time.time()
        while(time.time() - t0 < 2):
            response = Test_Scripts.uut.read_response()

        test_time = 10
        t0 = time.time()
        count = 0
        while(time.time() - t0 < test_time):
            #print count, time.time(), t0
            response = Test_Scripts.uut.read_response()
            #print response
            # Count up when S0/S1 packet recceived
            if response and response[0] == type.decode("hex"):
                #print response
                count = count+1
        #print "Count",count
        if(count != 0):
            return count/test_time
        else:
            return count

    def write_field_effective_test_rate_f(self):
        field = packet_rate_div_f
        val = [0x00, 0x01]      #packet rate div value
        expected_rate_hz = 100
        actual_rate_hz = 0

        '''Setup'''
        data = Test_Scripts.uut.imu383_command("RF", field)
        orig_field_val = []
        orig_field_val= orig_field_val + field
        # store original field value before changing
        orig_field_val.append(int(data[-4:-2],16))
        orig_field_val.append(int(data[-2:],16))     #read last two characters

        data = Test_Scripts.uut.imu383_command("SF", continuous_packet_type_f + S1)
        Test_Scripts.uut.silence_device()
        uut_packet_rate = self._get_packet_rate(S1)

        '''Execute'''
        # Write to packet rate field
        data = Test_Scripts.uut.imu383_command("WF", field + val)
        # packet rate souldn't change
        uut_packet_rate = self._get_packet_rate(S1)
        if(uut_packet_rate != 0):
            return False, uut_packet_rate, 0        # packet rate changed when it shouldn't
        else:
            # restart the device if the rate hasn't changed
            Test_Scripts.uut.restart_device()
            data = Test_Scripts.uut.imu383_command("SF", continuous_packet_type_f + S1)
            actual_rate_hz = self._get_packet_rate(S1)

        '''Reset to Original'''
        Test_Scripts.uut.imu383_command("WF", orig_field_val)
        Test_Scripts.uut.restart_device()
        Test_Scripts.uut.silence_device()
        Test_Scripts.uut.imu383_command("RF", field)

        # Verify that Packet rate is as expected after power cycle
        if(actual_rate_hz == expected_rate_hz):
            return True, actual_rate_hz, expected_rate_hz
        else:
            return False, actual_rate_hz, expected_rate_hz

    def set_field_retention_test(self, field, val):
        '''Setup'''
        Test_Scripts.uut.restart_device()
        Test_Scripts.uut.silence_device()
        data = Test_Scripts.uut.imu383_command("RF", field)
        #print data
        orig_field_val = int(data[-4:],16)     #read last two characters
        #print orig_field_val

        '''Execute'''
        data = Test_Scripts.uut.imu383_command("SF", field + val)
        #print data, field+val
        Test_Scripts.uut.restart_device()
        Test_Scripts.uut.silence_device()
        data = Test_Scripts.uut.imu383_command("RF", field)
        #print data
        '''Result'''
        #print int(data[-4:],16), orig_field_val
        # verify that GF value doesnt retain after power cycle and matches with EEPROM default value

        if(int(data[-4:],16) == orig_field_val):
            return True, int(data[-4:],16), orig_field_val
        else:
            return False, int(data[-4:],16), orig_field_val

    def set_field_effective_test_rate_f(self):
        field = continuous_packet_type_f

        '''Setup'''
        data = Test_Scripts.uut.imu383_command("RF", field)
        orig_field_val = data[-4:]

        data = Test_Scripts.uut.imu383_command("SF", continuous_packet_type_f + S0)
        data = Test_Scripts.uut.imu383_command("SF", packet_rate_div_f + [0x00,0x01])

        packet = Test_Scripts.uut.read_response();
        ptype = ''.join(hex(val)[2:] for val in S0)

        if(packet[0] != ptype.decode("hex")):
            return False, packet[0], ptype.decode("hex")

        Test_Scripts.uut.restart_device()
        data = Test_Scripts.uut.imu383_command("SF", packet_rate_div_f + [0x00,0x01])
        packet = Test_Scripts.uut.read_response();
        #print packet
        if(packet[0] != orig_field_val.decode("hex")):
            return False, packet[0], orig_field_val.decode("hex")

        return True, packet[0], orig_field_val.decode("hex")

    def read_packets_S0(self):
        data = Test_Scripts.uut.imu383_command("SF", continuous_packet_type_f + S0)
        data = Test_Scripts.uut.imu383_command("SF", packet_rate_div_f + [0x00,0x01])

        # conver list of hex value to string
        pt = ''.join(hex(val)[2:] for val in S0)
        # use pt.decode("hex") to conver pt ro ASCII

        '''Execute'''
        for each in range(1000000):
            response = Test_Scripts.uut.read_response()
            #print "S0",response

            if not response:
                return False, 'No response', 'Non zero packets'

            if response[0] == pt.decode("hex"):
                if(int(response[2],16) == 0):
                    #print response[2]
                    return False, response[2], 'Non zero packets'
            else:
                return False, response[2], 'Non zero packets'

        return True, 'Non zero packets', 'Non zero packets'


    def read_packets_S1(self):
        data = Test_Scripts.uut.imu383_command("SF", continuous_packet_type_f + S1)
        data = Test_Scripts.uut.imu383_command("SF", packet_rate_div_f + [0x00,0x01])

        # conver list of hex value to string
        pt = ''.join(hex(val)[2:] for val in S1)
        # use pt.decode("hex") to conver pt ro ASCII

        '''Execute'''
        for each in range(1000000):
            response = Test_Scripts.uut.read_response()
            #print "S1",response
            if not response:
                return False, 'No response', 'Non zero packets'

            if response[0] == pt.decode("hex"):
                if(int(response[2],16) == 0):
                    #print response[2]
                    return False, response[2], 'Non zero packets'
            else:
                return False, response[2], 'Non zero packets'

        return True, 'Non zero packets', 'Non zero packets'


    def _get_s0_sampling_count(self):
        # convert list of hex value to string
        pt = ''.join(hex(val)[2:] for val in S0)

        response = Test_Scripts.uut.read_response()

        if response and response[0] == pt.decode("hex"):
            len = int(response[1],16)
            msg = bytearray.fromhex(response[2])
            return self._combine_reg_ushort(msg[26],msg[27])
        return -1

    def s0_sampling_counter_test(self, rate_val, rate_hz):
        max_counter = 65536
        interval = max_counter/rate_hz
        #print interval
        once = True;
        Test_Scripts.uut.restart_device()
        Test_Scripts.uut.silence_device()
        data = Test_Scripts.uut.imu383_command("SF", continuous_packet_type_f + S0)
        data = Test_Scripts.uut.imu383_command("SF", packet_rate_div_f + rate_val)

        # convert list of hex value to string
        pt = ''.join(hex(val)[2:] for val in S0)
        # use pt.decode("hex") to conver pt ro ASCII

        '''Execute'''
        for each in range(10):
            curr_count = self._get_s0_sampling_count()
            if(curr_count == -1):
                Test_Scripts.uut.silence_device()
                return False, "Response", "No Response"

            # Set prev count
            if(once):
                once = False
                prev_count = curr_count
            else:
                # Fail case
                if(prev_count > curr_count):
                    diff = (65535 - prev_count) + curr_count;
                else:
                    diff = curr_count - prev_count
                #print prev_count, curr_count, diff
                if(diff != interval - 1 and diff != interval and diff != interval + 1):
                    Test_Scripts.uut.silence_device()
                    return False, diff, interval
                # pass case
                prev_count = curr_count

        Test_Scripts.uut.silence_device()
        return True, diff, interval

    def _get_s1_sampling_count(self):
        # convert list of hex value to string
        pt = ''.join(hex(val)[2:] for val in S1)

        response = Test_Scripts.uut.read_response()

        if response and response[0] == pt.decode("hex"):
            len = int(response[1],16)
            msg = bytearray.fromhex(response[2])
            return self._combine_reg_ushort(msg[20],msg[21])
        return -1

    def s1_sampling_counter_test(self, rate_val, rate_hz):
        max_counter = 65536
        interval = max_counter/rate_hz
        #print interval
        once = True;
        Test_Scripts.uut.restart_device()
        Test_Scripts.uut.silence_device()
        data = Test_Scripts.uut.imu383_command("SF", continuous_packet_type_f + S1)
        data = Test_Scripts.uut.imu383_command("SF", packet_rate_div_f + rate_val)

        # convert list of hex value to string
        pt = ''.join(hex(val)[2:] for val in S1)
        # use pt.decode("hex") to conver pt ro ASCII

        '''Execute'''
        for each in range(10):
            curr_count = self._get_s1_sampling_count()
            if(curr_count == -1):
                Test_Scripts.uut.silence_device()
                return False, "Response", "No Response"
            # Set prev count
            if(once):
                once = False
                prev_count = curr_count
            else:
                # Fail case
                if(prev_count > curr_count):
                    diff = (65535 - prev_count) + curr_count;
                else:
                    diff = curr_count - prev_count
                #print prev_count, curr_count, diff
                if(diff != interval - 1 and diff != interval and diff != interval + 1):
                    Test_Scripts.uut.silence_device()
                    return False, diff, interval
                # pass case
                prev_count = curr_count

        Test_Scripts.uut.silence_device()
        return True, diff, interval

#################################################

class Test_Environment:

    def __init__(self, device):
        self.scripts = Test_Scripts(device)
        self.test_sections = []

    # Add test scetions & test scripts here
    def setup_tests(self):

        section1 = Test_Section("UART Transaction Verification")
        self.test_sections.append(section1)
        section1.add_test_case(Code("Default Baudrate Test",   self.scripts.default_baudrate_test))
        section1.add_test_case(Code("Communication Test",      self.scripts.communication_test))
        section1.add_test_case(Code("Header Test",             self.scripts.header_test))
        section1.add_test_case(Code("Payload Length Test",     self.scripts.payload_length_test))
        section1.add_test_case(Code("Payload Test",            self.scripts.payload_test))
        section1.add_test_case(Code("CRC Test",                self.scripts.CRC_test))
        section1.add_test_case(Code("Polled Mode Test",        self.scripts.polled_mode_test))
        section1.add_test_case(Code("Continuous Mode Test",    self.scripts.continuouse_mode_test))
        section1.add_test_case(Code("Verify ID Packet Types",     self.scripts.verify_ID_packet_type))
        section1.add_test_case(Code("Verify VR Packet Types",     self.scripts.verify_VR_packet_type))
        section1.add_test_case(Code("Verify T0 Packet Types",     self.scripts.verify_T0_packet_type))
        section1.add_test_case(Code("Verify S0 Packet Types",     self.scripts.verify_S0_packet_type))
        section1.add_test_case(Code("Verify S1 Packet Types",     self.scripts.verify_S1_packet_type))
        section1.add_test_case(Code("Verify RF Packet Types",     self.scripts.verify_RF_packet_type))
        section1.add_test_case(Code("Verify WF Packet Types",     self.scripts.verify_WF_packet_type))
        section1.add_test_case(Code("Verify GF Packet Types",     self.scripts.verify_GF_packet_type))
        section1.add_test_case(Code("Verify SF Packet Types",     self.scripts.verify_SF_packet_type))

        section2 = Test_Section("Read Field Default Checks")
        self.test_sections.append(section2)
        section2.add_test_case(Condition_Check("Packet Rate Divider Default",                 self.scripts.rf_default_test, packet_rate_div_f,              0x0001))
        section2.add_test_case(Condition_Check("Unit Baudrate Default",                       self.scripts.rf_default_test, unit_baud_f,                    0x0005))
        section2.add_test_case(Condition_Check("Continuous Packet Type Default",              self.scripts.rf_default_test, continuous_packet_type_f,       0x534D))
        section2.add_test_case(Condition_Check("Gyro Filter Setting Default",                 self.scripts.rf_default_test, gyro_filter_setting_f,          0x085E))
        section2.add_test_case(Condition_Check("Accelerometer Filter Setting Default",        self.scripts.rf_default_test, accel_filter_setting_f,         0x085E))
        section2.add_test_case(Condition_Check("Orientation Default",                         self.scripts.rf_default_test, orientation_f,                  0x006B))
        section2.add_test_case(Condition_Check("Sensor Enable Setting Default",               self.scripts.rf_default_test, sensor_enable_f,                0x0007))
        section2.add_test_case(Condition_Check("Output Select Setting Default",               self.scripts.rf_default_test, output_select_f,                0x0007))
        section2.add_test_case(Condition_Check("Fault Detection - Chip1 Default",             self.scripts.rf_default_test, fault_detct_chip1_f,            0xFFFF))
        section2.add_test_case(Condition_Check("Fault Detection - Chip2 Default",             self.scripts.rf_default_test, fault_detct_chip2_f,            0xFFFF))
        section2.add_test_case(Condition_Check("Fault Detection - Chip3 Default",             self.scripts.rf_default_test, fault_detct_chip3_f,            0xFFFF))
        section2.add_test_case(Condition_Check("Accel Consistency Check Enable Default",      self.scripts.rf_default_test, accel_consistency_en_f,         0x0001))
        section2.add_test_case(Condition_Check("Rate-Sensor Consistency Check Enable Default",self.scripts.rf_default_test, rate_sensor_consistency_en_f,   0x0001))

        section3 = Test_Section("Get Field Default Checks")
        self.test_sections.append(section3)
        #section3.add_test_case(Condition_Check("Packet Rate Divider Default",                 self.scripts.gf_default_test, packet_rate_div_f,              0x0001))
        section3.add_test_case(Condition_Check("Unit Baudrate Default",                       self.scripts.gf_default_test, unit_baud_f,                    0x0005))
        section3.add_test_case(Condition_Check("Continuous Packet Type Default",              self.scripts.gf_default_test, continuous_packet_type_f,       0x534D))
        section3.add_test_case(Condition_Check("Gyro Filter Setting Default",                 self.scripts.gf_default_test, gyro_filter_setting_f,          0x085E))
        section3.add_test_case(Condition_Check("Accelerometer Filter Setting Default",        self.scripts.gf_default_test, accel_filter_setting_f,         0x085E))
        section3.add_test_case(Condition_Check("Orientation Default",                         self.scripts.gf_default_test, orientation_f,                  0x006B))
        section3.add_test_case(Condition_Check("Sensor Enable Setting Default",               self.scripts.gf_default_test, sensor_enable_f,                0x0007))
        section3.add_test_case(Condition_Check("Output Select Setting Default",               self.scripts.gf_default_test, output_select_f,                0x0007))
        section3.add_test_case(Condition_Check("Fault Detection - Chip1 Default",             self.scripts.gf_default_test, fault_detct_chip1_f,            0xFFFF))
        section3.add_test_case(Condition_Check("Fault Detection - Chip2 Default",             self.scripts.gf_default_test, fault_detct_chip2_f,            0xFFFF))
        section3.add_test_case(Condition_Check("Fault Detection - Chip3 Default",             self.scripts.gf_default_test, fault_detct_chip3_f,            0xFFFF))
        section3.add_test_case(Condition_Check("Accel Consistency Check Enable Default",      self.scripts.gf_default_test, accel_consistency_en_f,         0x0001))
        section3.add_test_case(Condition_Check("Rate-Sensor Consistency Check Enable Default",self.scripts.gf_default_test, rate_sensor_consistency_en_f,   0x0001))

        section4 = Test_Section("Packet Rate Divider Functional Test")
        self.test_sections.append(section4)
        section4.add_test_case(Condition_Check("Packet Rate Div 200Hz",  self.scripts.packet_rate_div, [0x00,0xC8], 200))
        section4.add_test_case(Condition_Check("Packet Rate Div 100Hz",  self.scripts.packet_rate_div, [0x00,0x01], 100))

        section4.add_test_case(Condition_Check("Packet Rate Div 50Hz",   self.scripts.packet_rate_div, [0x00,0x02], 50))
        section4.add_test_case(Condition_Check("Packet Rate Div 25Hz",   self.scripts.packet_rate_div, [0x00,0x04], 25))
        section4.add_test_case(Condition_Check("Packet Rate Div 20Hz",   self.scripts.packet_rate_div, [0x00,0x05], 20))
        section4.add_test_case(Condition_Check("Packet Rate Div 10Hz",   self.scripts.packet_rate_div, [0x00,0x0A], 10))
        section4.add_test_case(Condition_Check("Packet Rate Div 5Hz",    self.scripts.packet_rate_div, [0x00,0x14], 5))
        section4.add_test_case(Condition_Check("Packet Rate Div 4Hz",    self.scripts.packet_rate_div, [0x00,0x19], 4))
        section4.add_test_case(Condition_Check("Packet Rate Div 2Hz",    self.scripts.packet_rate_div, [0x00,0x32], 2))
        section4.add_test_case(Condition_Check("Packet Rate Div Quiet",  self.scripts.packet_rate_div, [0x00,0x00], 0))

        section5 = Test_Section("Continuous Packet Type Functional Test")
        self.test_sections.append(section5)
        section5.add_test_case(Code("Continuous Packet Type S0 Functional Test",  self.scripts.continuous_packet_type_S0))
        section5.add_test_case(Code("Continuous Packet Type S1 Functional Test",  self.scripts.continuous_packet_type_S1))

        section6 = Test_Section("Orientation Functional Test")
        self.test_sections.append(section6)
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x0000",        self.scripts.orientation, [0x00, 0x00]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x0009",        self.scripts.orientation, [0x00, 0x09]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x0023",        self.scripts.orientation, [0x00, 0x23]))

        section6.add_test_case(Condition_Check("Orientation Functional Test 0x002A",        self.scripts.orientation, [0x00, 0x2A]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x0041",        self.scripts.orientation, [0x00, 0x41]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x0048",        self.scripts.orientation, [0x00, 0x48]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x0062",        self.scripts.orientation, [0x00, 0x62]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x006B",        self.scripts.orientation, [0x00, 0x6B]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x0085",        self.scripts.orientation, [0x00, 0x85]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x008C",        self.scripts.orientation, [0x00, 0x8C]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x0092",        self.scripts.orientation, [0x00, 0x92]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x009B",        self.scripts.orientation, [0x00, 0x9B]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x00C4",        self.scripts.orientation, [0x00, 0xC4]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x00CD",        self.scripts.orientation, [0x00, 0xCD]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x00D3",        self.scripts.orientation, [0x00, 0xD3]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x00DA",        self.scripts.orientation, [0x00, 0xDA]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x0111",        self.scripts.orientation, [0x01, 0x11]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x0118",        self.scripts.orientation, [0x01, 0x18]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x0124",        self.scripts.orientation, [0x01, 0x24]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x012D",        self.scripts.orientation, [0x01, 0x2D]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x0150",        self.scripts.orientation, [0x01, 0x50]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x0159",        self.scripts.orientation, [0x01, 0x59]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x0165",        self.scripts.orientation, [0x01, 0x65]))
        section6.add_test_case(Condition_Check("Orientation Functional Test 0x016C",        self.scripts.orientation, [0x01, 0x6C]))
        #checking few random bad orientation values
        section6.add_test_case(Condition_Check("Orientation Functional Test Bad Command1",  self.scripts.check_bad_commands, orientation_f ,[0x11, 0x11]))
        section6.add_test_case(Condition_Check("Orientation Functional Test Bad Command2",  self.scripts.check_bad_commands, orientation_f ,[0x22, 0x22]))
        section6.add_test_case(Condition_Check("Orientation Functional Test Bad Command3",  self.scripts.check_bad_commands, orientation_f ,[0x33, 0x33]))
        section6.add_test_case(Condition_Check("Orientation Functional Test Bad Command4",  self.scripts.check_bad_commands, orientation_f ,[0x44, 0x44]))
        section6.add_test_case(Condition_Check("Orientation Functional Test Bad Command5",  self.scripts.check_bad_commands, orientation_f ,[0x55, 0x55]))
        section6.add_test_case(Condition_Check("Orientation Functional Test Bad Command6",  self.scripts.check_bad_commands, orientation_f ,[0x66, 0x66]))
        section6.add_test_case(Condition_Check("Orientation Functional Test Bad Command7",  self.scripts.check_bad_commands, orientation_f ,[0x99, 0x99]))
        section6.add_test_case(Condition_Check("Orientation Functional Test Bad Command8",  self.scripts.check_bad_commands, orientation_f ,[0xAA, 0xAA]))
        section6.add_test_case(Condition_Check("Orientation Functional Test Bad Command9",  self.scripts.check_bad_commands, orientation_f ,[0xBB, 0xBB]))
        section6.add_test_case(Condition_Check("Orientation Functional Test Bad Command10", self.scripts.check_bad_commands, orientation_f ,[0xCC, 0xCC]))
        section6.add_test_case(Condition_Check("Orientation Functional Test Bad Command11", self.scripts.check_bad_commands, orientation_f ,[0xDD, 0xDD]))
        section6.add_test_case(Condition_Check("Orientation Functional Test Bad Command12", self.scripts.check_bad_commands, orientation_f ,[0xEE, 0xEE]))

        # No need to test this
        #section7 = Test_Section("Read-only Test")
        #self.test_sections.append(section7)
        #section7.add_test_case(Condition_Check("Fault Detection Fault Cause - Chip1 read-only Test ",  self.scripts.read_only_test, fault_detct_chip1_f, [0x00, 0x02]))
        #section7.add_test_case(Condition_Check("Fault Detection Fault Cause - Chip2 read-only Test ",  self.scripts.read_only_test, fault_detct_chip2_f, [0x00, 0x02]))
        #section7.add_test_case(Condition_Check("Fault Detection Fault Cause - Chip3 read-only Test ",  self.scripts.read_only_test, fault_detct_chip3_f, [0x00, 0x02]))

        #section8 = Test_Section("Fault Detection Field Test")
        #self.test_sections.append(section8)
        #section8.add_test_case(Condition_Check("Fault Detection Field Test - accel ",   self.scripts.fault_detection_field_test, accel_consistency_en_f,         [0x00, 0x02]))
        #section8.add_test_case(Condition_Check("Fault Detection Field Test - rate ",    self.scripts.fault_detection_field_test, rate_sensor_consistency_en_f,   [0x00, 0x03]))

        section9 = Test_Section("Bad Field Values")
        self.test_sections.append(section9)
        section9.add_test_case(Condition_Check("Bad Field Value - Packet Rate",             self.scripts.check_bad_commands, packet_rate_div_f,         [0x00, 0x03]))
        # This test is always fails, its a legacy thing. Commenting out.
        #section9.add_test_case(Condition_Check("Bad Field Value - Baudrate",                self.scripts.check_bad_commands, unit_baud_f,               [0x00, 0x00]))
        section9.add_test_case(Condition_Check("Bad Field Value - Continuous Packet Type",  self.scripts.check_bad_commands, continuous_packet_type_f,  [0x00, 0x00]))

        section10 = Test_Section("Write Field Tests")
        self.test_sections.append(section10)
        section10.add_test_case(Condition_Check("Write Field Data Retention Test - Packet Rate Div",       self.scripts.write_field_retention_test, packet_rate_div_f,             [0x00, 0x32]))
        section10.add_test_case(Condition_Check("Write Field Data Retention Test - Continuous Packet Type",self.scripts.write_field_retention_test, continuous_packet_type_f,      [0x53, 0x30]))
        section10.add_test_case(Condition_Check("Write Field Data Retention Test - Orientation",           self.scripts.write_field_retention_test, orientation_f,                 [0x00, 0x62]))
        section10.add_test_case(Condition_Check("Write Field Data Retention Test - Gyro Filter Settings",  self.scripts.write_field_retention_test, gyro_filter_setting_f,         [0x00, 0x32]))
        section10.add_test_case(Condition_Check("Write Field Data Retention Test - Accel Filter Settings", self.scripts.write_field_retention_test, accel_filter_setting_f,        [0x00, 0x32]))
        section10.add_test_case(Condition_Check("Write Field Data Retention Test - Sensor Enable",         self.scripts.write_field_retention_test, sensor_enable_f,               [0x00, 0x32]))
        section10.add_test_case(Condition_Check("Write Field Data Retention Test - Output Select",         self.scripts.write_field_retention_test, output_select_f,               [0x00, 0x32]))
        section10.add_test_case(Condition_Check("Write Field Data Retention Test - Accel Consistency",     self.scripts.write_field_retention_test, accel_consistency_en_f,        [0x00, 0x32]))
        section10.add_test_case(Condition_Check("Write Field Data Retention Test - Rate Sens Consistency", self.scripts.write_field_retention_test, rate_sensor_consistency_en_f,  [0x00, 0x32]))
        section10.add_test_case(Code("Write Field Data Effectiveness Tests", self.scripts.write_field_effective_test_rate_f))
        section10.add_test_case(Condition_Check("Set Field Data Retention Test - Packet Rate Div",       self.scripts.set_field_retention_test, packet_rate_div_f,             [0x00, 0x32]))
        section10.add_test_case(Condition_Check("Set Field Data Retention Test - Continuous Packet Type",self.scripts.set_field_retention_test, continuous_packet_type_f,      [0x53, 0x30]))
        section10.add_test_case(Condition_Check("Set Field Data Retention Test - Orientation",           self.scripts.set_field_retention_test, orientation_f,                 [0x00, 0x62]))
        section10.add_test_case(Condition_Check("Set Field Data Retention Test - Gyro Filter Settings",  self.scripts.set_field_retention_test, gyro_filter_setting_f,         [0x00, 0x32]))
        section10.add_test_case(Condition_Check("Set Field Data Retention Test - Accel Filter Settings", self.scripts.set_field_retention_test, accel_filter_setting_f,        [0x00, 0x32]))
        section10.add_test_case(Condition_Check("Set Field Data Retention Test - Sensor Enable",         self.scripts.set_field_retention_test, sensor_enable_f,               [0x00, 0x32]))
        section10.add_test_case(Condition_Check("Set Field Data Retention Test - Output Select",         self.scripts.set_field_retention_test, output_select_f,               [0x00, 0x32]))
        section10.add_test_case(Condition_Check("Set Field Data Retention Test - Accel Consistency",     self.scripts.set_field_retention_test, accel_consistency_en_f,        [0x00, 0x32]))
        section10.add_test_case(Condition_Check("Set Field Data Retention Test - Rate Sens Consistency", self.scripts.set_field_retention_test, rate_sensor_consistency_en_f,  [0x00, 0x32]))
        section10.add_test_case(Code("set Field Data Effectiveness Tests", self.scripts.set_field_effective_test_rate_f))


        section11 = Test_Section("Sampling Counter Test")
        self.test_sections.append(section11)
        section11.add_test_case(Condition_Check("Sampling Counter Test - S0 Packet, 200Hz", self.scripts.s0_sampling_counter_test, [0x00,0xC8], 200))
        section11.add_test_case(Condition_Check("Sampling Counter Test - S0 Packet, 100Hz", self.scripts.s0_sampling_counter_test, [0x00,0x01], 100))
        section11.add_test_case(Condition_Check("Sampling Counter Test - S0 Packet, 50Hz",  self.scripts.s0_sampling_counter_test, [0x00,0x02], 50))
        section11.add_test_case(Condition_Check("Sampling Counter Test - S0 Packet, 25Hz",  self.scripts.s0_sampling_counter_test, [0x00,0x04], 25))
        section11.add_test_case(Condition_Check("Sampling Counter Test - S0 Packet, 20Hz",  self.scripts.s0_sampling_counter_test, [0x00,0x05], 20))
        section11.add_test_case(Condition_Check("Sampling Counter Test - S0 Packet, 10Hz",  self.scripts.s0_sampling_counter_test, [0x00,0x0A], 10))
        # Fix these in future, not critical
        #section11.add_test_case(Condition_Check("Sampling Counter Test - S0 Packet, 5Hz",   self.scripts.s0_sampling_counter_test, [0x00,0x14], 5))
        #section11.add_test_case(Condition_Check("Sampling Counter Test - S0 Packet, 4Hz",   self.scripts.s0_sampling_counter_test, [0x00,0x18], 4))
        #section11.add_test_case(Condition_Check("Sampling Counter Test - S0 Packet, 2Hz",   self.scripts.s0_sampling_counter_test, [0x00,0x32], 2))

        section11.add_test_case(Condition_Check("Sampling Counter Test - S1 Packet, 200Hz", self.scripts.s1_sampling_counter_test, [0x00,0xC8], 200))
        section11.add_test_case(Condition_Check("Sampling Counter Test - S1 Packet, 100Hz", self.scripts.s1_sampling_counter_test, [0x00,0x01], 100))
        section11.add_test_case(Condition_Check("Sampling Counter Test - S1 Packet, 50Hz",  self.scripts.s1_sampling_counter_test, [0x00,0x02], 50))
        section11.add_test_case(Condition_Check("Sampling Counter Test - S1 Packet, 25Hz",  self.scripts.s1_sampling_counter_test, [0x00,0x04], 25))
        section11.add_test_case(Condition_Check("Sampling Counter Test - S1 Packet, 20Hz",  self.scripts.s1_sampling_counter_test, [0x00,0x05], 20))
        section11.add_test_case(Condition_Check("Sampling Counter Test - S1 Packet, 10Hz",  self.scripts.s1_sampling_counter_test, [0x00,0x0A], 10))
        # Fix these in future, not critical
        #section11.add_test_case(Condition_Check("Sampling Counter Test - S1 Packet, 5Hz",   self.scripts.s1_sampling_counter_test, [0x00,0x14], 5))
        #section11.add_test_case(Condition_Check("Sampling Counter Test - S1 Packet, 4Hz",   self.scripts.s1_sampling_counter_test, [0x00,0x18], 4))
        #section11.add_test_case(Condition_Check("Sampling Counter Test - S1 Packet, 2Hz",   self.scripts.s1_sampling_counter_test, [0x00,0x32], 2))

        section12 = Test_Section("Longterm Packet Test")
        self.test_sections.append(section11)
        section12.add_test_case(Code("Longterm packet read test", self.scripts.read_packets_S0))
        section12.add_test_case(Code("Longterm packet read test", self.scripts.read_packets_S1))


    def run_tests(self):
        for test in self.test_sections:
            test.run_test_section()

    def print_results(self):
        print "\tTest Results::"
        for section in self.test_sections:
            print "\t\tSection " + str(section.section_id) + ": " + section.section_name + "\r\n"
            for test in section.test_cases:
                id = str(section.section_id) + "." + str(test.test_id)
                result_str = "\t\t\tPassed --> " if test.result['status'] else "\t\t\tFailed --x "
                print result_str + id + " " + test.test_case_name + "\r\n"

    def log_results(self, file_name):
        logger = TestLogger(file_name)
        field_names = ['id', 'test_name', 'expected', 'actual', 'status']
        logger.create(field_names)
        for section in self.test_sections:
            for test in section.test_cases:
                #print test.result['id'],test.result['test_name'],test.result['expected'],test.result['actual']
                logger.write_log(test.result)
