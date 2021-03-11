import sys
import pyvisa as visa

inter_loc = sys.argv[1]
command = sys.argv[2]

rm = visa.ResourceManager()
inst = rm.open_resource(inter_loc)
res = inst.query(command)
print(res)
