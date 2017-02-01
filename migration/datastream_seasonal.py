# -*- coding: utf-8 -*-
########################################
# Datastream Seasonal Aggregates Creator
# @author: collin bode
# @email: collin@berkeley.edu
# date: 2017-01-22
#
# Purpose: Creates monthly seasonal aggregates from datastreams
# (min,avg,max) for all years up to defined date.
# This is used by the Dendro Dashboard
# Variables to aggregate
# air temp
# soil temp
# soil moisture
# wind speed - daytime only?
# humidity
# barometric pressure? 
# solar - daily cumulative
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
    3077:'Air Temp Deg C Blue Oak Avg',
    3105:'Soil Temp Deg C 20 in Blue Oak Avg',
    3106:'Soil Moisture VWC Blue Oak Avg',
    3069:'Wind Speed m s Blue Oak Avg',
    3080:'Relative Humidity Per Blue Oak Avg',
    3081:'Barometric Pressure mbar Blue Oak Avg',
    #3061:'Total Solar Radiation W m2 Blue Oak Avg',
    3082:'Precipitation mm Blue Oak',
    3355:'Air Temp Deg C 2 m Angelo Avg',
    3373:'Soil Temp Deg C 20 in Angelo Avg',
    3374:'Soil Moisture VWC Angelo Avg',
    3336:'Wind Speed m s Angelo Avg',
    3348:'Relative Humidity Per Angelo Avg',
    3349:'Barometric Pressure mbar Angelo Avg',
    #3329:'Total Solar Radiation W m2 Angelo Avg',
    3350:'Precipitation mm Angelo'
}

# Get current year
now = dt.datetime.now()
year_current = now.year

# Use ODM_DEV or production ODM
booDev = True
# go to git base directory outside repository
gitpath = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+os.sep
pwfile = gitpath+'odm.pw'
print(gitpath)

for dsid,dsname in dslist.items():
    print(dsid,dsname)
    if(re.match('Precipitation',dsname)):
        print('TRUE! I found Precipitation:',dsid,dsname)

    # Connect to Sensor Database and get oldest year for DSID
    conn = odm_connect(pwfile,boo_dev=booDev)
    sql_oldest_year = 'SELECT min(year(LocalDateTime)) '+\
    ' FROM odm.datavalues_UCNRS '+\
    ' WHERE DatastreamID = '+str(dsid)
    cursor = conn.cursor()
    cursor.execute(sql_oldest_year)
    year_oldest = cursor.fetchall()[0][0]
    print(dsid,dsname+' Oldest Year: ',year_oldest)
    conn.close()

    for year in range(year_oldest+1,year_current):
        print('\t Year: ',year)
        
        sql_daily = 'CREATE TEMPORARY TABLE ztemp_date '+\
        'SELECT date(localdatetime) as ldate, '+\
        'count(*) as count_hour, '+\
        'min(DataValue) as min, '+\
        'avg(DataValue) as avg, '+\
        'max(DataValue) as max, '+\
        'sum(DataValue) as sum '+\
        'FROM odm.datavalues_UCNRS '+\
        "WHERE datastreamid = "+str(dsid)+" and LocalDateTime < '"+str(year)+"-01-01 00:00:00' "+\
        'GROUP BY date(localdatetime) '+\
        'ORDER BY date(localdatetime)'
        #print(sql_daily)
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
        
        dsidmin = 10000+dsid
        dsidavg = 20000+dsid
        dsidmax = 30000+dsid
        '''
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
            
        cursor.close()
        conn.close()
        '''
print('DONE!')