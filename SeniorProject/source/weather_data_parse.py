import csv

data_dir = '/home/krwenholz/Dropbox/Senior/Thesis/SeniorProject/Data/'
w_file = open(data_dir+'aggregate_weather.csv', 'w')
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
            #   direction), 30 (station pressure), 32 (pressure tendency), 
            #   34 (pressure change), 40 (hourly precip), 43 (altimeter)
            #nextRow = [row[ii]+',' for row in reader for ii in
            #            (1,2,4,6,10,14,18,22,24,26,30,32,34,40,43)]
            buildStr = []
            for row in reader:
                for ii in (1,2,4,6,10,14,18,22,24,26,30,32,34,40,42):
                    try:
                        buildStr.append(row[ii])
                    except Exception as e:
                        print e
                        print row
                        print yy
                        print mm
            buildStr.append('\n')
            w_file.write(''.join(buildStr))
w_file.close()



