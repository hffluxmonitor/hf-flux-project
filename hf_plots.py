# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 13:14:13 2018

@author: Timothy_Richards

Description:
"""
#%%
import pandas as pd
import fluxPlotBeforeandAfterLeafOut
import TK2537B_gradient_plots
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
#%%
def set_style():
    plt.style.use(['grayscale'])
    matplotlib.rc("font", family="Times New Roman")
    
def set_size(fig):
    fig.set_size_inches(7, 4)
    plt.tight_layout()
    plt.margins(0.005)

import os
username = os.getlogin()
#Prepare for plotting gradients with spike removal
df = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/flux_data.csv')
df.set_index('datetime',inplace=True)
df.index = pd.to_datetime(df.index)
df['month'] = df.index.month
df['flux_ma'] = df['flux'].rolling(window = 10).mean()
#%%
fluxPlotBeforeandAfterLeafOut.gradient_leafout(df)
fluxPlotBeforeandAfterLeafOut.diurnal_leafout(df)
#%%
TK2537B_gradient_plots.B_gradient_plots(df)
#%%
#Flux vs. time
df4 = df[df['month']==4]
df5 = df[df['month']==5]
df6 = df[df['month']==6]
df7 = df[df['month']==7]
fig, ax = plt.subplots()
ax.plot(df4['flux_ma'],color = 'green')
ax.plot(df5['flux_ma'],color = 'yellow')
ax.plot(df6['flux_ma'],color = 'maroon')
ax.plot(df7['flux_ma'],color = 'red')
fig.autofmt_xdate()

df4h = df4.pivot_table(columns = 'hour', values = 'flux_ma',aggfunc=np.mean).T
df5h = df5.pivot_table(columns = 'hour', values = 'flux_ma',aggfunc=np.mean).T
df6h = df6.pivot_table(columns = 'hour', values = 'flux_ma',aggfunc=np.mean).T
df7h = df7.pivot_table(columns = 'hour', values = 'flux_ma',aggfunc=np.mean).T

set_style()
fig2, ax2 = plt.subplots()
ax2.plot(df4h.flux_ma, color = 'green',label = 'April')
ax2.plot(df5h.flux_ma, color = 'gold',label = 'May')
ax2.plot(df6h.flux_ma, color = 'maroon',label = 'June')
ax2.plot(df7h.flux_ma, color = 'red',label = 'July')
ax2.legend()
ax2.set_xlabel('Hour')
ax2.set_xticks(df4h.index.values)
ax2.set_ylabel(r'GEM flux [ng m$\mathregular{^-}$$\mathregular{^2}$ h$\mathregular{^-}$$\mathregular{^1}$]')
ax2.xaxis.set_major_locator(plt.MultipleLocator(2))
ax2.set_yticks(df4h.flux_ma)
ax2.yaxis.set_major_locator(plt.MultipleLocator(2))
set_size(fig2)
fig2.tight_layout()

