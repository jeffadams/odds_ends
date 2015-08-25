#!/usr/bin/python
# Very basic check for a return of valid JSON. 

import json
import sys
import urllib2
status = { 'OK' : 0 , 'WARNING' : 1, 'CRITICAL' : 2 , 'UNKNOWN' : 3}

errors = "" 
urllib2.socket.setdefaulttimeout(3)

if len(sys.argv) < 1:
    sys.stderr.write('Need one argument: check_api.py http://jsonip.com') 
    sys.exit(1)
else:
    URL = sys.argv[1]

try:
    r = urllib2.urlopen(URL)
    a = r.read()
    data = json.loads(a)
except (urllib2.HTTPError, IOError, ValueError, KeyError, TypeError) as e:
    errors = ("%s %s" % (URL, e))
    next

if errors:
    print("WARN: %s" % errors)
    sys.exit(status['WARNING'])
else: 
    print("OK: %s" % URL)
    sys.exit(status['OK'])
