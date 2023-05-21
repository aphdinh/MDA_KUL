'StandardScaler__LC_HUMIDITY',
'StandardScaler__LC_DWPTEMP',
'StandardScaler__LC_n',
'StandardScaler__LC_RAD',
'StandardScaler__LC_RAININ',
'StandardScaler__LC_DAILYRAIN',
'StandardScaler__LC_WINDDIR',
'StandardScaler__LC_WINDSPEED',
'StandardScaler__LC_RAD60',
'StandardScaler__LC_TEMP_QCL0',
'StandardScaler__LC_TEMP_QCL1',
'StandardScaler__LC_TEMP_QCL2',
'StandardScaler__LC_TEMP_QCL3'

Which we can match with API:

humidity - OK

dewpoint_c - dwptemp - "Just" Celcius in essence. 

We should drop _LC_N - ok

uv (divide by 40m²/W for per second, then multiply for exposure ) - used for RAD/RAD60 

precip_mm - i've looked other API and precip could be a sum of rain + snow, not necessarily just rain

totalprecip_mm (from day not hour json part), can only do that for t=0 because otherwise it is a forecast? E.g. could sum over the expected amount of rain till that point on the day

Need unscaled + there appears to be an issue with the way we handel it because the values make no sense. Can then use wind_degree

wind_kph*1000/3600 - windspeed?

Should take either this or RAD imo. Just the same thing

temp_c (Imo use this for all 3 simply take average/median of 4 here)

### So only humidity, wind speed, temp, dwptemp are good?
No, we use Humidity, RAD, RAININ, DAILYRAIN, WINDSPEED, RAD60 (which is RAD in essence), and all TEMPs 
