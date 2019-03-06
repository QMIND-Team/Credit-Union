'''
@author: Dan Kailly

-Pulls all Geographic ID's (guids) from every single 2016 Census subdivision, in every province/territory of of Canada.
-Places the data into a CSV file
-Trims the CSV file from 5162 rows -> 3392 rows due to suppressed data (Held as confidential from Statistics Data)
    -If a data quality flag contains a '9', it means either income data and demographic data, be it long-form and
    short-form, is populated with an 'x' rather than a real value.
-More information on the URL's parameters can be found here: https://www12.statcan.gc.ca/wds-sdw/cr2016geo-eng.cfm
-the 'geos' and 'cpt' parameters are for specifying a result of divisions/subdivisions, and from what province/territory (or all provinces/territories)
'''

import urllib.request
import urllib.parse
import json
import csv
import pandas as pd

# Outputs HTTP response to text, placed into a json object later
def text_output(str):
    text_file = open("out-guids.txt", "w")
    text_file.write(str)
    text_file.close()

#obtains the subdivision name, data quality flag, and global non-response rate of every geographic uid in Canada
def requestResponse(url):
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    resp_string = resp.read().decode('utf-8')[2:]
    text_output(resp_string)

def guid_trim(filename):
    unwanted_flags = {9, 19, 29, 109, 909, 919, 929, 939, 949, 999, 1009, 1019, 1129, 1909, 1919, 1929, 1939, 1999,
                      2909, 2919, 2929, 2939, 3929, 3939, 4333, 4909, 4929, 4939, 4949, 4959, 4999, 5343, 5353, 5909,
                      5919, 5939, 5949, 5959, 5999, 9999, 19999,
                      21, 200, 201, 202, 1122, 1212,  2233, 2313, 2323, 3323,
                      2100, 1112, 2212, 212, 1211, 2200, 22, 122, 1222, 123, 12, 112, 4323, 2223,
                      1233, 2311, 2312, 1201, 2222, 23, 2213, 1323,
                      3100, 1313, 3333, 33, 3311, 1311, 303,}
    df = pd.read_csv(filename, encoding="ISO-8859-1")  # Import the raw data
    df.columns = ['GUID', 'PN', 'SDN', 'GT', 'GSF', 'GLF', 'DQF']  # Label the columns
    for flag in unwanted_flags:
        df_trim = df[df.DQF != flag]
        df = pd.DataFrame(df_trim)  # test if this correctly iterates

    guid_df = pd.DataFrame(df_trim)
    print(guid_df)
    guid_df.to_csv("../../Excel data/guids/subdivision-guids-trimmed.csv", index=False)

csv_to_trim = '../../Excel data/guids/subdivision-guids.csv'
url = 'https://www12.statcan.gc.ca/rest/census-recensement/CR2016Geo.json?lang=E&geos=CSD&cpt=00'
requestResponse(url)

with open('out-guids.txt') as jsonfile:
    data = json.load(jsonfile)

with open('../../Excel data/guids/subdivision-guids.csv', 'w', newline='') as csvfile:
    data_writer = csv.writer(csvfile)
    # The column names found in data
    data_writer.writerow(("GEO_UID", "Province_Name", "Subdivision_Name", "Geographic_Type", "GNR_SF", "GNR_LF", "Data_Quality_Flag"))
    for i in range(len(data['DATA'])):
        data_writer.writerow((data['DATA'][i][0], data['DATA'][i][2], data['DATA'][i][4], data['DATA'][i][5], data['DATA'][i][6], data['DATA'][i][7], data['DATA'][i][8]))

guid_trim(csv_to_trim)
