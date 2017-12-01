#!/usr/bin/python
# -*- coding: utf-8 -*-
# Thanx to:
# https://github.com/GolemMediaGmbH/OfficeTemperature/blob/master/Raspberry_Pi/Raspberry.py

import re
import requests
import RPi.GPIO as GPIO
from time import gmtime, strftime
import datetime
import config

# config
conf_sensor_nr = 2
# Sensor-ID according /sys/bus/w1/devices
conf_sensor_pfad = config.sensor_temp_02_id
#conf_sensor_id = "28-000007520a0a"
#conf_sensor_pfad = "/sys/bus/w1/devices/%s/w1_slave" % conf_sensor_id
# amount of days for delte old logs
delete_days_back = 5
# use temp buffer
use_temp_buffer = True


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
                print "temp current raw:      " + temp
                temp_a = int(temp)

                # Measured value on measuring point
                # is lower as the real flow temperature
                # so we have to correct it
                correct_level = "0"

                if temp_a < 20000:
                    temp_b = temp_a
                if temp_a >= 20000 and temp_a < 50000:
                    temp_b = temp_a + 20000
                    correct_level = "1"
                if temp_a >= 50000 and temp_a < 60000:
                    temp_b = temp_a + 25000
                    correct_level = "3"
                if temp_a >= 60000 and temp_a < 70000:
                    temp_b = temp_a + 28000
                    correct_level = "4"
                if temp_a >= 70000:
                    temp_b = temp_a + 35000
                    correct_level = "5"
                print "correcting temp level: " + correct_level
                temp = str(temp_b)
                print "temp corrected raw:    " + temp

    except IOError:
        print "Error reading Sensor"
    return temp


def read_last_temp(conf_sensor_nr):
    """read last registered temp from database"""
    last_temp = None
    payload = {'action': 'load_temp', 'pa': conf_sensor_nr}
    try:
        res = requests.get(
            config.logged_url, params=payload,
            auth=(config.logging_user, config.logging_pw))
        print "return message from read_last_temp: %r" % res
        print "temp last real:         " + res.text.strip()
        #print res.text.strip()
        last_temp = res.text
    except requests.exceptions.RequestException as e:
        print e
    return last_temp


def delete_old_temps(conf_sensor_nr, delete_days_back):
    """delete old registered temps from database"""
    time_now = datetime.datetime.now()
    #print time_now.hour
    if time_now.hour != 7:
        print "No time for deleting..."
        return
    if time_now.minute != 40:
        print "No time for deleting..."
        return

    print "It's time for deleting"
    payload = {'action': 'delete_logs',
        'pa': conf_sensor_nr, 'pb': delete_days_back}
    #payload = {'action': 'delete_logs', 'pa': '1', 'pb': '0'}
    try:
        res = requests.get(
            config.logging_url, params=payload,
            auth=(config.logging_user, config.logging_pw))
        print "return message from delete old logs: %r" % res
        print res.text.strip()
    except requests.exceptions.RequestException as e:
        print e


def send_temp(conf_sensor_nr, temp):
    """register current temp in database"""
    payload = {'action': 'add_temp', 'pa': conf_sensor_nr, 'pb': temp}
    try:
        res = requests.get(
            config.logging_url, params=payload,
            auth=(config.logging_user, config.logging_pw))
        print "return message from sent_temp: %r" % res
    except requests.exceptions.RequestException as e:
        print e


def write_temp_buffer(conf_sensor_nr, temp):
    """write config file for buffering temp via fhem"""
    if use_temp_buffer is None:
        print "Nothing to do, using buffer disabled..."
        return

    real_temp = int(temp) / 1000
    print "real temp:          " + str(real_temp)

    if real_temp < 90:
        print "disable buffer"
    if real_temp >= 90:
        print "using buffer 1"
    if real_temp >= 100:
        print "using buffer 2"


if __name__ == '__main__':
    print "\nLet's go"
    print strftime("%Y-%m-%d %H:%M:%S", gmtime())
    delete_old_temps(conf_sensor_nr, delete_days_back)

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    temp = read_temp(conf_sensor_pfad)

    if None != temp:
        write_temp_buffer(conf_sensor_nr, temp)
        temp_last = read_last_temp(conf_sensor_nr)
        #print temp_old.strip()
        #print temp[:2]
        # send only if different value
        if temp_last.strip() != temp[:2]:
            send_temp(conf_sensor_nr, temp)
        else:
            print "Nothing to do, temp hasn't changed..."
    print "Let's go home"
