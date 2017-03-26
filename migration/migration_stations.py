# -*- coding: utf-8 -*-
########################################
# Migration Stations
# @author: collin bode
# @email: collin@berkeley.edu
# date: 2017-03-25
#
# Purpose: 
# Convert Legacy Sensor Database stations into 
# Dendro MongoDB compliant JSON files.  
# Note: this requires converting lat/long from NAD83 to WGS84
# and merging stations table with site table
# People are not dealt with yet.    
########################################
import json 
import pandas as pd
import os

# go to git base directory outside repository
path = os.path.dirname(__file__)+os.sep
print(path)
json_path = path+'Template_Legacy_Station.json'
csv_path = path+'stations_legacy.csv'
station_path = path+'stations'+os.sep

# Load the CSV list of stations into pandas
df = pd.read_csv(csv_path)
rows = len(df)
columns = len(df.columns)

# Convert each station row into a JSON document
for i in range(0,rows):
    station_name =  df.iloc[i,0].strip()
    station_slug = station_name.replace(' ','-').lower()
    if(station_name == 'Angelo'):
        station_name = 'Angelo South'
        station_slug = 'angelo-south'
    lat = df.iloc[i,1]
    long = df.iloc[i,2]
    elev = df.iloc[i,3]
    mc = df.iloc[i,4].strip()
    stationid = df.iloc[i,5]
    print(station_name,mc)
    with open(json_path) as json_data:
        d = json.load(json_data)
        d['geo']['coordinates'] = [long,lat,elev]
        d['name'] = station_name
        d['slug'] = station_slug
        if(mc != 'UCNRS'):
            d['external_links'][0]['url'] = 'http://sensor.berkeley.edu/'
        d['external_refs'][0]['identifier'] = str(stationid)
        station_filename = station_name.replace(' ','_')+'.json'
        print(station_filename)
        print(json.dumps(d,indent=2,sort_keys=True))
        with open(station_path+station_filename, 'w') as f:
            json.dump(d, f, indent=2,sort_keys=True)
print('DONE!')
