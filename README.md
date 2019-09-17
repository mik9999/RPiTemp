# RPiTemp
RPiTemp is a simple script that uses data from Airly API, DHT22 thermometer and OpenWeather to display temperature (inside and outside) on a connected OLED panel.
Data from Airly and OpenWeather are downloaded using a curl command (in crontab) and saved as txt files that are afterwards processed by the display.py script.

It diplays (in order):
1. Current time
2. Inside temperature/humidity (DHT22)
3. Outside temperature/humidity (OpenWeather)
4. Air quality (Airly)

# Preview
![RPiTemp preview](https://raw.githubusercontent.com/mik9999/RPiTemp/master/image.jpg)
