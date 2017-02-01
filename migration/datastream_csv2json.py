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
dsfile_prefix = 'Legacy_Datastream_'
reserve_list = {
    'angelo_datastreams_code.csv':'Legacy_Datastream_Angelo_Generic.json',
    'borr_datastreams_code.csv':'Legacy_Datastream_Blue_Oak_Generic.json' 
}

for datastream_csv,json_template in reserve_list.items():
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
        hdunits = str(df.iloc[i,9])
        attributes = {}
        if(hd == 'height'):
            attributes = { 'height' : { 'height' : hdvalue, 'units' : hdunits } }
        if(hd == 'depth'):
            attributes = { 'depth' : { 'depth' : hdvalue, 'units' : hdunits } }
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
