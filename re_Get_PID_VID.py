import re


def here(a):
    if len(re.findall('Product ID', a)) > 0 and len(re.findall('Vender ID', a)) > 0:
        PID = (re.findall('Product ID: ([a-zA-Z0-9]+.)', a))
        VID = (re.findall('Vender ID: ([a-zA-Z0-9]+.)', a))
        res = PID[0] + ":" + VID[0]
        return res

    else:
        return "no find PID and VID"