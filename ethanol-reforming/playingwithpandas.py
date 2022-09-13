# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 14:34:43 2022

@author: erikg
"""
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np

data = pd.read_csv('C:/Users/erikg/Documents/GitHub/ml-catalysis-1/ethanol-reforming/database-dft.csv')
features_all = data[['d_NN(top)', 'd_NN(2nd)', 'EN(top)', 'EN(2nd)',
                         'Facet', 'Eads(CH3CH2OH)', 'N_H', 'Initial', 'Final']]
feature_scaler = StandardScaler().fit(np.array(features_all.values, dtype=np.float64))
features_all = feature_scaler.transform(np.array(features_all.values, dtype=np.float64))
idx = np.true(10)