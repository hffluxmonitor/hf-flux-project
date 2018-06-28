# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 16:33:24 2018

@author: Timothy_Richards2
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('TK2537BFull.csv')

df['datetime'] = pd.to_datetime(df['datetime'])
df.set_index('datetime',inplace=True)

dfA = df[df['cart']=='A']
dfB = df[df['cart']=='B']

dfA01 = dfA.pivot(columns = 'flag', values = 'conc')
dfA01.columns = ['0','1']
dfA01 = dfA01.resample('1H').mean()
dfA01['gradient'] = (dfA01['1']-dfA01['0'])/5.1
dfA01['hour'] = dfA01.index.hour

dfAhour = dfA01.pivot_table(columns = 'hour', values = 'gradient',aggfunc=np.mean).T

dfB01 = dfB.pivot(columns = 'flag', values = 'conc')
dfB01.columns = ['0','1']
dfB01 = dfB01.resample('1H').mean()
dfB01['gradient'] = (dfB01['1']-dfB01['0'])/5.1
dfB01['hour'] = dfB01.index.hour
dfBhour = dfB01.pivot_table(columns = 'hour', values = 'gradient',aggfunc=np.mean).T


plt.plot(dfA01['gradient'])
plt.plot(dfB01['gradient'],color='red')

fig, ax = plt.subplots(2,1,sharex=True,sharey=True)
ax[0].plot(dfAhour['gradient'],color = 'blue',label = 'A')
ax[0].legend()
ax[1].plot(dfBhour['gradient'],color = 'red', label = 'B')
ax[1].legend()