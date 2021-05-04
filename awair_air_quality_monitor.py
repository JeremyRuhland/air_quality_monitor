#!/bin/python3

# Awair air quality monitor data collector
# Inserts most recent sensor values from awair device into influxdb database

import requests
from influxdb import InfluxDBClient

db_name = 'indoor_air_quality'

awair_api_url = 'http://awair-elem-xxxxxx.local/air-data/latest'

client = InfluxDBClient(host='localhost', port=8086)


# Collect data from awair sensor on LAN
r = requests.get(awair_api_url, timeout=5)

if r:
    awair_data = r.json()
    awair_data.pop('timestamp', None) # Remove timestamp from dataset
    awair_data_timestamp = r.json()['timestamp']

    # These keys must be floats, convert them if they happen to be round numbers and get confused for integers
    awair_data['abs_humid'] = float(awair_data['abs_humid'])
    awair_data['dew_point'] = float(awair_data['dew_point'])
    awair_data['humid'] = float(awair_data['humid'])
    awair_data['temp'] = float(awair_data['temp'])

    insert_data = [{'measurement': 'awair',
                        'time': awair_data_timestamp,
                        'fields': awair_data}]

    client.write_points(insert_data, database=db_name)
    
client.close()
