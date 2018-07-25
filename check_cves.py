#!/usr/bin/env python

import datetime
import json
import os
import requests
import shutil
import gzip

url = "https://nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-recent.json.gz"
fn = url.split('/')[-1]
unzipped = fn.replace('.gz', '') + "_" + datetime.datetime.now().strftime("%Y-%m-%d")
print "Current Redhat and Linux related CVEs from the National Vulnerability \
Database (https://nvd.nist.gov/):"
print "\n"

r = requests.get(url, stream=True, allow_redirects=True)
with open(fn, "wb") as f:
    r = requests.get(url, stream=True, allow_redirects=True)
    f.write(r.content)

with gzip.open(fn, 'rb') as file_in:
    with open(unzipped, 'wb') as file_out:
        shutil.copyfileobj(file_in, file_out)

with open(unzipped, 'r') as l:
    all = json.load(l)

CVEs = {}
vendors = ['redhat', 'kernel', 'linux']

for k in all['CVE_Items']:
        try:
            vendor_name  = (k['cve']['affects']['vendor']['vendor_data'][0]['vendor_name'])
            product_name = (k['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'][0]['product_name'])
        except IndexError:
            continue

        if any(v in vendor_name for v in vendors) or any(p in product_name for p in vendors):
           print("CVE: %s" % k['cve']['CVE_data_meta']['ID'])
           print("Vendor: %s" %  vendor_name)
           print("Product Name: %s" %  product_name)
           print("Description: %s" % k['cve']['description']['description_data'][0]['value'])
           print("Severity: %s " % k['impact']['baseMetricV2']['severity'])
           print("Integrity Impact: %s" %  k['impact']['baseMetricV2']['cvssV2']['integrityImpact'])
           print("Confidentiality Impact %s" % k['impact']['baseMetricV2']['cvssV2']['confidentialityImpact'])
           print "References:"
           for r in k['cve']['references']['reference_data']:
               print r['url']
           print "\n"
