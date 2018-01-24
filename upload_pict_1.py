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
delete_older_than_local = 20  # days
delete_older_than_remote = 30  # days


def delete_pict():
    """delete old pictures"""
    now = time.time()
    old = now - delete_older_than_local * 24 * 60 * 60

    try:
        for f in os.listdir(config.pict_path_local_1):
            if f == ".gitignore":
                continue
            path = os.path.join(config.pict_path_local_1, f)
            if os.path.isfile(path):
                stat = os.stat(path)
                if stat.st_ctime < old:
                    print "removing: ", path
                    os.remove(path)
    except Exception as e:
        print e


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
        print "finish upload"
    except Exception as e:
        print e


def list_picts_remote():
    """list remote webcam picts"""
    picts_remote = None
    try:
        print "listing remote: ", config.pict_path_remote_1
        # Open a transport
        transport = paramiko.Transport((config.ssh_host, config.ssh_port))
        # Auth
        transport.connect(username=config.ssh_user, password=config.ssh_pw)
        # Go!
        sftp = paramiko.SFTPClient.from_transport(transport)
        # Get list
        picts_remote = sftp.listdir_attr(config.pict_path_remote_1)
        # Close
        sftp.close()
        transport.close()
        #print picts_remote
    except Exception as e:
        print e
    return picts_remote


def delete_picts_remote(picts_remote):
    """delete old pictures remote"""
    now = time.time()
    # 20 days more
    old = now - delete_older_than_remote * 24 * 60 * 60
    print old
    try:
        print "files remote:"
        print len(picts_remote)
    except Exception as e:
        print e

    try:
        print "deleting remote: ", config.pict_path_remote_1
        z = 0
        # Open a transport
        transport = paramiko.Transport((config.ssh_host, config.ssh_port))
        # Auth
        transport.connect(username=config.ssh_user, password=config.ssh_pw)
        # Go!
        sftp = paramiko.SFTPClient.from_transport(transport)
        for f in picts_remote:
            if f.st_mtime < old:
                z += 1
                print f.filename
                print f.st_mtime
                sftp.remove(config.pict_path_remote_1 + f.filename)
        print "files deleted:"
        print z
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
    picts_remote = list_picts_remote()
    delete_picts_remote(picts_remote)
    print "Let's go home"
