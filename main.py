import csv
import time
import requests
from collections import namedtuple

DEBUG = 0

if DEBUG == 1:
    URLS = 'urls_debug'
else:
    URLS = 'urls'



data_out = []
data_invalid = []
Record = namedtuple("Record", "Port Country Lat Lng Id AreaSize ShortName Region")
InvalidRecords = namedtuple("InvalidRecords", "url message")

index = 1
with open(URLS, 'r') as fh:
    while(url:=fh.readline().strip()):
        url = url.replace(' ', '%20')
        print(index, url)
        data_raw = requests.get(url)
        index += 1

        data_raw = data_raw.json()
        if DEBUG: print(data_raw)
        if 'features' not in data_raw:
            invalid_record = InvalidRecords(url, 'Feature is not present, error received')
            data_invalid.append(invalid_record._asdict())
            continue
        if not data_raw['features']:
            invalid_record = InvalidRecords(url, 'Feature is None')
            data_invalid.append(invalid_record._asdict())
            continue

        if len(data_raw['features']) > 1: 
            invalid_record = InvalidRecords(url, 'multiple choices')
            data_invalid.append(invalid_record._asdict())
            continue

        data = data_raw['features'][0]['properties']
        record = Record(data['port_name'],
                        data['country'],
                        data['latitude'],
                        data['longitude'],
                        data['port_id'],
                        data['areasize'],
                        data['short_name'],
                        data['sub_region'])
        
        # print(record)
        data_out.append(record._asdict())

        #time.sleep(1)


with open('ports.csv', 'w', newline='') as csvfile:
    fieldnames = ["Port", "Country", "Lat", "Lng", "Id", "AreaSize", "ShortName", "Region"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(data_out)


with open('invalid_ports.csv', 'w', newline='') as csvfile:
    fieldnames = ["url", "message"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(data_invalid)


        
