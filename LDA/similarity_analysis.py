# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 11:02:20 2019

@author: Caelum Kamps
"""
import gensim
import pickle
import numpy as np


# reload dictionary, corpus, and lda model
dictionary = gensim.corpora.Dictionary.load('dictionary.gensim')
corpus = pickle.load(open('corpus.pkl','rb'))
lda = gensim.models.ldamodel.LdaModel.load('model.gensim')

sim_matrix = np.zeros([len(corpus),len(corpus)])

# Filling the similarity matrix
for i in range(len(sim_matrix)):
    for j in range(len(sim_matrix)):
        # Calculate similarity
        sim_matrix[i,j] =  gensim.matutils.cossim(lda[corpus[i]],lda[corpus[j]])

# Number of recommendations to provide
NUM = 5
# saves top N most similar credit unions by website topic
top = []

for i in range(len(sim_matrix)):
    temp = []
    for j in range(len(sim_matrix)):
        if j != i:
            temp.append((sim_matrix[i,j],j))
            
    # Sort the list by its similarity metric
    temp = sorted(temp, key =lambda x: x[0], reverse = True)
    
    # Extract top N
    temp = temp[:NUM]
    
    top.append(temp)
    
    
