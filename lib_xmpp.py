#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A simple client example.

The script asks for a sender JID and password, target JID and a message.
Then, it connects to the sender's server and sends the message to the target
JID.
"""

import sys
import logging
from getpass import getpass

from pyxmpp2.jid import JID
from pyxmpp2.message import Message
from pyxmpp2.client import Client
from pyxmpp2.settings import XMPPSettings
from pyxmpp2.interfaces import EventHandler, event_handler, QUIT
from pyxmpp2.streamevents import AuthorizedEvent, DisconnectedEvent

class MyHandler(EventHandler):
    def __init__(self, target_jid, message):
        self.target_jid = target_jid
        self.message = message

    @event_handler(AuthorizedEvent)
    def handle_authorized(self, event):
        message = Message(to_jid = self.target_jid, body = self.message)
        event.stream.send(message)
        event.stream.disconnect()

    @event_handler(DisconnectedEvent)
    def handle_disconnected(self, event):
        return QUIT

    @event_handler()
    def handle_all(self, event):
        logging.info(u"-- {0}".format(event))

#logging.basicConfig(level = logging.INFO) # change to 'DEBUG' to see more
