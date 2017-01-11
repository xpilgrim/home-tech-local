#!/usr/bin/python
# -*- coding: utf-8 -*-
# Thanx to:
# https://github.com/GolemMediaGmbH/OfficeTemperature/blob/master/Raspberry_Pi/Raspberry.py

import re, urllib2
import requests
import RPi.GPIO as GPIO
import config

# config
url = config.logging_url

# Die Sensor-ID laut /sys/bus/w1/devices
sensorid = "28-000007520a0a"
sensorpfad = "/sys/bus/w1/devices/%s/w1_slave" % sensorid


def lies_temp(pfad):
    temp = None
    try:
        datei = open(pfad, "r")
        zeile = datei.readline()
        if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", zeile):
            zeile = datei.readline()
            m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", zeile)
            if m:
                #temp = float(m.group(2)) / 1000
                temp = m.group(2)
                datei.close()
                print temp
    except IOError:
        print "Konnte Sensor nicht lesen"
    return temp


def send_temp(temp):
    send_url = url % temp

    res = requests.get(send_url, auth=(config.logging_user, config.logging_pw))
    print res
    #try:
    #    result = urllib2.urlopen(send_url);
    #    print result
    #except urllib2.HTTPError as error:
    #    print error.code, error.reason

if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    temp = lies_temp(sensorpfad)

    if None != temp:
        send_temp(temp)
