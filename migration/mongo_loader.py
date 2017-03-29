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
# http://www.jaimegil.me/2012/12/26/a-python-restful-api-consumer.html                      
########################################
import os
import json
import requests
import glob
import time

# ARGS
# What are we loading?
target = 'stations'
#target = 'datastreams'
#target = 'organizations'

# Set paths
path = os.path.dirname(__file__)+'/'+target+'/'
tpath = path+'/'+'ztemp'+'/'
if(os.path.exists(tpath) == False):
    os.mkdir(tpath)

# Set URL to Station and pull station JSON list
url = 'http://128.32.109.75/api/v1/'+target
header = {"Content-Type":"application/json"}
r = requests.get(url,headers=header)
assert r.status_code == 200
rjson = r.json()
total = rjson['total']
print('Entries found: ',total)

# For each station, dump into a temp directory the JSON content
rdata = rjson['data']
for entry in rdata:
    print(entry['name'],entry['_id'])
    fname = entry['name'].replace(' ','_')
    ffile = tpath+fname+'.json'
    print(ffile)
    with open(ffile, 'w') as f:
         json.dump(entry, f, indent=2,sort_keys=True)

# Go through all the station JSON exported by migration_stations.py
# Check for a name match with existing stations, if it exists, delete it from Mongo
# Then post the new JSON into Mongo
print()
print('Loading JSON files now')
for filepath in glob.glob(path+"*.json"): 
    print(filepath)
    with open(filepath) as json_data:
        d = json.load(json_data)
        name = d['name']
        print(name)
        #print(json.dumps(d,indent=2,sort_keys=True))
        
        # Check for a match with existing station entries
        for entry in rdata:
            if(name == entry['name']):
                print('MATCH! '+name,entry['name'],entry['_id'])
                r2 = requests.delete(url+'/'+entry['_id'])
                assert r2.status_code == 200
                print('DELETED '+name+' in MongoDB')
        # Debug wait to deal with 500 internal error        
        time.sleep(2)
        print('slept 2 sec')
        
        # Insert new station JSON
        r3 = requests.post(url,headers=header,data=json.dumps(d))
        assert r3.status_code == 201        
        print(name+' inserted into MongoDB')
        
        time.sleep(2)
        print('slept 2 sec')


print('DONE!')                 