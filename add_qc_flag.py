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
df_flux['qc_flag'] = int(0)

for i in range(0,len(df)):
    i = 0
    mask = (df_flux['datetime'] > df.iloc[i].start_date) & (df_flux['datetime'] <= df.iloc[i].end_date)
    mask = pd.DataFrame(mask)
    mask.columns = ['qc_flag']
    mask['qc_flag'] =  (np.where(mask.qc_flag == True,int(1),int(0)))
    df_flux = df_flux.update(mask)
    #df_flux['qc_flag'] = df_flux.update(np.where(df_flux['mask'] == True,1,0))
    #df_flux['qc_flag'] = df_flux.update(mask)


