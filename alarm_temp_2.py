#!/usr/bin/python
# -*- coding: utf-8 -*-
# Thanx to:
# https://github.com/GolemMediaGmbH/OfficeTemperature/blob/master/Raspberry_Pi/Raspberry.py

from time import gmtime, strftime
import config

# config


def read_last_temp_from_file(filename):
    """read last registered temp from file"""
    try:
        with open(filename) as f:
            lines = f.readlines()
    except IOError as (errno, strerror):
        log_message = ("write_from_file: I/O error({0}): {1}"
                        .format(errno, strerror) + ": " + filename)
        print log_message

    lines = [x.strip() for x in lines]
    #print lines
    #pos = lines.index("<body>")
    #print pos
    return lines[9]


def lets_rock():
    """lets rock """
    # read and write last temp
    filename = "/home/pi/home-tech-local/public_html/temp_2_last.html"
    temp_last = read_last_temp_from_file(filename)
    print "temp last from file...." + temp_last
    filename = "/home/pi/home-tech-local/public_html/temp_2.html"
    temp = read_last_temp_from_file(filename)
    print "temp from file...." + temp


if __name__ == '__main__':
    print "\nLet's go"
    print strftime("%Y-%m-%d %H:%M:%S", gmtime())
    lets_rock()
    print "Let's go home"
