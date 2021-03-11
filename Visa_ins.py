import pyvisa as visa
import json
import getpass

current_user = getpass.getuser()
file = "/Users/" + current_user + "/Library/Atlas/Resources/test_config/serial_info.json"


def read_json_config(file):
    with open(file) as json_file:
        config = json.load(json_file)
    return config


stationInfo = read_json_config(file)
dev_list = stationInfo["Instrument_name"]

rm = visa.ResourceManager()
inter_list = rm.list_resources()
print(inter_list)
out_put = ""
for inter in inter_list:
    inst = rm.open_resource(inter)
    res = inst.query("*IDN?")
    for dev in dev_list:
        if dev in res:
            out_put = out_put + dev + ":" + inter + "|"

print(out_put)
