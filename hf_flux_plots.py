# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 13:30:20 2018

@author: Timothy_Richards

Description:
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

import os
username = os.getlogin()
df = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/flux_data.csv')
df.set_index('datetime',inplace=True)
df.index = pd.to_datetime(df.index)
df['month'] = df.index.month
df['hour'] = df.index.hour
df['flux_ma'] = df['flux'].rolling(window = 30,min_periods=1).mean()

df4 = df[df['month']==4]
df5 = df[df['month']==5]
df6 = df[df['month']==6]
df7 = df[df['month']==7]
df8 = df[df['month']==8]

#import seaborn as sns
#corr = df.corr()
#sns.heatmap(corr, 
#            xticklabels=corr.columns.values,
#            yticklabels=corr.columns.values)

#fig, ax = plt.subplots(1,4,sharey=True,figsize = (15,5))
#fig.subplots_adjust(wspace=0, hspace=0)
#fig.autofmt_xdate()
#df = str("df")
#for i in range(4,8):
#    i = str(i)
#    fupper = np.ma.masked_where(int(df+i)['flux_ma'] > 0, (df+i)['flux_ma'])
#    flower = np.ma.masked_where(df+i)['flux_ma'] < 0, (df+i)['flux_ma'])
#    b = 0
#    ax[b].plot(df+str(i).index.values,fupper,color = 'green')
#    ax[b].plot(df+str(i).index.values,flower,color = 'darkorange')
    

fig, ax = plt.subplots(2,3,sharey=True,figsize = (10,5))
fig.subplots_adjust(wspace=0, hspace=0.2)
fig.autofmt_xdate()
fig.suptitle('GEM Flux',weight = 'bold')
fig.text(0.07,0.55,'GEM Flux [ng m-2 h-1]',rotation = 'vertical',
         ha = 'center',va = 'center')
fupper = np.ma.masked_where(df4['flux_ma'] > 0, df4['flux_ma'])
flower = np.ma.masked_where(df4['flux_ma'] < 0, df4['flux_ma'])
ax[0,0].plot(df4.index.values,fupper,color = 'darkblue')
ax[0,0].plot(df4.index.values,flower,color = 'red')
ax[0,0].axhline(y=0,linestyle='dotted', color = 'black')
ax[0,0].set_title('April')
fupper = np.ma.masked_where(df5['flux_ma'] > 0, df5['flux_ma'])
flower = np.ma.masked_where(df5['flux_ma'] < 0, df5['flux_ma'])
ax[0,1].plot(df5.index.values,fupper,color = 'darkblue')
ax[0,1].plot(df5.index.values,flower,color = 'red')
ax[0,1].axhline(y=0,linestyle='dotted', color = 'black')
ax[0,1].set_title('May')
fupper = np.ma.masked_where(df6['flux_ma'] > 0, df6['flux_ma'])
flower = np.ma.masked_where(df6['flux_ma'] < 0, df6['flux_ma'])
ax[0,2].plot(df6.index.values,fupper,color = 'darkblue')
ax[0,2].plot(df6.index.values,flower,color = 'red')
ax[0,2].axhline(y=0,linestyle='dotted', color = 'black')
ax[0,2].set_title('June')
fupper = np.ma.masked_where(df7['flux_ma'] > 0, df7['flux_ma'])
flower = np.ma.masked_where(df7['flux_ma'] < 0, df7['flux_ma'])
ax[1,0].plot(df7.index.values,fupper,color = 'darkblue')
ax[1,0].plot(df7.index.values,flower,color = 'red')
ax[1,0].axhline(y=0,linestyle='dotted', color = 'black')
ax[1,0].set_title('July')
fupper = np.ma.masked_where(df8['flux_ma'] > 0, df8['flux_ma'])
flower = np.ma.masked_where(df8['flux_ma'] < 0, df8['flux_ma'])
ax[1,1].plot(df8.index.values,fupper,color = 'darkblue')
ax[1,1].plot(df8.index.values,flower,color = 'red')
ax[1,1].axhline(y=0,linestyle='dotted', color = 'black')
ax[1,1].set_title('August')






