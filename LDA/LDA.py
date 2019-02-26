# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 16:26:22 2019

@author: Caelum Kamps
"""

import text_preparation as tp
from gensim import corpora
import pickle
import gensim
#import pyLDAvis.gensim
#import pyLDAvis

text_data = []

with open('example2.txt') as f:
    for line in f:
        tokens = tp.prepare_text_for_lda(line)
        
        if len(tokens) > 0:
            text_data.append(tokens)    
            #print(tokens)

dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]

pickle.dump(corpus, open('corpus.pkl','wb'))
dictionary.save('dictionary.gensim')


NUM_TOPICS = 4
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
ldamodel.save('model5.gensim')

topics = ldamodel.print_topics(num_words=4)
for topic in topics:
    print(topic)

# pyLDAvis

'''
dictionary = gensim.corpora.Dictionary.load('dictionary.gensim')
corpus = pickle.load(open('corpus.pkl', 'rb'))

lda = gensim.models.ldamodel.LdaModel.load('model5.gensim')
lda_display = pyLDAvis.gensim.prepare(lda, corpus, dictionary, sort_topics=False)

pyLDAvis.save_html(lda_display, fileobj ='lda.html')
'''