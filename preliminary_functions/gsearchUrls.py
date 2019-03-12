from bs4 import BeautifulSoup
import pandas as pd
import requests
from time import sleep

df = pd.read_csv('Urls.csv')

df.columns = ["CU", "NO."]

df["URL"] = "not filled"

def gsearch(srch):
  try:
    res = requests.get("https://www.google.ca/search?q=" + srch)
  except:
    sleep(3)
    res = requests.get("https://www.google.ca/search?q=" + srch)
  res.raise_for_status()
  soup = BeautifulSoup(res.text, "html.parser")
  els = soup.select('.r a')
  try:
    first = els[0].get('href').replace('/url?q=','').split("&sa=U&ved=")[0]
  except:
    first = els[0].get('href').replace('/url?q=','')
  return first


df["URL"] = df.CU.apply(gsearch)

df.to_csv("urladds.csv")
