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