#!/usr/bin/env python
#
# capture an image from the pi camera and put it in the html directory
# from: https://picamera.readthedocs.io/en/release-1.12/recipes1.html#recipes1
#

from time import sleep, gmtime, strftime
from picamera import PiCamera

import datetime as dt
import picamera
import socket

#Get machine hostname
HostName=(socket.gethostname())
#set the web root where you want to write the image
WebRoot='/var/www/html/camera/'
#set the image name of the picture you want to save
ImageName='pi-cam-image.jpg'

#debug area
#print HostName
#print WebRoot + ImageName

camera = PiCamera()
# set camera to 1080p
camera.resolution = (1920, 1080)
camera.start_preview()
camera.annotate_background = picamera.Color('black')
camera.annotate_text = HostName + dt.datetime.now().strftime(' %m-%d-%Y %H:%M:%S') + strftime(' %Z',gmtime())
#
print ('Click......\n')
# Camera warm-up time
sleep(2)
#
# write image to sub-dir under the default web page called "camera" 
camera.capture(WebRoot + ImageName) 
#camera.capture(WebRoot + ImageName) '/var/www/html/camera/pi-cam-image.jpg')
print ('Clack\n')



