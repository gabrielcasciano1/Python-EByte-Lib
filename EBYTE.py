import serial
import io
import time

class EBYTE_E22_DEFS:

    # Register addresses
    ADDR_H = 0x00
    ADDR_L = 0x01
    NET_ID = 0x02
    REG0 = 0x03
    REG1 = 0x04
    REG2 = 0x05
    REG3 = 0x06
    CRYPT_H = 0x07
    CRYPT_L = 0x08
    PID = 0x09

    # Register 0 Mapping
    REG0_BAUD_1200 = 0x00
    REG0_BAUD_2400 = 0x20
    REG0_BAUD_4800 = 0x40
    REG0_BAUD_9600 = 0x60 # default
    REG0_BAUD_19200 = 0x80
    REG0_BAUD_38400 = 0xA0
    REG0_BAUD_57600 = 0xC0
    REG0_BAUD_115200 = 0xE0

    REG0_PARITY_8N1 = 0x00 # default
    REG0_PARITY_8O1 = 0x08
    REG0_PARITY_8E1 = 0x10

    REG0_WAR_0K3 = 0x00
    REG0_WAR_1K2 = 0x01
    REG0_WAR_2K4 = 0x02 # default
    REG0_WAR_4K8 = 0x03
    REG0_WAR_9K6 = 0x04
    REG0_WAR_19K2 = 0x05
    REG0_WAR_38K4 = 0x06
    REG0_WAR_62K5 = 0x07

    REG0_DEFAULT = REG0_BAUD_9600 | REG0_PARITY_8N1 | REG0_WAR_2K4

    # Register 1 Mapping
    REG1_PACKET_LEN_240 = 0x00 # default
    REG1_PACKET_LEN_128 = 0x40
    REG1_PACKET_LEN_64 = 0x80
    REG1_PACKET_LEN_32 = 0xC0

    REG1_RSSI_EN = 0x20
    REG1_RSSI_DIS = 0x00 # default

    REG1_TX_PWR_30 = 0x00 # default
    REG1_TX_PWR_27 = 0x01
    REG1_TX_PWR_24 = 0x02
    REG1_TX_PWR_21 = 0x03

    REG1_DEFAULT = REG1_PACKET_LEN_240 | REG1_RSSI_DIS | REG1_TX_PWR_30

    # Register 2 Mapping
    # 0-83 represents the total number of channels, frequency is calculated as follows:
    #
    #   F = 410.125 + CH * 1e6
    # 
    # ******* Todo: Double check the formula ^^^^  could also be (410.123+CH)*1e6 ??? data sheet was vague ********

    # Register 3 Mapping
    REG3_RSSI_EN = 0x80
    REG3_RSSI_DIS = 0x00 # default

    REG3_FIX_POINT_TX = 0x40
    REG3_TRANSPARENT_TX = 0x00 # default

    REG3_REPEATER_EN =  0x20
    REG3_REPEATER_DIS =  0x00 # default

    REG3_LBT_EN = 0x10
    REG3_LBT_DIS = 0x00 # default

    REG3_WOR_TX = 0x08
    REG3_WOR_RX = 0x00 # default

    REG3_WOR_500 = 0x00
    REG3_WOR_1000 = 0x01
    REG3_WOR_1500 = 0x02
    REG3_WOR_2000 = 0x03 # default
    REG3_WOR_2500 = 0x04
    REG3_WOR_3000 = 0x05
    REG3_WOR_3500 = 0x06
    REG3_WOR_4000 = 0x07
    
    REG3_DEFAULT = REG3_RSSI_DIS | REG3_TRANSPARENT_TX | REG3_REPEATER_DIS | REG3_LBT_DIS | REG3_WOR_RX | REG3_WOR_2000


class EBYTE_E22_MODE:
    NORMAL = 0
    WOR = 1
    CONFIGURATION = 2
    DEEP_SLEEP = 3

class EBYTE_E22_CMD:
    SET_REG = 0xC0
    READ_REG = 0xC1
    SET_TEMP = 0xC2
    WRLSS_CFG = 0xCF 
    WRONG_FRMT = 0xFF

