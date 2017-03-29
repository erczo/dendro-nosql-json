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

# Set URL
url = 'http://128.32.109.75/api/v1/'+target
header = {"Content-Type":"application/json"}

stations = requests.get(url,headers=header)

for station in stations:
    s = json.load(station)
    print(json.dumps(s,indent=2,sort_keys=True))

'''
for file in os.listdir(path):                      
    print(file)
    with open(path+file) as json_data:
        d = json.load(json_data)
        print(json.dumps(d,indent=2,sort_keys=True))
        #d['name'] = name
    #requests.get(url)
'''       
                 