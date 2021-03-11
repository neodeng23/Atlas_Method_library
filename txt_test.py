# -*- coding: utf-8 -*-
import getpass

current_user = getpass.getuser()
f = open("/Users/" + current_user + "/Desktop/test_res.txt", 'w+')

adr = "/dev/cu.usbserial-DMM"

Default = "1"
first_ok = "ok"
button0 = "ok"
sec_ok = "ok"
button1 = "ok"
# 文件内写入“文本内容”四个字
for i in range(10):
    for unit in ["1", "2", "3", "4"]:
        device_Path = adr + unit
        f.write(device_Path + "," + Default + "," + first_ok + "," + button0 + "," + sec_ok + "," + button1 + "\n")
# 关闭文件
f.close()
