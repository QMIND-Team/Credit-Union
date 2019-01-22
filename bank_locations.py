# -*- coding: utf-8 -*-
'''
Created on Tue Jan 15 19:20:16 2019

Author: Caelum Kamps

Program to import, clean, and prepare 
credit union location and information data.

Developed for the QMIND credit union team!
'''

import pandas as pd
import math

'''
Acronyms
--------------
RN : Routing Number
EP : Electronic Paper Number
IN : Institution Number
BN : Bank Name
PR : Province
PC : Postal Code
PA : Postal Address
'''

'''Import institution numbers
Source: https://support.kraken.com/hc/en-us/articles/
115012377707-Canadian-Financial-Institution-Numbers
'''
# Need to web scrape this source ^


df = pd.read_csv('bank_location_data.csv') # Import the raw data
df.columns = ['RN', 'EP', 'PA'] # Label the columns

#pd.to_numeric(df.RN)

df.drop_duplicates(inplace = True) # Drop duplicate values
df.reset_index(drop = True, inplace = True) # reset the index 


# Fixing roll over rows so that postal addresses are complete in one cell
for i in range(len(df)):
    if math.isnan(df['RN'][i]): # NaN routing values means rollover row        
        df['PA'][i-1] = (
                df['PA'][i-1] 
                + ' ' 
                + df['PA'][i]
                )

df.dropna(inplace = True) # Drop the rows that have been fixed
df.reset_index(drop = True, inplace = True) # reset the index 

# fixing rows that have a 'Sub to ########' comment at end of address
for i in range(len(df)):
    if df['PA'][i][-1] == ')':
       df['PA'][i] = df['PA'][i][:df['PA'][i].find('(') -1]
       

# Provice codes from the routing number
''' Source: https://en.wikipedia.org/wiki/Routing_number_(Canada) '''      
province_codes = {0 : 'British Columbia & Yukon',
                  1 : 'Western Quebec',
                  2 : 'Southern Ontario',
                  3 : 'Nova Scotia, PEI, Newfoundland',
                  4 : 'New Brunswick',
                  5 : 'Eastern Quebec',
                  6 : 'Eastern Ontario',
                  7 : 'Manitoba and North-Western Ontario',
                  8 : 'Saskatchewan',
                  9 : 'Alberta, NW Territories, Nunavut'}

IN = []
BN = []
PR = [] 
PC = []



for i in range(len(df)):    
    PC.append(df['PA'].loc[i][-7:])
    #PR.append(df)
            
df['PC'] = PC # New Row for postal code


df.to_pickle('CU_locations.p')


