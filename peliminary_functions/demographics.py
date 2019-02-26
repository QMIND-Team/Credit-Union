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
import json
import pandas as pd

# Outputs to text file
def text_output(str):
    text_file = open("out.txt", "w")
    text_file.write(str)
    text_file.close()

# Fetch resources from the URL
url = 'https://www12.statcan.gc.ca/rest/census-recensement/CPR2016.json?lang=E&dguid=2016A000011124&topic=7&notes=0'
req = urllib.request.Request(url)
resp = urllib.request.urlopen(req)

# Format from HTTPResponse to string
resp_string = resp.read().decode('utf-8')[2:] # Format out the initial '//' characters in the string

text_output(resp_string)

# Formats response data from string to json object
jsonStr = json.dumps(resp_string)
resp_json_obj = json.loads(jsonStr)

