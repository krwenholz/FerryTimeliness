import time
import csv
from datetime import datetime, date
import psycopg2


"""
    This file reads in data from the WSDOT Vessel Track data to store in a 
    PostgreSQL database.  

    A popular choice (used here) is to write the data into files with 
    vessel, departure, arrival, eta_departure/arrival, actual_departure/arrival,
    and date.  Times are stored as seconds from the start of the day (00:00).
    The date is actually stored as a date.
"""

def make_time(daytime):
    """
        Use just the time of day to make an integer value for the time.
    """
    return time.mktime(time.strptime('1970-01-01 '+daytime, 
                                     '%Y-%m-%d %H:%M'))-28800

def write_to_database(datas, data_file=None):
    """
        Takes in a data reader for the csv file and puts it all in a table.
    """
    FMT = '%m/%d/%Y %H:%M'
    FMT_DATE = '%m/%d/%Y'
    
    print 'Preparing to write data for ', datas.next()
    #conn = None
    #try:
    #    conn = psycopg2.connect("dbname='ferry_data' user='ferry_user' host='localhost' password='development2012'");
    #except Exception as e:
    #    print e
    #    print "I am unable to connect to the database"
        #return
    #cur = conn.cursor()

    # Several query strings are available
    #departure_query_string = "INSERT INTO departure_data(vessel, departing, arriving, scheduled_departure, actual_departure, date) VALUES(%s, %s, %s, %d, %d, %s);"
    #arrival_query_string = "INSERT INTO arrival_data(vessel, departing, arriving, scheduled_arrival, actual_arrival, date) VALUES(%s, %s, %s, %d, %d, %s);"
    # We will write in the vessel name, departure location, arrival location, 
    #   eta dep time, actual dep time, eta arrival time, actual arrival time
    csv_string = "%s, %s, %s, %d, %d, %d, %d, %s\n"

    failed_data = 0
    bad_time = 0
    write_attempts = 0
    data_file.write('vessel, departing, arriving, scheduled_departure, actual_departure, date\n')
    for row in datas:
        try:
            if (datetime.strptime(row[4], FMT) - datetime.strptime(row[7], FMT)).total_seconds() > 0:
                # Departure - Arrival > 0 is bad
                bad_time+=1
            try:
                # First, we tackle the departure data
                query_data = (row[0], row[1], row[2],
                              make_time(row[3].split(' ')[1]),
                              make_time(row[4].split(' ')[1]),
                              make_time(row[6].split(' ')[1]),
                              make_time(row[7].split(' ')[1]),
                              datetime.strptime(row[8], FMT_DATE).date())
                if not 'NULL' in query_data:
                    # We don't want to write NULLs into our final data
                    write_attempts += 1
                    data_file.write(csv_string % query_data)
                    #cur.execute(query_string, query_data)
            except:
                # Something went wrong in the data, probably a null
                failed_data+=1
            except:
                # Something went wrong, probably a null
                failed_data+=1
        except:
            # Probably a NULL in the time
            failed_data+=1
    print "Attempted to write ", write_attempts, " lines of data."
    print "Found ", bad_time, " lines of bad time data. (not written)"
    print "Found ", failed_data, " lines of bad data. (not written)"
    depart_file.close()
    arrival_file.close()
#    conn.commit()
#    cur.close()
#    conn.close()


##########
# Now make the nice looking calls to read data and such.
##########
fname = '/home/krwenholz/Dropbox/Senior/ThesisStorage/data_request_October2012.csv'
reader = csv.reader(open(fname, 'rb'))
data_dir = '../Data/'
data_file = open(data_dir+'ferry_data'+'.csv', 'w')
write_to_database(reader, data_file)


