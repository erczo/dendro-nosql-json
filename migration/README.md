# Dendro Migration from Sensor Database

Create "Rosetta Stone" tables to pair Sensor Database ODM vocabularies with Dendro vocabularies.  
Python and JSON code and csv tables.  

## Two phases to this work.
Phase I. Provide the minimum required information to make Dendro work, not to bring over all information.  Some flaggin of important fields and tables will be useful.
Phase II. Permanent transition. What values are required to not lose existing information?
Phase III. This may be synonemous with phase II.  Create ODM 1.1 complianted tagging.  

## Phase I
Sensor Database Tables needed to make the migration:
stations, datastreams: these are the primary source tables

variables:  most of the datastream metadata is encoded in the variable
'''VariableID,VariableCode,VariableName,  -- descriptions of the variable
VariableUnitsName,  -- dt-units
SampleMedium,  -- ds-medium
DataType -- ds-aggregate
IsRegular -- 0 = attributes "manual measurement"
'''
variables ValueType:only tells you that whether it is derived. redundant. GeneralCategory seems redundant with medium, and not currently needed. Leave for phase III. TimeSupport,TimeUnits,NoDataValue,Speciation are not used.

sites:  Lat/long, elevation, datum.  Non-WGS84 datums will need to be converted to WGS84.  
'''Latitude,Longitude,LatLongDatumName,Elevation_m -- geo'''

units: the UnitsType field may be useful in out ds-units vocabulary.  Not sure. 
'''UnitsName,UnitsType,UnitsAbbreviation'''

