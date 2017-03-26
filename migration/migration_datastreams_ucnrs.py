# -*- coding: utf-8 -*-
################################################################################
#
# ucnrs_dri_datastream_generator.py
# 
# Created on Sun Aug  7 12:16:45 2016
# @author: Collin Bode
# @date: 2016-08-07
#
# Dependency: odm.config  pw file.
#
# purpose:  to generate datastreams for UCNRS weather stations using
# header fields.  The assumption is that all headers represent the same 
# type of instruments and that each field is unique per station.
#
# Each Datastream needs the following fields:
# DatastreamName, StationName, SiteCode, VariableCode, MethodName, FieldName, 
# Contact, DataQualityIncoming, DataQualityCurrent, RangeMin, RangeMax,
# StartDate, StationID, VariableID, MethodID, SiteID, MC_Name
#
# @updated: 2016-12-27 Added option to insert one new station's set of datastreams
#    Requires the station to be manually defined in database and .dat header 
#    to be in header directory.
################################################################################
import sys
#import os
#import pandas as pd
import mysql.connector
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

def dri_header_reader(path,filename):
    header = path+'dri_headers/'+filename+'.header'
    fh = open(header,'r')
    row2 = fh.readlines()[1].split(',')
    fh.close()
    fields = []
    for field in row2:
        field = field.replace('"','')
        if(field == "TIMESTAMP" or field == "RECORD"):
            #print('-- Ignoring '+field)
            pass
        elif("_flag" in field):
            #print('-- Flag field, ignoring ',field)
            pass
        else:
            #print(field)
            fields.append(field)
    return fields

def dri_starttime_reader(path,filename):
    fpath = path+filename
    fh = open(fpath,'r')
    row4 = fh.readlines()[4].split(',')
    fh.close()
    startstring = row4[0].strip()
    startstring = startstring.replace('"','')
    starttime = dt.datetime.strptime(startstring,"%Y-%m-%d %H:%M:%S")
    return starttime
        
# Arguments
#path = '/data/sensor/UCNRS/'
#path = '/Users/cbode/Documents/GoogleDrive/UCNRS_WeatherStations/DATFiles_DRI/'
path = 'C:/Users/me/Google Drive/UCNRS_WeatherStations/DATFiles/'

#########
# open database connection 
cnx = odm_connect('odm.config',False)  # default = False which is production, True = dev database
cursor = cnx.cursor()
cursor.execute('SELECT database()')
db_used = cursor.fetchall()
print('DATABASE: '+db_used[0][0])

# Get list of stations
sql = "SELECT s.StationID, s.StationName, s.SiteCode, i.SiteID, s.Contact, s.filename "+\
"FROM stations as s, sites as i "+\
"WHERE MC_NAME = 'UCNRS' AND s.SiteCode = i.SiteCode AND s.filename is not null"
cursor.execute(sql)
stations = cursor.fetchall()
stationscount = 0
i = 0

#fout = open(path+'station_startdates.csv','w')
#fout.write('StationID,StationName,StartDate\n')
for (stationid,station_name,site_code,siteid,contact,filename) in stations:
    stationscount += 1
    print('XX',stationid,station_name,filename)
    
    # Get Start Date for station
    starttime = dri_starttime_reader(path,filename)
    #str_startdate = dt.datetime.strftime(starttime,"%Y-%m-%d %H:%M:%S")
    #str_out = str(stationid)+','+station_name+','+str_startdate+'\n'
    #fout.write(str_out)
    
    # Read DRI header directory and get field names
    fields = dri_header_reader(path,filename)
    
    # Loop through each field and construct a datastream from it and station
    for field in fields:
        #print station_name,field

        # Skip irrelevent fields
        if(field == 'Station_ID_Number'):
            continue
        # Skip field if already in database
        sql_check = "SELECT DatastreamName FROM datastreams WHERE FieldName = %s AND StationName = %s"
        cursor.execute(sql_check,(field,station_name))
        ds_exists =  cursor.fetchall()
        if(len(ds_exists) > 0):
            print(len(ds_exists),'Datastream Exists!',station_name,field,'Skipping...')
            continue
        
        # pull data from datastreams based on fieldname
        sql_ds = 'SELECT DatastreamName,StationName,SiteCode,VariableCode,MethodName,Comments,'+\
        'DataQualityIncoming,DataQualityCurrent,RangeMin,RangeMax,VariableID,MethodID '+\
        'FROM datastreams WHERE MC_Name = "UCNRS" AND FieldName = "'+field+'" AND DatastreamID < 3151 LIMIT 1'
        cursor.execute(sql_ds)
        ds_pull =  cursor.fetchall()
        (ds,StationNameDS,SiteCodeDS,VariableCode,MethodName,Comments,dqi,dqc,RangeMin,RangeMax,VariableID,MethodID) = ds_pull[0]
        
        # Datastream reconstructed
        prefsuf = ds.split(SiteCodeDS)   
        if(len(prefsuf) == 2):
            datastream = prefsuf[0].strip()+' '+station_name+' '+prefsuf[1].strip()   
        elif(len(prefsuf) == 1):
            datastream = prefsuf[0].strip()+' '+station_name
        else:
            print('WARNING! TOO MANY PARTS TO DATASTREAM. STOPPING.')
            sys.exit()
        #print "\t"+ds+'-->'+datastream
        
        # Variables need to be cleaned
        if(Comments is None):
            Comments = ''
        else:
            Comments = str(Comments)        
        
        RangeMin = float(RangeMin)
        RangeMax = float(RangeMax)
        
        # construct datastream from station information + datastream information
        # 17 fields to insert
        sql_insert_ds = ("INSERT INTO datastreams (DatastreamName,StationName,SiteCode,VariableCode,"+\
        "MethodName,FieldName,Comments,Contact,DataQualityIncoming,DataQualityCurrent,RangeMin,"+\
        "RangeMax,StartDate,StationID,VariableID,MethodID,SiteID,MC_Name) "+\
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        if(i == 0):
            #fout.write(sql_insert_ds)
            #fout.write('\n')
            pass
        # 17 data variables in order of insert
        data_insert_ds = (datastream,station_name,site_code,VariableCode,
        MethodName,field,Comments,contact,dqi,dqc,RangeMin,RangeMax,
        starttime,stationid,VariableID,MethodID,siteid,"UCNRS")
        
        # Insert new datastream 
        cursor.execute(sql_insert_ds,data_insert_ds) 
        
        #print(sql_insert_ds) 
        print(data_insert_ds)     
        #fout.write(str(data_insert_ds)+'\n')
        
        i += 1
        if(i > 100):
        #   break
            pass
    if(stationscount > 1):
        #break
        pass          
    
print('Datastreams processed: ',i)    
 
# Clean up
cursor.close()
cnx.close()

#fout.close()