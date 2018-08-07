# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 13:30:20 2018

@author: Timothy_Richards
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import os
username = os.getlogin()
#Prepare for plotting gradients with spike removal
df = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/flux_data.csv')
df.set_index('datetime',inplace=True)
df.index = pd.to_datetime(df.index)
df['month'] = df.index.month
df['hour'] = df.index.hour
df['flux_ma'] = df['flux'].rolling(window = 10).mean()

df4 = df[df['month']==4]
df5 = df[df['month']==5]
df6 = df[df['month']==6]
df7 = df[df['month']==7]

plt.plot(df4.index.values,df4.flux_ma)

