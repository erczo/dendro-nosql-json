#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################################
# datastream csv to json converter
# @author: collin bode
# @email: collin@berkeley.edu
# Created on Tue Jan 17 19:40:41 2017
#
# Requires: CSV file with fields to be altered
#           json template file
########################################
import json
import pandas as pd

path = '../examples/datastreams/'
datastream_csv = 'angelo_datastreams_code.csv'
json_template = 'Legacy_Datastream_Angelo_Generic.json'
dsfile_prefix = 'Legacy_Datastream_'

df = pd.read_csv(datastream_csv)
rows = len(df)
columns = len(df.columns)
for i in range(1,rows):
    name = df.iloc[i,0]
    aggregate = 'ds_Aggregate_'+str(df.iloc[i,1])
    medium = 'ds_Medium_'+str(df.iloc[i,2])
    variable = 'ds_Variable_'+str(df.iloc[i,3])
    units = 'dt_Unit_'+str(df.iloc[i,4])
    datestart = df.iloc[i,5]
    dsid = str(df.iloc[i,6])
    hd = df.iloc[i,7]
    hdvalue = df.iloc[i,8]
    hdunits = str(df.iloc[i,9])
    if(hd == 'height'):
        attributes = { 'height' : { 'height' : hdvalue, 'units' : hdunits } }
    if(hd == 'depth'):
        attributes = { 'depth' : { 'depth' : hdvalue, 'units' : hdunits } }
    print(i,dsid,name,aggregate,medium,variable,units,attributes)      
    with open(path+json_template) as json_data:
        d = json.load(json_data)
        d['name'] = name
        d['tags'] = [aggregate,medium,variable,units]
        d['attributes'] = attributes
        d['datapoints_config'][0]['begins_at'] = datestart
        d['datapoints_config'][0]['params']['query']['datastream_id'] = dsid
        print(json.dumps(d,indent=2,sort_keys=True))
        dsfile = path+dsfile_prefix+dsid+'.json'
        with open(dsfile, 'w') as f:
             json.dump(d, f, indent=2,sort_keys=True)
print('DONE!')
