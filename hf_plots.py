# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 13:14:13 2018

@author: Timothy_Richards

Description:
"""
#%%
import pandas as pd
import fluxPlotBeforeandAfterLeafOut
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from scipy.interpolate import spline
from matplotlib.ticker import MultipleLocator
#%%
def set_style():
    plt.style.use(['grayscale'])
    matplotlib.rc("font", family="Times New Roman", size = 14)
    
def set_size(fig):
    fig.set_size_inches(12, 8)
    plt.tight_layout()
    plt.margins(0.005)

import os
username = os.getlogin()
#Prepare for plotting gradients with spike removal
df = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/flux_data.csv')
df.set_index('datetime',inplace=True)
df.index = pd.to_datetime(df.index)
df['month'] = df.index.month
df['week'] = df.index.week
df['flux_ma'] = df['flux'].rolling(window = 10).mean()
df['gradient_ma'] = df['gradient'].rolling(window = 5).mean()
df['gradient_std'] = df['gradient']-df['gradient'].mean()

#Create datafrom with hourly means for diurnal gradient plot
df['hour'] = df.index.hour
df_hour = df.pivot_table(columns = 'hour',
                         values = ['lower_0','upper_1','gradient','Wspd.m/s',
                                   'Wdir.deg','T','Fheat','gradient_std'],
                                   aggfunc = 'mean').T

#Flux vs. time
df4 = df[df['month']==4]
df5 = df[df['month']==5]
df6 = df[df['month']==6]
df7 = df[df['month']==7]
df8 = df[df['month']==8]
fig, ax = plt.subplots()
ax.plot(df4['flux_ma'],color = 'green')
ax.plot(df5['flux_ma'],color = 'yellow')
ax.plot(df6['flux_ma'],color = 'maroon')
ax.plot(df7['flux_ma'],color = 'red')
ax.plot(df8['flux_ma'],color = 'darkblue')
ax.axhline(0,linestyle='dotted')
fig.autofmt_xdate()
fig.tight_layout()

df4h = df4.pivot_table(columns = 'hour', values = ['flux_ma','gradient_ma'],aggfunc=np.mean).T
df5h = df5.pivot_table(columns = 'hour', values = ['flux_ma','gradient_ma'],aggfunc=np.mean).T
df6h = df6.pivot_table(columns = 'hour', values = ['flux_ma','gradient_ma'],aggfunc=np.mean).T
df7h = df7.pivot_table(columns = 'hour', values = ['flux_ma','gradient_ma'],aggfunc=np.mean).T
df8h = df8.pivot_table(columns = 'hour', values = ['flux_ma','gradient_ma'],aggfunc=np.mean).T
df8h = df8h.fillna(method = 'ffill') #Temporary; as of 8/10, no 9 am values for flux
#%%
fluxPlotBeforeandAfterLeafOut.gradient_leafout(df)
fluxPlotBeforeandAfterLeafOut.diurnal_leafout(df)
#%%
def B_gradient_plots():
    
    #Plot gradient over entire study period
    fig, ax = plt.subplots(figsize = (10,5))
    ax.plot(df['gradient'],color='red',label = 'gradient',linewidth = 0.5)
    ax.set_ylabel(r'GEM [ng $\mathrm{m^{-4}]}$')
    ax.set_title('GEM gradient over duration of study period')
    fig.autofmt_xdate()
    ax.grid(alpha=0.7)
    
    fig2,ax2 = plt.subplots()
    fig2.tight_layout()
    majorxLocator = MultipleLocator(2)
    ax2.xaxis.set_major_locator(majorxLocator)
    ax2.fill_between(df_hour.index.values,df_hour['gradient']+df_hour['gradient_std'],
                 df_hour['gradient']-df_hour['gradient_std'],alpha=0.2)
    ax2.plot(df_hour['gradient'],label = 'gradient')
    ax2.axvspan(0,5,alpha=0.2,color='gray')
    ax2.axvspan(18,24,alpha=0.2,color='gray')
    ax2.axhline(0,linestyle = 'dotted')
    ax2.margins(0)
    ax2.grid(alpha = 0.7,axis='x')
    ax2.set_title('Diurnal GEM gradient')
    ax2.set_xlabel('$time\/[hour]$')
    ax2.set_ylabel('$GEM_{gradient}$\n'+'[ng m$\mathregular{^-}$$\mathregular{^4}$]')
    return

#%%
def diurnal_flux_plot():
    set_style()
    fig2, ax2 = plt.subplots()
    ##Smoothline plots
    #April
    x = df4h.index.values
    y = df4h.flux_ma
    x_sm = np.array(df4h.index.values)
    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    y_smooth = spline(x, y, x_smooth)
    ax2.plot(x_smooth,y_smooth, color = 'green',label = 'April')
    
    #May
    x = df5h.index.values
    y = df5h.flux_ma
    x_sm = np.array(df5h.index.values)
    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    y_smooth = spline(x, y, x_smooth)
    ax2.plot(x_smooth,y_smooth, color = 'gold',label = 'May')
    
    #June
    x = df6h.index.values
    y = df6h.flux_ma
    x_sm = np.array(df6h.index.values)
    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    y_smooth = spline(x, y, x_smooth)
    ax2.plot(x_smooth,y_smooth, color = 'maroon',label = 'June')
    
    #July
    x = df7h.index.values
    y = df7h.flux_ma
    x_sm = np.array(df7h.index.values)
    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    y_smooth = spline(x, y, x_smooth)
    ax2.plot(x_smooth,y_smooth, color = 'red',label = 'July')
    
    #August
    x = df8h.index.values
    y = df8h.flux_ma
    x_sm = np.array(df8h.index.values)
    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    y_smooth = spline(x, y, x_smooth)
    ax2.plot(x_smooth,y_smooth, color = 'darkblue',label = 'August')
    
    #Other plot stuff
    ax2.legend()
    ax2.axhline(0,linestyle='dotted')
    ax2.set_xlabel('Hour')
    ax2.set_xticks(df4h.index.values)
    ax2.set_ylabel(r'GEM flux [ng m$\mathregular{^-}$$\mathregular{^2}$ h$\mathregular{^-}$$\mathregular{^1}$]')
    ax2.xaxis.set_major_locator(plt.MultipleLocator(2))
    ax2.set_yticks(df4h.flux_ma)
    ax2.yaxis.set_major_locator(plt.MultipleLocator(2))
    set_size(fig2)
    fig2.tight_layout()
    fig2.savefig('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/Plots/GEM_hourly_flux.jpg')

def diurnal_gradient_plot():
    set_style()
    fig3, ax3 = plt.subplots()
    ##Plot smooth lines
    #Plot April
    x = df4h.index.values
    y = df4h.gradient_ma
    x_sm = np.array(df4h.index.values)
    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    y_smooth = spline(x, y, x_smooth)
    ax3.plot(x_smooth,y_smooth, color = 'green',label = 'April')
    
    #Plot May
    x = df5h.index.values
    y = df5h.gradient_ma
    x_sm = np.array(df5h.index.values)
    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    y_smooth = spline(x, y, x_smooth)
    ax3.plot(x_smooth,y_smooth, color = 'gold',label = 'May')
    
    #June
    x = df6h.index.values
    y = df6h.gradient_ma
    x_sm = np.array(df6h.index.values)
    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    y_smooth = spline(x, y, x_smooth)
    ax3.plot(x_smooth,y_smooth, color = 'maroon',label = 'June')
    
    #July
    x = df7h.index.values
    y = df7h.gradient_ma
    x_sm = np.array(df7h.index.values)
    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    y_smooth = spline(x, y, x_smooth)
    ax3.plot(x_smooth,y_smooth, color = 'red',label = 'July')
    
    #August
    x = df8h.index.values
    y = df8h.gradient_ma
    x_sm = np.array(df8h.index.values)
    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    y_smooth = spline(x, y, x_smooth)
    ax3.plot(x_smooth,y_smooth, color = 'darkblue',label = 'August')
    
    #Set other plot stuff
    ax3.legend()
    ax3.axhline(0,linestyle='dotted')
    ax3.set_xlabel('Hour')
    ax3.set_xticks(df4h.index.values)
    ax3.set_ylabel(r'GEM gradient [ng m$\mathregular{^-}$$\mathregular{^4}$]')
    ax3.xaxis.set_major_locator(plt.MultipleLocator(2))
    set_size(fig3)
    fig3.tight_layout()
    fig3.savefig('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/Plots/GEM_hourly_gradient.jpg')
#%%
#Weekly means for flux/gradient
df_week = df.pivot_table(columns = 'week', values = ['flux_ma','gradient_ma'],aggfunc=np.mean).T

#%%
#Day vs. night gradient/flux

#%%
#Scatter plots of flux vs. envi variables (rain, soil temp, temp, wind)
#Daily flux vs. avg precip rate (mm/hour)
#Add labels and all that fun stuff
p_rates = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/PrecipData/DailyPrecip/MeanDailyPrecipRates.csv',
                           names = ['date','precip_rate_mm_hour','type_precip'],header = 0)
p_rates['date'] = pd.to_datetime(p_rates.date)
p_rates = p_rates.set_index(p_rates.date)

d_flux = df.resample('1D').mean()
d_flux = d_flux.set_index(pd.DatetimeIndex(d_flux.index))
pavg_rates = pd.merge(p_rates,d_flux, how='inner', left_index=True, right_index=True)

figP, axP = plt.subplots(figsize = (12,8),sharex=True)
axP.plot(pavg_rates['precip_rate_mm_hour'])
axP.xaxis.set_major_locator(plt.MultipleLocator(15))
axF = axP.twinx()
axF.plot(pavg_rates['flux'], color = 'red', linestyle = 'dotted')
figP.autofmt_xdate()
figP.savefig('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/Plots/DailyFlux_PrecipRates.jpg')


#%%
#Plot corrected (adjusted) flux/gradient (subtract .004 from all gradients)

#%%
#Windrose plots
 
#%%
#Plot plots
B_gradient_plots() 
diurnal_flux_plot()
diurnal_gradient_plot()


