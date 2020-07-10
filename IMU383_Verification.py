from IMU383_Uart import UART_Dev
from Test_Case import Test_Section
from Test_Case import Test_Case
from IMU383_Tests import Test_Scripts
from IMU383_Tests import Test_Environment
#import scripts

def ping_message_test():
    print " "

def unit_baudrate_test():
    print "printing from function"

def continuous_packet_type_test():
    print "printing from function"

if __name__ == "__main__":

    uut = UART_Dev("/dev/tty.usbserial-144400", 115200 )
    print("\r\n \t#######   IMU383 UART Interface Verification V1.0   #######\r\n")
    serial_number, model = uut.get_serial_number()
    version = uut.get_version()

    print "\r\n \t# UUT Model: ", model
    print "\r\n \t# UUT Serial Number: ", serial_number
    print "\r\n \t# UUT Version: ", version

    print "\r\n \t##########  Setting up tests...  ##########################\r\n"
    uut.silence_device()

    env = Test_Environment(uut)
    env.setup_tests()
    print "\r\n \t##########  Executing tests...   ##########################\r\n"
    env.run_tests()
    print "\r\n \t##########  Results   #####################################\r\n"
    env.print_results()
