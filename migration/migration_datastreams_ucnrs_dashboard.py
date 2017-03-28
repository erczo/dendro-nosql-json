#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################################
# datastream csv to json converter
# @author: collin bode
# @email: collin@berkeley.edu
# Created on Tue Jan 17 19:40:41 2017
#
# Requires: 
#   migration_datastreams_ucnrs_dashboard.csv: CSV file with fields to be altered.
#   Template_Legacy_Datastream.json: json template file.
#   migration_stations.py must be run first
########################################
import json
import pandas as pd
import mysql.connector
import os

path = os.path.dirname(__file__)+os.sep
dspath = path+'datastreams'
json_template = 'Template_Legacy_Datastream.json'
dsfile_prefix = 'Legacy_Datastream_'


for datastream_csv,stationid in reserve_list.items():
    dfall = pd.read_csv(datastream_csv)
    df = dfall[dfall['DASHBOARD9'] == 1] # select only the datastreams used in dashboard. 
    rows = len(df)
    columns = len(df.columns)
    
    for i in range(0,rows):
        name = df.iloc[i,0]
        aggregate = 'ds_Aggregate_'+str(df.iloc[i,1])
        medium = 'ds_Medium_'+str(df.iloc[i,2])
        variable = 'ds_Variable_'+str(df.iloc[i,3])
        units = 'dt_Unit_'+str(df.iloc[i,4])
        datestart = df.iloc[i,5]
        dsid = int(df.iloc[i,6])
        hd = df.iloc[i,7]
        hdvalue = float(df.iloc[i,8])
        hdunits = 'dt_Unit_'+str(df.iloc[i,9])
        attributes = {}
        if(hd == 'height'):
            attributes = { 'height' : { 'value' : hdvalue, 'unit' : hdunits } }
        if(hd == 'depth'):
            attributes = { 'depth' : { 'value' : hdvalue, 'unit' : hdunits } }
        print(i,dsid,name,aggregate,medium,variable,units,attributes)      
        with open(json_template) as json_data:
            d = json.load(json_data)
            d['name'] = name
            d['tags'] = [aggregate,medium,variable,units]
            if(attributes != {}):
                print(dsid,'Adding Attributes')
                d['attributes'] = attributes
            d['datapoints_config'][0]['begins_at'] = datestart
            d['datapoints_config'][0]['params']['query']['datastream_id'] = dsid
            d['station_id'] = stationid
            #print(json.dumps(d,indent=2,sort_keys=True))
            dsfile = path+dsfile_prefix+str(dsid)+'.json'
            #print(dsfile)
            with open(dsfile, 'w') as f:
                 json.dump(d, f, indent=2,sort_keys=True)
        aggregate = ''
        attributes = {}
        medium = ''
        variable = ''
        units = ''
        datestart = ''
        dsid = 0
        hd = ''
    
print('DONE!')
