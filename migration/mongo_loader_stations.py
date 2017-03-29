#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################################
#  mongo_loader_stations.py
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
# http://www.jaimegil.me/2012/12/26/a-python-restful-api-consumer.html                      
########################################
import os
import json
import requests
import glob
import time

# Set paths
path = os.path.dirname(__file__)+'/'+target+'/'
tpath = path+'/'+'ztemp'+'/'
if(os.path.exists(tpath) == False):
    os.mkdir(tpath)

# Set URL to Station and pull station JSON list
url = 'http://128.32.109.75/api/v1/stations'
header = {"Content-Type":"application/json"}
r = requests.get(url+'?$limit=2000',headers=header)  # note the addition of 2000 record limit 
assert r.status_code == 200
rjson = r.json()
total = rjson['total']
print('Entries found: ',total)

# For each station, dump into a temp directory the JSON content
# Then delete from Mongo
rdata = rjson['data']
for entry in rdata:
    print(entry['name'],entry['_id'])
    fname = entry['name'].replace(' ','_')
    ffile = tpath+fname+'.json'
    #print(ffile)
    with open(ffile, 'w') as f:
         json.dump(entry, f, indent=2,sort_keys=True)
    r2 = requests.delete(url+'/'+entry['_id'])
    assert r2.status_code == 200
    print('DELETED '+entry['name']+' in MongoDB')
    
# Go through all the station JSON exported by migration_stations.py
# Post the new JSON into Mongo
print('Loading JSON files now\n')
for filepath in glob.glob(path+"*.json"): 
    print(filepath)
    with open(filepath) as json_data:
        d = json.load(json_data)
        name = d['name']
        print(name)

        # Insert new station JSON
        r3 = requests.post(url,headers=header,data=json.dumps(d))
        assert r3.status_code == 201        
        print(name+' inserted into MongoDB')

print('DONE!')                 