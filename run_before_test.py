#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import time
import sys
import os
import datetime
import re
from os.path import join, getsize

monitor_dir = "/vault/Atlas/Archive"
log_dir = "/Users/wts-sw/Desktop/Log/"
day_time = datetime.datetime.now().strftime('%Y-%m-%d')

def getdirsize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([getsize(join(root, name)) for name in files])
    return size


def del_oldlog(dir):
    list = os.listdir(dir)
    for i in range(0, len(list)):
        if bool(re.search(day_time, list[i])):
            os.remove(dir + list[i])


#检测log文件夹是否存在
if os.path.exists(log_dir):
    print('OK, the Log file exists.')
else:
    print("Sorry, I cannot find the Log file, Creat New One")
    os.makedirs(log_dir)


now_size = getdirsize(monitor_dir)
while True:
    new_size = getdirsize(monitor_dir)
    if now_size != new_size:
        now_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        del_oldlog(log_dir)
        os.system("/Users/wts-sw/Desktop/get_sum_csv.py.command")
        print(now_time + ", New log added")
    else:
        pass
    now_size = new_size
