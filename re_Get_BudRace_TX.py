import re
import sys

a = sys.argv[1]

if len(re.findall('TX:', a)) > 0:
    res = (re.findall('TX: (\d+)', a))
    print(res[0])
else:
    print("no find Voltage")
