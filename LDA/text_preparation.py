# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 16:26:22 2019

@author: Caelum Kamps
"""

import spacy
import nltk
from spacy.lang.en import English
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

parser = English()

nltk.download('stopwords')
nltk.download('wordnet')
en_stop = set(nltk.corpus.stopwords.words('english'))

def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens

def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else: 
        return lemma

def get_lemma2(word):
    return WordNetLemmatizer.lemmatize(word)

def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens






