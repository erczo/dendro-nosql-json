DATAVALUES SEASONAL AGGREGATES

-- Temporary table for storing function aggregates for Dendro Dashboard
CREATE TABLE datavalues_seasonal (
  ValueID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  DataValue double DEFAULT NULL,
  ValueAccuracy double DEFAULT NULL,
  LocalDateTime datetime NOT NULL,
  UTCOffset tinyint(4) NOT NULL,
  QualifierID mediumint(8) unsigned NOT NULL,
  DerivedFromID smallint(5) unsigned DEFAULT NULL,
  QualityControlLevelCode char(4) NOT NULL,
  DatastreamID smallint(5) unsigned NOT NULL,
  PRIMARY KEY (ValueID),
  INDEX time_dsid (LocalDateTime,DatastreamID)
);

Rules for aggregation:  each of the aggregations will be its own datastream.
DerivedFromID: DSID of original datastream
DatastreamID: 
	990000 + DSID: Maximum
	980000 + DSID: Average
	970000 + DSID: Minimum
UTCOffset = -8
QualifierID = 2
QualityControlLevelCode = 2

-- Get the oldest date for each datastream 
SELECT min(year(LocalDateTime))   
FROM odm.datavalues_UCNRS 
WHERE DatastreamID = 3077;

-- Create Daily Min & Max Values
CREATE TEMPORARY TABLE ztemp_date     
SELECT date(localdatetime) as ldate, 
    count(*) as count_hour, 
    min(DataValue) as min, 
    avg(DataValue) as avg,   
    max(DataValue) as max  
FROM odm.datavalues_UCNRS 
WHERE datastreamid = 3077 and LocalDateTime < '2012-01-01 00:00:00' 
GROUP BY date(localdatetime) 
ORDER BY date(localdatetime);

-- This will create a temporary table with dates, not timestamps.   Next, average all years by month.  

-- Average all years by month
CREATE TEMPORARY TABLE ztemp_month     
SELECT month(ldate) as month, 
	count(*) as count_month, 
	sum(count_hour) as count_hour, 
  avg(airtemp_min) as min_avg, 
  avg(airtemp_avg) as avg_avg, 
  avg(airtemp_max) as max_avg   
FROM ztemp_date  
GROUP BY month(ldate);

-- The result with be 12 rows with the average low, average average, and average high air temp for each month for all years.   This code doesn't allow for a month to month iteration of the process, so it doesn't provide you with a nice datastream.  

-- INSERT the results into the datavalues_seasonal table
INSERT into datavalues_seasonal Values (
	DataValue,
	ValueAccuracy,
	SeasonDateTime,
	UTCOffset,
	QualifierID,
	DerivedFromID,
	QualityControlLevelCode,
	DatastreamID
);