import json 
import csv
from datetime import datetime

with open('datasets/our_meteo2023_3.json') as json_file: 
    weather_data = json.load(json_file)


data_to_write = []
for entry in weather_data['list']:
    dt_iso = datetime.utcfromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M:%S +0000 UTC')
    temp = entry['main']['temp']
    feels_like = entry['main']['feels_like']
    temp_min = entry['main']['temp_min']
    temp_max = entry['main']['temp_max']
    pressure = entry['main']['pressure']
    humidity = entry['main']['humidity']
    wind_speed = entry['wind']['speed']
    clouds_all = entry['clouds']['all']
    weather_description = entry['weather'][0]['description']
    
    row = [entry['dt'], dt_iso, 'local', temp, feels_like, temp_min, temp_max, pressure, '', '', humidity, wind_speed, '', clouds_all, weather_description]
    data_to_write.append(row)

# Writing data to a CSV file
csv_columns = ['dt', 'dt_iso', 'city_name', 'temp', 'feels_like', 'temp_min', 'temp_max', 'pressure', 'sea_level', 'grnd_level', 'humidity', 'wind_speed', 'rain_1h', 'clouds_all', 'weather_description']
csv_file = "datasets/weather_data.csv"

with open(csv_file, 'a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data_to_write)