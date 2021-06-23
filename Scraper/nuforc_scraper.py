from urllib.request import Request, urlopen
import re
import time
import win32api
import threading

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

def make_soup_from_url(url):
    """Returns a BeautifulSoup object made from the page at the provided url.
    """
    request = Request(url, headers = {'User-Agent':'Mozilla/5.0'})
    soup = BeautifulSoup(urlopen(request).read(), 'html.parser')
    
    return soup

def grab_url_from_row(row, 
                      link_pos = 0,
                      url_template = 'http://www.nuforc.org/webreports/{}'):
    """This function grabs the href from the specified index of a tr element.

    args:
        row - iterable of bs4.element.Tag td objects.
    optional_args:
        link_pos - integer position of link element in row
            defaults to 0
        url_template - optional template to which the href should be inserted
            defaults to 'http://www.nuforc.org/webreports/{}'
    """
    row = row.findAll('td')
    link_td = row[link_pos]
    url_tail = link_td.find('font').find('a')['href']
    # Format with template as the 'a' tag only contains the tail of the url.
    url = url_template.format(url_tail)
    
    return url

def grab_row_data(row_element, year):
    """This function compiles all the data in a row on the NUFORC database into
    a matching pandas series.
    
    args:
        row_element - tr element containing td tags
        year - year in which the sighting on the provided row takes place
    """
    # Row is just tr element so create a list of all the td elements in each.
    row = row_element.findAll('td')
    # Split the timestamp into its individual parts and pad them with 0 if
    # needed.
    time = re.split('[:/ ]', row[0].text)
    time = list(map(lambda x : '0{}'.format(x) if len(x) == 1 else x, time))
    # Substitute "99" for missing minute and second values if needed.
    time += ['99'] * (5 - len(time))
    # Reorder the time list to [Year, Month, Day, Minute, Second].
    time = [time[i] for i in [2, 1, 0, 3, 4]]
    # Replace year with year argument as the row only has the 2 digit year.
    time[0] = year
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
    """This function finds the first table on the provided NUFORC
    database webpage and converts that table into a pandas dataframe.
    """
    page = make_soup_from_url(url)
    rows = page.find('tbody').findAll('tr')
    
    rows = list(map(grab_row_data, rows, np.full(len(rows), url[-11:-7])))
    
    return pd.DataFrame(rows)

def compile_and_export(dataframes, path):
    """Compiles provided iterable of dataframes and exports it to the default
    path.
    """
    data = pd.concat(dataframes, ignore_index = True)
    data.to_csv(path)

dataframes = []

def scrape_pages(urls, delay, i = 0):
    """Starts a recursion loop which will scrape the provided list of NUFROC
    database urls. When completed this function will output the data into the
    datasets directory.
    
    args:
        urls - list of urls to scrape
        delay - quantity of seconds between scrapes
    returns:
        None
    """
    if i < len(urls):
        # Recurse after a specified delay. Threads are used so the delay isn't
        # padded by the run time of the function.
        scrape_next = lambda: scrape_pages(urls, delay, i + 1)
        threading.Timer(delay, scrape_next).start()
        # Estimate remaining time and output that estimate to the console.
        time_estimate = int((len(urls) - i) * delay)
        print('Time remaining: {} seconds'.format(time_estimate), end = '\r')
        
        dataframes.append(grab_table_from_url(urls[i]))
    else:
        # Delay to allow the last scrape operation to complete.
        time.sleep(5)
        
        compile_and_export(dataframes, '../Datasets/nuforc_events_new.csv')
        # Alert user of completed scrape.
        print('Time remaining: 0 seconds')
        win32api.MessageBox(0, 'Scraping Complete!', '', 0x00001000)


# From the directory page create list of URLs to scrape.
homepage = make_soup_from_url('http://www.nuforc.org/webreports/ndxevent.html')
homepage_rows = homepage.find('tbody').findAll('tr')[:-1]

urls = list(map(grab_url_from_row, homepage_rows))

scrape_pages(urls, 2)