#!/usr/bin/python
# -*- coding: utf-8 -*-
# Thanx to:
# https://github.com/GolemMediaGmbH/OfficeTemperature/blob/master/Raspberry_Pi/Raspberry.py

import re
import requests
import RPi.GPIO as GPIO
import config

# config
conf_sensor_nr = 2
# Die Sensor-ID laut /sys/bus/w1/devices
conf_sensor_id = "28-000007520a0a"
conf_sensor_pfad = "/sys/bus/w1/devices/%s/w1_slave" % conf_sensor_id


def read_temp(pfad):
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
                temp_a = int(temp)
                print "a"
                print temp_a

                # Measured value on measuring point
                # is lower as the real flow temperature
                # so we have to correct it
                if temp_a < 20000:
                    temp_b = temp_a
                    print 0
                if temp_a >= 20000 and temp_a < 50000:
                    temp_b = temp_a + 20000
                    print 1
                if temp_a >= 50000 and temp_a < 60000:
                    temp_b = temp_a + 25000
                    print 2
                if temp_a >= 60000 and temp_a < 70000:
                    temp_b = temp_a + 28000
                    print 3
                if temp_a >= 70000:
                    temp_b = temp_a + 35000
                    print 4
                temp = str(temp_b)
                print temp

    except IOError:
        print "Konnte Sensor nicht lesen"
    return temp


def read_last_temp(conf_sensor_nr):
    last_temp = None
    payload = {'action': 'load_temp', 'pa': conf_sensor_nr}
    try:
        res = requests.get(
            config.logged_url, params=payload,
            auth=(config.logging_user, config.logging_pw))
        print res.text
        last_temp = res.text
    except requests.exceptions.RequestException as e:
        print e
    return last_temp


def send_temp(conf_sensor_nr, temp):
    payload = {'action': 'add_temp', 'pa': conf_sensor_nr, 'pb': temp}
    try:
        res = requests.get(
            config.logging_url, params=payload,
            auth=(config.logging_user, config.logging_pw))
        print res
    except requests.exceptions.RequestException as e:
        print e


if __name__ == '__main__':
    print "Let's go"
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    temp = read_temp(conf_sensor_pfad)

    if None != temp:
        temp_old = read_last_temp(conf_sensor_nr)
        print temp_old.strip()
        print temp[:2]
        # send only if different value
        if temp_old.strip() != temp[:2]:
            send_temp(conf_sensor_nr, temp)
        else:
            print "Nothing to do, temp hasn't changed"
    print "Let's go home"
