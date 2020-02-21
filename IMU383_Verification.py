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

    print("\r\n \tIMU383 UART Interface Verification V1.0\r\n")

    uut = UART_Dev("/dev/tty.usbserial-A7004TCD", 115200 )
    uut.silence_device()

    env = test_environment(uut)
    env.setup_tests()
    env.run_tests()
    env.print_results()

    #ser.write(serial.to_bytes(ping))
    #print serial.to_bytes(ping)
    #Quiet_packet = uut.create_packet(Quiet)
    #uut.set_field_command(quiet_field)
