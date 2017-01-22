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
# solar - daily cumulative
# precip - daily cumulative
# barometric pressure? 
########################################
import pandas as pd
import mysql.connector
import datetime as dt

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
    3081:'Barometric Pressure mbar Blue Oak Avg'

}