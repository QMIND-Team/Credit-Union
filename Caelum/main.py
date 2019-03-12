# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 17:25:24 2019

@author: Caelum Kamps
"""

import pandas as pd
import pickle
import os

locations = pickle.load(open('CU_locations.p','rb'))
corpus_path = 'corpus/'
article_paths = [os.path.join(corpus_path,p) for p in os.listdir(corpus_path)]

urls = pd.read_csv('Completed_URLS.csv')


df = pd.DataFrame(columns = ['name','postal_code'])

names = []
postal = []

for article in article_paths:
    name = article.split('/')[1].split('.')[0]
    if len(name) < 3:
        name = urls['name'][int(name) - 1]
        
        
    index = locations.index[locations.CU == name]
    post = locations.PC[index]
    if len(post) > 0:
        post = post.values[0]
    else:
        post = None
        
    names.append(name)
    postal.append(post)
df.name = names
df.postal_code = postal

pickle.dump(df,open('indexed_names.p','wb'))