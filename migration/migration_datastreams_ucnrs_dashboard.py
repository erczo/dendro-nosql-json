#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################################
# UCNRS datastream csv to json for the dashboard
# @author: collin bode
# @email: collin@berkeley.edu
# Created on Tue Jan 17 19:40:41 2017
# 
# Purpose: creates JSON files for all UCNRS stations
# for only the datastreams needed for the dashboard.
#
# Requires: 
#   migration_datastreams_ucnrs_dashboard.csv: CSV file with fields to be altered.
#   Template_Legacy_Datastream.json: json template file.
#   migration_stations.py must be run first
#
# Note: 
########################################
import json
import pandas as pd
import mysql.connector
import os
import datetime as dt

def odm_connect(pwfilepath,boo_dev=False):
    # NOTE: password file (pwfile) should NEVER be uploaded to github!
    fpw = open(pwfilepath,'r')
    user = fpw.readline().strip()
    pw = fpw.readline().strip()
    fpw.close()
    if(boo_dev == True):
        db = 'odm_dev'
    else:
        db = 'odm'
    cnx = mysql.connector.connect(
        user=user,
        password=pw,
        host='gall.berkeley.edu',
        database=db)
    return cnx

# Set paths
path = os.path.dirname(__file__)+os.sep
dspath = path+'datastreams'+os.sep
json_template = 'Template_Legacy_Datastream.json'
dsfile_prefix = 'Legacy_Datastream_'

# Load the generic list of datastreams needed for the dashboard
df = pd.read_csv(path+'migration_datastreams_ucnrs_dashboard.csv')
rows = len(df)
columns = len(df.columns)

#########
# open database connection 
gitpath = os.path.dirname(os.path.dirname(os.path.dirname(path)))+os.sep
cnx = odm_connect(gitpath+'odm.pw',False)  # default = False which is production, True = dev database
cursor = cnx.cursor()
cursor.execute('SELECT database()')
db_used = cursor.fetchall()
print('DATABASE: '+db_used[0][0])

# Get list of stations
sql = "SELECT StationID,StationName FROM stations WHERE MC_Name = 'UCNRS'"
cursor.execute(sql)
stations = cursor.fetchall()
stationscount = 0
i = 0

for (stationid,station_name) in stations:
    stationscount += 1
    print('XX',stationscount,stationid,station_name)
        
    for i in range(0,rows):
        # Construct variables for JSON from DataFrame
        pref = df.iloc[i,0].strip()
        suf = df.iloc[i,1]
        if(suf != suf):
            suf = ''
        else:
            suf = suf.strip()
        name = pref+' '+station_name+' '+suf
        aggregate = 'ds_Aggregate_'+str(df.iloc[i,2])
        medium = 'ds_Medium_'+str(df.iloc[i,3])
        variable = 'ds_Variable_'+str(df.iloc[i,4])
        units = 'dt_Unit_'+str(df.iloc[i,5])
        hd = df.iloc[i,6]
        hdvalue = float(df.iloc[i,7])
        hdunits = 'dt_Unit_'+str(df.iloc[i,8])
        
        # attributes 
        attributes = {}
        if(hd == 'height'):
            attributes = { 'height' : { 'value' : hdvalue, 'unit' : hdunits } }
        if(hd == 'depth'):
            attributes = { 'depth' : { 'value' : hdvalue, 'unit' : hdunits } }
        
        # check to make sure it all looks good
        #print(i,name,aggregate,medium,variable,units,attributes)      
        
        # Get Datastream by name and confirm it exists,else continue
        sql = 'SELECT DatastreamID,StartDate FROM datastreams WHERE DatastreamName = "'+name+'"'
        cursor.execute(sql)
        try:
            dsid,datestart = cursor.fetchall()[0]
            #print('\t',dsid,name,datestart)
        except:
            print(name+' does not exist on '+station_name+'. continuing...')
            continue
        
        # Open JSON template and modify DOM
        with open(json_template) as json_data:
            d = json.load(json_data)
            d['name'] = name
            d['tags'] = [aggregate,medium,variable,units]
            # add external references to the sensor database id's
            d['external_refs'][0]['identifier'] = str(dsid)
            d['external_refs'][1]['identifier'] = str(stationid)
            if(attributes != {}):
                print(dsid,'Adding Attributes')
                d['attributes'] = attributes
            d['datapoints_config'][0]['begins_at'] = dt.datetime.strftime(datestart,"%Y-%m-%dT%H:%M:%SZ")
            d['datapoints_config'][0]['params']['query']['datastream_id'] = dsid
            #if(medium == 'Precipitation'):
            #    d['datapoints_config'][0]['path'] = "/legacy/datavalues-day"
            #d['station_id'] = stationid
            #print(json.dumps(d,indent=2,sort_keys=True))
            # Export to JSON
            dsname = name.replace(' ','_')
            dsfile = dspath+dsfile_prefix+dsname+'_'+str(dsid)+'.json'
            print(dsfile)
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
    
# Clean up
cursor.close()
cnx.close()

print('DONE!')
