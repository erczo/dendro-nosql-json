#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################################
# UCNRS datastream seasonal json for the dashboard
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
#   migration_datastreams_ucnrs_dashboard.py must be run first
# Note: 
########################################
import json
import mysql.connector
import os
import re

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
path = os.path.dirname(__file__)+'/'
fpath = path+'datastreams'+'/'
spath = path+'seasonal'+'/'
if(os.path.exists(spath) == False):
    os.mkdir(spath)
dsfile_prefix = 'Legacy_Datastream_'
#########
# open database connection 
gitpath = os.path.dirname(os.path.dirname(os.path.dirname(path)))+os.sep
cnx = odm_connect(gitpath+'odm.pw',False)  # default = False which is production, True = dev database
cursor = cnx.cursor()
cursor.execute('SELECT database()')
db_used = cursor.fetchall()
print('DATABASE: '+db_used[0][0])

# Get list of mma and sum datastreams from sensor database
sql = "SELECT d.datastreamid, d.datastreamname FROM cfg_load_datavalues_day_sum as c, datastreams as d WHERE d.datastreamid = c.datastreamid"
cursor.execute(sql)
dailysums = cursor.fetchall()
sql = "SELECT d.datastreamid, d.datastreamname FROM cfg_load_datavalues_day_mma as c, datastreams as d WHERE d.datastreamid = c.datastreamid"
cursor.execute(sql)
dailymma = cursor.fetchall()
cursor.close()
cnx.close()

#########
# Iterate through both sets of datastreams
dslistlist = {'sum':dailysums, 'mma':dailymma}
for dspath,dslist in dslistlist.items():
    print(dspath)
    
    for dsid,dsname in dslist:
        #print(dsid,dsname)
        dsfname = dsfile_prefix+dsname.replace(' ','_')+'_'+str(dsid)+'.json'
        if(os.path.exists(fpath+dsfname)):
            aggregation_list = {10000:'Minimum',20000:'Average',30000:'Maximum'}
            if(dspath == 'sum'):
                aggregation_list[40000] = 'Cumulative'
            # acode = prefix to datastreamid for seasonal min=1,avg=2,max=3
            for acode,agg in aggregation_list.items():             
                #print(dspath,fpathname)
                with open(fpath+dsfname) as json_data:
                    d = json.load(json_data)
                    # Define new parameters for JSON
                    name = d['name']+' Seasonal '+agg
                    dsids = int(acode+int(dsid)) # dsids = datastream id seasonal
                    seasonal_tag = 'ds_Function_Seasonal'
                    aggregate_tag = 'ds_Aggregate_'+agg
        
                    # check for attribute existance
                    attributes = {}
                    for key in d.keys():
                        if(key == 'attributes'):
                            attributes = d['attributes']
                    #print(dsids,name,'Aggregate tag: '+aggregate_tag)
        
                    # Add Interval tag if using a daily aggregate 
                    # path is seasonal unless precip
                    path = "/legacy/datavalues-seasonal"
                    if(acode == 40000):
                        interval_tag = 'ds_Interval_Day'
                        path = "/legacy/datavalues-day"
        
                    # Assign parameters
                    if(len(attributes) > 0):
                        d['attributes'] = attributes
                    d['description'] = "This Datastream is derived from the legacy datastreamid: "+str(dsid)
                    d['name'] = name
                    #d['derived_from_datastream_ids'] = [dsid]
                    d['datapoints_config'][0]['params']['query']['datastream_id'] = dsids
                    d['datapoints_config'][0]['path'] = path
                    d['source_type'] = 'procedure'
                    taglist = d['tags']
                    for tag in taglist:
                        if(re.match('ds_Aggregat',tag)):
                            #print('Found Aggregate! Removing.',tag)
                            taglist.remove(tag)
                    taglist.append(aggregate_tag)
                    if(acode == 40000):
                        taglist.append(interval_tag)
                    else:
                        taglist.append(seasonal_tag)                
                    taglist.sort()
                    d['tags'] = taglist
                    
                    # Export JSON to file
                    #print(json.dumps(d,indent=2,sort_keys=True))
                    dsfile = spath+dsfile_prefix+'Seasonal_'+str(dsids)+'.json'
                    with open(dsfile, 'w') as f:
                        json.dump(d, f, indent=2,sort_keys=True)
                    print(dsfile+' exported.')
        else:
            print(dsfname+' ...file not found. skipping...')

print('DONE!')
