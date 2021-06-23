from urllib.request import Request, urlopen
import re
import time

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
# This is needed because the href only 
def grab_url_from_row(row, 
                      link_index = 0,
                      url_template = 'http://www.nuforc.org/webreports/{}'):
    """This function grabs the href from the specified index of a tr element.
    
    ----------------------------------------------------------------------------
    
    args:
        row - iterable of bs4.element.Tag td objects.
        
    optional_args:
        link_index - integer position of link element in row
            defaults to 0
        url_template - optional template to insert found href into
            defaults to 'http://www.nuforc.org/webreports/{}'
            
    returns:
        string containing href found in row
    """
    # Grab href from specified element in table.
    row = row.findAll('td')
    link = row[link_index]
    link = link.find('font').find('a')['href']
    # Format with template because the href only contains the non-standard part.
    link = url_template.format(link)
    
    return link

def grab_row_data(row_element):
    """This function compiles all the data in a row on the nuforc database into
    a matching pandas series.
    
    ----------------------------------------------------------------------------
    
    args:
        row_element - bs4.element.Tag of the type tr that contains td elements. 
        Needs to specifically have the schema:
        | Date/Time | City | State | Shape | Duration | Summary | Posted |
            
    returns:
        pandas series of the schema:
        | event_time | event_date | year | month | day | hour | minute | second
        | city | state | shape | duration | summary | event_url |
    """
    # Row is just tr element so create a list of all the td elements in each.
    row = row_element.findAll('td')
    # Split the timestamp into its individual parts and pad them with 0 if
    # needed.
    time = re.split('[:/ ]', row[0].text)
    time = list(map(lambda x : '0{}'.format(x) if len(x) == 1 else x, time))
    time += ['99'] * (5 - len(time))
    # Assign all row values in correct order.
    s = pd.Series(dtype = 'object')
    s['event_time'] = '{}-{}-{}T{}:{}:00Z'.format(*time)
    s['event_date'] = '{}-{}-{}'.format(*time[0:3])
    s['year'],    \
    s['month'],   \
    s['day'],     \
    s['hour'],    \
    s['minute'], = list(map(int, time))
    s['city'],    \
    s['state'],   \
    s['shape'],   \
    s['duration'],\
    s['summary'] = list(map(lambda x : x.text, row[1:6]))
    # Get the link from the first element in the row. It needs the original row
    # element, not the list of td elements made from the row element.
    s['event_url'] = grab_url_from_row(row_element)
    
    return s

def grab_table_from_url(url):
    """This function finds the first table on the provided webpage and converts
    that table into a pandas dataframe. This function only works with NUFORC
    database webpages like the one below.
    
    Example: http://www.nuforc.org/webreports/ndxe202105.html
    
    ----------------------------------------------------------------------------
    
    args:
        url - string url that links to a NUFORC database webpage like the one
        above
            
    returns:
        pandas dataframe of the first table on the provided page
    """
    request = Request(url, headers = {'User-Agent':'Mozilla/5.0'})
    page = BeautifulSoup(urlopen(request).read(), 'html.parser')
    rows = page.find('tbody').findAll('tr')
    
    rows = list(map(grab_row_data, rows))
    
    return pd.DataFrame(rows)

# From the directory page create list of URLs to scrape.
homepage = Request('http://www.nuforc.org/webreports/ndxevent.html', 
                   headers = {'User-Agent':'Mozilla/5.0'})
homepage = BeautifulSoup(urlopen(homepage).read(), 'html.parser')
urls = list(map(grab_url_from_row,
                homepage.find('tbody').findAll('tr')[:-1]))
urls = urls[0:3]

dataframes = []
# Added a delay because even if NUFORC doesn't have scraping protection I don't
# want to be rude.
delay = 2
for i, url in enumerate(urls):
    time.sleep(delay)
    
    time_estimate = int((len(urls) - i) * delay)
    print('Time remaining: {} seconds'.format(time_estimate), 
          end = '\r')
    
    dataframes.append(grab_table_from_url(url))

data = pd.concat(dataframes, ignore_index = True)
data.to_csv('../Datasets/nuforc_events_new.csv')