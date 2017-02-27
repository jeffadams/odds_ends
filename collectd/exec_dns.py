#!/usr/bin/env python

import os
import pickle
import re
import signal
import socket
import subprocess
import sys
import time

class RNDCStats(object):
    def __init__(self):
        self.LAST_RUN  = '/var/tmp/dns_stats.pickle'
        self.STATSFILE = '/var/named/data/named_stats.txt'
        self.HOSTNAME = socket.gethostname()
        self.metric_list = [
            'IPv4_requests_received',
            'queries_resulted_in_NXDOMAIN',
            'queries_resulted_in_nxrrset',
            'queries_resulted_in_authoritative_answer',
            'responses_sent',
            'queries_resulted_in_successful_answer',
            'queries_caused_recursion',
            'queries_resulted_in_SERVFAIL',
            'queries_resulted_in_non_authoritative_answer',
        ]

        try:
            self.last_run = pickle.load( open( self.LAST_RUN, "rb" ) )
        except IOError:
            self.last_run = {}

        signal.signal(signal.SIGTERM, self.signal_handler)

    def run(self):
        stats = self.collect()
        self.put_stats(stats)

    def collect(self):
        try:
            os.remove(self.STATSFILE)
        except OSError as e:
            pass
        # Create new stats file.
        rndc  = subprocess.Popen(['which', 'rndc'], stdout=subprocess.PIPE).communicate()[0].strip()
        cmd   = subprocess.Popen(['rndc', 'stats'], stdout=subprocess.PIPE).communicate()[0]
        stats_file = open(self.STATSFILE, 'r')
        ## Data we want is between these lines.
        stats_start_re = re.compile('\++\s+Name Server Statistics\s+\++')
        stats_end_re   = re.compile('\++\s+Zone Maintenance Statistics\s+\++')
        this_run = {}
        get_line = False
        for line in stats_file:
            if  stats_start_re.match(line):
                get_line = True
                continue
            if  stats_end_re.match(line):
                break
            if get_line:
                temp  = line.strip().split()
                value = temp.pop(0)
                key   = '_'.join(temp)
                this_run[key] = int(value)
        if self.last_run:
            stats_dict = self.get_current(this_run)
        else:
            stats_dict =  this_run
        self.last_run = this_run
        return stats_dict
    
    def get_current(self, current_run):
        if current_run['IPv4_requests_received'] < self.last_run['IPv4_requests_received']:
            return current_run
        new_stats = {}
        for metric in self.metric_list:
            try:
                new_stats[metric] = (current_run[metric] - self.last_run[metric])
            except KeyError:
                new_stats[metric] = 0
        return new_stats
    
    def put_stats(self, stats):
        if not stats:
            return
        for metric in self.metric_list:
            try:
                print('PUTVAL "%s/dns/tcp_connections-%s" interval=%s N:%s' % (self.HOSTNAME, metric, str(COLLECTD_INTERVAL), str(stats[metric])))
                sys.stdout.flush()
            except KeyError:
                print('PUTVAL "%s/dns/tcp_connections-%s" interval=%s N:%s' % (self.HOSTNAME, metric, str(COLLECTD_INTERVAL), str(0)))
                sys.stdout.flush()
    
    def signal_handler(self, signal, frame):
        try:
            pickle.dump( self.last_run, open( self.LAST_RUN, "wb" ) )
        except IOError, e:
          print e
        sys.exit(0)


if __name__ == '__main__':
    COLLECTD_INTERVAL = float(os.environ.get('COLLECTD_INTERVAL'))
    stats = RNDCStats()
    while True:
        stats.run()
        time.sleep(COLLECTD_INTERVAL)
