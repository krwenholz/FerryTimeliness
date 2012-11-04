import csv

def time_buckets(dataf='../Data/ferry_data.csv', times=[300,600]):
    """
        Tests how many boat trips fit into the different time intervals.
    """
    data = csv.reader(open(dataf, 'r'))
    counts = [0 for ii in range(len(times)+1)]
    print data.next()
    for row in data:
        counts[len(filter(lambda x: x<int(row[4])-int(row[3]), times))]+=1
    # This is now a very "safe" and "sure" check
    #for row in data:
    #    rowDiff = int(row[4])-int(row[3])
    #    for ii in range(len(counts)):
    #        if ii == len(times):
    #            counts[ii] += 1
    #            break
    #        if rowDiff < times[ii]:
    #            counts[ii] += 1
    #            break
    return counts

