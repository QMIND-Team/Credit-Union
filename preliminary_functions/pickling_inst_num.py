import urllib
import urllib.request
from bs4 import BeautifulSoup as bs
import pandas as pd
from pandas import DataFrame
import pickle

#soups kraken site
def cr8soup(url):
  site = urllib.request.urlopen(url)
  webpage = bs(site, "html.parser")
  return webpage

soup = cr8soup("https://support.kraken.com/hc/en-us/articles/115012377707-Canadian-Financial-Institution-Numbers")

#creates 2 dimensional matrix from lists of kraken table
y = []

for rec in soup.findAll('tr'):
  x = []
  for data in rec.findAll('td'):
    x.append(data.text)
  y.append(x)

#sets first row as headers
headers = y.pop(0)

#converts matrix to dataframe
data = pd.DataFrame(y, columns = headers)

#pickles dataframe
data.to_pickle("inst_num.pickle")