from IMU383_Uart import UART_Dev
from IMU383_test_cases import test_section
from IMU383_test_cases import test_case
from scripts import test_scripts
from scripts import test_environment
#import scripts

def ping_message_test():
    print " "

def unit_baudrate_test():
    print "printing from function"

def continuous_packet_type_test():
    print "printing from function"

if __name__ == "__main__":

    uut = UART_Dev("/dev/tty.usbserial-A7004TCD", 115200 )
    print("\r\n \t#######   IMU383 UART Interface Verification V1.0   #######\r\n")
    serial_number, model = uut.get_serial_number()
    version = uut.get_version()

    print "\r\n \t# UUT Model: ", model
    print "\r\n \t# UUT Serial Number: ", serial_number
    print "\r\n \t# UUT Version: ", version

    print "\r\n \t##########  Setting up tests...  ##########################\r\n"
    uut.silence_device()

    env = test_environment(uut)
    env.setup_tests()
    print "\r\n \t##########  Executing tests...   ##########################\r\n"
    env.run_tests()
    print "\r\n \t##########  Results   #####################################\r\n"
    env.print_results()
