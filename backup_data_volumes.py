#!/usr/bin/env python

from datetime import datetime
import logging
import logging.handlers
import os
import sys
import syslog
import time

from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import RegionInfo

import ConfigParser

'''
Make a snapshot of every volume with a tag of 'backup_name:somevalue' and cleanup older ones. 
The Name value must be unique among volumes in your account. 
Use only with data volumes -- root volumes are likely to fail.
Snapshots are kept for one day.
'''

my_logger = logging.getLogger(sys.argv[0])
my_logger.setLevel(logging.DEBUG)
if sys.platform == 'darwin':
    handler = logging.handlers.SysLogHandler(address = '/var/run/syslog')
else:
    handler = logging.handlers.SysLogHandler(address = '/dev/log')
my_logger.addHandler(handler)

def get_config():
    config = ConfigParser.ConfigParser()
    config.read(["/etc/nagios3/conf.d/.boto.cfg"])
    AWS_ACCESS_KEY  = config.get('Credentials','access_key')
    AWS_SECRET_KEY  = config.get('Credentials','secret_key')
    return[AWS_ACCESS_KEY, AWS_SECRET_KEY]

creds = get_config()
region = RegionInfo(name='us-east-1', endpoint='ec2.us-east-1.amazonaws.com')

try:
    conn = EC2Connection(aws_access_key_id=creds[0], aws_secret_access_key=creds[1], region=region)
except AttributeError:
    my_logger.critical("Couldn't connect. Check credentials.")
    sys.exit()

all_volumes = conn.get_all_volumes()
all_snaps   = conn.get_all_snapshots(owner='self')
retention_period = 86400 

def make_snapshot(backup_name, vol_id):
    readable_name = backup_name + "_backup"
    description   = ("%s backup %s" % (backup_name, datetime.now().strftime("%m-%d-%y")))
    start = time.time()
    snap   = conn.create_snapshot(vol_id, description, dry_run=False)
    status = snap.update()
    while status != '100%':
        time.sleep(2)
        status = snap.update()
    end = time.time()
    my_logger.info("%s %s created in %s seconds." % (readable_name, snap.id, (end - start)))
    conn.create_tags(snap.id, {'created': time.time() , 'backup_name': backup_name, 'Name': readable_name,})

def cleanup_snapshots(backup_name, lifetime):
    for s in all_snaps:
        tmp = {}
        tags = conn.get_all_tags({'resource-id': s.id })
        for t in tags:
            tmp[t.name] = t.value
                
        backup = None
        try:
            if tmp['backup_name'] == backup_name:
                backup = tmp['backup_name']
        except KeyError:
            next 

        if backup:
            if time.time() - float(tmp['created']) > lifetime:
                conn.delete_snapshot(s.id)
                my_logger.info("Deleted %s snapshot %s" % (backup, s.id))

def main():
    for v in all_volumes:
        d = {}
        tags = conn.get_all_tags({'resource-id': v.id })
        for t in tags:
            d[t.name] = t.value

        try:
            backup_name = d['backup_name']
        except KeyError:
            backup_name = None

        if backup_name:
            make_snapshot(backup_name, v.id)
            cleanup_snapshots(backup_name, retention_period)
 
if __name__ == '__main__':
    main()