class EBYTE_E22:
    def __init__(self, COM_PORT:str, BAUD:int = 9600, MAX_SIZE:int = 256, M0_PIN:int = 0, M1_PIN:int = 1, CHANNEL:int = 0):
        # Need to do some error checking.
        self.__PORT = COM_PORT
        self.__BAUD = BAUD
        self.__MAX_SIZE = MAX_SIZE
        self.__CHANNEL = CHANNEL
        
        self.__m0 = M0_PIN
        self.__m1 = M1_PIN

        self.__OPEN = False
        self.__OUT_BUFFER = None
        self.__IN_BUFFER = None
        self.__MODE = EBYTE_E22_MODE.NORMAL
        self.__com_port = None

        self.set_config()


    def __change_mode(self, mode:int):
        if mode == EBYTE_E22_MODE.NORMAL:
            # set M0 = 0 and M1 = 0 
            pass
        elif mode == EBYTE_E22_MODE.WOR:
            # set M0 = 1 and M1 = 0
            pass
        elif mode == EBYTE_E22_MODE.CONFIGURATION:
            # set M0 = 0 and M1 = 1
            pass
        elif mode == EBYTE_E22_MODE.DEEP_SLEEP:
            # set M0 = 1 and M1 = 1
            pass
        else:
            # do something about incorrect values
            pass 

        time.sleep(0.01) # sleep for 10 ms to allow mode change to take place

    def __open_port(self): 
        try:
            self.__com_port = serial.Serial(port=self.__PORT, baudrate=self.__BAUD)
            self.__OPEN = True
            print(f"Successful connection on port: {self.__PORT} with baud: {self.__BAUD} and max data size {self.__MAX_SIZE}")
        except Exception as se:
            print(f"Failed to open connection on port: {self.__PORT} with baud: {self.__BAUD} and max data size {self.__MAX_SIZE}.\nException: {se}")

    def __close_port(self):
        try:
            if self.__OPEN or self.__com_port:
                self.__com_port.close()
                self.__OPEN = False
                print(f"Successful closure of port: {self.__PORT}")
        except Exception as se:
            print(f"Failed to close connection on port: {self.__PORT}.\nException: {se}")

    def __send_data(self, data:list):
        if self.__OPEN and self.__com_port:
            try:
                if self.__com_port.writable():
                    self.__com_port.write(io.BytesIO(data))
                raise Exception("com port {self.__PORT} is not writable")
            except Exception as se:
                print(f"Could not send data on port: {self.__PORT}.\nExceptiom {se}")
        else:
            print(f"Could not send data, port not open")

    def __recv_data(self):
        if self.__OPEN and self.__com_port:
            try:
                if self.__com_port.readable():
                    self.__IN_BUFFER = self.__com_port.readall()
                    return self.__IN_BUFFER
                else:
                    raise Exception("com port {self.__PORT} was not readable")
            except Exception as se:
                print(f"Could not recv data on port: {self.__PORT}.\nExceptiom {se}")
                return []
        else:
            print(f"Could not recv data, port not open")
            return [] 


    def __set_reg(self, start_addr: int, data:list):
        buff = [EBYTE_E22_CMD.SET_REG, hex(start_addr), hex(len(data))]
        for d in data:
            buff.append( d if type(d) is hex else hex(d))

        print(f"Tx on port: {self.__PORT},\n data: {' '.join(map(str, buff))}")
        self.__send_data(buff)
        print(f"Rx on port: {self.__PORT},\n data: {' '.join(map(str, self.__recv_data()))}")

    def __read_reg(self, start_addr: int, length: int):
        buff = [EBYTE_E22_CMD.READ_REG, hex(start_addr), hex(length)]
        
        print(f"Tx on port: {self.__PORT},\n data: {' '.join(map(str, buff))}")
        self.__send_data(buff)
        data = self.__recv_data()
        print(f"Rx on port: {self.__PORT},\n data: {' '.join(map(str, data))}")
        return data
    
    def __check_device(self):
        r = self.__read_reg(EBYTE_E22_DEFS.PID, 1)
        print("EByte E22 on Port {self.__PORT} has product ID: {r[-1]}")
        return len(r) > 0

    def get_net_id(self):
        pass

    def set_net_id(self, id:int):
        pass

    def get_addr(self):
        pass

    def set_addr(self, addr:int):
        pass
    
    def set_channel(self, channel:int):
        if 0 <= channel <= 83: 
            self.__CHANNEL = channel
            self.__change_mode(EBYTE_E22_MODE.CONFIGURATION) # put the E22 in config mode
            self.__set_reg(EBYTE_E22_DEFS.REG2, [hex(channel)])
            self.__change_mode(EBYTE_E22_MODE.NORMAL) # put the E22 back in normal mode

    def set_config(self, reg0:hex = EBYTE_E22_DEFS.REG0_DEFAULT, reg1:hex = EBYTE_E22_DEFS.REG1_DEFAULT, reg3:hex = EBYTE_E22_DEFS.REG3_DEFAULT):
        config = [reg0, reg1, self.__CHANNEL, reg3]

        self.__change_mode(EBYTE_E22_MODE.CONFIGURATION) # put the E22 in config mode
        self.__set_reg(EBYTE_E22_DEFS.REG0, config)
        self.__change_mode(EBYTE_E22_MODE.NORMAL) # put the E22 back in normal mode
