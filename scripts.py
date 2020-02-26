import time
import struct
from IMU383_Uart import UART_Dev
from IMU383_test_cases import test_section
from IMU383_test_cases import test_case
from IMU383_test_cases import code
from IMU383_test_cases import condition_check
from math import pi



# TODO: Update all the Field and Packey Type address to pre-defined variables for portability

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
output_selecf_f                 = [0x00,0x43]
fault_detct_chip1_f             = [0x00,0x4C]
fault_detct_chip2_f             = [0x00,0x4D]
fault_detct_chip3_f             = [0x00,0x4E]
accel_consistency_en_f          = [0x00,0x61]
rate_sensor_consistency_en_f    = [0x00,0x62]


# Add test scripts here
class test_scripts:
    uut = None

    def __init__(self, device):
        test_scripts.uut = device

    def echo_test(self):
        #test_scripts.uut.send_message(echo)
        #pt,pll,pl = test_scripts.uut.unpacked_response()
        response = test_scripts.uut.imu383_command("CH",[0x41])
        if(int(response,16) == 0x41):
            return True
        else:
            return False

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
        return self.echo_test
    def polled_mode_test(self):
        response = test_scripts.uut.imu383_command("GP", [0x53,0x30])
        if(response[0] == 'S0'):
            return True
        else:
            return False
    def continuouse_mode_test(self):
        data = test_scripts.uut.imu383_command("SF",[0x00,0x03,0x53,0x30])
        #print data
        data = test_scripts.uut.imu383_command("SF", [0x00,0x01,0x00,0x32])
        #print data
        t0 = time.time()
        count = 0
        while(time.time() - t0 < 10.00):
            count = count+1
            response = test_scripts.uut.read_response()
            #print count
            #time.sleep(2)
        # verify that UUT reads data 20 times in 10 seconds,
        # more ofthen than not it reads 21 times due to time it takes to read
        if(count == 20 or count == 21):
            return True
        else:
            return False

    def id_test(self):
        response = test_scripts.uut.imu383_command("GP", ID)
        '''
        payload_len = data[1]
        payload = data[2]
        serial_number = payload[:4]
        model_string = payload[4:]
        #remaining = payload[]
        print packet_type
        print payload_len
        print payload
        print bytearray.fromhex(serial_number)
        print bytearray.fromhex(model_string)
        '''
        if(response[0] == 'ID'):
            return True
        else:
            return False

    def version_data_test(self):
        response = test_scripts.uut.imu383_command("GP", VR)
        if(response[0] == 'VR'):
            return True
        else:
            return False
    def Test0_test(self):
        response = test_scripts.uut.imu383_command("GP", T0)
        if(response[0] == 'T0'):
            return True
        else:
            return False
    def scaled_sensor0_test(self):
        response = test_scripts.uut.imu383_command("GP", S0)
        if(response[0] == 'S0'):
            return True
        else:
            return False
    def scaled_sensor1_test(self):
        response = test_scripts.uut.imu383_command("GP", S1)
        if(response[0] == 'S1'):
            return True
        else:
            return False

    def get_field_test(self):
        response = test_scripts.uut.imu383_command("GF", [0x00, 0x01])
        if not response:
            return False
        else:
            return True
    def read_field_test(self):
        response = test_scripts.uut.imu383_command("RF", [0x00, 0x01])
        if not response:
            return False
        else:
            return True

    def set_field_test(self):
        response = test_scripts.uut.imu383_command("SF", [0x00, 0x01, 0x00, 0x00])
        if not response:
            return False
        else:
            return True
    def write_field_test(self):
        response = test_scripts.uut.imu383_command("WF", [0x00, 0x01, 0x00, 0x00])
        if not response:
            return False
        else:
            return True

    def verify_packet_types(self):
        ping_test = test_scripts.uut.ping_device()
        echo_test = self.echo_test()
        get_packet_test = self.polled_mode_test()
        id = self.id_test()
        vr = self.version_data_test()
        t0 = self.Test0_test()
        s0 = self.scaled_sensor0_test()
        s1 = self.scaled_sensor1_test()
        rf = self.read_field_test()
        wf = self.write_field_test()
        gf = self.get_field_test()
        sf = self.set_field_test()

        return ping_test and echo_test and get_packet_test and id and vr    \
                and t0 and s0 and s1 and gf and rf and wf and sf

    def rf_default_test(self, cmd, param):
        response = test_scripts.uut.imu383_command("RF", cmd)

        if(int(response[6:],16) == param):
            return True
        else:
            return False

    def gf_default_test(self, cmd, param):
        response = test_scripts.uut.imu383_command("GF", cmd)

        if(int(response[6:],16) == param):
            return True
        else:
            return False

    # rate_val is packet_rate_value in list, eg:[0x00, 0x05]
    # rateHz is rate at which packets are expected
    def packet_rate_div(self, rate, rateHz):

        '''Setup'''
        # Set S0 as continuous packet type
        data = test_scripts.uut.imu383_command("SF",[0x00,0x03,0x53,0x30])

        test_time = 20
        field = packet_rate_div_f      # Packet Rate Div Field Address

        resp = test_scripts.uut.imu383_command("SF", field + rate)

        if not resp:
            print "ERORR: Dint receive data"
            return False
        #print data

        '''Execute'''
        t0 = time.time()
        count = 0
        while(time.time() - t0 < test_time):
            response = test_scripts.uut.read_response()
            # Count up when S0 packet recceived
            if response and response[0] == "S0":
                #print response
                count = count+1

        test_scripts.uut.silence_device()

        '''Result'''
        if(rateHz == 0):
            return True if(count == 0) else False
        elif(((rateHz * test_time - 1) < count) or (count < (rateHz * test_time + 1))):
            return True
        else:
            return False

    def combine_reg_short(self,lsb,msb):
            lsb = struct.pack('B',lsb)
            msb = struct.pack('B',msb)
            return struct.unpack('h',msb+lsb)[0]

    def combine_reg_ushort(self,lsb,msb):
            lsb = struct.pack('B',lsb)
            msb = struct.pack('B',msb)
            return struct.unpack('H',msb+lsb)[0]

    def continuous_packet_type_S0(self):
        '''Setup'''
        passed = True

        data = test_scripts.uut.imu383_command("SF", continuous_packet_type_f + S0)
        data = test_scripts.uut.imu383_command("SF", packet_rate_div_f + [0x00,0x01])

        # conver list of hex value to string
        pt = ''.join(hex(val)[2:] for val in S0)
        # use pt.decode("hex") to conver pt ro ASCII

        '''Execute'''
        for each in range(10):
            response = test_scripts.uut.read_response()
            if response and response[0] == pt.decode("hex"):
                len = int(response[1],16)
                msg = bytearray.fromhex(response[2])

                x_accel = self.combine_reg_short(msg[0],msg[1]) * (20.0/65536)
                y_accel = self.combine_reg_short(msg[2],msg[3]) * (20.0/65536)
                z_accel = self.combine_reg_short(msg[4],msg[5]) * (20.0/65536)
                x_rate = self.combine_reg_short(msg[6],msg[7]) * (1260.0/65536)
                y_rate = self.combine_reg_short(msg[8],msg[9]) * (1260.0/65536)
                z_rate = self.combine_reg_short(msg[10],msg[11]) * (1260.0/65536)
                x_temp = self.combine_reg_short(msg[18],msg[19]) * (200.0/65536)
                y_temp = self.combine_reg_short(msg[20],msg[21]) * (200.0/65536)
                z_temp = self.combine_reg_short(msg[22],msg[23]) * (200.0/65536)
                board_temp = self.combine_reg_short(msg[24],msg[25]) * (200.0/65536)
                timer = self.combine_reg_ushort(msg[26],msg[27]) * 15.259022
                BIT = self.combine_reg_ushort(msg[28],msg[29])
                '''Result'''
                #print board_temp
                if( not (lower_limit_accel < x_accel and x_accel < upper_limit_accel) and\
                    (lower_limit_accel < y_accel and y_accel < upper_limit_accel) and\
                    (lower_limit_accel < z_accel and z_accel < upper_limit_accel) and\
                    (lower_limit_accel < x_accel and x_accel < upper_limit_accel) and\
                    (lower_limit_accel < y_accel and y_accel < upper_limit_accel) and\
                    (lower_limit_accel < z_accel and z_accel < upper_limit_accel)    \
                   ) :
                   return False

        return True

    def continuous_packet_type_S1(self):
        '''Setup'''
        passed = True

        data = test_scripts.uut.imu383_command("SF", continuous_packet_type_f + S1)
        data = test_scripts.uut.imu383_command("SF", packet_rate_div_f + [0x00,0x01])

        # conver list of hex value to string
        pt = ''.join(hex(val)[2:] for val in S1)
        # use pt.decode("hex") to conver pt ro ASCII

        '''Execute'''
        for each in range(10):
            response = test_scripts.uut.read_response()
            if response and response[0] == pt.decode("hex"):
                len = int(response[1],16)
                msg = bytearray.fromhex(response[2])

                x_accel = self.combine_reg_short(msg[0],msg[1]) * (20.0/65536)
                y_accel = self.combine_reg_short(msg[2],msg[3]) * (20.0/65536)
                z_accel = self.combine_reg_short(msg[4],msg[5]) * (20.0/65536)
                x_rate = self.combine_reg_short(msg[6],msg[7]) * (1260.0/65536)
                y_rate = self.combine_reg_short(msg[8],msg[9]) * (1260.0/65536)
                z_rate = self.combine_reg_short(msg[10],msg[11]) * (1260.0/65536)
                x_temp = self.combine_reg_short(msg[12],msg[13]) * (200.0/65536)
                y_temp = self.combine_reg_short(msg[14],msg[15]) * (200.0/65536)
                z_temp = self.combine_reg_short(msg[16],msg[17]) * (200.0/65536)
                board_temp = self.combine_reg_short(msg[18],msg[19]) * (200.0/65536)
                timer = self.combine_reg_ushort(msg[20],msg[21]) * 15.259022
                BIT = self.combine_reg_ushort(msg[22],msg[23])
                '''Result'''
                #print board_temp
                if( not (lower_limit_accel < x_accel and x_accel < upper_limit_accel) and\
                    (lower_limit_accel < y_accel and y_accel < upper_limit_accel) and\
                    (lower_limit_accel < z_accel and z_accel < upper_limit_accel) and\
                    (lower_limit_accel < x_accel and x_accel < upper_limit_accel) and\
                    (lower_limit_accel < y_accel and y_accel < upper_limit_accel) and\
                    (lower_limit_accel < z_accel and z_accel < upper_limit_accel)    \
                   ) :
                   return False

        return True

    def orientation(self, config, void):
        '''Setup'''
        field = orientation_f
        field.extend(config)
        print field
        '''Execute'''

        '''Result'''
        return False
