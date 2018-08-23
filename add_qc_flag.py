# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 14:55:58 2018
@author: FluxMonitor
"""
import os
import pandas as pd

username = os.getlogin()

df = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/qc_log_B.csv')
df.start_date = pd.to_datetime(df.start_date,yearfirst = True)
df.end_date = pd.to_datetime(df.end_date,yearfirst = True)
df_flux = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/flux_data.csv')
df_flux['datetime'] = pd.to_datetime(df_flux['datetime'])
df_flux['qc_flag'] = 0

for i in range(0,2):  
    sd = df.iloc[i].start_date
    ed = df.iloc[i].end_date 
    col_idx = 'qc_flag'
    row_idx = (df_flux['datetime'] > sd) & (df_flux['datetime'] <= ed)
    df_flux.loc[row_idx, col_idx] = 1
    
df_flux.to_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/flux_data.csv')


