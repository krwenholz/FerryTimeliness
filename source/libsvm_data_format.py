import csv
import sys

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# TODO: check the categorical variables to see what categories I need.
def categoricals(list1):
    return [ii for ii in range(len(list1)) if not is_number(list1[ii])]

# TODO: turn categorical variables into things like feature vectors
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
print weather_list.pop(0)
print departure_list.pop(0)
print categoricals(weather_list[1])
print categoricals(departure_list[1])
# arrival_read = csv.reader(open(sys.argv[3], 'rb'))
