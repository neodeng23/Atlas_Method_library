import re
import sys

a = sys.argv[1]

if len(re.findall('Raw SoC', a)) > 0:
    res = (re.findall('Raw SoC: (\d+)', a))
    print(res[0])
else:
    print("no find soc value")
