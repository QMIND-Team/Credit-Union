"""
Created on Thu Feb 27 15:39:37 2019

@author: Ali Masoumnia
"""
from bs4 import BeautifulSoup as bs
import html2text
import requests
import pandas as pd
import re
import time

df = pd.read_csv("Completed_URLS.csv").iloc[:25]
df.columns = ["CU","LOC","URL"]

def fix(string):
    fixed_string = string.rstrip()
    return fixed_string
  
df["URL"] = df.URL.apply(fix)

for x in range(len(df)):
  url = df["URL"][x]
  f = html2text.HTML2Text()
  f.ignore_links = True
  f.ignore_anchors = True
  f.ignore_images = True
  f.ignore_emphasis = True
  f.skip_internal_links = True
  try:
    r = requests.get(url)
  except:
    time.sleep(5)
    r = requests.get(url)
  r.raise_for_status()
  
  soup = bs(r.content, "lxml").prettify()

  rendered_content = f.handle(str(soup))
  rendered_content = re.sub(r'{{.+?}}', '', rendered_content)
  rendered_content = rendered_content.replace("*", "").replace("#", "").replace("_", "").replace("\n\n\n\n", "\n").replace("\n\n\n", "\n\n")
                             
  file_name = df["CU"][x] + ".txt"
  f = open(file_name, "w", encoding="utf-8")
  f.write(rendered_content)
  f.close()