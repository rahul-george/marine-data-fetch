import csv
import time
import requests
from collections import namedtuple

data_out = []
data_invalid = []
Record = namedtuple("Record", "Port Country Lat Lng Id AreaSize ShortName Region")
InvalidRecords = namedtuple("InvalidRecords", "url")

with open('urls', 'r') as fh:
    while(url:=fh.readline()):
        data_raw = requests.get(url.strip())
        data_raw = data_raw.json()
        if len(data_raw['features']) > 1: 
            print('data_raw: ', data_raw)
            invalid_record = InvalidRecords(url)
            data_invalid.append(invalid_record._asdict())
        data = data_raw['features'][0]['properties']
        record = Record(data['port_name'],
                        data['country'],
                        data['latitude'],
                        data['longitude'],
                        data['port_id'],
                        data['areasize'],
                        data['short_name'],
                        data['sub_region'])
        
        print(record)
        data_out.append(record._asdict())

        time.sleep(1)


print(data_out)

with open('ports.csv', 'w', newline='') as csvfile:
    fieldnames = ["Port", "Country", "Lat", "Lng", "Id", "AreaSize", "ShortName", "Region"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(data_out)


with open('invalid_ports.csv', 'w', newline='') as csvfile:
    fieldnames = ["url"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(data_invalid)


        
