import csv
from datetime import datetime
import time

"""
    Takes weather data from the state as input and makes a huge mess of a csv 
    table containing the 
    1 (Date), 2 (time), 4 (sky condition), 6 (visibility),
    10 (dry bulb fahrenheit), 14 (wet bulb fahrenheit), 18 (dew point 
    fahrenheit), 22 (relative humidity), 24 (wind speed), 26 (wind
    direction), 30 (station pressure), 43 (altimeter)
    The date is made to look nice and time is done as seconds after midnight.
"""

data_dir = '../Data/'
w_file = open(data_dir+'weather.csv', 'w')
w_file.write('date, time, sky_condition, visibility, d-bulb_F, w-bulb_F, dew_point_F, rel_humidity, wind_speed, wind_dir, station_pressure, altimeter\n')
for yy in ('2010','2011','2012'):
    for mm in ('01','02','03','04','05','06','07','08','09','10','11','12'):
        if not (yy=='2011' or yy=='2010' and mm in ('12', '11', '10', '09')
            or (yy=='2012' and mm not in ('12','11','10'))):
            # We don't have data for these months
            pass
        else:
            deep_dir = 'WeatherData/TacomaNarrows-NOAA-NoHDR/'
            reader = csv.reader(open(data_dir+deep_dir+mm+'_'+yy+'.csv', 'rb'))
            # Columns I want 1 (Date), 2 (time), 4 (sky condition), 6 (visibility),
            #   10 (dry bulb fahrenheit), 14 (wet bulb fahrenheit), 18 (dew point 
            #   fahrenheit), 22 (relative humidity), 24 (wind speed), 26 (wind
            #   direction), 30 (station pressure), 43 (altimeter)
            buildStr = []
            for row in reader:
                buildStr.append(str(datetime.strptime(row[1].strip(), "%Y%m%d").date()))
                buildStr.append(',')
                buildStr.append(str(time.mktime(time.strptime('1970-01-01 '+row[2].strip(), '%Y-%m-%d %H%M'))-28800))
                for ii in (4,6,10,14,18,22,24,26,30,42):
                   if not row[ii] in (' ', '', '  '):
                            # we don't want to insert empty data
                            buildStr.append(', ')
                            buildStr.append(row[ii].strip())
                buildStr.append('\n')
            w_file.write(''.join(buildStr))
w_file.close()



