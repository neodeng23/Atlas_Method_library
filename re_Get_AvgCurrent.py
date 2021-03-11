import re


def here(a):
    if len(re.findall('Avg Current', a)) > 0:
        res = (re.findall('Avg Current: (\d+)', a))
        return res[0]
    else:
        return "Avg Current"