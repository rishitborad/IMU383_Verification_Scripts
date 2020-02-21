import serial
import time
from CRC16_class import CRC16

ping = [0x50,0x4B,0x00]
Quiet = [0x53,0x46,0x05,0x01,0x00,0x01,0x00,0x00]
quiet_field= [0x00,0x01,0x00,0x00]
#ping = [0x55,0x55,0x50,0x4B,0x00,0x9E,0xf4]
echo = [0x43,0x48,0x01,0x41]

crc16 = CRC16()

###########################################################
class UART_Dev:
    def __init__(self, port, baudrate):
        self.baudrate = baudrate
        self.port = port
        self.UUT = serial.Serial(port, baudrate, timeout = 2)
        self.header_bytes = 2
        self.packet_type_bytes = 2
        self.payload_len_bytes = 1
        self.crc_bytes = 2


    def create_packet(self, data):
        header = [0x55, 0x55]
        packet = []
        packet.extend(bytearray(header))
        packet.extend(data)

        crc = crc16.crcb(data)
        crc_hex = hex(crc)[2:]
        crc_bytes = bytearray.fromhex(crc_hex)
        packet.extend(crc_bytes)

        data = packet
        #print data
        return data

    def unpacked_response(self):
        str_list = self.read_response()
        packet_type = ""
        payload_length = ""
        payload = ""

        if not str_list:
            return packet_type, payload_length, payload
        else:
            packet_type = str_list[0]
            payload_length = str_list[1]
            payload = str_list[2]
            return packet_type, payload_length, payload

    def read_response(self, timeout = 10):
        t0 = time.time()
        str_list = []
        while True:
            hex = self.UUT.read(1).encode("hex")
            if(len(hex) == 0):
                if(time.time() - t0 > timeout):
                    print "timed out"
                    return str_list

            elif(hex == '55'):
                hex = self.UUT.read(1).encode("hex")
                if(hex == '55'):
                    #once header found, read other fields from the packet
                    str_list.append(self.UUT.read(self.packet_type_bytes))
                    #print "Packet Type = " + packet_type
                    payload_size = self.UUT.read(self.payload_len_bytes).encode("hex")
                    str_list.append(payload_size)
                    str_list.append(self.UUT.read(int(payload_size,16)).encode("hex"))
                    #print "Data = " + data_hex
                    str_list.append(self.UUT.read(self.crc_bytes).encode("hex"))
                    #print "CRC = " + crc_hex
                    return str_list
            else:
                print hex
                return str_list

    def send_message(self, data):
        self.UUT.write(self.create_packet(data))

    def set_field_command(self, message):
        packet = []
        message_type = "SF"
        msg_len = 1 + len(message)
        no_of_fields = len(message)/4
        packet.extend(bytearray(message_type))
        packet.append(msg_len)
        packet.append(no_of_fields)
        packet.extend(message)
        print packet

        # serial write
        self.UUT.write(self.create_packet(packet))
        # serial read
        pt, pll, pl = self.unpacked_response()
        if(pt == 'SF'):
            return True
        else:
            return False

    def silence_device(self):
        print("Silent Mode ON")
        self.set_field_command(quiet_field)
