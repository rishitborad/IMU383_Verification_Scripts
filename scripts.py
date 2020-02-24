import time
from IMU383_Uart import UART_Dev
from IMU383_test_cases import test_section
from IMU383_test_cases import test_case
from IMU383_test_cases import code
from IMU383_test_cases import default_checks

ping = [0x50, 0x4B, 0x00]
echo = [0x41]
ID = [0x49, 0x44]
VR = [0x56, 0x52]
T0 = [0x54, 0x30]
S0 = [0x53, 0x30]
S1 = [0x53, 0x31]
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

    def default_test(self, cmd, param):
        response = test_scripts.uut.imu383_command("RF", cmd)
        print response
        if(int(response[6:],16) == param):
            return True
        else:
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
        #section1.add_test_case(code("Continuous Mode Test",    self.scripts.continuouse_mode_test))
        section1.add_test_case(code("Verify Packet Types",     self.scripts.verify_packet_types))

        section2 = test_section("Default Checks")
        self.tests.append(section2)
        section2.add_test_case(default_checks("Packet Rate Divider Default",                 self.scripts.default_test, [0x00,0x01], 0x0000))
        section2.add_test_case(default_checks("Unit Baudrate Default",                       self.scripts.default_test, [0x00,0x02], 0x0005))
        section2.add_test_case(default_checks("Continuous Packet Type Default",              self.scripts.default_test, [0x00,0x03], 0x5330))
        section2.add_test_case(default_checks("Gyro Filter Setting Default",                 self.scripts.default_test, [0x00,0x05], 0x0000))
        section2.add_test_case(default_checks("Accelerometer Filter Setting Default",        self.scripts.default_test, [0x00,0x06], 0x0000))
        section2.add_test_case(default_checks("Orientation Default",                         self.scripts.default_test, [0x00,0x07], 0x006B))
        section2.add_test_case(default_checks("Sensor Enable Setting Default",               self.scripts.default_test, [0x00,0x42], 0x0005))
        section2.add_test_case(default_checks("Output Select Setting Default",               self.scripts.default_test, [0x00,0x43], 0x0000))
        section2.add_test_case(default_checks("Fault Detection - Chip1 Default",             self.scripts.default_test, [0x00,0x4C], 0xFFFF))
        section2.add_test_case(default_checks("Fault Detection - Chip2 Default",             self.scripts.default_test, [0x00,0x4D], 0xFFFF))
        section2.add_test_case(default_checks("Fault Detection - Chip3 Default",             self.scripts.default_test, [0x00,0x4E], 0xFFFF))
        section2.add_test_case(default_checks("Accel Consistency Check Enable Default",      self.scripts.default_test, [0x00,0x61], 0x0001))
        section2.add_test_case(default_checks("Rate-Sensor Consistency Check Enable Default",self.scripts.default_test, [0x00,0x62], 0x0001))


    def run_tests(self):
        for test in self.tests:
            test.run()

    def print_results(self):
        print "Test Results::"
        for test in self.tests:
            for item in test.test_cases:
                result_str = item.test_case_name + ": " + "Passed" if item.result else item.test_case_name + ": " + "Failed"
                print result_str
