#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import paramiko
from time import localtime, strftime
import time
import config

# to install paramiko:
# sudo pip install paramiko

# config
paramiko.util.log_to_file(config.ssh_log)
file_prefix = "pict_1_"
delete_older_than = 20  # days


def delete_pict():
    """delete old pictures"""
    now = time.time()
    old = now - delete_older_than * 24 * 60 * 60

    for f in os.listdir(config.pict_path_local_1):
        if f == ".gitignore":
            continue
        path = os.path.join(config.pict_path_local_1, f)
        if os.path.isfile(path):
            stat = os.stat(path)
            if stat.st_ctime < old:
                print "removing: ", path
                os.remove(path)


def upload_pict():
    """upload webcam pict"""
    if int(strftime("%M", localtime())) - 1 < 10:
        minute = '0' + str(int(strftime("%M", localtime())) - 1)
    else:
        minute = str(int(strftime("%M", localtime())) - 1)
    file_local = (config.pict_path_local_1
        + file_prefix + strftime("%Y-%m-%d_%H", localtime()) + minute) + ".jpg"
    print file_local
    file_remote = (config.pict_path_remote_1
        + file_prefix + strftime("%Y-%m-%d_%H", localtime()) + minute) + ".jpg"
    print file_remote
    try:
        print "uploading: ", file_local
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
    delete_pict()
    print "Let's go home"
