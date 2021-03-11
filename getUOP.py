import requests
import json
import sys

SerialNumber = sys.argv[1]
file = "/vault/data_collection/test_station_config/gh_station_info.json"


def read_json_config(file):
    with open(file) as json_file:
        config = json.load(json_file)
    return config


stationInfo = read_json_config(file)
shopfloorURL = stationInfo["ghinfo"]["SFC_IP"]
Tsid = stationInfo["ghinfo"]["STATION_ID"]
URL = "http://" + shopfloorURL + " /BobcatService.svc/request?sn=" + SerialNumber + "&p=unit_process_check&c=QUERY_RECORD&tsid=" + Tsid
res = requests.get(url=URL)
print(res.text)
