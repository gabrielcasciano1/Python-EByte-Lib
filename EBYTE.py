import serial
import io
import time

class EBYTE_E22_MODE:
    NORMAL = 0
    WOR = 1
    CONFIGURATION = 2
    DEEP_SLEEP = 3



class EBYTE_E22:
    def __init__(self, COM_PORT:str, BAUD:int = 9600, MAX_SIZE:int = 256, M0_PIN:int = 0, M1_PIN:int = 1):
        # Need to do some error checking.
        self.__PORT = COM_PORT
        self.__BAUD = BAUD
        self.__MAX_SIZE = MAX_SIZE
        
        self.__m0 = M0_PIN
        self.__m1 = M1_PIN

        self.__OPEN = False
        self.__OUT_BUFFER = None
        self.__IN_BUFFER = None
        self.__MODE = EBYTE_E22_MODE.NORMAL
        self.__com_port = None

    def __change_mode(self, mode:EBYTE_E22_MODE):
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
                self.__com_port.write(io.StringIO(data))
            except Exception as se:
                print(f"Could not send data on port: {self.__PORT}.\nExceptiom {se}")
        else:
            print(f"Could not send data, port not open")

    def __recv_data(self, data:list):
        if self.__OPEN and self.__com_port:
            try:
                self.__IN_BUFFER = self.__com_port.readall()
                return self.__IN_BUFFER
            except Exception as se:
                print(f"Could not recv data on port: {self.__PORT}.\nExceptiom {se}")
        else:
            print(f"Could not recv data, port not open")    


        


