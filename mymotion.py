#! /usr/bin/python
#
# mymotion.py
# test PIR Motion Sensor from: https://diyhacking.com/raspberry-pi-gpio-control/
# D. Cappello Oct 2016
#
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
while True:
       i=GPIO.input(11)
       if i==0:                 #When output from motion sensor is LOW
             print "No Motion, No intruders! ",i
             time.sleep(0.1)
       elif i==1:               #When output from motion sensor is HIGH
             print "Motion Detected, Intruder Alert! ",i
             time.sleep(0.1)
