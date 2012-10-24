import time
import csv
from datetime import datetime
import psycopg2


"""
    This file reads in data from the WSDOT Vessel Track data to store in a 
    PostgreSQL database.
"""

def make_time(daytime):
    """
        Use just the time of day to make an integer value for the time.
    """
    return time.mktime(time.strptime('1970-01-01 '+daytime, 
                                     '%Y-%m-%d %H:%M'))-28800

def write_to_database(datas):
    """
        Takes in a data reader for the csv file and puts it all in a table.
    """
    # TODO: I need to just pull out the time instead of date (or else it relies
    #   on date past 2000 rather than time of day.
    FMT = '%m/%d/%Y %H:%M'
    FMT_DATE = '%m/%d/%Y'
    
    print 'Preparing to write data for ', datas.next()
    conn = None
    try:
        conn = psycopg2.connect("dbname='ferry_data' user='ferry_user' host='localhost' password='development2012'");
    except Exception as e:
        print e
        print "I am unable to connect to the database"
        #return
    #cur = conn.cursor()
    query_string = "INSERT INTO (vessel, departing, arriving, scheduled_departure, actual_departure, route_name, initial_eta, actual_arrival, date) VALUES(%s, %s, %s, %d, %d, %s, %d, %d, %s);"
    for row in datas:
        # times are in (3, 4, 6, 7)
        try:
            if (datetime.strptime(row[4], FMT) - datetime.strptime(row[7], FMT)).total_seconds() > 0:
                # departure - arrival > 0 checks for a proper time entry
                print 'Found bad data with ', row
            else:
                print datetime.strptime(reader.next()[8], FMT_DATE).date()
                query_data = (
                cur.execute(query_string, query_data)
#
#    conn.commit()
#    cur.close()
#    conn.close()


##########
# Now make the nice looking calls to read data and such.
##########
fname = '/home/krwenholz/Dropbox/Senior/ThesisStorage/data_request_October2012.csv'
reader = csv.reader(open(fname, 'rb'))
write_to_database(reader)


