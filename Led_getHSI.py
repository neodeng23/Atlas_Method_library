import serial
import re
import binascii
import time
import json
import getpass

current_user = getpass.getuser()
file = "/Users/" + current_user + "/Library/Atlas/Resources/test_config/serial_info.json"
with open(file) as json_file:
    config = json.load(json_file)


class LEDAnalyser(object):
    def __init__(self, port):
        self.__port = config["serial_test_Feasa"]["devicePath"]
        self.__serialPort = serial.Serial(port=self.__port,
                                          baudrate=config["serial_test_Feasa"]["baudrate"],
                                          parity=config["serial_test_Feasa"]["parity"],
                                          stopbits=config["serial_test_Feasa"]["stopbits"],
                                          databits=config["serial_test_Feasa"]["databits"],
                                          timeout=config["serial_test_Feasa"]["timeout"])

    def is_ready(self):
        try:
            if self.__serialPort.is_open:
                print '{} open ok'.format(self.__port)
                return True
        except:
            print '{} open fail'.format(self.__port)
            return False

    def capture(self):
        command = 'capture'
        command_Hex = binascii.hexlify(command) + '0d'
        self.__serialPort.write(bytearray.fromhex(command_Hex))
        print 'check LED Analyser response("OK")'
        self.__serialPort.timeout = 3
        ret = binascii.b2a_hex(self.__serialPort.readline())
        print(ret + ',' + ret.decode("hex"))
        if re.search('4f4b', ret):  # 4f4b: OK
            print ('Get the response from Analyser')
            return True
        else:
            print ("Didn't get the response from Analyser")
            return False

    def get_HSI(self, channel):
        loopFlag = True
        retryCount = 3
        isfloatFlag = False
        while (loopFlag):
            print 'Return HSI data for fiber ##(01~20).'
            if (20 < channel or channel < 1):
                print("Incorrect channel number, must between 01 to 20!")
                return False

            # capture data from fiber (All channels)
            print 'Store LED Color and Intensity Data, uses a wide intensity range.'
            command = 'capture'
            command_Hex = binascii.hexlify(command) + '0d'
            self.__serialPort.write(bytearray.fromhex(command_Hex))
            print 'check LED Analyser response("OK")'
            self.__serialPort.timeout = 3
            ret = binascii.b2a_hex(self.__serialPort.readline())
            print(ret + ',' + ret.decode("hex"))
            if re.search('4f4b', ret):  # 4f4b: OK
                print ('Get the response from Analyser')

                loopFlag = False
            else:
                print ("Didn't get the response from Analyser")

                time.sleep(1)
                retryCount = retryCount - 1
                if (retryCount < 0):
                    loopFlag = False
                    return False

            command = 'getHSI' + ("%02d" % channel)
            command_hex = binascii.hexlify(command) + '0d'
            self.__serialPort.write(bytearray.fromhex(command_hex))
            self.__serialPort.timeout = 3
            ret = (binascii.b2a_hex(self.__serialPort.readline())).decode("hex")
            print(ret)
            result = ret.split()

            if len(result) > 2 and result[0] != "999.99" and result[0] != "xxx.xx":

                try:
                    float(result[0])
                    isfloatFlag = True
                except ValueError:
                    print("[Error:] %s can't convert to float!" % result[0])
                    isfloatFlag = False
                if (isfloatFlag):
                    loopFlag = False
            else:
                loopFlag = True
                time.sleep(1)
                retryCount = retryCount - 1
                if (retryCount < 0):
                    loopFlag = False
        if isfloatFlag == True and len(result) > 2:
            #return float(result[0]), int(result[1]), int(result[2])
            print("p1_H:" + result[0] + "|" + "p1_S:" + result[1] + "|" + "p1_I:" + result[2])
        else:
            return -1, -1, -1


if __name__ == "__main__":
    LEDAnalyser.get_HSI()