from BeautifulSoup import BeautifulSoup
from time import sleep
from selenium import webdriver
import time

import psycopg2


"""
    This file reads in data from the WSDOT Vessel Track site to store in a MySQL
    database.
"""

def get_nice_html(url, elem_id):
    """
        Grab raw html from a url (using Selenium to bypass Javascript pains),
        and return a cleaned up version using BeautifulSoup.
    """

    browser = webdriver.Firefox() # Get local session of firefox
    browser.get(url) # Load page
    time.sleep(0.2) # Let the page load, will be added to the API
    element = browser.find_element_by_id(elem_id) # Find the query box
    html_raw = element.get_attribute('innerHTML')
    browser.close()

    html_soup = BeautifulSoup(''.join(html_raw))

    return html_soup

def format_table(html_soup,
                 col_names,
                 vessels,
                 row_type='div', 
                 row_attrs={'class': 'vslLstRow INSvslLstRow'},
                 col_type='div',
                 col_attrs=None):
    """
        Uses the BeautifulSoup library to find a table with the given parameters
        and then put it in a nice Python style dictionary.
    """
    data = []
    table = html_soup
    rows = table.findAll(row_type, attrs=row_attrs)
    for ii in range(0,len(rows)):
        nextVessel = {}
        cols = rows[ii].findAll(col_type, attrs=col_attrs)
        for jj in range(0,len(col_names)):
            if col_names[jj]=='vessel':
                for vv in vessels:
                    if vv in str(cols[jj]):
                        nextVessel[col_names[jj]]=vv
            else:
                nextVessel[col_names[jj]]=cols[jj].find(text=True)
        if len(nextVessel)==len(col_names):
            data.append(nextVessel)
    for dd in data:
        for kk in dd.keys():
            if kk in ['est_arrival','actual_departure','scheduled_departure']:
                try:
                    time.strptime(dd[kk],'%H:%M')
                except:
                    dd[kk]='00:00'
    print data
    return data

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
        query_string = "INSERT INTO site_data (vessel, knots, departing, arriving, scheduled_departure, actual_departure, estimated_arrival, route, date) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, 'now');"
        query_data = (dd['vessel'], dd['knots'], dd['departing'],
                                   dd['arriving'], dd['scheduled_departure'], 
                                   dd['actual_departure'], dd['est_arrival'],
                                   dd['route'],)
        print query_string % query_data
        cur.execute(query_string, query_data)

    conn.commit()
    cur.close()
    conn.close()


##########
# Now make the nice looking calls to read data and such.
##########

table_heading = ['date', 
                 'pos', 
                 'route', 
                 'est_arrival', 
                 'actual_departure', 
                 'scheduled_departure', 
                 'arriving', 
                 'departing', 
                 'icon',
                 'knots',
                 'vessel']
vessel_names = ['Chelan', 
                'Yakima', 
                'Hyak', 
                'Evergreen State', 
                'Elwha', 
                'Kennewick', 
                'Salish', 
                'Cathlamet', 
                'Kittitas', 
                'Puyallup', 
                'Spokane',
                'Tacoma',
                'Wenatchee',
                'Kitsap',
                'Kaleetan',
                'Tillikum',
                'Sealth',
                'Issaquah',
                'Chetzemoka']
while(True):
    html = get_nice_html('http://www.wsdot.com/ferries/vesselwatch/Default.aspx', 'vesselListDiv')
    data = format_table(html, col_names=table_heading, vessels=vessel_names)
    write_to_database(data)
    time.sleep(600)
    print '###  Starting next data read ###'


