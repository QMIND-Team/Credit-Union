# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 11:02:20 2019

@author: Caelum Kamps
"""
import gensim
import pickle
import numpy as np
from scipy.stats import entropy

TOPICS = 4

#%% Cosine Similarity Analysis
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
    #temp = temp[:NUM]
    
    top.append(temp)
  
#%% KLD analysis
# Generate prob distributions
distributions = [lda[corpus[i]] for i in range(len(corpus))]
zero_v = 0.00001

# added missing topics to the distributions
for j in range(len(distributions)):
    topics = []
    for topic in distributions[j]:
        topics.append(topic[0])
    
    # added zero vectors
    for i in range(TOPICS):
        if i not in topics:
            distributions[j].append((i,zero_v))
    
    # sorted by topic identifier     
    distributions[j] = sorted(distributions[j], key = lambda x: x[0])
    
    # Prepared for KLD analysis
    for k in range(TOPICS):
        distributions[j][k] = distributions[j][k][1]
    

# Intialize KLD array
KLDiv = np.zeros([len(distributions),len(distributions)])   
 
# Calculate KLD for each CU against each other
for i in range(len(KLDiv)):
    for j in range(len(KLDiv)):
        KLDiv[i,j] = entropy(distributions[i],distributions[j])

# Find 5 most similar CUs to each CU    
KLD_top = []

for i in range(len(KLDiv)):
    temp = []
    for j in range(len(KLDiv)):
        if j != i:
            temp.append((KLDiv[i,j],j))
            
    # Sort the list by its similarity metric
    temp = sorted(temp, key =lambda x: x[0], reverse = False)
    
    # Extract top N
    #temp = temp[:NUM]
    
    KLD_top.append(temp)
    
    
# KLD save
pickle.dump(KLD_top,open('Dash/KLD_similarity.pkl','wb'))
pickle.dump(top,open('Dash/Cosine_similarity.pkl','wb'))
pickle.dump(corpus,open('Dash/corpus.pkl','wb'))
pickle.dump(dictionary,open('Dash/dictionary.pkl','wb'))


