SELECT 
	ds.datastreamid,
	ds.datastreamname,
	ds.stationname,
	ds.variableid,
	v.variableid,
	ds.variablecode,
	v.variablecode  
FROM datastreams as ds, variables as v 
WHERE ds.variableid = v.variableid 
AND mc_name = 'UCNRS';

-- variables table
| Field               | Type                | Null | Key | Default | Extra          |
+---------------------+---------------------+------+-----+---------+----------------+
| VariableID          | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
| VariableCode        | varchar(50)         | NO   | UNI | NULL    |                |
| VariableName        | varchar(255)        | NO   |     | NULL    |                |
| VariableDescription | text                | YES  |     | NULL    |                |
| Speciation          | varchar(50)         | NO   |     | NULL    |                |
| VariableUnitsName   | varchar(255)        | NO   |     | NULL    |                |
| SampleMedium        | varchar(50)         | NO   |     | NULL    |                |
| ValueType           | varchar(50)         | NO   |     | NULL    |                |
| IsRegular           | tinyint(4)          | NO   |     | NULL    |                |
| TimeSupport         | int(11)             | NO   |     | NULL    |                |
| TimeUnits           | varchar(255)        | YES  |     | NULL    |                |
| DataType            | varchar(50)         | NO   |     | NULL    |                |
| GeneralCategory     | varchar(50)         | NO   |     | NULL    |                |
| NoDataValue         | double              | YES  |     | NULL    |                |


SELECT 
VariableID,
VariableCode,
VariableName,
VariableUnitsName,
SampleMedium,
ValueType,
DataType 
FROM variables; 
131 rows 

