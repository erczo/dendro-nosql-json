# -*- coding: utf-8 -*-
########################################
# Migration Stations
# @author: collin bode
# @email: collin@berkeley.edu
# date: 2017-03-25
#
# Purpose: 
# Convert Legacy Sensor Database stations into 
# Dendro MongoDB compliant JSON files.  
# Note: this requires converting lat/long from NAD83 to WGS84
# and merging stations table with site table
# People are not dealt with yet.    
########################################
import json 

# go to git base directory outside repository
gitpath = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+os.sep
pwfile = gitpath+'odm.pw'
print(gitpath)

print('DONE!')