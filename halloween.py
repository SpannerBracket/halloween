#!/usr/bin/env python
from phue import Bridge
import time
import logging
import requests
import random
import socket
import struct
import binascii
import psutil
import sys
import os 
import datetime

logging.basicConfig()

def halloween():
	"Trick or Treat"
	# Play halloween on Squeezebox
	#sound = {'file':'Halloween.wav', 'length':25, 'message':'Trick or Treat'}
	sound = {'file':'Halloween.wav', 'length':25, 'message':'Trick or Treat'}
	
	r = requests.get("http://192.168.1.4:9000/status.html?p0=playlist&p1=play&p2=/raid/music/sounds/%s&player=00:04:20:06:49:c5" % (sound['file']))

	# Set message on Squeezebox
	r = requests.get("http://192.168.1.4:9000/status.html?p0=display&p1=Emergency&p2=%s&p3=%s&player=00:04:20:06:49:c5" % (sound['message'], sound['length']))

	# Connect to philips hue bridge
	b = Bridge("192.168.1.79")

	lights = b.lights

	#Get original state
	for light in lights:
		if light.name.startswith('Lamp Right'):
			lamp = light
			origlight = {'on':lamp.on, 'xy':lamp.xy, 'brightness':lamp.brightness}
			print lamp.xy
		if light.name.startswith('Lamp F Right'):
			lamp2 = light

	time.sleep(2.5)
	
	lamp.on = True
	lamp.transitiontime = 0
	lamp.brightness = 0
	print "Brightness 0"
	time.sleep(0.1)
	lamp.brightness = 254
	print "Brightness 254"
	time.sleep(0.2)
	lamp.brightness = 20
	print "Brightness 50"
	time.sleep(1)
	lamp.xy = [0.6587, 0.3348]
	lamp.on = False
	lamp.transitiontime = 100
	time.sleep(2)
	lamp.on = True
	#lamp.xy = [0.6587, 0.3348]
	print "Orange"
	lamp.brightness = 254
	time.sleep(5.1)
	
	lamp.transitiontime = 0
	lamp2.transitiontime = 0
	lamp2.on = True
	lamp.xy = [0.3411, 0.3523]
	lamp2.bightness = 254
	time.sleep(0.8)
	lamp2.on = False
	lamp.xy = [0.6587, 0.3348]
	time.sleep(9)
	

	print "Finished!"
	# Restore original light state
	lamp.transitiontime = 4
	lamp.on = True
	lamp.xy = [0.3411, 0.3523]
	lamp.brightness = 254
	
	return True

def createLockFile():
	"Create Lock File"
	fhandle = open('/var/www/octoalert/halloween.lock', 'w')
	fhandle.write('%s' % datetime.datetime.now())
	fhandle.close()
	return True

# Start main loop
fname = '/var/www/octoalert/halloween.lock'
if os.path.isfile(fname):
	fhandle = open(fname, 'r')
	lockTime = fhandle.read()
	fhandle.close()
	print datetime.datetime.strptime(lockTime, '%Y-%m-%d %H:%M:%S.%f')
	print datetime.datetime.now()-datetime.timedelta(seconds=25)
	if datetime.datetime.now()-datetime.timedelta(seconds=25) < datetime.datetime.strptime(lockTime, '%Y-%m-%d %H:%M:%S.%f'):
		print "Already running, exiting!"
		exit()
	else:
		createLockFile()
else:
	createLockFile()

halloween()
