from urllib.request import Request, urlopen

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