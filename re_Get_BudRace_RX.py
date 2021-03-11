import re
import sys

a = sys.argv[1]

if len(re.findall('RX:', a)) > 0:
    res = (re.findall('RX: (\d+)', a))
    print(res[0])
else:
    print("no find Voltage")
