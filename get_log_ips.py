#!/usr/bin/python

from collections import Counter, OrderedDict
import sys

if len(sys.argv) < 2:
    print "Usage: ./get_log_ips.py <logfile> <optional num of ips to display>"
    sys.exit(0)
else:
    infile = sys.argv[1]

lines = []
with open(infile) as f:
    f = f.readlines()

for line in f:
    x = line.split(' ', )
    lines.append(x[0])

if len(sys.argv) == 3:
    a = Counter(lines).most_common(int(sys.argv[2]))
    for x in a:
        print("%s %s" % (x[1], x[0])) 
else:
    a = Counter(lines)
    # http://docs.python.org/dev/library/collections.html#ordereddict-examples-and-recipes
    all_ips = OrderedDict(sorted(a.items(), key=lambda t: t[1], reverse=True))

    for x in all_ips:
        print all_ips[x], x 
