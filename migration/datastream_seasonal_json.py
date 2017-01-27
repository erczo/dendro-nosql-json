# -*- coding: utf-8 -*-
########################################
# Datastream Seasonal JSON Creator
# @author: collin bode
# @email: collin@berkeley.edu
# date: 2017-01-23
#
# Purpose: Creates JSON configuration files for each of the datastreams created
# by datastream_seasonal.py.  
# Assumes this script is in the same directory as JSON conf files.
#
# Variables to create json configurations for
# air temp
# soil temp
# soil moisture
# wind speed - daytime only?
# humidity
# barometric pressure? 
# precip - daily cumulative
# solar - daily cumulative <-- did not implement
########################################
import json
import os
import re

dslist = {
    3077:'Air Temp Deg C Blue Oak Avg',
    3105:'Soil Temp Deg C 20 in Blue Oak Avg',
    3106:'Soil Moisture VWC Blue Oak Avg',
    3069:'Wind Speed m s Blue Oak Avg',
    3080:'Relative Humidity Per Blue Oak Avg',
    3081:'Barometric Pressure mbar Blue Oak Avg',
    #3061:'Total Solar Radiation W m2 Blue Oak Avg',
    #3082:'Precipitation mm Blue Oak',
    3355:'Air Temp Deg C 2 m Angelo Avg',
    3373:'Soil Temp Deg C 20 in Angelo Avg',
    3374:'Soil Moisture VWC Angelo Avg',
    3336:'Wind Speed m s Angelo Avg',
    3348:'Relative Humidity Per Angelo Avg',
    3349:'Barometric Pressure mbar Angelo Avg',
    #3329:'Total Solar Radiation W m2 Angelo Avg',
    3350:'Precipitation mm Angelo'
}

dsfile_prefix = 'Legacy_Datastream_'
fpath = '../examples/datastreams/'

for dsid,dsname in dslist.items():
    print(dsid,dsname)

    # acode = prefix to datastreamid for seasonal min=1,avg=2,max=3
    for acode,agg in {10000:'Minimum',20000:'Average',30000:'Maximum'}.items():
        with open(fpath+dsfile_prefix+str(dsid)+'.json') as json_data:
            d = json.load(json_data)
            # Define new parameters for JSON
            name = d['name']+' Seasonal '+agg
            dsids = acode+int(dsid) # dsids = datastream id seasonal
            seasonal_tag = 'ds_Function_Seasonal'
            aggregate_tag = 'ds_Aggregate_'+agg
            path = "/legacy/datavalues-seasonal"
            print(dsids,name,'Aggregate tag: '+aggregate_tag)
            
            # Assign parameters
            d['name'] = name
            d['derived_from_datastream_ids'] = [dsid]
            d['datapoints_config'][0]['params']['query']['datastream_id'] = dsids
            d['datapoints_config'][0]['path'] = path
            taglist = d['tags']
            for tag in taglist:
                if(re.match('ds_Aggregat',tag)):
                    #print('Found Aggregate! Removing.',tag)
                    taglist.remove(tag)
            taglist.append(aggregate_tag)
            taglist.append(seasonal_tag)
            taglist.sort()
            d['tags'] = taglist
            
            # Export JSON to file
            print(json.dumps(d,indent=2,sort_keys=True))
            dsfile = fpath+dsfile_prefix+'Seasonal_'+str(dsids)+'.json'
            with open(dsfile, 'w') as f:
                json.dump(d, f, indent=2,sort_keys=True)