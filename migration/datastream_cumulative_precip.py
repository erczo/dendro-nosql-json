# -*- coding: utf-8 -*-
########################################
# Datastream Cumulation Aggregates Creator
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
import re
import os

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

dslist = {
    #3061:'Total Solar Radiation W m2 Blue Oak Avg',
    3082:'Precipitation mm Blue Oak',
    #3329:'Total Solar Radiation W m2 Angelo Avg',
    3350:'Precipitation mm Angelo'
}

# Get current day
today = dt.date.today()
today_f =  dt.datetime.strftime(today,"%Y-%m-%d %H:%M:%S")
print(today_f)
# Use ODM_DEV or production ODM
booDev = True

# go to git base directory outside repository
gitpath = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+os.sep
pwfile = gitpath+'odm.pw'
print(gitpath)

for dsid,dsname in dslist.items():
    print(dsid,dsname)

    # Seasonal Derived Datastream ID Code      
    dsidcumday = 40000+dsid     # Cumulative for one day (24h) midnight to midnight
    
    # Get most recent day in record for cumulative DSID
    # if there is no records yet, script will do the entire datastream - current day
    conn = odm_connect(pwfile,boo_dev=booDev)
    sql_last_entry = 'SELECT max(LocalDateTime) '+\
    ' FROM odm.datavalues_UCNRS '+\
    ' WHERE DatastreamID = '+str(dsidcumday)
    cursor = conn.cursor()
    cursor.execute(sql_last_entry)
    if(cursor.rowcount > 0):
        last_date = cursor.fetchall()[0][0]
        booRecordsExist = True
        last_date_f = dt.datetime.strftime(last_date,"%Y-%m-%d %H:%M:%S")
        print(dsid,dsname+' last date: ',last_date_f)
    else:
        booRecordsExist = False            
    conn.close()
    print('Do previous records exist?',booRecordsExist)
    
    sql_daily = 'CREATE TEMPORARY TABLE ztemp_date '+\
    'SELECT date(localdatetime) as ldate, '+\
    'count(*) as count_hour, '+\
    'sum(DataValue) as sum '+\
    'FROM odm.datavalues_UCNRS '+\
    "WHERE datastreamid = "+str(dsid)
    if(booRecordsExist == True):       
        sql_daily+" AND LocalDateTime > '"+last_date_f+"' "+\
    sql_daily+" AND LocalDateTime < '"+today_f+"' "+\
    'GROUP BY date(localdatetime) '+\
    'ORDER BY date(localdatetime)'
    print(sql_daily)
    '''
    conn = odm_connect(pwfile,boo_dev=booDev)
    cursor = conn.cursor()
    cursor.execute(sql_daily)

    sql_monthly = 'SELECT month(ldate) as month, '+\
    'count(*) as count_month, '+\
    'sum(count_hour) as count_hour, '+\
    'avg(min) as min_avg, '+\
    'avg(avg) as avg_avg, '+\
    'avg(max) as max_avg, '+\
    'min(sum) as min_sum, '+\
    'avg(sum) as avg_sum, '+\
    'max(sum) as max_sum '+\
    'FROM ztemp_date GROUP BY month(ldate)'
    #print(sql_monthly)
    df = pd.read_sql_query(sql_monthly,con=conn)
    
    for i in range(0,len(df)):
        month =  df['month'][i]
        mmin = df['min_avg'][i]
        mavg = df['avg_avg'][i]
        mmax = df['max_avg'][i]
        mminsum = df['min_sum'][i]
        mavgsum = df['avg_sum'][i]
        mmaxsum = df['max_sum'][i]
        
        # Insert monthly values into the datavalues_seasonal table
        SeasonDateTime = str(year)+'-'+str(month).zfill(2)+'-01 00:00:00'
        print(SeasonDateTime,dsid,dsname,' INSERTING')
        # DataValue,ValueAccuracy,SeasonDateTime,UTCOffset,QualifierID,DerivedFromID,QualityControlLevelCode,DatastreamID  
        sql_insert = 'INSERT into datavalues_seasonal (DataValue,LocalDateTime,'+\
        'UTCOffset,QualifierID,DerivedFromID,QualityControlLevelCode,DatastreamID) '+\
        'Values (%s,%s,%s,%s,%s,%s,%s)'
        if(re.match('Precipitation',dsname)):
            cursor.execute(sql_insert,(float(mminsum),SeasonDateTime,-8,2,dsid,2,dsidmin))
            cursor.execute(sql_insert,(float(mavgsum),SeasonDateTime,-8,2,dsid,2,dsidavg))
            cursor.execute(sql_insert,(float(mmaxsum),SeasonDateTime,-8,2,dsid,2,dsidmax))
        else:   
            cursor.execute(sql_insert,(float(mmin),SeasonDateTime,-8,2,dsid,2,dsidmin))
            cursor.execute(sql_insert,(float(mavg),SeasonDateTime,-8,2,dsid,2,dsidavg))
            cursor.execute(sql_insert,(float(mmax),SeasonDateTime,-8,2,dsid,2,dsidmax))
    '''    
    cursor.close()
    conn.close()

print('DONE!')