# -*- coding: utf-8 -*-
########################################
# Datastream Daily Cumulation Aggregates Creator
# @author: collin bode
# @email: collin@berkeley.edu
# date: 2017-01-28
#
# Purpose: Creates daily cumulations from datastreams
# This is used by the Dendro Dashboard
# Variables to aggregate
# solar - daily cumulative (not yet)
# precip - daily cumulative
########################################
import mysql.connector
import datetime as dt
import pandas as pd
import os
import sys

def odm_connect(pwfilepath,boo_dev=False):
    # NOTE: password file should NEVER be uploaded to github!
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

# Get current day
today = dt.date.today()
today_f =  dt.datetime.strftime(today,"%Y-%m-%d %H:%M:%S")
print(today_f)

# Use ODM_DEV or production ODM
booDev = False


# go to git base directory outside repository
if(sys.platform == 'linux'):
    gitpath = '/home/collin/git/'    
else:
    gitpath = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+os.sep
pwfile = gitpath+'odm.pw'
print(pwfile)

# Establish database connection
conn = odm_connect(pwfile,boo_dev=booDev)

# Perform Aggregation for each Monitoring collection desired, since they have different datavalues tables
MC_List = {'UCNRS':'datavalues_UCNRS','Angelo Reserve':'datavalues2'}

for MC,dv_table in MC_List.items():
    print(MC,dv_table)
    # Build list of Datastreams with precipitation to aggregate based on VariableCode
    sql_ds_list = ' SELECT DatastreamID,DatastreamName FROM datastreams '+\
    'WHERE VariableCode = "Rainfall mm" AND MC_Name = "'+MC+'"'
    cursor = conn.cursor()
    cursor.execute(sql_ds_list)
    ds_list = cursor.fetchall()
    cursor.close()
    
    for dsid,dsname in ds_list:
        print(dsid,dsname)
    
        # Seasonal Derived Datastream ID Code      
        dsidcumday = 40000+dsid     # Cumulative for one day (24h) midnight to midnight
        
        # CHECKS      
        booRecordsExist = False # Is this a first time run or do records already exist?
        booSkip = False         # Skip this datastream, because it is up to date     
                                              
        # Get most recent day in record for cumulative DSID
        # if there is no records yet, script will do the entire datastream - current day
        sql_check = 'SELECT count(*) FROM datavalues_seasonal WHERE DatastreamID = '+str(dsidcumday)
        cursor = conn.cursor()
        cursor.execute(sql_check)
        entries = cursor.fetchall()[0][0]
        print(dsname,dsidcumday,' record count" ',entries)
        if(entries > 0):
            sql_last_entry = 'SELECT max(LocalDateTime) FROM datavalues_seasonal WHERE DatastreamID = '+str(dsidcumday)
            #print(sql_last_entry)
            booRecordsExist = True
            cursor.execute(sql_last_entry)
            last_date_day = cursor.fetchall()[0][0]
            last_date_day = last_date_day.date()
            last_date_day_f = dt.datetime.strftime(last_date_day,"%Y-%m-%d %H:%M:%S")
            print(dsid,dsname+'    day last date: ',last_date_day_f)
            
            # Check if there are enough new records to create another 24 hour aggregate
            sql_last_entry = 'SELECT max(LocalDateTime) FROM odm.'+dv_table+' WHERE DatastreamID = '+str(dsid)
            cursor.execute(sql_last_entry)
            last_date_source = cursor.fetchall()[0][0]
            last_date_source_f = dt.datetime.strftime(last_date_day,"%Y-%m-%d %H:%M:%S")
            print(dsid,dsname+' source last date: ',last_date_day_f)
    
            # Compare the two days
            last_date_source_d = last_date_source.date()
            if(last_date_day == last_date_source_d):
                booSkip = True
                print('SKIPPING ',dsid,dsidcumday,' ALREADY UP TO DATE')                
        print('Do previous records exist?',booRecordsExist)
        cursor.close()
        
        if(booSkip == False):
            #  Aggregates readings to a daily level place into Panda Table
            sql_daily = 'SELECT date(localdatetime) as ldate, '+\
            'count(*) as count, '+\
            'sum(DataValue) as sum '+\
            'FROM odm.'+dv_table+\
            " WHERE datastreamid = "+str(dsid)
            if(booRecordsExist == True):       
                sql_daily = sql_daily+" AND LocalDateTime > '"+last_date_day_f+"' "
            sql_daily = sql_daily + " AND LocalDateTime < '"+today_f+"' "+\
            'AND QualifierID < 3 '+\
            'GROUP BY date(localdatetime) '+\
            'ORDER BY date(localdatetime)'
            print(sql_daily)
    
            df = pd.read_sql_query(sql_daily,con=conn)
            cursor = conn.cursor()
            # Insert each day into the seasonal table
            for i in range(0,len(df)):
                # Insert daily values into the datavalues_seasonal table
                SeasonDateTime = dt.datetime.strftime(df.iloc[i,0],"%Y-%m-%d 00:00:00")
                daysum = float(df.iloc[i,2])
                print('INSERT ',SeasonDateTime,dsidcumday,dsname,daysum)
                # DataValue,ValueAccuracy,SeasonDateTime,UTCOffset,QualifierID,DerivedFromID,QualityControlLevelCode,DatastreamID               
                sql_insert = 'INSERT into datavalues_seasonal (DataValue,LocalDateTime,'+\
                'UTCOffset,QualifierID,DerivedFromID,QualityControlLevelCode,DatastreamID) '+\
                'Values (%s,%s,%s,%s,%s,%s,%s)'
                cursor.execute(sql_insert,(daysum,SeasonDateTime,-8,2,dsid,2,dsidcumday))
                
            cursor.close()
# Clean up
conn.close()
print('DONE!')