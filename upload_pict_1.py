#!/usr/bin/python
# -*- coding: utf-8 -*-

import paramiko
from time import localtime, strftime
import config

# to install paramiko:
# sudo pip install paramiko

# config
paramiko.util.log_to_file(config.ssh_log)
file_prefix = "pict_1_"


def upload_pict():
    """upload webcam pict"""
    minute = str(int(strftime("%M", localtime())) - 1)
    file_local = (config.pict_path_local_1
        + file_prefix + strftime("%Y-%m-%d_%H", localtime()) + minute) + ".jpg"
    print file_local
    file_remote = (config.pict_path_remote_1
        + file_prefix + strftime("%Y-%m-%d_%H", localtime()) + minute) + ".jpg"
    print file_remote
    try:
        # Open a transport
        transport = paramiko.Transport((config.ssh_host, config.ssh_port))
        # Auth
        transport.connect(username=config.ssh_user, password=config.ssh_pw)
        # Go!
        sftp = paramiko.SFTPClient.from_transport(transport)
        # Upload
        #sftp.put(config.pict_file_local_1, config.pict_file_remote_1)
        sftp.put(file_local, file_remote)
        # Close
        sftp.close()
        transport.close()
    except Exception as e:
        print e


if __name__ == '__main__':
    print "\nLet's go"
    print strftime("%Y-%m-%d %H:%M:%S", localtime())
    upload_pict()
    print "Let's go home"