#################################################

class test_environment:

    def __init__(self, device):
        self.scripts = test_scripts(device)
        self.tests = []

    # Add test scetions & test scripts here
    def setup_tests(self):

        section1 = test_section("UART Transaction Verification")
        self.tests.append(section1)
        section1.add_test_case(code("Default Baudrate Test",   self.scripts.default_baudrate_test))
        section1.add_test_case(code("Comminication Test",      self.scripts.communication_test))
        section1.add_test_case(code("Header Test",             self.scripts.header_test))
        section1.add_test_case(code("Payload Length Test",     self.scripts.payload_length_test))
        section1.add_test_case(code("Payload Test",            self.scripts.payload_test))
        section1.add_test_case(code("CRC Test",                self.scripts.CRC_test))
        section1.add_test_case(code("Polled Mode Test",        self.scripts.polled_mode_test))
        section1.add_test_case(code("Continuous Mode Test",    self.scripts.continuouse_mode_test))
        section1.add_test_case(code("Verify Packet Types",     self.scripts.verify_packet_types))

        section2 = test_section("Read Field Default Checks")
        self.tests.append(section2)
        section2.add_test_case(condition_check("Packet Rate Divider Default",                 self.scripts.rf_default_test, packet_rate_div_f,              0x0000))
        section2.add_test_case(condition_check("Unit Baudrate Default",                       self.scripts.rf_default_test, unit_baud_f,                    0x0005))
        section2.add_test_case(condition_check("Continuous Packet Type Default",              self.scripts.rf_default_test, continuous_packet_type_f,       0x5330))
        section2.add_test_case(condition_check("Gyro Filter Setting Default",                 self.scripts.rf_default_test, gyro_filter_setting_f,          0x0000))
        section2.add_test_case(condition_check("Accelerometer Filter Setting Default",        self.scripts.rf_default_test, accel_filter_setting_f,         0x0000))
        section2.add_test_case(condition_check("Orientation Default",                         self.scripts.rf_default_test, orientation_f,                  0x006B))
        section2.add_test_case(condition_check("Sensor Enable Setting Default",               self.scripts.rf_default_test, sensor_enable_f,                0x0005))
        section2.add_test_case(condition_check("Output Select Setting Default",               self.scripts.rf_default_test, output_selecf_f,                0x0000))
        section2.add_test_case(condition_check("Fault Detection - Chip1 Default",             self.scripts.rf_default_test, fault_detct_chip1_f,            0xFFFF))
        section2.add_test_case(condition_check("Fault Detection - Chip2 Default",             self.scripts.rf_default_test, fault_detct_chip2_f,            0xFFFF))
        section2.add_test_case(condition_check("Fault Detection - Chip3 Default",             self.scripts.rf_default_test, fault_detct_chip3_f,            0xFFFF))
        section2.add_test_case(condition_check("Accel Consistency Check Enable Default",      self.scripts.rf_default_test, accel_consistency_en_f,         0x0001))
        section2.add_test_case(condition_check("Rate-Sensor Consistency Check Enable Default",self.scripts.rf_default_test, rate_sensor_consistency_en_f,   0x0001))

        section3 = test_section("Get Field Default Checks")
        self.tests.append(section3)
        section3.add_test_case(condition_check("Packet Rate Divider Default",                 self.scripts.gf_default_test, packet_rate_div_f,              0x0000))
        section3.add_test_case(condition_check("Unit Baudrate Default",                       self.scripts.gf_default_test, unit_baud_f,                    0x0005))
        section3.add_test_case(condition_check("Continuous Packet Type Default",              self.scripts.gf_default_test, continuous_packet_type_f,       0x5330))
        section3.add_test_case(condition_check("Gyro Filter Setting Default",                 self.scripts.gf_default_test, gyro_filter_setting_f,          0x0000))
        section3.add_test_case(condition_check("Accelerometer Filter Setting Default",        self.scripts.gf_default_test, accel_filter_setting_f,         0x0000))
        section3.add_test_case(condition_check("Orientation Default",                         self.scripts.gf_default_test, orientation_f,                  0x006B))
        section3.add_test_case(condition_check("Sensor Enable Setting Default",               self.scripts.gf_default_test, sensor_enable_f,                0x0005))
        section3.add_test_case(condition_check("Output Select Setting Default",               self.scripts.gf_default_test, output_selecf_f,                0x0000))
        section3.add_test_case(condition_check("Fault Detection - Chip1 Default",             self.scripts.gf_default_test, fault_detct_chip1_f,            0xFFFF))
        section3.add_test_case(condition_check("Fault Detection - Chip2 Default",             self.scripts.gf_default_test, fault_detct_chip2_f,            0xFFFF))
        section3.add_test_case(condition_check("Fault Detection - Chip3 Default",             self.scripts.gf_default_test, fault_detct_chip3_f,            0xFFFF))
        section3.add_test_case(condition_check("Accel Consistency Check Enable Default",      self.scripts.gf_default_test, accel_consistency_en_f,         0x0001))
        section3.add_test_case(condition_check("Rate-Sensor Consistency Check Enable Default",self.scripts.gf_default_test, rate_sensor_consistency_en_f,   0x0001))

        section4 = test_section("Packet Rate Divider Functional Test")
        self.tests.append(section4)
        section4.add_test_case(condition_check("Packet Rate Div 100Hz",  self.scripts.packet_rate_div, [0x00,0x01], 100))
        section4.add_test_case(condition_check("Packet Rate Div 50Hz",   self.scripts.packet_rate_div, [0x00,0x02], 50))
        section4.add_test_case(condition_check("Packet Rate Div 25Hz",   self.scripts.packet_rate_div, [0x00,0x04], 25))
        section4.add_test_case(condition_check("Packet Rate Div 20Hz",   self.scripts.packet_rate_div, [0x00,0x05], 20))
        section4.add_test_case(condition_check("Packet Rate Div 10Hz",   self.scripts.packet_rate_div, [0x00,0x0A], 10))
        section4.add_test_case(condition_check("Packet Rate Div 5Hz",    self.scripts.packet_rate_div, [0x00,0x14], 5))
        section4.add_test_case(condition_check("Packet Rate Div 4Hz",    self.scripts.packet_rate_div, [0x00,0x19], 4))
        section4.add_test_case(condition_check("Packet Rate Div 2Hz",    self.scripts.packet_rate_div, [0x00,0x32], 2))
        section4.add_test_case(condition_check("Packet Rate Div Quiet",  self.scripts.packet_rate_div, [0x00,0x00], 0))

        section5 = test_section("Continuous Packet Type Functional Test")
        self.tests.append(section5)
        section5.add_test_case(code("Continuous Packet Type S0 Functional Test",  self.scripts.continuous_packet_type_S0))
        section5.add_test_case(code("Continuous Packet Type S1 Functional Test",  self.scripts.continuous_packet_type_S1))

        section6 = test_section("Orientation Functional Test")
        self.tests.append(section6)
        section6.add_test_case(condition_check("Orientation Functional Test",  self.scripts.orientation, [0x00, 0x00]))

    def run_tests(self):
        for test in self.tests:
            test.run()

    def print_results(self):
        print "Test Results::"
        for test in self.tests:
            for item in test.test_cases:
                result_str = item.test_case_name + ": " + "\t\t\t\tPassed" if item.result else item.test_case_name + ": " + "\t\t\t\tFailed"
                print result_str
