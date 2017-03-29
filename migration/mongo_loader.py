#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################################
# 
# @author: collin bode
# @email: collin@berkeley.edu
# @date: 2017-03-28 
# 
# Purpose: Posts JSON documents to MongoDB through Scott's 
# Dendro API.  
#
# Requires: 
#   migration_stations.py must be run first
#   migration_datastreams_dashboard.py must be run first
#   Assumes station, datastream directories
########################################
import json
import requests
import datetime as dt
import pandas as pd
import os
import sys

# ARGS
# What are we loading?
target = 'stations'
#target = 'datastreams'
#target = 'organizations'

# Set paths
path = os.path.dirname(__file__)+os.sep+target+os.sep
tpath = path+'ztemp'+os.sep
if(os.path.exists(tpath) == False):
    os.mkdir(tpath)
                      
# http://www.jaimegil.me/2012/12/26/a-python-restful-api-consumer.html                      
# Set URL
url = 'http://128.32.109.75/api/v1/'+target
header = {"Content-Type":"application/json"}
r = requests.get(url,headers=header)
assert r.status_code == 200
rjson = r.json()
total = rjson['total']
print('Entries found: ',total)

rdata = rjson['data']
for entry in rdata:
    print(entry['name'],entry['_id'])
    fname = entry['name'].replace(' ','_')
    ffile = tpath+fname+'.json'
    print(ffile)
    with open(ffile, 'w') as f:
         json.dump(entry, f, indent=2,sort_keys=True)

for file in os.listdir(path): 
    print(file)
    with open(path+file) as json_data:
        d = json.load(json_data)
        #print(json.dumps(d,indent=2,sort_keys=True))
        for entry in rdata:
            if(d['name'] == entry['name']):
                print('MATCH! '+d['name'],entry['name'],entry['_id'])

print('DONE!')                 