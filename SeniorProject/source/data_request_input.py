import time
import csv

import psycopg2


"""
    This file reads in data from the WSDOT Vessel Track data to store in a 
    PostgreSQL database.
"""

def write_to_database(datas):
    """
        Takes in the formatted html data for ferries and writes it to the 
        database sitting in 409.
    """
    conn = None
    try:
        conn = psycopg2.connect("dbname='ferry_data' user='ferry_user' host='localhost' password='development2012'");
    except Exception as e:
        print e
        print "I am unable to connect to the database"
        return
    cur = conn.cursor()
    for dd in datas:
        # TODO: adjust the insert to work with another column
        query_string = "INSERT INTO (vessel, knots, departing, arriving, scheduled_departure, actual_departure, estimated_arrival, route, date, flags) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, 'now', %s);"
        query_data = (dd['vessel'], dd['knots'], dd['departing'],
                                   dd['arriving'], dd['scheduled_departure'], 
                                   dd['actual_departure'], dd['est_arrival'],
                                   dd['route'], dd['flags'],)
        print query_string % query_data
        cur.execute(query_string, query_data)

    conn.commit()
    cur.close()
    conn.close()


##########
# Now make the nice looking calls to read data and such.
##########
fname = '/home/krwenholz/Dropbox/Senior/ThesisStorage/data_request_October2012.csv'
reader = csv.reader(open(fname, 'rb'))
write_to_database(reader)


