import re
import sys

a = sys.argv[1]


if len(re.findall('Temperature', a)) > 0:
    res = (re.findall('Temperature: (\d+.\d)', a))
    print(res[0])
else:
    print("no find Temperature")
