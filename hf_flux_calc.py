# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 08:33:38 2018

@author: Timothy_Richards
"""
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import FluxSpikeRemoval

username = os.getlogin()

c = 23 #m height of canopy
z = 27.9 #m height of sonic
d = (2/3)*c #m 
rho = 1.225 #kg/m3
c_p = 1005 #J/kgK
k = 0.4
g = 9.81 #m/s2
z1 = 24.1 #m
z2 = 29 #m

def calc_micromet_vars(df):
    df['u*'] = np.sqrt(-1*df['cov(uw)']) #m/sec
    #convert T to Kelvin
    df['T_K'] = df['T']+273
    
    df['H'] = df['Fheat']*100 #obviously not correct, but sensible heat flux seems to be off by factor of 100
    
    #Calculate L
    df['L'] = ((-(df['u*']**3)*df['T_K']*rho*c_p)/(k*g*(df['H'])))
    
    #Calculate (z-d)/L
    df['(z-d)/L'] = (z-d)/df['L']
    
    df['StabilityClass'] = np.where(df['(z-d)/L']<-0.02,'U',
                                              (np.where(df['(z-d)/L']>0.02,'S',
                                                   (np.where(np.logical_and(df['(z-d)/L']>-0.02,df['(z-d)/L']<0.02),'N',np.NaN)))))
    
    ##Using Edwards Flux equation
    s1 = lambda x:-4.7*((z1-d)/x)
    s2 = lambda x:-4.7*((z2-d)/x)
    y1 = lambda x:(((1-15*((z1-d)/x)))**0.25)**2
    y2 = lambda x:(((1-15*((z2-d)/x)))**0.25)**2
    u1 = lambda x:2*np.log((1+y1(df['L']))/2)
    u2 = lambda x:2*np.log((1+y2(df['L']))/2)
    
    df['psi1'] = np.where(df['StabilityClass']=="S",s1(df['L']),
                                      (np.where(df['StabilityClass']=="U",u1(df['L']),'0')))
    df['psi2'] = np.where(df['StabilityClass']=="S",s2(df['L']),
                                      (np.where(df['StabilityClass']=="U",u2(df['L']),'0')))
    df['psi1'] = df['psi1'].astype(float)
    df['psi2'] = df['psi2'].astype(float)
    df_flux = df
    
    df_flux['GEM_avg_conc'] = (df_flux['lower_0']+df_flux['upper_1'])/2
    return df_flux

def qc_data(df):
    #Drop values where T>50 C (bad data)
    df[df['T'] > 50] = np.nan
    
    #friction velocity and drop data when u* < 0.17 (poorly developed turbulent cond)
    df[df['u*'] < 0.17] = np.nan
    
    return df
def flux_calc(df):
    df_flux = calc_micromet_vars(df)
    df_flux = qc_data(df_flux)
    a = (z2-d)/(z1-d)
    df_flux['flux'] = (-(df_flux['u*']*k*df_flux['gradient'])/(np.log(a)-df_flux['psi2']+df_flux['psi1']))*60*60
    df_flux = FluxSpikeRemoval.qc_spike_removal(df_flux,23) #flux
    df_flux = FluxSpikeRemoval.qc_spike_removal(df_flux,16) #H
    df_flux = FluxSpikeRemoval.qc_spike_removal(df_flux,22) #GEM avg conc
    
    return df_flux

if __name__ == "__main__":
    df = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/TimeSeries/TK2537B_sonic_30min.csv')
    df.index = pd.to_datetime(df['datetime'])
    df = df.drop('datetime',axis=1)
    df_flux = flux_calc(df)
    df_flux.to_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/flux_data.csv')
    #%%
    plt.plot(df_flux['flux'])
    #%%
    mu = df_flux['flux'].mean()
    sigma2 = df_flux['flux'].std()
    num_bins = 50
    
    fig, ax = plt.subplots()
    # the histogram of the data
    n, bins, patches = ax.hist(df_flux['flux'], num_bins, density=1, range=(np.nanmin(df_flux['flux']),np.nanmax(df_flux['flux'])))
    # add a 'best fit' line
    y = ((1 / (np.sqrt(2 * np.pi) * sigma2)) *
         np.exp(-0.5 * (1 / sigma2 * (bins - mu))**2))
    ax.plot(bins, y, '--')
    ax.set_xlabel('GEM Flux [ng m-2 h-1]')
    ax.set_ylabel('Probability density')
    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    plt.show()
    #%%
    #Scatter Plots
    figScat, ax = plt.subplots(4,sharex=True,figsize = (9,9))
    
    ax[3].scatter(df_flux.index.values,df_flux['flux'],color='r',s=3)
    ax[3].set_ylabel('GEM Flux (ng m$\mathregular{^-}$$\mathregular{^2}$ h$\mathregular{^-}$$\mathregular{^1}$)',
                      color = 'r')
    ax[0].set_xlim(df_flux.index.values.min(),df_flux.index.values.max())
    ax[0].scatter(df_flux.index.values,df_flux['H'],color='orange',s=1)
    ax[0].yaxis.set_label_position("right")
    ax[1].set_ylabel('Air Temperature (K)',color = 'purple')
    ax[1].scatter(df_flux.index.values,df_flux['T_K'],color='purple',s=1)
    ax[2].set_ylabel('GEM Concentration (ng m$\mathregular{^-}$$\mathregular{^3}$)',color = 'darkgreen')
    ax[2].scatter(df_flux.index.values,df_flux['GEM_avg_conc'],color='darkgreen',s=1)
    ax[0].set_ylabel('Heat Flux (W m$\mathregular{^-}$$\mathregular{^2}$)',color = 'orange')
    ax[2].yaxis.set_label_position("right")
    figScat.autofmt_xdate()
    #%%
    bLeaf = df_flux.ix['2018-04-17':'2018-05-01'] #prior to leaf out
    aLeaf = df_flux.ix['2018-06-13':'2018-06-27'] #two most recent weeks
        
    bLeaf['hour'] = bLeaf.index.hour
    bLeaf_hour = bLeaf.pivot_table(columns = 'hour',
                         values = ['lower_0','upper_1','gradient','Wspd.m/s',
                                   'Wdir.deg','T','Fheat','u*','T_K',
                                   'H','L','(z-d)/L','StabilityClass','psi1',
                                   'psi2','GEM_avg_conc','flux'],
                                   aggfunc = 'mean').T
                                    
    aLeaf['hour'] = aLeaf.index.hour
    aLeaf_hour = aLeaf.pivot_table(columns = 'hour',
                         values = ['lower_0','upper_1','gradient','Wspd.m/s',
                                   'Wdir.deg','T','Fheat','u*','T_K',
                                   'H','L','(z-d)/L','StabilityClass','psi1',
                                   'psi2','GEM_avg_conc','flux'],
                                   aggfunc = 'mean').T
        
    fig2,ax2 = plt.subplots(2,1,sharex=True)
    ax2[0].set_title("Diurnal above canopy GEM flux before and after leaf-out")
    ax2[0].plot(bLeaf_hour['flux'],linewidth=2,label = "Before Leaf-out")
    ax2[0].axvspan(0,5,alpha=0.2,color='gray')
    ax2[0].axvspan(18,24,alpha=0.2,color='gray')
    ax2[0].set_ylabel('$GEM_{gradient}$\n'+'[ng m$\mathregular{^-}$$\mathregular{^4}$]')
    ax2[1].set_ylabel('$GEM_{gradient}$\n'+'[ng m$\mathregular{^-}$$\mathregular{^4}$]')
    ax2[1].margins(0)
        
    ax2[1].plot(aLeaf_hour['flux'],color = 'r',linewidth = 2,
       label = "After Leaf-out")
    ax2[1].axvspan(0,5,alpha=0.2,color='gray')
    ax2[1].axvspan(18,24,alpha=0.2,color='gray')
    ax2[0].legend()
    ax2[1].legend()
    ax2[1].set_xlabel('$time\/[hour]$')
    fig2.tight_layout()