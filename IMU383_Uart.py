import serial
import time
from CRC16_class import CRC16

ping        = [0x50,0x4B,0x00]
quiet_field = [0x00,0x01,0x00,0x00]
echo        = [0x43,0x48,0x01,0x41]

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


    # appends Header and Calculates CRC on data
    # data should have packet_type + payload_len + payload
    def _create_packet(self, data):
        header = [0x55, 0x55]
        packet = []

        packet = packet + header
        packet = packet + data

        crc = crc16.crcb(data)
        crc_hex = hex(crc)[2:]

        # CRC has to be 4 char long + odd length strings dont go through bytearray.fromhex()
        if(len(crc_hex) < 4):
            for i in range(4-len(crc_hex)):
                crc_hex = "0"+crc_hex

        crc_bytes = bytearray.fromhex(crc_hex)
        packet.extend(crc_bytes)

        data = packet
        #print data
        # At this point, data is ready to send to the UUT
        return data

    # returns Packet_type, Payload_length, payload
    def _unpacked_response(self):
        str_list = self.read_response()
        packet_type = ""
        payload_length = ""
        payload = ""

        # when serial read times out, str_list is empty
        if not str_list:
            return packet_type, payload_length, payload
        # serial read was succesful
        else:
            packet_type = str_list[0]
            payload_length = str_list[1]
            payload = str_list[2]
            return packet_type, payload_length, payload

    # Reads raw data from the UUT
    # Returns list of strings [Packet_type, Payload_length, payload]
    # Returns empty list in case of timeout
    def read_response(self, timeout = 10):
        retry = 0
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
            else:    # gets here if it received a byte that is not header(0x55)
                retry += 1
                t0 = time.time()
                if(retry > 100):
                    print "Error: Couldnt find header"
                    return str_list

    # appends Header and Calculates CRC on data
    # data should have packet_type + payload_len + payload
    def send_message(self, data):
        self.UUT.write(self._create_packet(data))

    # Message type = 2 byte packet types
    # Message = raw data, this methods formats it to IMU383 requirement, adds CRC and header, message length and number of fields.
    # Enables user to just send field ID and Data
    # this methods figures out number of fields and payload length
    # For the message types that dont need field address, send message directly
    def imu383_command(self, message_type, message):
        packet = []
        packet.extend(bytearray(message_type))

        if(message_type == "WF" or message_type == "SF"):
            msg_len = 1 + len(message)
            no_of_fields = len(message)/4
            packet.append(msg_len)
            packet.append(no_of_fields)
            final_packet = packet + message
            #print packet
        elif(message_type == "GF" or message_type == "RF"):
            msg_len = 1 + len(message)
            no_of_fields = len(message)/2
            packet.append(msg_len)
            packet.append(no_of_fields)
            final_packet = packet + message
        else:
            msg_len = len(message)
            packet.append(msg_len)
            final_packet = packet + message
            #print final_packet

        self.UUT.write(self._create_packet(final_packet))
        response = self.read_response()

        if response:
            if(response[0] == message_type):
                return response[2]          # just payload
            elif("GP" == message_type):
                return response             # packet_type + payload_len + payload
            else:
                return response
        else:
            print "Error: No response Received in imu383_commnd"
            return None

    # set packet rate = Quiet
    def silence_device(self):
        #print("Silent Mode ON")
        retry = 0
        self.send_message([0x53,0x46,0x05,0x01,0x00,0x01,0x00,0x00])
        response = self.read_response()
        print "SD:raw_resp", response

        while(True):
            response = self.read_response()
            if not response:
                break
            print "SD:waiting for SF ", response
        print "SD:Device in quiet mode", response
        '''
        while(response[0] != 'SF' and retry < 10):
            response = self.read_response()
            print "SD:waiting for SF ", response
            retry = retry+1
        #print response
        #response = self.imu383_command("SF",quiet_field)

        '''
    # returns true if ping was successful
    def ping_device(self):
        self.send_message(ping)
        pt,pll,pl = self._unpacked_response()
        if(pt == "PK"):
            return True
        else:
            return False

    def restart_device(self):
        self.send_message([0x53,0x52,0x00])
        response = self.read_response()
        while(response[0] != "SR"):
            response = self.read_response()
        time.sleep(2)# Allow unit to back up

        #print response
