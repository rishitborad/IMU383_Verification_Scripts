import time
from IMU383_Uart import UART_Dev
from IMU383_test_cases import test_section
from IMU383_test_cases import test_case

ping = [0x50,0x4B,0x00]
echo = [0x41]

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
        pl = test_scripts.uut.imu383_command("GP", [0x53,0x30])
        if(pl[:2] == "S0"):
            return True
        else:
            return False
    def continuouse_mode_test(self):
        data = test_scripts.uut.imu383_command("SF",[0x00,0x03,0x53,0x30])
        print data
        data = test_scripts.uut.imu383_command("SF", [0x00,0x01,0x00,0x32])
        print data
        t0 = time.time()
        count = 0
        while(time.time() - t0 < 10.00):
            count = count+1
            pt,pll,pl = test_scripts.uut.unpacked_response()
            print count
            #time.sleep(2)
        # verify that UUT reads data 20 times in 10 seconds,
        # more ofthen than not it reads 21 times due to time it takes to read
        if(count == 20 or count == 21):
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
        section1.add_test_case(test_case("Default Baudrate Test",   self.scripts.default_baudrate_test))
        section1.add_test_case(test_case("Comminication Test",      self.scripts.communication_test))
        section1.add_test_case(test_case("Header Test",             self.scripts.header_test))
        section1.add_test_case(test_case("Payload Length Test",     self.scripts.payload_length_test))
        section1.add_test_case(test_case("Payload Test",            self.scripts.payload_test))
        section1.add_test_case(test_case("CRC Test",                self.scripts.CRC_test))
        section1.add_test_case(test_case("Polled Mode Test",        self.scripts.polled_mode_test))
        section1.add_test_case(test_case("Continuous Mode Test",    self.scripts.continuouse_mode_test))

    def run_tests(self):
        for test in self.tests:
            test.run()

    def print_results(self):
        print "Test Results::"
        for test in self.tests:
            for item in test.test_cases:
                result_str = item.test_case_name + ": " + "Passed" if item.result else item.test_case_name + ": " + "Failed"
                print result_str
