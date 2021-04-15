#!/usr/bin/env python
# coding=utf-8
import os
import re
import csv
import json
import calendar
import time,datetime

Csv_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".csv"
screen_time = datetime.datetime.now().strftime('%Y%m%d')
csvFile = open("/Users/wts-sw/Desktop/Log/" + Csv_name, 'w')
sum_write = csv.writer(csvFile)
hr_dir = "/vault/Atlas/Archive"

js_file = "/vault/data_collection/test_station_config/gh_station_info.json"

def get_siteid(file):
    with open(file) as json_file:
        json_data = json.load(json_file)
    site_id = json_data["ghinfo"]["STATION_NUMBER"]
    return site_id

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def format_time(t):
	timeArray = time.strptime(t, "%b %d %Y %I:%M:%S.%f %p")
	otherStyle = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
	return otherStyle


row_list = []
result_list = []
Channel_list = []
header_lines = ["SerialNumber","STATION" ,"Test Start Time","Test Stop Time","total time", "Channel", "Result","Fail Item",
                "Open Test_PP1V8_HALL to GND", "Open Test_PP1V8_HALL to HALL_OUT",
				"Open Test_PP1V8_HALL to BUD_RIGHT_POS", "Open Test_PP1V8_HALL to BUTTON",
                "Open Test_PP1V8_HALL to BUD_LEFT_POS",
                "Open Test_HALL_OUT to GND", "Open Test_HALL_OUT to BUD_RIGHT_POS",
                "Open Test_HALL_OUT to BUTTON", "Open Test_HALL_OUT to BUD_LEFT_POS",
                "Open Test_BUD_RIGHT_POS to GND","Open Test_BUD_RIGHT_POS to BUTTON",
                "Open Test_BUD_RIGHT_POS to BUD_LEFT_POS",
                "Open Test_BUTTON to GND", "Open Test_BUTTON to BUD_LEFT_POS ", "Open Test_BUD_LEFT_POS  to GND",
                "Button Test_Default Status",
                "Button Test_Press", "Button Test_Release",
                "Hall Test_Default Status", "Hall Test_ON",
                "Hall Test_OFF"]

Upper_lines = ["Upper Limited----------->", "","", "", "", "", "", "", "","",
				"", "", "","", "", "", "", "",
                "","", "10100", "", "",
                "0.3", "1.9", "0.3",
                "1.9", "0.3", "1.9"]

down_lines = ["Lower Limited----------->", "", "","", "", "", "", "","5000", "5000",
				"5000", "5000", "5000","5000", "5000", "5000", "5000", "5000",
                "5000","5000", "9900", "5000", "5000",
                "0", "1.7", "0",
                "1.7", "0", "1.7"]

unit_lines = ["Measurement unit------>", "", "","", "", "", "", "","ohm", "ohm",
                "ohm", "ohm", "ohm","ohm", "ohm", "ohm", "ohm", "ohm",
                "ohm","ohm", "ohm", "ohm", "ohm","V", "V", "V", "V", "V", "V"]

sum_write.writerow(header_lines)
sum_write.writerow(Upper_lines)
sum_write.writerow(down_lines)
sum_write.writerow(unit_lines)
pattern = re.compile(screen_time)
site_id = get_siteid(js_file)
for filename in os.listdir(hr_dir):
    if len(filename) == 17:
        sec_dir = hr_dir + "/" + filename
        for filename_a in os.listdir(sec_dir):
            if pattern.search(filename_a) is not None:
                input_lines = []
                TT = 0.0
                trd_dir = hr_dir + "/" + filename + "/" + filename_a + "/" + "AtlasLogs"
                for filename_c in os.listdir(trd_dir):
                    if filename_c == 'Records.csv':
                        csv_file = open(trd_dir + "/" + filename_c)
                        reader = csv.reader(csv_file)
                        result = "Pass"
                        for row in reader:
                            row_list.append(row)
                            if is_number(row[15]):
                                TT = TT + float(row[15])
                            if row[2] == "Check SN":
                                SN = row[3]
                                input_lines.append(SN)
                            Channel_list.append(row[1])
                            result_list.append(row[4])
                            if is_number(row[6]):
                                input_lines.append((row[6]))
                        if "FAIL" in result_list:
                            input_lines.insert(1, "FAIL")
                            index_num = result_list.index("FAIL")
                            index_item = row_list[index_num][3]
                            input_lines.insert(2, index_item)
                        elif "ERROR" in result_list:
                            input_lines.insert(1, "ERROR")
                            index_num = result_list.index("ERROR")
                            index_item = row_list[index_num][1]
                            input_lines.insert(2, index_item)
                        else:
                            input_lines.insert(1, "PASS")
                            input_lines.insert(2, "")
                        del result_list[:]

                        if "unit:1" in Channel_list:
                            input_lines.insert(1, "unit:1")
                        elif "unit:2" in Channel_list:
                            input_lines.insert(1, "unit:2")
                        elif "unit:3" in Channel_list:
                            input_lines.insert(1, "unit:3")
                        else:
                            input_lines.insert(1, "unit:4")
                        del Channel_list[:]
                        Start_time = row_list[1][13]
                        End_time = row_list[len(row_list)-1][14]
                        input_lines.insert(1, TT)
                        input_lines.insert(1, format_time(End_time))
                        input_lines.insert(1, format_time(Start_time))
                        input_lines.insert(1, site_id)
                        del row_list[:]
                sum_write.writerow(input_lines)
                del input_lines[:]
csvFile.close()
