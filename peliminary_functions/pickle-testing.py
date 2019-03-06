import urllib.request
import urllib.parse
import json
import pickle
import numpy as np
import itertools
import requests
import pandas as pd
import csv


unpickled_df = pd.read_pickle("../Pickled Data/demographics-data.pkl")
#print(unpickled_df)
unpickled_df.to_csv("income-data-ontario.csv", index=False)
print("done")

