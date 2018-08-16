# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 11:59:13 2018

@author: Timothy_Richards

Description: This program will take 5 min Tekran B data and join it with 30 min
sonic data to create one master file for flux calculations.
 Also calculates gradient of flux (B) system.
"""

import pandas as pd
import numpy as np
import os

username = os.getlogin()

#%%
def merge_gemB_sonic_data():    
    #Load files and prepare for merge
    df_gem = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/TimeSeries/TK2537B.csv')
    df_gem['datetime'] = pd.to_datetime(df_gem['datetime'],yearfirst=True)
    df_gem.set_index('datetime',inplace=True)
    df_gem = df_gem[(df_gem['flag'] == 0) | (df_gem['flag'] == 1)] #Only keep flux (intake 0,1) data
    
    #Create pivot table with one column for each intake
    df_gem_piv = df_gem.pivot(columns = 'flag',values = 'conc')
    df_gem_piv.columns = ['lower_0','upper_1']
    df_gem_piv = df_gem_piv.astype(float)
    
    #Apply moving average to fill in gaps, window = 4 (20 minute period)
    df_gem_piv['lower_0'] = df_gem_piv['lower_0'].rolling(window=4,min_periods=1).mean()
    df_gem_piv['upper_1'] = df_gem_piv['upper_1'].rolling(window=4,min_periods=1).mean()
    df_gem_piv['gradient'] = (df_gem_piv['upper_1']-df_gem_piv['lower_0'])/4.9 #Divide by delta-z to calc dC/dz
    
    #Resample GEM data to 30 min averages to join with sonic data
    df_gem_30 = df_gem_piv.resample('30min').mean()
    
    #%%
    df_sonic = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/sonicData.csv')
    df_sonic['Datetime'] = pd.to_datetime(df_sonic['Datetime'],yearfirst=True)
    df_sonic.set_index('Datetime',inplace=True)
    df_sonic.columns = ['day.EST','Wspd.m/s','Wdir.deg','sigmaU','cov(u,v)',
                     'cov(uw)','sigmaV','sigmaW','T','sigmaT','Fheat']
    
    #Resample to 30 min means to merge with GEM data
    df_sonic_30 = df_sonic.resample('30min').mean()
    #%%
    #Join sonic and gem data into one file
    TK2537B_sonic_30min = df_gem_30.join(df_sonic_30)
    
    TK2537B_sonic_30min.to_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/TimeSeries/TK2537B_sonic_30min.csv')
    return
#%%
def merge_gemX_sonic_data():
     #Load files and prepare for merge
     #%%
    df_gem = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/TimeSeries/TK2537X.csv')
    df_gem['datetime'] = pd.to_datetime(df_gem['datetime'],yearfirst=True)
    df_gem.set_index('datetime',inplace=True)
    #%%
    #Create pivot table with one column for each intake
    df_gem_piv = df_gem.pivot(columns = 'flag',values = 'conc')
    df_gem_piv = df_gem_piv.drop(np.nan,axis=1)
    df_gem_piv.columns = ['1','2','3','4','5','6']
    df_gem_piv = df_gem_piv.astype(float)
    #%%
    #Apply moving average to fill in gaps, window = 24 (60 minute period)
    df_gem_piv['1'] = df_gem_piv['1'].rolling(window=24,min_periods=1).mean()
    df_gem_piv['2'] = df_gem_piv['2'].rolling(window=24,min_periods=1).mean()
    df_gem_piv['3'] = df_gem_piv['2'].rolling(window=24,min_periods=1).mean()
    df_gem_piv['4'] = df_gem_piv['2'].rolling(window=24,min_periods=1).mean()
    df_gem_piv['5'] = df_gem_piv['2'].rolling(window=24,min_periods=1).mean()
    df_gem_piv['6'] = df_gem_piv['2'].rolling(window=24,min_periods=1).mean()
    #%%
    #Resample GEM data to 30 min averages to join with sonic data
    df_gem_30 = df_gem_piv.resample('30min').mean()
    #%%
    df_sonic = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/sonicData.csv')
    df_sonic['Datetime'] = pd.to_datetime(df_sonic['Datetime'],yearfirst=True)
    df_sonic.set_index('Datetime',inplace=True)
    df_sonic.columns = ['day.EST','Wspd.m/s','Wdir.deg','sigmaU','cov(u,v)',
                     'cov(uw)','sigmaV','sigmaW','T','sigmaT','Fheat']
    
    #Resample to 30 min means to merge with GEM data
    df_sonic_30 = df_sonic.resample('30min').mean()
    
    #Join sonic and gem data into one file
    TK2537X_sonic_30min = df_gem_30.join(df_sonic_30)
    
    TK2537X_sonic_30min.to_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/TimeSeries/TK2537X_sonic_30min.csv')
    return