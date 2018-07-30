# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 10:28:52 2018

@author: Timothy_Richards
"""
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def B_gradient_plots(df):
    df['gradient_std'] = df['gradient']-df['gradient'].mean()
    #%%
    #Plot gradient over entire study period
    fig, ax = plt.subplots(figsize = (10,5))
    ax.plot(df['gradient'],color='red',label = 'gradient',linewidth = 0.5)
    ax.set_ylabel(r'GEM [ng $\mathrm{m^{-4}]}$')
    ax.set_title('GEM gradient over duration of study period')
    fig.autofmt_xdate()
    ax.grid(alpha=0.7)
    #%%
    #Create one figure with all sonic variables
    fig1, ax1 = plt.subplots(4,1,sharex=True,figsize = (10,5))
    ax1[0].plot(df['gradient'])
    ax1[1].plot(df['Wspd.m/s'])
    ax1[2].plot(df['T'])
    ax1[3].plot(df['Fheat'])
    #%%
    #Create datafrom with hourly means for diurnal gradient plot
    df['hour'] = df.index.hour
    df_hour = df.pivot_table(columns = 'hour',
                             values = ['lower_0','upper_1','gradient','Wspd.m/s',
                                       'Wdir.deg','T','Fheat','gradient_std'],
                                       aggfunc = 'mean').T
    
    #%%
    fig2,ax2 = plt.subplots()
    fig2.tight_layout()
    majorxLocator = MultipleLocator(2)
    ax2.xaxis.set_major_locator(majorxLocator)
    ax2.fill_between(df_hour.index.values,df_hour['gradient']-df_hour['gradient'].sem(),
                 df_hour['gradient']+df_hour['gradient'].sem(),
                alpha=0.2,color='b')
    ax2.plot(df_hour['gradient'],label = 'gradient')
    ax2.axvspan(0,5,alpha=0.2,color='gray')
    ax2.axvspan(18,24,alpha=0.2,color='gray')
    ax2.margins(0)
    ax2.grid(alpha = 0.7,axis='x')
    ax2.set_title('Diurnal GEM gradient (4/17-6/27)')
    ax2.set_xlabel('$time\/[hour]$')
    ax2.set_ylabel('$GEM_{gradient}$\n'+'[ng m$\mathregular{^-}$$\mathregular{^4}$]')
    return

