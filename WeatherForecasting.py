#! usr/bin/env python3
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime
from WeatherDB import app, db, update_weather_db
#import pandas as pd

load_dotenv("env-var.env")
WEATHER_APIKEY = os.environ.get("OpenWeather_APIKEY", 'Not Found')

def combine_parent_child_dict(old_dict):
    new_dict = {}
    for key,value in old_dict.items():
        if isinstance(value, dict):
            for item in value.keys():
                new_key = f"{key}_{item}"
                new_value = value[item]
                new_dict[new_key] = new_value
    return new_dict

#print(datetime.datetime.now())
def get_lat_lon(city_name='Toronto',country='Canada'):
    limit = 5
    URL = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={WEATHER_APIKEY}"
    response = requests.get(url=URL).json()
    return response[0]['lat'], response[0]['lon']

def get_weather_forecast(LAT, LON):
    EXCLUDE = "minutely"
    URL = f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={WEATHER_APIKEY}&units=metric"
    response = requests.get(url=URL).json()
    print(response['list'][0])
    
def get_current_weather(LAT, LON):
    URL = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={WEATHER_APIKEY}&units=metric"
    response = requests.get(url=URL).json()
    #print(response)
    return response

def transform_current_weather_data(**data):
    transformed = {}
    transformed['time'] = datetime.fromtimestamp(data['dt'])
    description = ''
    for weather in data['weather']:
        description += weather['description'] + ","
    transformed['description'] = description[:-1]
    
    keys_to_extract = ['temp', 'feels_like', 'temp_min', 'temp_max', 'pressure', 'humidity']
    weather_table_data = {}
    # extracting keys using a for loop and conditional statement
    for key, value in data['main'].items():
        if key in keys_to_extract:
            weather_table_data[key] = value
            
    transformed.update(weather_table_data)

    transformed.update(combine_parent_child_dict({'clouds': data['clouds']}))
    new_data = {'main': transformed}
    new_data['location'] = data['name']
    if 'wind' in data.keys():
        new_data['wind'] = data['wind']
    if 'rain' in data.keys():
        new_data['rain'] = data['rain']
        new_data['rain']['rain_1hr'] = new_data['rain'].pop('1h', None)
        new_data['rain']['rain_3hr'] = new_data['rain'].pop('3h', None)
    if 'snow' in data.keys():
        new_data['snow'] = data['snow']
        new_data['snow']['snow_1hr'] = new_data['snow'].pop('1h', None)
        new_data['snow']['snow_3hr'] = new_data['snow'].pop('3h', None)

    return new_data

def transform_weather_forecast_data():
    pass

def save_transformed_data(data):
    try:
        update_weather_db(data)
        print('Weather Database successfully updated')
    except Exception as e:
        print("Error has occured when updating database")
        print(e)


if __name__=='__main__':
    for city in ['Toronto', 'Ottawa']:
        lat, lon = get_lat_lon(city_name=city)
        current_weather = get_current_weather(lat,lon)
        print(current_weather)
        transformed_data = transform_current_weather_data(**current_weather)
        save_transformed_data(transformed_data)





