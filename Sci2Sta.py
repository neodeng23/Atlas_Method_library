import sys
import re

sci_num = sys.argv[1]

if "\n" in sci_num:
    sci_num = re.sub(r"\n", "", sci_num)

if "\r" in sci_num:
    sci_num = re.sub(r"\r", "", sci_num)

sci_num = eval(sci_num)

print("%.3f" % sci_num)