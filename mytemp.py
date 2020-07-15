#! /usr/bin/python
#
# mytemp.py
# Read and test the DHT22 sensor on the Pi remmeber you can read more than every 2 seconds form the sensor.
# D. Cappello Oct 2016
#
# NOTE don't forget to sudo pigpiod to get that going BEFORE you run this script 
import pigpio
import DHT22
import datetime as dt
from time import sleep, strftime, gmtime
#
# Initiate GPIO for pigpio
pi = pigpio.pi()
# Setup the Sensor
dht22 = DHT22.sensor(pi, 27) # use the actual GPIO pin name
# take a reading the first one doesn't count
dht22.trigger()

# We need to sleep for more than 2 seconds so we don't overwhelm the sensor
SleepTime=5

# define a function to get the readings
def ReadDHT22():
	# get a new reading
	dht22.trigger()
	# Save our values
	humidity = '%.2f' % (dht22.humidity())
	temp = '%.2f' % (dht22.temperature())
	ftemp = float(temp) * 1.8 + 32
	return (humidity,str(ftemp))

print 'Getting the readings......'
ReadDHT22()
sleep(SleepTime)
print '.....'
ReadDHT22()
sleep(SleepTime)
#
while True:
	humidity,temperature = ReadDHT22()
	print ("On " + dt.datetime.now().strftime(' %m-%d-%Y %H:%M:%S') + strftime(' %Z',gmtime()) + " Humidity is: " + humidity + "%")
	print ("Temperature is: " + temperature + "F")
	sleep(SleepTime)

#EOF

