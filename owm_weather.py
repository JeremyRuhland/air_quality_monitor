#!/usr/bin/python3

# Open weather maps air quality/weather data collector

import requests
from datetime import datetime
from influxdb import InfluxDBClient

db_name = 'indoor_air_quality'

openweathermap_air_api_url = 'https://api.openweathermap.org/data/2.5/air_pollution?lat=xx.xx&lon=xxx.xx&appid=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
openweathermap_weather_api_url = 'https://api.openweathermap.org/data/2.5/weather?q=xxxx&units=metric&appid=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'


client = InfluxDBClient(host='localhost', port=8086)
insert_data = []

# Collect air quality data from web API
r = requests.get(openweathermap_air_api_url, timeout=5)

if r:
    owm_data = r.json()['list'][0]
    owm_time = datetime.utcfromtimestamp(owm_data['dt']).isoformat()
    scrubbed_owm_data = {k:float(v) for k, v in owm_data['components'].items()} # Convert all values to floats

    insert_data.append({'measurement': 'owm',
                    'time': owm_time,
                    'fields': scrubbed_owm_data})


# Collect basic weather conditions from web API
r = requests.get(openweathermap_weather_api_url, timeout=5)

if r:
    owm_data = r.json()
    owm_time = datetime.utcfromtimestamp(owm_data['dt']).isoformat()
    
    # Force fields to have proper type (20.0 degrees gets interpenetrated as int)
    owm_fields = {'temp': float(owm_data['main']['temp']),
                  'pressure': int(owm_data['main']['pressure']),
                  'RH': int(owm_data['main']['humidity'])}

    insert_data.append({'measurement': 'owm',
                    'time': owm_time,
                    'fields': owm_fields})

if insert_data:
    client.write_points(insert_data, database=db_name)

client.close()
