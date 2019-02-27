# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 14:40:24 2019

@author: Caelum Kamps
"""

import gensim
import pickle
import pyLDAvis.gensim

dictionary = gensim.corpora.Dictionary.load('dictionary.gensim')
corpus = pickle.load(open('corpus.pkl','rb'))
lda = gensim.models.ldamodel.LdaModel.load('model.gensim')

lda_display = pyLDAvis.gensim.prepare(lda,corpus,dictionary,sort_topics = False)
pyLDAvis.save_html(lda_display, 'LDA.html')