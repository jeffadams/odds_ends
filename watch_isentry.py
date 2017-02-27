#!/usr/bin/env python
# iSentry is a nifty free program that uses the Mac's builtin camera
# to take snapshots when it detects motion. 
# This script watches the iSentry directory (must be configured)
# and uploads the snapshots to S3. Requires the s3cmd.  

import os, sys, time

home = os.environ['HOME']
watch_dir = home + "/isentry_snapshots/"
date = time.strftime("%Y-%m-%d")
before = dict ([(f, None) for f in os.listdir (watch_dir)])

mypid = os.fork()
if mypid!=0:
    sys.exit(0)

while 1:
    time.sleep (5)
    after = dict ([(f, None) for f in os.listdir (watch_dir)])
    new = [f for f in after if not f in before]
    removed = [f for f in before if not f in after]
    if new: 
        print "new: ", ", ".join (new)
        os.system("/usr/local/bin/s3cmd sync %s s3://isentry/%s/" % (watch_dir, date))
    before = after
