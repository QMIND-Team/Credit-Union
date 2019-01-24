'''
@author: Dan Kailly
-Pulls all Geographic ID's (guids) from every single 2016 Census subdivision, in every province/territory of of Canada.
-Places the data into a CSV file

-More information on the URL's parameters can be found here: https://www12.statcan.gc.ca/wds-sdw/cr2016geo-eng.cfm
-the 'geos' and 'cpt' parameters are for specifying a result of divisions/subdivisions, and from what province/territory (or all provinces/territories)
'''

import urllib.request
import urllib.parse
import json
import csv

# Outputs the HTTP response to a text file, used to place the data into a json object later
def text_output(str):
    text_file = open("out-geography.txt", "w")
    text_file.write(str)
    text_file.close()

url = 'https://www12.statcan.gc.ca/rest/census-recensement/CR2016Geo.json?lang=E&geos=CSD&cpt=00' # Testing subdivisions in Nunavut
req = urllib.request.Request(url)
resp = urllib.request.urlopen(req)
resp_string = resp.read().decode('utf-8')[2:]
text_output(resp_string)


with open('out-geography.txt') as jsonfile:
    data = json.load(jsonfile)

# print(data['COLUMNS']) leftover from debugging
with open('subdivision-guids.csv', 'w', newline='') as csvfile:
    data_writer = csv.writer(csvfile)
    # The column names found in data
    data_writer.writerow(("GEO_UID", "Province_Name", "Subdivision_Name", "Geographic_Type", "GNR_SF", "GNR_LF", "data_quality_flag"))
    for i in range(len(data['DATA'])):
        data_writer.writerow((data['DATA'][i][0], data['DATA'][i][2], data['DATA'][i][4], data['DATA'][i][5], data['DATA'][i][6], data['DATA'][i][7], data['DATA'][i][8]))
