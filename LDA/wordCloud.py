# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 16:19:27 2019

@author: ALi M, Sean
"""
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
import pandas as pd

corpus_df = pd.read_pickle("corpus_pickle_words.pkl")
stopwords = set(STOPWORDS) 

mstring = ""
for i in range(len(corpus_df)):
    for j in range(len(corpus_df.columns)):
        try: 
            str(corpus_df[j][i])
            mstring = mstring + " " + corpus_df[j][i]         
        except:
            pass
        
wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = stopwords, 
                min_font_size = 10).generate(mstring) 
  
# plot the WordCloud image                        
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
plt.savefig('wordcloud.png', dpi=10000)
plt.show() 
