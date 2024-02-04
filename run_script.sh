#!/bin/bash
cd "$(dirname "$0" )"
/usr/bin/python3 WeatherForecasting.py

{ /usr/bin/python3 WeatherForecasting.py >> /home/mleahy/PythonProject/OpenWeather/log_files/weatherlog.log 2>&1; } 2>&1
