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
import itertools
import requests
import pandas as pd
import csv

# Outputs to text file
def text_output(str):
    text_file = open("out.txt", "w")
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
with open('subdivision-guids.csv') as csvfile:
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

#writing demographics to a csv
with open('demographics-table-test.csv', 'w', newline='') as writeCsvFile:
    data_writer = csv.writer(writeCsvFile)
    # The column names found in data
    data_writer.writerow(("GEO_UID" , "Province_Name", "Subdivision_Name", "Geographic_Type", "Prov_Terr_ID",
                          "Province_Terr_Name", "GEO_UID", "GEO_ID", "GEO_NAME", "GEO_TYPE",
                          "TOPIC_THEME", "TEXT_ID", "HIER_ID", "INDENT_ID", "TEXT_NAME",
                          "NOTE_ID", "NOTE", "T_DATA", "T_SYM", "M_DATA",
                          "F_DATA",))

    loop_count = 1
    for (a,b,c,d) in zip(dguid_list, prov_name, subdiv_name, subdiv_type_list):
        #print(a, b, c, d)
        dguid = a
        print(a,b,c,d)
        url_test = 'https://www12.statcan.gc.ca/rest/census-recensement/CPR2016.json?lang=E&dguid=' + dguid + '&topic=0&notes=0'
        text_output(requestResponse(url_test))
        with open('out.txt') as jsonfile:
            data = json.load(jsonfile)

        for i in range(len(data['DATA'])):
            data_writer.writerow((a, b, c, d, data['DATA'][i][0],
                                data['DATA'][i][1], data['DATA'][i][2], data['DATA'][i][3], data['DATA'][i][4], data['DATA'][i][5],
                                data['DATA'][i][6], data['DATA'][i][7], data['DATA'][i][8], data['DATA'][i][9], data['DATA'][i][10],
                                data['DATA'][i][11], data['DATA'][i][12], data['DATA'][i][13], data['DATA'][i][14], data['DATA'][i][15],
                                data['DATA'][i][17]))
    loop_count += 1
print('done writing to csv.')
