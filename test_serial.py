# -*- coding: utf-8 -*-
import sys
import time
import serial
import getpass

timeout = "1500"
endsymbol = '0D0A'


def main():
    current_user = getpass.getuser()
    f = open("/Users/" + current_user + "/Desktop/test_res.txt", 'w+')
    for i in range(100):
        for unit in ["1", "2", "3", "4"]:
            device_Path, baud_Rate, Data_Bits = serial_config(unit)
            Default = communiate(device_Path, "VOL_BUTTON", baud_Rate, timeout, endsymbol)
            time.sleep(1)
            first_ok = communiate(device_Path, "SetButton", baud_Rate, timeout, endsymbol)
            time.sleep(1)
            button0 = communiate(device_Path, "VOL_BUTTON", baud_Rate, timeout, endsymbol)
            time.sleep(1)
            sec_ok = communiate(device_Path, "ResetButton", baud_Rate, timeout, endsymbol)
            time.sleep(1)
            button1 = communiate(device_Path, "VOL_BUTTON", baud_Rate, timeout, endsymbol)
            f.write(unit + "," + Default + "," + first_ok + "," + button0 + "," + sec_ok + "," + button1 + "\n")


def serial_config(unit):
    adr = "/dev/cu.usbserial-DMM"
    device_Path = adr + unit
    baud_Rate = "115200"
    Data_Bits = "8"
    return device_Path, baud_Rate, Data_Bits


def communiate(PortName, cmd, BaudRate, timeout, endsymbol):
    cmd += '\r\n'
    ser = serial.Serial(PortName, int(BaudRate), timeout=float(timeout))
    ser.flush()

    trans_cmd = cmd.encode()
    ser.write(trans_cmd)

    # timeout==0 表示只写不读
    if float(timeout) == 0:
        ser.flush()
        ser.close()
        return ''

    _end = endsymbol
    if _end == '0D0A':
        _end = '\r\n'

    reports = ''
    tickbegin = time.time()
    while True:
        tickend = time.time()
        if (tickend - tickbegin) >= float(timeout):
            ser.flush()
            ser.close()
            break

        time.sleep(0.001)
        reports += ser.read(ser.inWaiting()).decode()

        if not endsymbol == 'no endSymble':
            if endsymbol in reports:
                ser.flush()
                ser.close()
                return reports
                break

            if _end in reports:
                ser.flush()
                ser.close()
                return reports
                break


if __name__ == '__main__':
    main()