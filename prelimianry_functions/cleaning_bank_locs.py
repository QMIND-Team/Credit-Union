import pandas as pd
import urllib
import urllib.request
from bs4 import BeautifulSoup as bs

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

#converts matrix to dataframe
ins = pd.DataFrame(y, columns = ["Financial Institution", "Instituion Number"])

"""
--------------------------------------------------

Author: Ali Masoumnia

Acronyms
--------------
RN : Routing Number
EP : Electronic Paper Number
IN : Institution Number
BN : Bank Name
PR : Province
PC : Postal Code
PA : Postal Address
"""

df = pd.read_csv('bank_location_data.csv') # Import the raw data
df.columns = ['RN', 'EP', 'PA'] # Label the columns

df.drop_duplicates(inplace=True) # Drop duplicate values
df.reset_index(drop = True, inplace = True) # reset the index 

#stragnate dataframes for nulls of each column, only for index reference
emptyRN = df['RN'].isna()
emptyEP = df['EP'].isna()
emptyPA = df['PA'].isna()

#grabbing extensions of PAs to next line back to the line before (does not cut out extension line)
for i in range(len(df)):
  if emptyRN[i] == True and emptyEP[i] == True:
    df['PA'][i-1] = df['PA'][i-1] + " " + df['PA'][i]
  else:
    pass

#grabs error 
for i in range(len(df)):
  try:
    if len(df['RN'][i]) == 19:
      x = df['RN'][i].split(" ")
      try: 
        int(x[0])
        if emptyPA[i] == True:
          df['PA'][i] = df['EP'][i]
        elif emptyPA[i] == False:
          pass
        else:
          pass
        df['EP'][i] = x[1]
        df['RN'][i] = str(x[0])
      except:
        pass
  except:
    pass

for i in range(len(df)):
    if emptyEP[i] == True and emptyPA[i] == True:
      x = df['RN'][i].split(" ")
      try:
        int(x[0])
        y = x[2:len(x)]
        df['PA'][i] = " ".join(y)
        df['RN'][i] = x[0]
        df['EP'][i] = x[1]
      except:
        pass

df.dropna(how = "any", inplace = True)
df.reset_index(drop = True, inplace = True) # reset the index 

"""
#makes df for dirty data,  maintains index to reference main dataframes for testing
errtypes = pd.DataFrame(columns=['errRN','errEP', "errPA"])
for row in range(len(df)):
  try:
    if len(df['RN'][row]) != 9 and len(df['EP'][row]) != 9:
      errtypes.loc[row] = df.loc[row].values.tolist()
  except:
    errtypes.loc[row] = df.loc[row].values.tolist()
"""

df['TN'] = df["EP"].str.split("-", n = 1, expand = True)[0]
df['IN'] = df["EP"].str.split("-", n = 1, expand = True)[1]

df['BN'] = df.IN.map(dict(ins[["Instituion Number", "Financial Institution"]].values))

import re

df["PA"] = df.PA.apply(lambda x : re.sub(r" \(.*?$", r"", x))

for l in range(len(df)):
  try:
      int(df["PA"][l][-1])
      int(df["PA"][l][-3])
      int(df["PA"][l][-6])
  except:
    print(df["PA"][l])

df.to_pickle("cleaned_bank_locations.pickle")

#pd.to_numeric(df.RN)

