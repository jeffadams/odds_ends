#!/usr/bin/env python
# Send Squid stats via Collectd's exec plugin.
import os
import pickle
import re
import signal
import socket
import subprocess
import sys
import time

class SquidStats(object):
    def __init__(self):
        self.LAST_RUN  = '/var/tmp/collectd_squid.pickle'
        self.HOSTNAME = socket.gethostname()
        self.metric_list = [
            'Number of clients accessing cache',
            'Number of HTTP requests received',
            'Number of ICP messages received',
            'Number of ICP messages sent',
        ]
        try:
            self.last_run = pickle.load( open( self.LAST_RUN, "rb" ) )
        except IOError:
            self.last_run = {}
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)

    def run(self):
        stats = self.collect()
        self.put_stats(stats)

    def collect(self):
        squidclient  = subprocess.Popen(['which', 'squidclient'], stdout=subprocess.PIPE).communicate()[0].strip()
        cmd   = subprocess.Popen([squidclient, 'cache_object://localhost/info'], stdout=subprocess.PIPE).communicate()[0]
        out = cmd.split("\n")
        stats = {}
        for line in out:
            line = line.strip()
            for m in self.metric_list:
                if re.match(m, line):
                    tmp = line.split(':')
                    key  = self.format_key(tmp[0])
                    stats[key] = tmp[1].strip('\t')
        self.last_run = stats
        return self.get_current(stats)
    
    def get_current(self, current_run):
        testkey = next(iter(current_run))
        if current_run[testkey] < self.last_run[testkey]:
            return current_run
        new_stats = {}
        for m in self.metric_list:
            metric = self.format_key(m)
            try:
                new_stats[metric] = (int(current_run[metric]) - int(self.last_run[metric]))
            except KeyError:
                new_stats[metric] = 0
        return new_stats

    def format_key(self, line):
        line = line.replace('Number of ', '')
        line = line.replace(' ', '_').lower()
        return line

    def put_stats(self, stats):
        if not stats:
            return
        for metric in stats:
            try:
                print('PUTVAL "%s/squid/tcp_connections-%s" interval=%s N:%s' % (self.HOSTNAME, metric, str(COLLECTD_INTERVAL), str(stats[metric])))
                sys.stdout.flush()
            except KeyError:
                print('PUTVAL "%s/squid/tcp_connections-%s" interval=%s N:%s' % (self.HOSTNAME, metric, str(COLLECTD_INTERVAL), str(0)))
                sys.stdout.flush()
    
    def signal_handler(self, signal, frame):
        try:
            pickle.dump( self.last_run, open( self.LAST_RUN, "wb" ) )
            sys.exit(0)
        except IOError, e:
            print e
            sys.exit(0)

if __name__ == '__main__':
    COLLECTD_INTERVAL = float(os.environ.get('COLLECTD_INTERVAL'))
    stats = SquidStats()
    while True:
        stats.run()
        time.sleep(COLLECTD_INTERVAL)
