import csv
import sys

def is_number(s):
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

# TODO: turn categorical variables into things like feature vectors
def make_features(indices, datas):
    feature_sets = [list(set([row[ii] for row in datas])) for ii in indices]
    print 'Found in columns ', indices, ' the following values.\n', feature_sets
    print 'These columns will be replaced with an appended feature vector.'
    for row in datas:
        features = [row[ii] for ii in indices]
        for ii in indices:
            row.pop(ii)
        row.extend([0 if not attr==features[ii] else 1 
                      for ii in range(len(features))
                      for attr in feature_sets[ii]])
    return datas

# TODO: scale the data in my highest*1.5 method
# TODO: make sure to output anything done specially in the above (e.g. I have
#   x ferries and each one corresponds to a '1' in position y of the final 
#   feature vector)
# TODO: spit it out into a format usable by LibSVM
#   <classification label> <index1>:<value1> <index2>:<value2>. . . .\n
#   . . . .


print 'Usage: python2 libsvm_data_format.py <weather data> <departures> <arrivals>'
weather_read = csv.reader(open(sys.argv[1], 'rb'))
departure_read = csv.reader(open(sys.argv[2], 'rb'))
weather_list = [row for row in weather_read]
departure_list = [row for row in departure_read]
print 'Weather is ', weather_list.pop(0)
print 'Departure list is ', departure_list.pop(0)
# I have to remove the date from the end for departures and date from start for 
# weather
make_features(categoricals(departure_list[0])[:-1], departure_list)
print departure_list[0]
# arrival_read = csv.reader(open(sys.argv[3], 'rb'))
