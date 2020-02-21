from IMU383_Uart import UART_Dev
from IMU383_test_cases import test_section
from IMU383_test_cases import test_case

ping = [0x50,0x4B,0x00]

# Add test scripts here
class test_scripts:
    uut = None

    def __init__(self, device):
        test_scripts.uut = device

    def ping_test(self):
        test_scripts.uut.send_message(ping)
        pt,pll,pl = test_scripts.uut.unpacked_response()
        if(pt == "PK"):
            return True

    def header_test(self):
        return self.ping_test()

    def CRC_test(self):
        return self.ping_test()

    def NAK_test(self):
        nak = [0x00, 0x00, 0x01,0x00]

        test_scripts.uut.send_message(nak)
        pt,pll,pl = test_scripts.uut.unpacked_response()
        if(pt == 0x1515):
            return True
        else:
            print pt
            return False
#################################################

class test_environment:

    def __init__(self, device):
        self.scripts = test_scripts(device)
        self.tests = []

    # Add test scetions & test scripts here
    def setup_tests(self):

        section1 = test_section("Config Fields Verification")
        self.tests.append(section1)
        section1.add_test_case(test_case("Header Test", self.scripts.header_test))
        section1.add_test_case(test_case("CRC Test", self.scripts.CRC_test))
        section1.add_test_case(test_case("NAK Test", self.scripts.NAK_test))

    def run_tests(self):
        for test in self.tests:
            test.run()

    def print_results(self):
        print "Test Results::"
        for test in self.tests:
            for item in test.test_cases:
                result_str = item.test_case_name + ": " + "Passed" if item.result else item.test_case_name + ": " + "Failed"
                print result_str
