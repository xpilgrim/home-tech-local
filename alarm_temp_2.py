#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from time import gmtime, strftime
import config
import lib_xmpp

CONFIG_MOOD = 1
LIST_MOOD = []
LIST_MOOD.append("Ofen Temp: ")
LIST_MOOD.append("Heb Deinen Arsch und leg Holz nach! ")
LIST_MOOD.append("Na, mein Lieber, willst Du mich nicht mal besuchen? ")

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

    # compare
    if temp < temp_last:
        if int(temp) < 70 and int(temp) > 65:
            send_xmpp(LIST_MOOD[CONFIG_MOOD] + temp)
            #if CONFIG_MOOD == 1:
            #    send_xmpp("Ofen Temp: " + temp)
            #if CONFIG_MOOD == 2:
            #    send_xmpp("Heb Deinen Arsch und leg Holz nach! " + temp)
            #if CONFIG_MOOD == 3:
            #    send_xmpp("Na, mein Lieber, willst Du mich nicht mal besuchen? " + temp)

def send_xmpp(xmpp_message):
    """ send_xmpp"""
    print "send_xmpp..."
    lib_xmpp.logging.basicConfig(level=lib_xmpp.logging.INFO)
    if sys.version_info.major < 3:
        xmpp_jid = config.xmpp_jid.decode("utf-8")
        xmpp_password = config.xmpp_password.decode("utf-8")
        xmpp_target_jid = config.xmpp_jid_target.decode("utf-8")
        xmpp_message = xmpp_message.decode("utf-8")
    else:
        xmpp_jid = config.xmpp_jid
        xmpp_password = config.xmpp_password
        xmpp_target_jid = config.xmpp_jid_target
        xmpp_message = xmpp_message

    handler = lib_xmpp.MyHandler(lib_xmpp.JID(xmpp_target_jid), xmpp_message)
    settings = lib_xmpp.XMPPSettings({
                            u"password": xmpp_password,
                            u"starttls": True,
                            u"tls_verify_peer": False,
                            })
    client = lib_xmpp.Client(lib_xmpp.JID(xmpp_jid), [handler], settings)
    client.connect()
    client.run()


if __name__ == '__main__':
    print "\nLet's go"
    print strftime("%Y-%m-%d %H:%M:%S", gmtime())
    lets_rock()
    #send_xmpp("test")
    print "Let's go home"
