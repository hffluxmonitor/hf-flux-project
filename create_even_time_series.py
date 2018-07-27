# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 10:11:45 2018

@author: Timothy_Richards

Description: Create evenly spaced (5 min) time file and save as csv
"""
import os
import pandas as pd

username = os.getlogin()
#%%
#Tekran B file
def TKB_5_min_time_series():
    dataB = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/TK2537BData.csv')
    dataB['datetime'] = pd.to_datetime(dataB['datetime'])
    dataB = dataB.set_index('datetime')
    dataB = dataB.truncate(before=pd.Timestamp('2018-04-17'))
    #Drop any row that isn't type = CONT, stat == OK
    dataB = dataB[dataB['type']=='CONT']
    dataB = dataB[dataB['stat']=='OK']
    #Resample to create evenly spaced data
    dataB = dataB.resample('5T').asfreq()
    
    dataB.to_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/TimeSeries/TK2537B.csv')
    return

#Tekran X file
def TKX_2_5_min_time_series():
    dataX = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/TK2537XData.csv')
    dataX = dataX.drop('Unnamed: 0',axis=1)
    dataX['datetime'] = pd.to_datetime(dataX['date']+" " +dataX['time'],yearfirst = True)
    dataX = dataX.set_index('datetime')
    dataX = dataX.truncate(before=pd.Timestamp('2018-05-08'))
    #Drop any row that isn't type = CONT, stat == OK, flag < 7 (only 6 intakes)
    dataX = dataX[dataX['type']=='CONT']
    dataX = dataX[dataX['stat']=='OK']
    dataX = dataX[dataX['flag']<7]
    #Resample to create evenly spaced data
    dataX = dataX.resample('2.5T').asfreq()
    
    dataX.to_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/TimeSeries/TK2537X.csv')
    return
