'''
@author: Daniel Kailly

Goal: Obtain a Canadian 2016 Census subdivision name from entering a 6-digit postal code.

Here are some useful links on how postal codes in Canada are organized:
-https://www.canadapost.ca/tools/pg/manual/PGaddress-e.asp?ecid=murl10006450#1437302 (Section 5.1)
-https://www.ic.gc.ca/eic/site/bsf-osb.nsf/eng/br03396.html
'''

import requests
import pandas as pd
from bs4 import BeautifulSoup

def requestResponse(url):
    req = requests.get(url)
    # Locates the desired HTML block, then trims the <a> tag that contains the name of the Census subdivision we want
    soup = BeautifulSoup(req.content, 'html.parser')
    summary = soup.find("summary", string="Census subdivisions")
    if(summary == None):
        result = "N/A"
        return result
    ul = summary.findNext('ul')
    first_li = ul.findNext('li')
    first_link = ul.findNext("a")
    first_link_str = str(first_link)
    head, sep, tail = first_link_str.partition('Data table: ')
    head2, sep2, tail2 = tail.partition(' (')
    #print(head2)
    return head2

def obtainSubdivisionName(pc_name):
    # print(pc_and_name['Postal_Code'])
    pcs_str = []

    # adding all postal code elements into a list of strings
    for postal_code in pc_name['Postal_Code']:
        pc_trim = postal_code.replace(" ", "")
        pcs_str.append(pc_trim)

    for i in range(len(pcs_str)):
        url = 'https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/prof/search-recherche/frm_res_postalcode.cfm?' \
              'Lang=E&TABID=1&G=1&Geo1=PR&Code1=01&Geo2=PR&Code2=35&SearchText=' + pcs_str[i]
        subdiv_name_response = requestResponse(url)
        pc_name['Subdivision_Name'].loc[i] = subdiv_name_response
        print(pc_name['Subdivision_Name'].loc[i])
    return pc_name;

# Import CU location data from Caelum's bank_locations.py
unpickled_df = pd.read_pickle("../CU_locations.p")

#Dataframe that will share city/town name associated with the postal code
df_columns =['Postal_Code', 'Subdivision_Name']
pc_and_name = pd.DataFrame(columns=df_columns)
pc_and_name['Postal_Code'] = unpickled_df["PC"]
# print(pc_and_name['Postal_Code'])

pc_and_name_final = obtainSubdivisionName(pc_and_name)

pc_and_name_final.to_pickle("../../Pickled Data/demographics/postalcode-subdiv-name.pkl",)
unpickled_df = pd.read_pickle("../../Pickled Data/demographics/postalcode-subdiv-name.pkl")
unpickled_df.to_csv("../../Excel data/demographics/postalcode-subdiv-name.csv", index=False, encoding="utf-8-sig")
print("Subdiv name + postal code to a pickle + csv :)")