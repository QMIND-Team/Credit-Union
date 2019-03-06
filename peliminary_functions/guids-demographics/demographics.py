'''
@author: Daniel Kailly

Obtains Demographic Statistics, found in the 2016 Census, from a specified geographical region of Canada.
Developed by the QMIND Credit Union team!

Visit these links to find out more about what data is being pulled:
    1. 2016 Census Profile: https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/index.cfm?Lang=E#
    2. 2016 Census Profile Web Data Service: https://www12.statcan.gc.ca/wds-sdw/cr2016geo-eng.cfm
    https://www12.statcan.gc.ca/wds-sdw/cpr2016-eng.cfm
'''

import urllib.request
import urllib.parse
import json
import pandas as pd
import csv

# Outputs to text file
def text_output(str):
    text_file = open("out-demographics.txt", "w")
    text_file.write(str)
    text_file.close()

# performs a URL request on the Census Profile's Web Data Service, and formats it into a string that will be later formatted into json data.
def requestResponse(url):
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    # Format from HTTPResponse to string
    resp_string = resp.read().decode('utf-8')[2:]  # Format out the initial '//' characters in the string
    return resp_string

# reading from the subdivision guid csv
dguid_list = []
prov_name = []
subdiv_name = []
subdiv_type_list = []
gnr_sf_list = []
gnr_lf_list = []
data_quality_flag_list = []

# adding stuff to good ol lists
# Currently getting infor for BC(current), AB, SK, MA
with open('../../Excel data/guids/guids-bc.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        dguid_list.append(row[0])
        prov_name.append(row[1])
        subdiv_name.append((row[2]))
        subdiv_type_list.append((row[3]))
dguid_list = dguid_list[1:]
prov_name = prov_name[1:]
subdiv_name = subdiv_name[1:]
subdiv_type_list = subdiv_type_list[1:]


#writing columns and column contents to a dataframe
ddf_columns = ['GUID', 'PROVID', 'PROVNAME', 'SDNAME', 'GEOTYPE', 'TEXTTHEME', 'TEXTID',
                           'HIER', 'INDENT', 'TEXTNAME', 'TEXTDATA', 'MDATA', 'FDATA'] # Label the columns
demographics_df = pd.DataFrame(columns= ddf_columns)

for (a, b, c, d) in zip(dguid_list, prov_name, subdiv_name, subdiv_type_list):
    print(a, b, c, d)
    dguid = a
    url = 'https://www12.statcan.gc.ca/rest/census-recensement/CPR2016.json?lang=E&dguid=' + dguid + '&topic=7&notes=0' # receives income data from subdivisions in a province
    text_output(requestResponse(url))
    with open('out-demographics.txt') as jsonfile:
        data = json.load(jsonfile)
        for i in range(len(data['DATA'])):
            demographics_df.loc[-1] = [a, data['DATA'][i][0], b, c,
                                       d, data['DATA'][i][6], data['DATA'][i][7], data['DATA'][i][8],
                                       data['DATA'][i][9], data['DATA'][i][10], data['DATA'][i][13],
                                       data['DATA'][i][15],
                                       data['DATA'][i][17]]
            demographics_df.index = demographics_df.index + 1
demographics_df.to_pickle("../../Pickled Data/demographics/income-data-bc.pkl")
print("done, file is pickled.")
