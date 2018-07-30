# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 11:15:49 2018

@author: Timothy_Richards
"""
import pandas as pd
import matplotlib.pyplot as plt

sonic = pd.read_csv('C://Users/Timothy_Richards/Documents/sonicHg30min.csv')
sonic['Datetime'] = pd.to_datetime(sonic['day.EST'],unit='d')
sonic['Datetime'] = sonic['Datetime'] + pd.DateOffset(years=48, days = -1)
sonic.set_index('Datetime',inplace=True)

sonic30m = sonic.resample('30min').mean()
sonic30mwind = sonic30m[['Wspd.m/s','Wdir.deg']]

Hg = pd.read_csv('C://Users/Timothy_Richards/Documents/Hg/HgMA.csv')
Hg['Datetime'] = pd.to_datetime(Hg['Unnamed: 0'])
Hg.set_index('Datetime',inplace=True)
Hg30m = Hg.resample('30min').mean()

windData = Hg30m.join(sonic30mwind)

windData.plot.scatter('Wspd.m/s','Lower')
windData.plot.scatter('Wspd.m/s','Upper')


windData['Wspd.m/s'].plot.box()

fig, ax = plt.subplots()

plt.scatter(windData['Wspd.m/s'],windData['Lower'],s = windData['Lower']*50)



                      
windData.to_csv('C://Users/Timothy_Richards/Documents/WindData/WindHg.csv')