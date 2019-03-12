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
PA : Postal Address
PC : Postal Code
CU : Credit Union
'''

# Function to find the nth index of a specific character or substring
def find_nth(string, value, n):
    start = string.find(value)
    while start >= 0 and n > 1:
        start = string.find(value, start+len(value))
        n -= 1
    return start


df = pd.read_csv('location_data.csv') # Import the raw data
df.columns = ['RN', 'EP', 'PA'] # Label the columns

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
       

pc = [] # Postal Code
cu = [] # Credit union 


for i in range(len(df)):    
    pc.append(df['PA'].loc[i][-7:])
    cu.append(df['PA'].loc[i][:df['PA'].loc[i].find(',')])
            
df['PC'] = pc # New Row for postal code
df['CU'] = cu # New Row for Credit Union Name

df.to_pickle('CU_locations.p')


