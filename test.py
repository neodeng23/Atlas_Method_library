import serial.tools.list_ports


reslt =  serial.tools.list_ports.comports()
print serial.tools.list_ports.ListPortInfo.name