#!/bin/bash

# Should only be run on ec2 instances.
# Insert the AWS internal NTP server at the top of the server list in ntp.conf.

CONF='/etc/ntp.conf'
NTP_SERVER='169.254.169.123'

if [ ! -f ${CONF} ]; then
    echo "ntpd doesn't seem to be installed."
    exit 1
fi

if grep -q "server ${NTP_SERVER}" ${CONF}; then
   echo "Already configured to use AWS ntp servers"
   exit 0
fi

LINE_NUM=`awk '/0.centos.pool.ntp.org/ {print FNR}' ${CONF}`
sed -i "${LINE_NUM}i#First entry is the AWS Internal NTP Server\nserver 169.254.169.123       iburst" ${CONF}
