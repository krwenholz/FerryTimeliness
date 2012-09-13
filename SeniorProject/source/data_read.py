from BeautifulSoup import BeautifulSoup

from selenium import webdriver
import time


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
                 row_type='div', 
                 row_attrs={'class': 'vslLstRow INSvslLstRow'},
                 col_type='div',
                 col_attrs=None,):
    """
        Uses the BeautifulSoup library to find a table with the given parameters
        and then put it in a nice Python style dictionary.
    """
    data = []
    table = html_soup
    rows = table.findAll(row_type, attrs=row_attrs)
    for ii in range(len(rows)):
        data.append({})
        cols = rows[ii].findAll(col_type, attrs=col_attrs)
        for jj in range(len(cols)):
            data[ii][col_names[jj]: cols[jj].find(text=True)]
            print data[ii][col_names[jj]]
        print

##########
# Now make the nice looking calls to read data and such.
##########

html = get_nice_html('http://www.wsdot.com/ferries/vesselwatch/Default.aspx', 'vesselListDiv')
table_heading = ['Date', 'Pos', 'Route', 'Est. Arrival', 'Actual Departure', 
                 'Sched Departure', 
                 'Arriving', 
                 'Departing', 
                 'Icon',
                 'Knots',
                 'Vessel']
format_table(html, col_names=table_heading)
