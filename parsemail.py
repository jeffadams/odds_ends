#!/usr/bin/python
# Crudely read an email line by line from stdin and send an 
# acknowledgement command to Nagios if appropriate.
# Use with procmail. 
import os
import re
import sys
import time

ack = None
cmd_fifo = "/var/lib/nagios3/rw/nagios.cmd"

for line in sys.stdin:
    if line.startswith('Subject'):
        subject = line.strip()
    elif re.match('ack', line, re.IGNORECASE):
        ack = 'True'
    elif line.startswith('From:'):
        from_addr = line.strip()

if ack is None:
    exit()

mylist = subject.split(" ")
now = int(time.time())

if 'Host' in mylist: # Host down alerts.
    cmd = ("[%s] ACKNOWLEDGE_HOST_PROBLEM;%s;1;1;1;email;%s;ack'd by email" % (now, mylist[2], from_addr))
else:	             # Service Alerts.
    cmd = ("[%s] ACKNOWLEDGE_SVC_PROBLEM;%s;%s;1;1;1;%s;ack'd by email" % (now, mylist[2], mylist[3], from_addr))

f = open(cmd_fifo, "w")
f.write(cmd)
f.close()
