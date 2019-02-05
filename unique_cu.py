# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 17:50:22 2019

@author: Caelum Kamps
"""

import pandas as pd

CU = pd.read_pickle('CU_locations.p')
CU = CU.CU.value_counts()

CU = CU[:200]
CU.columns = ['Name','Number of instances']
CU.to_csv('Urls.csv')