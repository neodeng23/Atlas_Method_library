import re
import sys

a = sys.argv[1]

"""
数据结构如下
b = "[00]: 0x23\n" \
    "[01]: 0x1A\n" \
    "[02]: 0x94\n" \
    "[03]: 0xC2\n" \
    "[04]: 0x40\n" \
    "[05]: 0x8E\n" \
    "[06]: 0xE6\n" \
    "[07]: 0x4C\n" \
    "[08]: 0x34\n" \
    "[09]: 0x00\n" \
    "[10]: 0x80\n" \
    "[11]: 0x2C\n" \
    "[12]: 0x75"
"""


if len(re.findall('\[09\]:', a)) > 0:
    res = (re.findall('\[09\]: ([a-zA-Z0-9]+.)', a))
    print(res[0])
else:
    print("no find BAT_TS value")
