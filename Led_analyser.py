import serial
import re
import binascii
import time


class LEDAnalyser(object):
    def __init__(self, port):
        self.__port = port
        self.__serialPort = serial.Serial(port=self.__port,
                                          baudrate=57600,
                                          parity='N',
                                          stopbits=1,
                                          bytesize=8,
                                          rtscts=0,
                                          timeout=5)

    def is_ready(self):
        print('check serial port')
        try:
            if self.__serialPort.is_open:
                print '{} open ok'.format(self.__port)
                return True
        except:
            print '{} open fail'.format(self.__port)
            return False

    def capture(self):
        print 'Store LED Color and Intensity Data, uses a wide intensity range.'
        command = 'capture'
        command_Hex = binascii.hexlify(command)+'0d'
        self.__serialPort.write(bytearray.fromhex(command_Hex))
        print 'check LED Analyser response("OK")'
        self.__serialPort.timeout = 3
        ret = binascii.b2a_hex(self.__serialPort.readline())
        print(ret+',' + ret.decode("hex"))
        if re.search('4f4b', ret):      # 4f4b: OK
            print ('Get the response from Analyser')
            return True
        else:
            print ("Didn't get the response from Analyser")
            return False

    def capture_range(self, range):
        """
        Range list
        1: Low
        2: Medium
        3: High
        4: Super
        5: Ultra
        """
        if ( 5 < range or range < 1 ):
            print("Incorrect capture range, must between 01 to 5!")
            return False
        print 'Store LED Color and Intensity Data, uses a pre-selected exposure time designated Range.'
        command = 'capture'+str(range)
        command_Hex = binascii.hexlify(command)+'0d'
        self.__serialPort.write(bytearray.fromhex(command_Hex))
        print 'check LED Analyser response("OK")'
        self.__serialPort.timeout = 3
        ret = binascii.b2a_hex(self.__serialPort.readline())
        print(ret + ',' + ret.decode("hex"))
        if re.search('4f4b', ret):      # 4f4b: OK
            print ('Get the response from Analyser')
            return True
        else:
            print ("Didn't get the response from Analyser")
            return False

    def get_RGBI(self, channel):
        print 'Return RGB and intensity data for fiber ##(01~20).'
        if ( 20 < channel or channel < 1 ):
            print("Incorrect channel number, must between 01 to 20!")
            return False
        command = 'getRGBI'+("%02d" % channel)
        command_hex = binascii.hexlify(command)+'0d'
        self.__serialPort.write(bytearray.fromhex(command_hex))
        self.__serialPort.timeout = 3
        ret = (binascii.b2a_hex(self.__serialPort.readline())).decode("hex")
        print(ret)
        return ret

    def get_HSI(self, channel):
        loopFlag = True
        retryCount = 3
        isfloatFlag = False
        while(loopFlag):
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
                retryCount=retryCount-1
                if(retryCount<0):
                    loopFlag = False
                    return False

            command = 'getHSI' + ("%02d" % channel)
            command_hex = binascii.hexlify(command) + '0d'
            self.__serialPort.write(bytearray.fromhex(command_hex))
            self.__serialPort.timeout = 3
            ret = (binascii.b2a_hex(self.__serialPort.readline())).decode("hex")
            print(ret)
            result = ret.split()
            if (len(result) > 2 and result[0] != "999.99" and result[0] != "xxx.xx"):

                try:
                    float(result[0])
                    isfloatFlag=True
                except ValueError:
                    print("[Error:] %s can't convert to float!" % num)
                    isfloatFlag=False
                if(isfloatFlag):
                    loopFlag = False
            else:
                loopFlag = True
                time.sleep(1)
                retryCount = retryCount - 1
                if (retryCount < 0):
                    loopFlag = False
        if(isfloatFlag == True and len(result) > 2):
            return float(result[0]), int(result[1]), int(result[2])
        else:
            return -1, -1, -1

    def get_xy(self, channel):
        print 'Return xy data for fiber ##(01~20).'
        if ( 20 < channel or channel < 1 ):
            print("Incorrect channel number, must between 01 to 20!")
            return False
        command = 'getxy'+("%02d" % channel)
        command_hex = binascii.hexlify(command)+'0d'
        self.__serialPort.write(bytearray.fromhex(command_hex))
        self.__serialPort.timeout = 3
        ret = (binascii.b2a_hex(self.__serialPort.readline())).decode("hex")
        print(ret)
        return ret

    def get_xoffset(self, channel):
        print 'Return xoffset data for fiber ##(01~20).'
        if ( 20 < channel or channel < 1 ):
            print("Incorrect channel number, must between 01 to 20!")
            return False
        command = 'getxoffset'+("%02d" % channel)
        command_hex = binascii.hexlify(command)+'0d'
        self.__serialPort.write(bytearray.fromhex(command_hex))
        self.__serialPort.timeout = 3
        ret = (binascii.b2a_hex(self.__serialPort.readline())).decode("hex")
        print(ret)
        return ret

    def get_yoffset(self, channel):
        print 'Return yoffset data for fiber ##(01~20).'
        if ( 20 < channel or channel < 1 ):
            print("Incorrect channel number, must between 01 to 20!")
            return False
        command = 'getyoffset'+("%02d" % channel)
        command_hex = binascii.hexlify(command)+'0d'
        self.__serialPort.write(bytearray.fromhex(command_hex))
        self.__serialPort.timeout = 3
        ret = (binascii.b2a_hex(self.__serialPort.readline())).decode("hex")
        print(ret)
        return ret

    def get_uv(self, channel):
        print 'Return uv data for fiber ##(01~20).'
        if ( 20 < channel or channel < 1 ):
            print("Incorrect channel number, must between 01 to 20!")
            return False
        command = 'getuv'+("%02d" % channel)
        command_hex = binascii.hexlify(command)+'0d'
        self.__serialPort.write(bytearray.fromhex(command_hex))
        self.__serialPort.timeout = 3
        ret = (binascii.b2a_hex(self.__serialPort.readline())).decode("hex")
        print(ret)
        return ret

    def get_intensity(self, channel):
        print 'Return intensity data for fiber ##(01~20).'
        if ( 20 < channel or channel < 1 ):
            print("Incorrect channel number, must between 01 to 20!")
            return False
        command = 'getintensity'+("%02d" % channel)
        command_hex = binascii.hexlify(command)+'0d'
        self.__serialPort.write(bytearray.fromhex(command_hex))
        self.__serialPort.timeout = 3
        ret = (binascii.b2a_hex(self.__serialPort.readline())).decode("hex")
        print(ret)
        return ret


if __name__ == "__main__":
    print ("Hello from Fesea LED Analyser module")