+------------+-----------------------------------+-----------------------------------+---------------------------------------------------+---------------+-------------------+------------------------+
| VariableID | VariableCode                      | VariableName                      | VariableUnitsName                                 | SampleMedium  | ValueType         | DataType               |
|         35 | Rainfall mm                       | Precipitation                     | millimeter                                        | Precipitation | Field Observation | Continuous             |
|          2 | Water Temp C                      | Temperature                       | degree celcius                                    | Surface Water | Field Observation | Continuous             |
|          3 | Air Temp C                        | Temperature                       | degree celcius                                    | Air           | Field Observation | Continuous             |
|          4 | PAR Instant                       | Radiation, incoming PAR           | micromoles of photons per square meter per second | Other         | Field Observation | Continuous             |
|          5 | PAR umole                         | Radiation, incoming PAR           | micromoles of photons per square meter per second | Other         | Field Observation | Average                |
|          6 | Rainfall Cumulative mm            | Precipitation                     | millimeter                                        | Precipitation | Field Observation | Cumulative             |
|          7 | Wind Speed Avg KPH                | Wind speed                        | kilometers per hour                               | Air           | Field Observation | Average                |
|          8 | Wind Speed Max KPH                | Wind speed                        | kilometers per hour                               | Air           | Field Observation | Maximum                |
|          9 | Wind Direction Degrees            | Wind direction                    | degree                                            | Air           | Field Observation | Continuous             |
|         10 | Battery Voltage                   | Battery voltage                   | volts                                             | Other         | Field Observation | Continuous             |
|         13 | Rel Humidity Perc                 | Relative humidity                 | percent                                           | Air           | Field Observation | Continuous             |
|         14 | Solar Radiation Total kW/m^2      | Radiation, total shortwave        | kilowatts per square meter                        | Not Relevant  | Field Observation | Continuous             |
|         15 | Barometric Pressure mb            | Barometric pressure               | millibar                                          | Air           | Field Observation | Average                |
|         16 | Wind Speed Avg MS                 | Wind speed                        | meters per second                                 | Air           | Field Observation | Average                |
|         17 | Gage Height meters                | Gage height                       | meter                                             | Surface Water | Field Observation | Continuous             |
|         18 | Turbidity NTU                     | Turbidity                         | nephelometric turbidity units                     | Surface Water | Field Observation | Continuous             |
|         20 | Logger Temp c                     | Temperature                       | degree celcius                                    | Air           | Field Observation | Continuous             |
|         21 | Solar Radiation Total MJ/m^2      | Radiation, total shortwave        | megajoules per square meter                       | Not Relevant  | Field Observation | Continuous             |
|         22 | Snow Depth Meters                 | Snow depth                        | meter                                             | Snow          | Field Observation | Cumulative             |
|         23 | Water Pressure mV                 | Water pressure                    | millivolts                                        | Ground Water  | Field Observation | Continuous             |
|         24 | Rainfall Intensity mm/h           | Precipitation                     | millimeters per hour                              | Precipitation | Field Observation | Maximum                |
|         25 | Hail Cumulative mm                | Precipitation                     | millimeter                                        | Precipitation | Field Observation | Cumulative             |
|         26 | Hail Intensity mm/h               | Precipitation                     | millimeters per hour                              | Precipitation | Field Observation | Maximum                |
|         27 | Dielectric                        | TDR waveform relative length      | square root of dielectric                         | Ground Water  | Field Observation | Continuous             |
|         28 | Wind Direction Standard Deviation | Wind direction                    | degree                                            | Air           | Derived Value     | StandardDeviation      |
|         29 | Snow-water equivalent inches      | Snow Water Equivalent             | inch of water                                     | Snow          | Derived Value     | Average                |
|         30 | Soil Temperature C                | Temperature                       | degree celcius                                    | Soil          | Derived Value     | Average                |
|         31 | Soil Conductivity ds              | Specific conductance              | decisiemens per centimeter                        | Not Relevant  | Derived Value     | Average                |
|         32 | Soil Moisture mV                  | Volumetric water content          | millivolts                                        | Ground Water  | Unknown           | Average                |
|         33 | Resistance                        | Resistance                        | kilo-ohms                                         | Ground Water  | Unknown           | Unknown                |
|         34 | Evapotranspiration                | Evapotranspiration                | millimeter                                        | Air           | Derived Value     | Average                |
|         36 | Soil Temperature Volts            | Temperature                       | volts                                             | Soil          | Field Observation | Average                |
|         37 | Soil Moisture Volts               | Volumetric water content          | volts                                             | Ground Water  | Field Observation | Average                |
|         38 | Par Instant lux                   | Radiation, incoming PAR           | lux                                               | Other         | Field Observation | Continuous             |
|         39 | Solar Radiation Total lux         | Radiation, total shortwave        | lux                                               | Not Relevant  | Field Observation | Continuous             |
|         40 | Logger Voltage V                  | Battery voltage                   | volts                                             | Other         | Field Observation | Continuous             |
|         46 | Solar Radiation Total W/m^2       | Radiation, incoming shortwave     | watts per square meter                            | Not Relevant  | Field Observation | Continuous             |
|         42 | Solar Panel Voltage V             | Battery voltage                   | volts                                             | Not Relevant  | Field Observation | Continuous             |
|         43 | Raw Sensor Response               | Bulk electrical conductivity      |                                                   | Not Relevant  | Field Observation | Continuous             |
|         44 | Radio Signal Strength dB          | Signal strength                   | decibel                                           | Not Relevant  | Field Observation | Continuous             |
|         45 | Electrical Current mA             | Electrical Current                | milliamp                                          | Not Relevant  | Field Observation | Continuous             |
|         47 | Solar Radiation Total kJ/m^2      | Radiation, incoming shortwave     | kiloJoules per square meter                       | Not Relevant  | Field Observation | Continuous             |
|         48 | Wind Speed Max MS                 | Wind speed                        | meters per second                                 | Air           | Field Observation | Maximum                |
|         49 | Snow Depth Signal Quality         | Signal strength                   | dimensionless                                     | Snow          | Field Observation | Continuous             |
|         50 | Sap Flow cm/hr                    | Velocity                          | centimeters per hour                              | Other         | Field Observation | Continuous             |
|         51 | Snow Depth cm                     | Snow depth                        | centimeter                                        | Snow          | Field Observation | Average                |
|         52 | Rainfall Cumulative cm            | Precipitation                     | centimeter of water                               | Precipitation | Sample            | Cumulative             |
|         53 | Rainfall Cumulative in.           | Precipitation                     | inch of water                                     | Precipitation | Sample            | Cumulative             |
|         54 | Snow Depth mv                     | Snow depth                        | millivolts                                        | Snow          | Field Observation | Average                |
|         55 | Sap Flow mV                       | Velocity                          | millivolts                                        | Other         | Field Observation | Average                |
|         56 | Rainfall Raw Hz                   | Precipitation                     | hertz                                             | Precipitation | Field Observation | Cumulative             |
|         57 | Rainfall Raw Std Dev Hz           | Precipitation                     | hertz                                             | Precipitation | Field Observation | StandardDeviation      |
|         58 | Soil Conductivity Avg S/m         | Specific conductance              | siemens per meter                                 | Soil          | Field Observation | Average                |
|         59 | Soil Moisture Pct Avg             | Volumetric water content          | percent by volume                                 | Not Relevant  | Field Observation | Average                |
|         60 | Solar Radiation Clear-Sky MJ/m^2  | Radiation, incoming shortwave     | megajoules per square meter                       | Not Relevant  | Derived Value     | Continuous             |
|         61 | Solar Radiation Avg W/m^2         | Radiation, incoming shortwave     | watts per square meter                            | Not Relevant  | Field Observation | Average                |
|         62 | Water Depth m                     | Water depth                       | meter                                             | Ground Water  | Field Observation | Cumulative             |
|         63 | Water Level Manual m              | Water level                       | meter                                             | Ground Water  | Field Observation | Sporadic               |
|         64 | Water Level m                     | Water level                       | meter                                             | Ground Water  | Field Observation | Continuous             |
|         65 | Water Pressure psi                | Water pressure                    | pound force per square inch                       | Ground Water  | Field Observation | Continuous             |
|         66 | Rainfall inches                   | Precipitation                     | inch of water                                     | Precipitation | Field Observation | Continuous             |
|         67 | Snow Depth in.                    | Snow depth                        | inch                                              | Snow          | Field Observation | Average                |
|         68 | Discharge                         | Discharge                         | cubic meters per second                           | Surface Water | Derived Value     | Continuous             |
|         69 | Soil Moisture Pct                 | Volumetric water content          | percent by volume                                 | Soil          | Derived Value     | Continuous             |
|         70 | Electrical Conductivity dS/m      | Bulk electrical conductivity      | decisiemens per meter                             | Soil          | Derived Value     | Continuous             |
|         71 | Solar Radiation Net W/m^2         | Radiation, net                    | watts per square meter                            | Not Relevant  | Field Observation | Average                |
|         72 | CO2 Concentration ppm/10          | Carbon dioxide, transducer signal | parts per million                                 | Ground Water  | Sample            | Constant Over Interval |
|        181 | Wind Speed Avg MPH                | Wind speed                        | miles per hour                                    | Air           | Field Observation | Average                |
|        182 | Wind Speed Max MPH                | Wind speed                        | miles per hour                                    | Not Relevant  | Field Observation | Maximum                |
|        183 | Wind Speed Min MPH                | Wind speed                        | miles per hour                                    | Air           | Field Observation | Average                |
|        184 | Wind Speed Stdev MPH              | Wind speed                        | miles per hour                                    | Air           | Field Observation | StandardDeviation      |
|        185 | Solar Voltage                     | Battery voltage                   | volts                                             | Not Relevant  | Field Observation | Continuous             |
|        186 | External Voltage                  | Battery voltage                   | volts                                             | Not Relevant  | Field Observation | Continuous             |
|        190 | Soil Moisture cbar                | Volumetric water content          | centibar                                          | Ground Water  | Field Observation | Continuous             |
|        189 | Unknown                           | Unknown                           |                                                   | Not Relevant  | Unknown           | Unknown                |
|        191 | Leaf Wetness Minutes              | Leaf wetness                      | minute                                            | Not Relevant  | Unknown           | Unknown                |
|        192 | Water Pressure mbar               | Water pressure                    | millibar                                          | Ground Water  | Field Observation | Continuous             |
|        193 | Rock Moisture Percent             | Volumetric water content          | percent by volume                                 | Ground Water  | Field Observation | Continuous             |
|        194 | Rock Temperature C                | Temperature                       | degree celcius                                    | Rock          | Field Observation | Continuous             |
|        195 | Leaf Wetness Excitation mV        | Leaf wetness                      | millivolts                                        | Surface Water | Field Observation | Continuous             |
|        196 | Leaf Wetness cnts mV              | Leaf wetness                      | millivolts                                        | Surface Water | Field Observation | Continuous             |
|        197 | Solar Radiation Max W/m^2         | Radiation, incoming shortwave     | watts per square meter                            | Not Relevant  | Unknown           | Maximum                |
|        198 | Solar Radiation Min W/m^2         | Radiation, incoming shortwave     | watts per square meter                            | Not Relevant  | Unknown           | Minimum                |
|        199 | Solar Radiation Std W/m^2         | Radiation, incoming shortwave     | watts per square meter                            | Not Relevant  | Derived Value     | StandardDeviation      |
|        200 | Wind Vector Magnitude MS          | Wind speed                        | meters per second                                 | Air           | Derived Value     | Unknown                |
|        201 | Wind Gust MS                      | Wind speed                        | meters per second                                 | Air           | Field Observation | Unknown                |
|        202 | Wind Speed Stdev MS               | Wind speed                        | meters per second                                 | Air           | Field Observation | StandardDeviation      |
|        203 | Wind Speed Min MS                 | Wind speed                        | meters per second                                 | Air           | Field Observation | Minimum                |
|        204 | Air Temp C Min                    | Temperature                       | degree celcius                                    | Air           | Field Observation | Minimum                |
|        205 | Air Temp C Max                    | Temperature                       | degree celcius                                    | Air           | Field Observation | Maximum                |
|        206 | Air Temp C Avg                    | Temperature                       | degree celcius                                    | Air           | Field Observation | Average                |
|        207 | Rel Humidity Per Max              | Relative humidity                 | percent                                           | Air           | Field Observation | Maximum                |
|        208 | Rel Humidity Per Min              | Relative humidity                 | percent                                           | Air           | Field Observation | Minimum                |
|        209 | Rel Humidity Per Avg              | Relative humidity                 | percent                                           | Air           | Field Observation | Average                |
|        210 | Derived Cumulative Precipitation  | Precipitation                     | millimeter                                        | Precipitation | Derived Value     | Cumulative             |
|        211 | Rain Gauge Temp C                 | Temperature                       | degree celcius                                    | Not Relevant  | Field Observation | Average                |
|        212 | Air Temp Delta C Max              | Temperature                       | degree celcius                                    | Air           | Derived Value     | Maximum                |
|        213 | Air Temp Delta C Min              | Temperature                       | degree celcius                                    | Air           | Derived Value     | Minimum                |
|        214 | Air Temp Delta C Avg              | Temperature                       | degree celcius                                    | Air           | Derived Value     | Average                |
|        215 | Soil Temp C Max                   | Temperature                       | degree celcius                                    | Soil          | Field Observation | Maximum                |
|        216 | Soil Temp C Min                   | Temperature                       | degree celcius                                    | Soil          | Field Observation | Minimum                |
|        217 | Soil Temp C Avg                   | Temperature                       | degree celcius                                    | Soil          | Field Observation | Average                |
|        218 | Soil Temp C 4 in MAX              | Temperature                       | degree celcius                                    | Soil          | Field Observation | Maximum                |
|        219 | Soil Temp C 4 in MIN              | Temperature                       | degree celcius                                    | Soil          | Field Observation | Minimum                |
|        220 | Soil Temp C 4 in AVG              | Temperature                       | degree celcius                                    | Soil          | Field Observation | Average                |
|        221 | Soil Temp C 8 in AVG              | Temperature                       | degree celcius                                    | Soil          | Field Observation | Average                |
|        222 | Soil Temp C 8 in MIN              | Temperature                       | degree celcius                                    | Soil          | Field Observation | Minimum                |
|        223 | Soil Temp C 8 in MAX              | Temperature                       | degree celcius                                    | Soil          | Field Observation | Maximum                |
|        224 | Soil Temp C 20 in MAX             | Temperature                       | degree celcius                                    | Soil          | Field Observation | Maximum                |
|        225 | Soil Temp C 20 in MIN             | Temperature                       | degree celcius                                    | Soil          | Field Observation | Minimum                |
|        226 | Soil Temp C 20 in AVG             | Temperature                       | degree celcius                                    | Soil          | Field Observation | Average                |
|        227 | Battery Voltage Max               | Battery voltage                   | volts                                             | Not Relevant  | Field Observation | Maximum                |
|        228 | Battery Voltage Min               | Battery voltage                   | volts                                             | Not Relevant  | Field Observation | Minimum                |
|        229 | Battery Voltage Avg               | Battery voltage                   | volts                                             | Not Relevant  | Field Observation | Average                |
|        230 | Fuel Moisture Per Avg             | Unknown                           | percent                                           | Unknown       | Field Observation | Average                |
|        231 | Wind Vector Speed m s             | Wind speed                        | meters per second                                 | Air           | Field Observation | Unknown                |
|        232 | Snow Temp Deg C Avg               | Temperature                       | degree celcius                                    | Snow          | Field Observation | Average                |
|        233 | Snow Depth mm Max                 | Snow depth                        | millimeter                                        | Snow          | Field Observation | Maximum                |
|        234 | Snow Temp Deg C Max               | Temperature                       | degree celcius                                    | Snow          | Field Observation | Maximum                |
|        235 | Snow Depth mm Min                 | Snow depth                        | millimeter                                        | Snow          | Field Observation | Minimum                |
|        236 | Snow Temp Deg C Min               | Temperature                       | degree celcius                                    | Snow          | Field Observation | Minimum                |
|        237 | Snow Depth mm                     | Snow depth                        | millimeter                                        | Snow          | Field Observation | Unknown                |
|        238 | GEONOR GAUGE FREQ hz              | Unknown                           | hertz                                             | Not Relevant  | Field Observation | Unknown                |
|        239 | GEONOR PRECIP cm                  | Precipitation                     | centimeter                                        | Precipitation | Field Observation | Unknown                |
|        240 | Raingauge mm                      | Precipitation                     | millimeter                                        | Precipitation | Field Observation | Unknown                |
|        241 | Enclosure RH Per                  | Relative humidity                 | percent                                           | Unknown       | Field Observation | Unknown                |
|        242 | Leaf Wetness Percent              | Leaf wetness                      | percent                                           | Not Relevant  | Field Observation | Unknown                |
|        243 | Sky Quality Avg                   | Unknown                           |                                                   | Not Relevant  | Field Observation | Average                |
|        244 | Sky Quality Max                   | Unknown                           |                                                   | Not Relevant  | Field Observation | Average                |
|        245 | Sky Quality Min                   | Unknown                           |                                                   | Not Relevant  | Field Observation | Minimum                |
|        246 | Sky Quality                       | Unknown                           |                                                   | Not Relevant  | Field Observation | Unknown                |
