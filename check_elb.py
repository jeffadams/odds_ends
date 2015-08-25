#!/usr/bin/python
# Simple Nagios check for unhealthy ELB hosts. 

import datetime
import sys
from boto.exception import BotoServerError
import boto

def get_config():
  import ConfigParser
  config = ConfigParser.ConfigParser()
  config.read(["/etc/nagios3/conf.d/.boto.cfg"])
  AWS_ACCESS_KEY  = config.get('Credentials','aws_access_key_id')
  AWS_SECRET_KEY  = config.get('Credentials','aws_secret_access_key')
  return[AWS_ACCESS_KEY, AWS_SECRET_KEY]

creds = get_config()


class MyInstances(dict):
        def __init__(self, name, value):
           self[name] = value


def get_elb_stats(name, metric, minutes=60, period=60):
    print '%s for %s for the last %dm (bucket: %ds):' % (metric, name, minutes, period)
    try:
        c = boto.connect_cloudwatch(aws_access_key_id=creds[0], aws_secret_access_key=creds[1])
        end = datetime.datetime.utcnow()
        start = end - datetime.timedelta(minutes=minutes)
        stats = c.get_metric_statistics(period, start, end, metric,
                                        'AWS/ELB', 'Sum',
                                        MyInstances('LoadBalancerName', name)
        )
        for stat in stats:
            print '\t%s: %f' % (stat[u'Timestamp'], stat[u'Sum'])

    except BotoServerError, error:
        print >> sys.stderr, 'Boto API error: ', error


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print >> sys.stderr, 'Usage: %s <ELB name>' % sys.argv[0]
        sys.exit(1)

stats = ['RequestCount', 'HTTPCode_Backend_2XX', 'HTTPCode_Backend_3XX', 'HTTPCode_ELB_4XX', 'HTTPCode_ELB_5XX','UnHealthyHostCount']
for stat in stats:
     get_elb_stats(sys.argv[1], stat, 5, 300)

