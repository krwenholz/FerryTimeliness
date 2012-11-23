import csv
import sys
import random


def is_number(s):
    """
        Is s a number?  True if 'tis so.  False otherwise.
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
            row.pop(indices[ii] - ii)
        row.extend([0 if not attr == features[ii] else 1
                         for ii in range(len(features))
                         for attr in feature_sets[ii]])


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
    dropped_data = 0
    for row in d_ferry:
        # TODO: It may be possible to see if arrival is less than dep or something
        #   with the estimates to then use the correct weather day
        wdata = weather_map.get(row[4].strip())
        if wdata:
            # Now we find the closest time and append weather data to ferry data
            # in the new_data.
            minidxval = (0, 999999999)
            for ii in range(len(wdata)):
                diff = abs(float(wdata[ii][0]) - float(row[0]))
                if diff < minidxval[1]:
                    # We have a new minimum!
                    minidxval = (ii, diff)
            # XXX: Easy place to adjust the output columns
            row_join = row[:4]  # Remove the date
            row_join.extend(row[5:])
            row_join.extend(wdata[minidxval[0]])
            new_data.append(row_join)
        else:
            dropped_data += 1
    print 'We found that ', dropped_data, ' points lacked a matching weather date.'
    print 'These points have been removed.\n'
    return new_data


def label_data(datas, col1, col2, isMulti):
    """
        Labels the data according to the difference between col2 and col1.
        The labels are for multi-class only if isMulti is True.
    """
    if isMulti:
        label_groups = [180, 300, 600]
        for row in datas:
            row.insert(0, len(filter(lambda x: x < int(row[col2]) - int(row[col1]),
                                     label_groups)))
    else:
        for row in datas:
            row.insert(0, 1 if int(row[col2]) - int(row[col1]) < 180 else - 1)


def scale_data(datas):
    """
        For every row in datas we replace the value stored there with
        value/(max*1.5), where max is the maximum value
        the index takes on in datas.  This modifies datas.  The only column
        not changed is the first.
    """
    maxima = [float(ele) for ele in datas[0]]
    for row in datas:
        for ii in range(len(row)):
            maxima[ii] = max(maxima[ii], float(row[ii]))
    print 'The maxima are ', maxima
    print 'The columns will be replaced with value/max.'
    for row in datas:
        for ii in range(1, len(row)):
            row[ii] = repr(float(row[ii]) / float(maxima[ii]))


def SVMable(datas, outfile, test_outfile):
    """
        Formats datas a list of lists, where the embedded lists are instances.
        The format written to outfile is
        <label> <index1>:<value1> <index2>:<value2>...
        <label> is the SVM class label.
        <indexI> starts at 1.
        <valueI> is the value associated with the index.
    """
    outStr = ['%d']
    outStr.extend([' ' + str(ii) + ':%s' for ii in range(1, len(datas[0]))])
    outStr.append('\n')
    outStr = ''.join(outStr)
    for row in datas:
        if True:
            outfile.write(outStr % tuple(row))


#####
# READ IN
#####
print 'Usage: python2 libsvm_data_format.py <weather data> <ferry_data>'
print 'Reading data in. . . .'
weather_read = csv.reader(open(sys.argv[1], 'rb'))
ferry_read = csv.reader(open(sys.argv[2], 'rb'))
weather_list = [row for row in weather_read]
ferry_list = [row for row in ferry_read]
# arrival_read = csv.reader(open(sys.argv[3], 'rb'))
whdr = weather_list.pop(0)
fhdr = ferry_list.pop(0)
print 'Weather is ', whdr
print '\n'
print 'Ferry list is ', fhdr
print '\n'

#####
# CATEGORIZE
#####
# I have to remove the date from the end for departures and date from start for
# weather
print 'Making feature vectors of categorical variables. . . .'
categoricals_f = categoricals(ferry_list[0])[:-1]
make_features(categoricals_f, ferry_list)

categoricals_w = categoricals(weather_list[0])[1:]
make_features(categoricals_w, weather_list)

#####
# COMBINE WEATHER AND FERRIES
#####
print 'Combining data tables. . . .'
join = join_data(ferry_list, weather_list)
print 'From join_data on ferries and weather\n', join[0]

print 'Prepending with class labels. . . .'
# Rows 2 and 3 correspond to eta and actual arrival, respectively
label_data(join, 2, 3, False)
print 'Labels now look like\n', join[0]
# Now I filter out the actual arrival since that's what I'll be predicting
for ii in range(len(join)):
    new_row = []
    new_row.extend(join[ii][:3])
    new_row.extend(join[ii][4:])
    join[ii] = new_row


#####
# OUTPUT
#####
print 'Outputting final data. . . .'
outfile = open('../Data/svm_points_data.txt', 'w')
test_outfile = open('../Data/svm_points_test.txt', 'w')
SVMable(join, outfile, test_outfile)

print 'Looks like it was a success!'
