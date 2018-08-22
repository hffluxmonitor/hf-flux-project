# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 14:55:58 2018
@author: FluxMonitor
"""
import os
import pandas as pd
import numpy as np

username = os.getlogin()

df = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/qc_log_B.csv')
df.start_date = pd.to_datetime(df.start_date,yearfirst = True)
df.end_date = pd.to_datetime(df.end_date,yearfirst = True)
df_flux = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/flux_data.csv')
df_flux['datetime'] = pd.to_datetime(df_flux['datetime'])
df_flux['qc_flag'] = 0
qc = []

for j, row in df_flux.iterrows():
    for i in range(0,2):
            sd = df.iloc[i].start_date
            ed = df.iloc[i].end_date
            df_flux.iloc[j]['qc_flag'] = np.where(((row['datetime'] > sd) & (row['datetime'] <= ed)),1,0)

#This creates a list with two indices, one for each qc log. Maybe append list with df_flux dataframe?
for i in range(0,2):  
    sd = df.iloc[i].start_date
    ed = df.iloc[i].end_date  
    qc.append(np.where(((df_flux['datetime'] > sd) & (df_flux['datetime'] <= ed)),1,0))


