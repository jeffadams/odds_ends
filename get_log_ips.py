#!/usr/bin/python

from collections import Counter
import sys

class GetIps(object):
    def __init__(self):
        pass
    
    def count(self, file, offset=None): 
        results = []
        with open(file) as f:
            f = f.readlines()
        for line in f:
            x = line.split(' ', )
            results.append(x[0])

        if offset is not None:
            ip_list = Counter(results).most_common(offset)
    	else:
            ip_list = Counter(results).most_common(len(results))
        return ip_list

def main(args):
    if len(args) < 2:
        print "Usage: ./get_log_ips.py <logfile> <optional num of ips to display>"
        sys.exit(0)
    l = GetIps()
    if len(args) == 3:
        a = l.count(args[1], int(args[2]))
    else:
        a = l.count(args[1])
    for x in a:
        print("%s %s" % (x[1], x[0])) 

if __name__ == "__main__":
    main(sys.argv)
