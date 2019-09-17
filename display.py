# -*- coding: utf-8 -*-

import time
import datetime
import json

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Load default font.
font = ImageFont.truetype('/var/www/html/VCR_OSD.ttf', 15)
font2 = ImageFont.truetype('/var/www/html/VCR_OSD.ttf', 19)
font3 = ImageFont.truetype('/var/www/html/VCR_OSD.ttf', 36)
font4 = ImageFont.truetype('/var/www/html/VCR_OSD.ttf', 26)

f=open("/var/www/html/current.txt","r")
cur = f.read()
f.close()

with open('/var/www/html/weather.txt', 'r') as myfile:
    data=myfile.read()
obj = json.loads(data)

with open('/var/www/html/air.txt', 'r') as myfile2:
    data2=myfile2.read()
air = json.loads(data2)

f = open("/var/www/html/arduino.txt","w+")
f.write(cur.split(' ')[1]+";"
    +cur.split(' ')[3].split('.')[0]+";"
    +"{:.1f}".format(obj['main']['temp'])+";"
    +str(obj['main']['humidity'])+";"
    +"{:03.0f}".format(air['current']['indexes'][0]['value'])+";"
    +datetime.datetime.now().strftime("%H:%M")+";"
    +datetime.datetime.now().strftime("%d/%m")+";"
    +datetime.datetime.now().strftime("%Y"))
f.close()

while datetime.datetime.now().second < 59:
    now = datetime.datetime.now()

    second = int(now.strftime("%S")[1])
    if second >= 5:
        second = second-5

    if (now.second >= 0 and now.second < 5) or (now.second >= 20 and now.second < 25) or (now.second >= 40 and now.second < 45):
        mode = 0
    if (now.second >= 5 and now.second < 10) or (now.second >= 25 and now.second < 30) or (now.second >= 45 and now.second < 50):
        mode = 1
    if (now.second >= 10 and now.second < 15) or (now.second >= 30 and now.second < 35) or (now.second >= 50 and now.second < 55):
        mode = 2
    if (now.second >= 15 and now.second < 20) or (now.second >= 35 and now.second < 40) or (now.second >= 55 and now.second < 59):
        mode = 3

    if mode == 0:
        image = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image)
        if now.second%2==0:
            draw.text((10, -6), now.strftime("%H:%M"),  font=font3, fill=255)
        else:
            draw.text((10, -6), now.strftime("%H %M"),  font=font3, fill=255)

    if mode == 1:
        image = Image.open('/var/www/html/home.ppm').convert('1')
        draw = ImageDraw.Draw(image)
        draw.text((35, -3), cur.split(' ')[1].split('.')[0],  font=font3, fill=255)
        draw.text((79, 10), cur.split(' ')[1].split('.')[1],  font=font2, fill=255)
        draw.text((98, 6), cur.split(' ')[3].split('.')[0],  font=font4, fill=255)
        draw.text((79, -3), 'o',  font=font, fill=255)
        draw.text((120, -3), '%',  font=font, fill=255)

    if mode == 2:
        image = Image.open('/var/www/html/city.ppm').convert('1')
        draw = ImageDraw.Draw(image)
        temp = "{:.1f}".format(obj['main']['temp'])
        draw.text((35, -3), temp.split('.')[0],  font=font3, fill=255)
        draw.text((79, 10), temp.split('.')[1],  font=font2, fill=255)
        draw.text((98, 6), str(obj['main']['humidity']),  font=font4, fill=255)
        draw.text((79, -3), 'o',  font=font, fill=255)
        draw.text((120, -3), '%',  font=font, fill=255)

    if mode == 3:
        image = Image.open('/var/www/html/air.ppm').convert('1')
        draw = ImageDraw.Draw(image)
        index = air['current']['indexes'][0]['value']

        draw.text((35, -3), "{:03.0f}".format(index),  font=font3, fill=255)

        if index > 10:
            draw.rectangle([(112, 27), (122, 22)], fill=255)
        if index > 25:
            draw.rectangle([(112, 20), (122, 15)], fill=255)
        if index > 50:
            draw.rectangle([(112, 13), (122, 8)], fill=255)
        if index > 75:
            draw.rectangle([(112, 6), (122, 1)], fill=255)

        draw.line([(127, 1), (127, 27)], fill=255)
        draw.line([(125, 0), (127, 0)], fill=255)
        draw.line([(125, 7), (127, 7)], fill=255)
        draw.line([(125, 14), (127, 14)], fill=255)
        draw.line([(125, 21), (127, 21)], fill=255)
        draw.line([(125, 28), (127, 28)], fill=255)

        draw.line([(107, 1), (107, 27)], fill=255)
        draw.line([(107, 0), (109, 0)], fill=255)
        draw.line([(107, 7), (109, 7)], fill=255)
        draw.line([(107, 14), (109, 14)], fill=255)
        draw.line([(107, 21), (109, 21)], fill=255)
        draw.line([(107, 28), (109, 28)], fill=255)

    draw.line([(0,31), ((127.0/5.0)*(float(second)+float(float(now.microsecond)/1000000)),31)], fill=255)
    disp.image(image)
    disp.display()
    time.sleep(0.05)
