from urllib import urlopen
from BeautifulSoup import BeautifulSoup


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time


"""
    This file reads in data from the WSDOT Vessel Track site to store in a MySQL
    database.
"""

def get_nice_html(url, elem_id):
    """
        Grab raw html from a url and return a cleaned up version using BeautifulSoup.
    """

    # XXX: Attepmt at selenium
    browser = webdriver.Firefox() # Get local session of firefox
    browser.get(url) # Load page
    time.sleep(0.2) # Let the page load, will be added to the API
    element = browser.find_element_by_id(elem_id) # Find the query box
    html_raw = element.get_attribute('innerHTML')
    browser.close()

    html_soup = BeautifulSoup(''.join(html_raw))

    print html_soup.prettify()

    return html_soup

def format_table(html_soup, cellspacing='0', cellpadding='0', border='0',
                 style='width:inherit;'):
    """
        Uses the BeautifulSoup library to find a table with the given parameters
        and then put it in a nice Python style dictionary.
    """
    table = html_soup.find('table', attrs={'cellspacing':cellspacing, 
                                           'cellpadding':cellpadding, 
                                           'border':border, 
                                           'style':style}
                          )
    rows = table.findAll('div', attrs={'class': 'vslLstRow INSvslLstRow'})
    # vslLstRow INSvslLstRow
    for row in rows:
        print 'iterating through rows'
        cols = row.findAll('td')
        for td in cols:
            text = ''.join(td.find(text=True))
            print text+"|",
        print

##########
# Now make the nice looking calls to read data and such.
##########

html = get_nice_html('http://www.wsdot.com/ferries/vesselwatch/Default.aspx', 'vesselListDiv')
format_table(html)
