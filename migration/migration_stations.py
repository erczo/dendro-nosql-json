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


# WRCC has codes for each UC weather station
ucnrs_station_list = {'Hastings':'ucha',
    'Blue Oak Ranch':'ucbo',
    'Angelo Reserve South Meadow':'ucac',
    'Bodega':'ucbm',
    'Deep Canyon':'ucde',
    'Burns':'ucbu',
    'Chickering':'ucca',
    'Elliott':'ucel',
    'James':'ucja',
    'Jepson':'ucjp',
    'Rancho Marino':'ucrm',
    'BigCreek Whale':'whpt',
    'BigCreek Highlands':'hipk',
    'BigCreek Gatehouse':'ucbc',
    'McLaughlin':'ucmc',
    'Motte':'ucmo',
    'Santa Cruz Island':'ucsc',
    'Sedgwick':'ucse',
    'SNARL':'ucsh',
    'Anza Borrego':'ucab',
    'Stunt Ranch':'ucsr',
    'Granites':'ucgr',
    'WhiteMt Summit':'wmtn',
    'WhiteMt Barcroft':'barc',
    'WhiteMt Crooked':'croo',
    'Younger':'ucyl',
    'Sagehen Creek':'sagh'
}

organization_list = {
        'UCNRS':'58db17c424dc720001671378',
        'ERCZO':'58db17e824dc720001671379'
}
org_id = organization_list['UCNRS']

# Set path to current directory
path = os.path.dirname(__file__)+os.sep
print(path)
json_path = os.path.join(path,'Template_Legacy_Station.json')
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
        station_name = 'Angelo Reserve South Meadow'
        station_slug = 'angelo-south'
    lat = df.iloc[i,1]
    long = df.iloc[i,2]
    elev = df.iloc[i,3]
    mc = df.iloc[i,4].strip()
    stationid = df.iloc[i,5]
            
    # Get the DRI code for the station
    dri_code = ''
    for s,dri in ucnrs_station_list.items():
        if(s == station_name):
            dri_code = dri
    if(dri_code == ''):
        if(mc != 'UCNRS'):
            dri_code = station_slug
        else:
            print(station_name+' not in WRCC DRI codes. Skipping')
            continue
    print(station_name,mc,dri_code)
    
    # Assign variable to JSON template
    with open(json_path) as json_data:
        d = json.load(json_data)
        d['geo']['coordinates'] = [long,lat,elev]
        d['name'] = station_name
        d['slug'] = station_slug
        if(mc != 'UCNRS'):
            d['external_links'][0]['url'] = 'http://sensor.berkeley.edu/'
        d['external_refs'][0]['identifier'] = str(stationid)
        # Assuming the images do not change, 
        # the following will assign DRI 4 digit code to the image urls
        for j in range(0,len(d['media'])):
            for msize in d['media'][j]['sizes']:
                old_url = d['media'][j]['sizes'][msize]['url']
                new_url = old_url.replace('DRICODE',dri_code)
                d['media'][j]['sizes'][msize]['url'] = new_url
                #print(d['media'][j]['sizes'][msize]['url'])               
        d['organization_id'] = org_id
         
       # Export the DOM to JSON file
        station_filename = station_name.replace(' ','_')+'.json'
        print(station_filename)
        #print(json.dumps(d,indent=2,sort_keys=True))
        with open(station_path+station_filename, 'w') as f:
            json.dump(d, f, indent=2,sort_keys=True)
        
print('DONE!')
