#!/usr/bin/python

from collections import Counter
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
else:
    a = Counter(lines).most_common(len(lines))
     
for x in a:
    print("%s %s" % (x[1], x[0])) 
