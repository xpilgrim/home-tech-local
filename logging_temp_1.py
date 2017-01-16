#!/usr/bin/python
# -*- coding: utf-8 -*-
# Thanx to:
# https://github.com/GolemMediaGmbH/OfficeTemperature/blob/master/Raspberry_Pi/Raspberry.py

import re
import requests
import RPi.GPIO as GPIO
from time import gmtime, strftime
import config

# config
conf_sensor_nr = 1
# Sensor-ID according /sys/bus/w1/devices
conf_sensor_id = "28-00000750f60a"
conf_sensor_pfad = "/sys/bus/w1/devices/%s/w1_slave" % conf_sensor_id


def read_temp(pfad):
    """read temp from sensor"""
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
                print "current temp:"
                print temp

    except IOError:
        print "Error reading Sensor"
    return temp


def send_temp(conf_sensor_nr, temp):
    """register current temp in database"""
    payload = {'action': 'add_temp', 'pa': conf_sensor_nr, 'pb': temp}
    try:
        res = requests.get(
            config.logging_url, params=payload,
            auth=(config.logging_user, config.logging_pw))
        print "return message from sent_temp:"
        print res
    except requests.exceptions.RequestException as e:
        print e


if __name__ == '__main__':
    print "Let's go"
    print strftime("%Y-%m-%d %H:%M:%S", gmtime())
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    temp = read_temp(conf_sensor_pfad)

    if None != temp:
        send_temp(conf_sensor_nr, temp)
    print "Let's go home"
