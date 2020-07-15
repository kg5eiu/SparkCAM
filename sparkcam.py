# -*- coding: utf-8 -*-
#!/usr/bin/ python
#
# sparkcam.py
# post a file/image to cisco Spark Room when motion is detected
# Capture a file from the camera put it in the WebRoot area for easy viewing 
# post to a Spark Room.
# Oct 3, 2016
# D. Cappello 
#
# NOTE 
# don't forget to sudo pigpiod to get that going BEFORE you run this script 
#


import time
from requests_toolbelt import MultipartEncoder
from time import sleep, gmtime, strftime
from picamera import PiCamera
import datetime as dt
import picamera
import socket
import requests
import json
import pigpio
import DHT22

import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
# We are using pin 11 for the sensor
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor

# External Temp and Humidity Sensor init
# Initiate GPIO for pigpio
MyPi = pigpio.pi()
# Setup the Sensor
dht22 = DHT22.sensor(MyPi, 27) # use the actual GPIO pin name
# take a reading the first one doesn't count
dht22.trigger()
PICPUtemp = str(round((9.0/5.0) * (int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3) + 32, 2)) # Get Pi CPU temp

# define a function to get the readings from the temp and humidity sensor
# return them in F (sensor defaults to C)
def ReadDHT22():
	# get a new reading
	dht22.trigger()
	# Save our values
	humidity = '%.2f' % (dht22.humidity())
	temp = '%.2f' % (dht22.temperature())
	ftemp = float(temp) * 1.8 + 32
	return (str(humidity),str(ftemp))

#
# capture an image from the pi camera and put it in the html directory
# from: https://picamera.readthedocs.io/en/release-1.12/recipes1.html#recipes1
#

# setup some variables for use later
#
# Get local machine hostname
HostName=(socket.gethostname())

# set the web root of this server to where you want to write the image
# note the permissions on the file
WebRoot='/var/www/html/camera/'

# set the file name of the image/picture you want to save
ImageName='picam-image.jpg'

# point to the file/image I want to post to Spark, Spark needs the full path name including / (root)
# Spark needs the file type as well
# Note - the file permissions on that directory and filename need to be 666 since this process is writing the image to location
PostFile = WebRoot + ImageName
FileType = 'image/jpg'

#
# Spark URL to post messages  get this URL from the Dev site
SparkUrl = "https://api.ciscospark.com/v1/messages"

# We need to sleep for more than 2 seconds so we don't overwhelm the sensor
SleepTime=5

# Init the Pi Camera
camera = PiCamera()

# set camera to 1080p
camera.resolution = (1920, 1080)
# uncomment to show the camera on the screen if you want
# camera.start_preview()
# set up the color background of the text overlay
camera.annotate_background = picamera.Color('black')
# setup the image so you it looks like a photo
#camera.hflip = True
camera.vflip = True
#

# Cisco Spark Token - need to get Cisco Dev Spark token in order to post stuff into a room etc.
# from: https://developer.ciscospark.com
# storing the Authentication token in a file in the OS (spark-tok.txt) vs. leaving in script
fat=open ("./spark-tok.txt","r+")
accesstoken=fat.readline().rstrip()
fat.close
print 'Got The Spark Token: ' + accesstoken

# Set the room id in Spark from the room name that you want to post the image to.
# This is my Room ID
roomId='Y2lzY29zcGFyazovL3VzL1JPT00vNWMzMzZmZjAtYTI5ZS0zZWQ5LWJkNzItNjczM2NjMDFhNDIx'

#
# Start the main loop to sense motion from the Pi PIR
while True:
	# Take a short rest  1/2 a second
	sleep(.5)
	# init the GPIO motion sensor on the pin()
	i=GPIO.input(11)
	if i==0:   #When output from motion sensor is low - don't post to spark room
	  print "No Motion Deteced " + dt.datetime.now().strftime(' %m-%d-%Y %H:%M:%S') + strftime(' %Z',gmtime())
	  sleep(2)
	elif i==1:	#When output from motion sensor is high - post to the spark room 
	  # Take a picutre from the camera write to the web server and post the file/image to the Spark Room
	  print ('Detecting Motion And Posting Image To Spark ' + dt.datetime.now().strftime(' %m-%d-%Y %H:%M:%S') + strftime(' %Z',gmtime()))
	  #
	  # Read the sensor for temp and humidity
	  Humidity,Temperature = ReadDHT22()
	  # get internal Pi CPU Temp
	  PICPUtemp = str(round((9.0/5.0) * (int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3) + 32, 2)) # Get Pi CPU temp

	  # Set the overlay text with the HostName current date time and timezone
	  camera.annotate_text = HostName + dt.datetime.now().strftime(' %m-%d-%Y %H:%M:%S') + strftime(' %Z  ',gmtime()) + 'Air Temp:' + Temperature + 'F ' + 'Humidity:' + Humidity + '%' + ' CPU Temp:' + PICPUtemp + 'F'
	  print (camera.annotate_text)
	  #
	  # Capture an image from the Pi camera and write image to sub-dir under the default web page on the Pi
	  camera.capture(PostFile)
          #
	  my_fields={'roomId': roomId, 'text': ' Motion Detected....', 'files': (ImageName, open(PostFile, 'rb'), FileType) }
	  m=MultipartEncoder(fields=my_fields)
	  SparkResp=requests.post(SparkUrl, data=m, headers={'Content-Type': m.content_type,'Authorization': 'Bearer ' + accesstoken})
	  SparkResp.json()
          sleep(SleepTime)
#EOF
