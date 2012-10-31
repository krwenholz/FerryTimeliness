import csv
import sys

def is_number(s):
    """
        Is s a number?  True is 'tis so.  False otherwise.
    """
    try:
        float(s)
        return True
    except ValueError:
        return False

def categoricals(datas):
    """
        Finds indices in a list which are not numbers.
    """
    return [ii for ii in range(len(datas)) if not is_number(datas[ii])]

def make_features(indices, datas):
    """
        Given an iterable of indices, for every row in datas, we remove the
        offending index and append a bit-vector equivalent to the end of the
        row. This modifies datas.
    """
    indices.sort()
    feature_sets = [list(set([row[ii] for row in datas])) for ii in indices]
    print 'Found in columns ', indices, ' the following values.\n', feature_sets
    print 'These columns will be replaced with an appended feature vector.\n'
    for row in datas:
        features = [row[ii] for ii in indices]
        for ii in range(len(indices)):
            row.pop(indices[ii]-ii)
        row.extend([0 if not attr==features[ii] else 1 
                         for ii in range(len(features))
                         for attr in feature_sets[ii]])
    return datas

def scale_data(datas):
    """
        For every row in datas we replace the value stored there with 
        value/(max*1.5), where max is the maximum value
        the index takes on in datas.  This modifies datas.
    """
    maxima = [max([ele for ele in row]) for row in datas]
    #print 'Found in columns the following maxima.\n', maxima 
    print 'These columns will be replaced with value/(max*1.5).'
    for row in datas:
        for ii in range(len(row)):
            row[ii] = (row[ii]/(maxima[ii]*1.5))
    return new_data 

def join_data(d_ferry, d_weather):
    """
        This method takes in ferry data and joins appropriate weather data.
        That is, we first match on dates (drop the data if no matching dates
        exist) then by closest time.  Thus, we create rows of all departure 
        data followed by all the weather data, without any dates.
    """
    new_data = []
    weather_map = {}
    # We need a nice way to look up the dates
    for row in d_weather:
        if row[0] in weather_map:
            weather_map[row[0]].append(row[1:])
        else:
            weather_map.setdefault(row[0], [row[1:]])
    print weather_map
    dropped_data = 0
    for row in d_ferry:
        # FIXME: This comparison looks very broken since it never works
        if row[2] in weather_map:
            # Now we find the closest time and append weather data to ferry data
            # in the new_data.
            wdata = weather_map[row[0]]
            minidxval = (0,999999999)
            for ii in range(len(wdata)):
                if abs(wdata[ii][0]-row[0]) < minidxval[1]:
                    # We have a new minimum!
                    minidxval = (ii, wdata[ii][0]-row[0])
            join = row[:2]
            join.extend(row[3:])
            join.extend(wdata[ii])
            new_data.append(join)
        else:
            dropped_data += 1
    print 'We found that ', dropped_data, ' points lacked a matching weather date.'
    print 'These points have been removed.\n'
    return new_data

# TODO: make sure to output anything done specially in the above (e.g. I have
#   x ferries and each one corresponds to a '1' in position y of the final 
#   feature vector)
# TODO: spit it out into a format usable by LibSVM
#   <classification label> <index1>:<value1> <index2>:<value2>. . . .\n
#   . . . .

#####
# READ IN
#####
print 'Usage: python2 libsvm_data_format.py <weather data> <departures> <arrivals>'
weather_read = csv.reader(open(sys.argv[1], 'rb'))
departure_read = csv.reader(open(sys.argv[2], 'rb'))
weather_list = [row for row in weather_read]
departure_list = [row for row in departure_read]
# arrival_read = csv.reader(open(sys.argv[3], 'rb'))
print 'Weather is ', weather_list.pop(0)
print 'Departure list is ', departure_list.pop(0)

#####
# CATEGORIZE
#####
# I have to remove the date from the end for departures and date from start for 
# weather
categoricals_d = categoricals(departure_list[0])[:-1]
make_features(categoricals_d, departure_list)
print 'From make_features on departures\n', departure_list[0]

categoricals_w = categoricals(weather_list[0])[1:]
make_features(categoricals_w, weather_list)
print 'From make_features on weather \n', weather_list[0]

print '\n'
#####
# COMBINE WEATHER AND FERRIES
#####
joined_dep = join_data(departure_list, weather_list)
print 'From join_data on departures and weather\n', joined_dep[0]



#####
# SCALE
#####
#scale_data(departure_list)
#print departure_list[0]
#all([ii <= 1 or -1 <= ii for ii in row for row in departure_list])

#####
# OUTPUT
#####
# Append and write
