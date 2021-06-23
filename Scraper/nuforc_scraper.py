from urllib.request import Request, urlopen
import re

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

# Create list of URLs to scrape
homepage = Request('http://www.nuforc.org/webreports/ndxevent.html', 
           headers = {'User-Agent':'Mozilla/5.0'})
homepage = BeautifulSoup(urlopen(homepage).read(), 'html.parser')

urls = []

for tr in homepage.find('tbody').findAll('tr'):
    month = tr.findAll('td')[0].text.split('/')
    month = '{}{}'.format(month[1], month[0])
    url = 'http://www.nuforc.org/webreports/ndxe{}.html'.format(month)
    urls.append(url)

del urls[-1]

def grab_row_data(row):
    row = row.findAll('td')
    series = pd.Series()
    timestamp = re.split('[:/ ]', row[0].text)
    timestamp = list(map(lambda x : '0{}'.format(x) if len(x) == 1 else x, timestamp))
    year = timestamp[0]
    month = timestamp[1]
    day = timestamp[2]
    hour = timestamp[3]
    minute = timestamp[4]
    second = '00'
    # Generate timestamp
    ts = '{}-{}-{}T{}:{}:{}Z'
    series['event_time'] = ts.format(year, month, day, hour, minute, second)
    # Generate datestamp
    ds = '{}-{}-{}'
    series['event_date'] = ds.format(year, month, day)
    # Add individual time components
    series['year'] = year
    series['month'] = month
    series['day'] = day
    series['hour'] = hour
    series['minute'] = minute
    series['second'] = second
    # city
    series['city'] = row[1].text
    # state
    series['state'] = row[2].text
    # shape
    series['shape'] = row[3].text
    # duration
    series['duration'] = row[4].text
    # summary
    series['summary'] = row[5].text
    # event_url
    series['event_url'] = row[0].find('font').find('a')['href']
    
    return series

def grab_table_from_url(url):
    request = Request(url, 
              headers = {'User-Agent':'Mozilla/5.0'})
    page = BeautifulSoup(urlopen(request).read(), 'html.parser')
    table = page.find('tbody').findAll('tr')
    
    rows = list(map(grab_row_data, row))
    
    frame = pd.DataFrame(rows)

def 
    
frames = list(map(grab_table_from_url, urls))
data = pd.concat(frames,
                 ignore_index = True)