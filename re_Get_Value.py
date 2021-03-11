import re
import sys

a = sys.argv[1]
check_value = sys.argv[2]


if "\n" in a:
    a = re.sub(r"\n", "", a)

if "\r" in a:
    a = re.sub(r"\r", "", a)

if "|" in check_value:
    vlist = check_value.split('|')
    re_a = vlist[0]
    re_b = vlist[1]
    reslist = re.findall(re_a + '.*' + re_b, a)
    res = reslist[0]
    res = re.sub(re_a, '', res)
    res = re.sub(re_b, '', res)
    print(res)
else:
    if len(re.findall(check_value, a)) > 0:
        res = (re.findall(check_value + '(\d+)', a))
        print(res[0])
    else:
        print("no find " + check_value)
