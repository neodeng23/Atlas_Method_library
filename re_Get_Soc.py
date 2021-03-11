import re
import sys

a = sys.argv[1]

if len(re.findall('Smooth SoC', a)) > 0:
    res = (re.findall('Smooth SoC: (\d+)', a))
    print(res[0])
else:
    print("no find soc value")
