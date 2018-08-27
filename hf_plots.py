# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 13:14:13 2018
@author: Timothy_Richards
Description:
"""
#%%
import pandas as pd
#import fluxPlotBeforeandAfterLeafOut
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from scipy.interpolate import spline
from matplotlib.ticker import MultipleLocator
from numpy.polynomial.polynomial import polyfit
import statsmodels.api as sm
import seaborn as sns
from scipy import stats
#%%
#['seaborn-ticks',
# 'seaborn-talk',
# 'seaborn-darkgrid',
# 'seaborn-dark-palette',
# 'fivethirtyeight',
# 'seaborn-white',
# 'seaborn-muted',
# 'seaborn-bright',#
# 'bmh',
# 'seaborn-whitegrid',
# 'seaborn-pastel',
# 'classic',
# 'ggplot',
# 'seaborn-deep',
# 'seaborn-poster',
# 'seaborn-colorblind',
# 'seaborn-paper',
# 'seaborn-notebook',
# 'seaborn-dark',
# 'grayscale',
# 'dark_background']

def set_style():
    plt.style.use(['classic'])
    matplotlib.rc("font", family="Times New Roman", size = 10)
    
def set_size(fig):
    fig.set_size_inches(8, 5)
    plt.tight_layout()
    plt.margins(0.005)
    
def set_windrose_style():
    plt.style.use(['fivethirtyeight'])

import os
username = os.getlogin()
#Prepare for plotting gradients with spike removal
df = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/flux_data.csv')
df.set_index('datetime',inplace=True)
df.index = pd.to_datetime(df.index)
df = df.drop('Unnamed: 0',axis = 1)
df['month'] = df.index.month
df['week'] = df.index.week
df['flux_ma'] = df['flux'].rolling(window = 10).mean()
df['gradient_ma'] = df['gradient'].rolling(window = 5).mean()
df['gradient_std'] = df['gradient'].rolling(window = 10, min_periods=1).std()
df['gradient_adj'] = df['gradient'] - .004

#Create datafromes with hourly means for diurnal gradient plot
df['hour'] = df.index.hour
df_hour = df.pivot_table(columns = 'hour',
                         values = ['lower_0','upper_1','gradient','Wspd.m/s',
                                   'Wdir.deg','T','Fheat','gradient_std',
                                   'gradient_adj','flux'],
                                   aggfunc = 'mean').T

#Create dataframes for each month
d = {}
months = {'df_4','df_5','df_6','df_7','df_8'}  
  
for m in months:
    d[m] = pd.DataFrame()
    d[m] = df[df['month']== int(m.split(sep='_')[1])]    

dfh = df.pivot_table(columns = 'hour', values = ['flux_ma','gradient_ma','gradient_adj'],aggfunc=np.mean).T
df4h = d['df_4'].pivot_table(columns = 'hour', values = ['flux_ma','gradient_ma','gradient_adj'],aggfunc=np.mean).T
df5h = d['df_5'].pivot_table(columns = 'hour', values = ['flux_ma','gradient_ma','gradient_adj'],aggfunc=np.mean).T
df6h = d['df_6'].pivot_table(columns = 'hour', values = ['flux_ma','gradient_ma','gradient_adj'],aggfunc=np.mean).T
df7h = d['df_7'].pivot_table(columns = 'hour', values = ['flux_ma','gradient_ma','gradient_adj'],aggfunc=np.mean).T
df8h = d['df_8'].pivot_table(columns = 'hour', values = ['flux_ma','gradient_ma','gradient_adj'],aggfunc=np.mean).T
df8h = df8h.fillna(method = 'ffill') #Temporary; as of 8/10, no 9 am values for flux

#Get daily precip rates
p_rates = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/PrecipData/DailyPrecip/MeanDailyPrecipRates.csv',
                      names = ['date','rate_mm_hour','type','sunrise','sunset'],header = 0)
p_rates['date'] = pd.to_datetime(p_rates.date)
p_rates = p_rates.set_index(p_rates.date)

#create daily flux df and merge it with p_rates
d_flux = df.resample('1D').mean()
d_flux = d_flux.set_index(pd.DatetimeIndex(d_flux.index))
pavg_rates = pd.merge(p_rates,d_flux, how='inner', left_index=True, right_index=True)

def GEM_flux():
    #Flux vs. time
    set_style()
    fig, ax = plt.subplots()
    ax.plot(d['df_4']['flux_ma'])
    ax.plot(d['df_5']['flux_ma'])
    ax.plot(d['df_6']['flux_ma'])
    ax.plot(d['df_7']['flux_ma'])
    ax.plot(d['df_8']['flux_ma'])
    ax.axhline(0,linestyle='dotted')
    ax.set_ylabel(r'GEM flux [ng m$\mathregular{^-}$$\mathregular{^2}$ h$\mathregular{^-}$$\mathregular{^1}$]')
    set_size(fig)
    fig.autofmt_xdate()
    fig.tight_layout()
#%%
#fluxPlotBeforeandAfterLeafOut.gradient_leafout(df)
#fluxPlotBeforeandAfterLeafOut.diurnal_leafout(df)
#%%
def B_gradient_plots():
    
    #Plot gradient over entire study period
    fig, ax = plt.subplots(figsize = (6,4))
    ax.plot(df['gradient'],label = 'gradient',linewidth = 0.5)
    ax.set_ylabel(r'GEM [ng $\mathrm{m^{-4}]}$')
    ax.set_title('GEM gradient')
    fig.autofmt_xdate()
    ax.grid(alpha=0.7)
    
    fig2,ax2 = plt.subplots(figsize = (6,4))
    fig2.tight_layout()
    majorxLocator = MultipleLocator(2)
    ax2.xaxis.set_major_locator(majorxLocator)
    ax2.plot(df_hour['gradient'], marker = 'o')
    #ax2.errorbar(df_hour.index.values, df_hour['gradient'],
    #             yerr=df_hour.gradient_std,
    #            ls='--', marker='o',
    #            capsize=5, capthick=1, ecolor='black',fillstyle='full')
    ax2.fill_between(df_hour.index.values,df_hour.gradient+df_hour.gradient_std,
                     df_hour.gradient-df_hour.gradient_std,alpha = 0.3)
    ax2.axvspan(0,5,alpha=0.2,color='gray')
    ax2.axvspan(18,24,alpha=0.2,color='gray')
    ax2.axhline(0,linestyle = 'dotted')
    ax2.margins(0)
    ax2.grid(alpha = 0.7,axis='x')
    ax2.set_title('Diurnal GEM gradient')
    ax2.set_xlabel('time [h]')
    ax2.set_xlim(0,23)
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
    ax2.plot(x_smooth,y_smooth,label = 'April')
    
    #May
    x = df5h.index.values
    y = df5h.flux_ma
    x_sm = np.array(df5h.index.values)
    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    y_smooth = spline(x, y, x_smooth)
    ax2.plot(x_smooth,y_smooth,label = 'May')
    
    #June
    x = df6h.index.values
    y = df6h.flux_ma
    x_sm = np.array(df6h.index.values)
    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    y_smooth = spline(x, y, x_smooth)
    ax2.plot(x_smooth,y_smooth,label = 'June')
    
    #July
    x = df7h.index.values
    y = df7h.flux_ma
    x_sm = np.array(df7h.index.values)
    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    y_smooth = spline(x, y, x_smooth)
    ax2.plot(x_smooth,y_smooth,label = 'July')
    
    #August
    x = df8h.index.values
    y = df8h.flux_ma
    x_sm = np.array(df8h.index.values)
    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    y_smooth = spline(x, y, x_smooth)
    ax2.plot(x_smooth,y_smooth,label = 'August')
    
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
    fig2.savefig('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/Plots/GEM_hourly_flux.pdf')

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
    ax3.plot(x_smooth,y_smooth,label = 'April')
    
    #Plot May
    x = df5h.index.values
    y = df5h.gradient_ma
    x_sm = np.array(df5h.index.values)
    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    y_smooth = spline(x, y, x_smooth)
    ax3.plot(x_smooth,y_smooth,label = 'May')
    
    #June
    x = df6h.index.values
    y = df6h.gradient_ma
    x_sm = np.array(df6h.index.values)
    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    y_smooth = spline(x, y, x_smooth)
    ax3.plot(x_smooth,y_smooth,label = 'June')
    
    #July
    x = df7h.index.values
    y = df7h.gradient_ma
    x_sm = np.array(df7h.index.values)
    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    y_smooth = spline(x, y, x_smooth)
    ax3.plot(x_smooth,y_smooth,label = 'July')
    
    #August
    x = df8h.index.values
    y = df8h.gradient_ma
    x_sm = np.array(df8h.index.values)
    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    y_smooth = spline(x, y, x_smooth)
    ax3.plot(x_smooth,y_smooth,label = 'August')
    
    #Set other plot stuff
    ax3.legend()
    ax3.axhline(0,linestyle='dotted')
    ax3.set_xlabel('Hour')
    ax3.set_xticks(df4h.index.values)
    ax3.set_ylabel(r'GEM gradient [ng m$\mathregular{^-}$$\mathregular{^4}$]')
    ax3.xaxis.set_major_locator(plt.MultipleLocator(2))
    set_size(fig3)
    fig3.tight_layout()
    fig3.savefig('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/Plots/GEM_hourly_gradient.pdf')
#%%
#Weekly means for flux/gradient
def weekly_fluxgradient():
    df_week = df.pivot_table(columns = 'week', values = ['flux_ma','gradient_ma'],aggfunc=np.mean).T
    df_week['flux_std'] = df_week['flux_ma'].rolling(window = 5, min_periods=1).std()
    
    set_style()
    figW, axW = plt.subplots()
    axW.plot(df_week.index.values, df_week.flux_ma,label = 'Flux')
    axW.fill_between(df_week.index.values,df_week.flux_ma+df_week.flux_std,
                     df_week.flux_ma-df_week.flux_std,alpha = 0.3)
    axW.xaxis.set_major_locator(plt.MultipleLocator(2))
    axY = axW.twinx()
    axY.plot(df_week.index.values, df_week.gradient_ma, color = 'orange',label = 'Gradient')
    axW.set_xlabel('Week of year')
    axW.set_ylabel('Flux')
    axY.set_ylabel('Gradient')
    figW.tight_layout()
    figW.legend()

#%%
#Day vs. night gradient/flux
#Convert time (UTC) to EDT (UTC-4)
avg_sunrise = np.nanmean(pavg_rates.sunrise)
avg_sunrise = pd.to_datetime(avg_sunrise, unit = 's') - pd.Timedelta('04:00:00')
avg_sunset = np.nanmean(pavg_rates.sunset)
avg_sunset = pd.to_datetime(avg_sunset, unit = 's') - pd.Timedelta('04:00:00')



#%%
#Scatter plots of flux vs. envi variables (rain, soil temp, temp, wind)
#Daily flux vs. avg precip rate (mm/hour)
#Add labels and all that fun stuff
def flux_precip():
    set_style()    
    
    figP, axF = plt.subplots(figsize = (12,8),sharex=True)
    axF.plot(pavg_rates.index.values,pavg_rates['flux'], color = 'black', linestyle = 'solid', linewidth = 1.5, marker = 'o', markersize = 4)
    axF.set_ylabel(r'GEM flux [ng m$\mathregular{^-}$$\mathregular{^2}$ h$\mathregular{^-}$$\mathregular{^1}$]')
    axF.axhline(0,color = 'black', linestyle = 'dashed', alpha = 0.7)
    axF.xaxis.set_major_locator(plt.MultipleLocator(15))
    axP = axF.twinx()
    axP.plot(pavg_rates['rate_mm_hour'], linestyle = 'dashed',linewidth = 1.5, color = 'blue', alpha = 0.6)
    axP.set_ylabel(r'Liquid precipitation rate [mm h$\mathregular{^-}$$\mathregular{^1}$]', color = 'blue')
    axP.set_title('GEM flux vs mean precipitation rate')
    axP.axvspan('2018-06-23 00:00:00','2018-08-14 00:00:00', color = 'yellow', alpha = 0.1)
    figP.autofmt_xdate()
    set_size(figP)
    figP.tight_layout()
    figP.savefig('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/Plots/DailyFlux_PrecipRates.pdf')
    


#%%
#Plot corrected (adjusted) flux/gradient (subtract .004 from all gradients)
set_style()
fig3, ax3 = plt.subplots()
##Plot smooth lines
#Plot April
x = df4h.index.values
y = df4h.gradient_adj
x_sm = np.array(df4h.index.values)
x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
y_smooth = spline(x, y, x_smooth)
ax3.plot(x_smooth,y_smooth,label = 'April',linestyle = 'dashed')

#Plot May
x = df5h.index.values
y = df5h.gradient_adj
x_sm = np.array(df5h.index.values)
x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
y_smooth = spline(x, y, x_smooth)
ax3.plot(x_smooth,y_smooth,label = 'May',linestyle = 'dashed')

#June
x = df6h.index.values
y = df6h.gradient_adj
x_sm = np.array(df6h.index.values)
x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
y_smooth = spline(x, y, x_smooth)
ax3.plot(x_smooth,y_smooth,label = 'June',linestyle = 'dashed')

#July
x = df7h.index.values
y = df7h.gradient_adj
x_sm = np.array(df7h.index.values)
x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
y_smooth = spline(x, y, x_smooth)
ax3.plot(x_smooth,y_smooth,label = 'July', linestyle = 'dashed')

#August
x = df8h.index.values
y = df8h.gradient_adj
x_sm = np.array(df8h.index.values)
x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
y_smooth = spline(x, y, x_smooth)
ax3.plot(x_smooth,y_smooth,label = 'August', linestyle = 'dashed')

#Set other plot stuff
ax3.legend()
ax3.axhline(0,linestyle='dotted')
ax3.set_xlabel('Hour')
ax3.set_xticks(df4h.index.values)
ax3.set_ylabel(r'GEM adjusted gradient [ng m$\mathregular{^-}$$\mathregular{^4}$]')
ax3.xaxis.set_major_locator(plt.MultipleLocator(2))
set_size(fig3)
fig3.tight_layout()

#%%
#Plot flux, gradient, adjusted diurnal over entire time period

fig4, ax4 = plt.subplots()
ax4.plot(dfh['flux_ma'])

fig5, ax5 = plt.subplots()
ax5.plot(dfh['gradient_ma'])
ax5.plot(dfh['gradient_adj'],linestyle='dashed')


#%%
#Windrose plots
def windrose():
    from windrose import plot_windrose,WindroseAxes
    import matplotlib.cm as cm
    
    set_windrose_style()
    ws = df['Wspd.m/s'].ffill()
    wd = df['Wdir.deg'].ffill()
    conc = df['GEM_avg_conc'].ffill()
    dfW = pd.DataFrame({'speed': ws, 'direction': wd, 'conc': conc})
    plot_windrose(dfW, kind='contourf', bins=np.arange(0.01,8,1), cmap=cm.hot, lw=3)
    
    ax = WindroseAxes.from_ax()
    ax.bar(dfW.direction, dfW.conc, normed=True, opening=0.8, edgecolor='white')
    ax.set_legend()
    
    plot_windrose(dfW, kind='contourf', var_name='conc', direction_name='direction',
                  bins=np.arange(0.01,dfW.conc.max(),0.2))
    
#%%
#Scatter plots
def scatter_windspd():
    set_style()
    figS, axS = plt.subplots()
    x = df['Wspd.m/s'].ffill()
    y = df.GEM_avg_conc.ffill()
    axS.set_xlabel(r'Wind speed - m s$\mathregular{^-}$$\mathregular{^1}$')
    axS.set_ylabel(r'GEM concentration - ng m$\mathregular{^-}$$\mathregular{^3}$')    
    figS.tight_layout()
    
    p = sns.regplot(x,y,ci=68)
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    r_squared = r_value**2
    
    p.axes.text(0.7,0.9,'r-squared = '+ str(round(r_squared,4)),transform = p.axes.transAxes,
                fontsize = 14)
    
    figS.savefig('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/Plots/scatter_flux_windspd.pdf')
    
def scatter_preciprate():
    set_style()
    figSP, axSP = plt.subplots()
    x = pavg_rates['rate_mm_hour'].ffill()
    y = pavg_rates.GEM_avg_conc.ffill()
    axSP.set_xlabel(r'Liquid precipitation rate - mm h$\mathregular{^-}$$\mathregular{^1}$')
    axSP.set_ylabel(r'GEM concentration - ng m$\mathregular{^-}$$\mathregular{^3}$')    
    figSP.tight_layout()
    p = sns.regplot(x,y,dropna=True)
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    r_squared = r_value**2
    
    p.axes.text(0.7,0.9,'r-squared = '+ str(round(r_squared,4)),transform = p.axes.transAxes,
                fontsize = 14)
    
    figSP.savefig('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/Plots/scatter_flux_windspd.pdf')
    
def scatter_flux_micro():
    #Scatter Plots
    set_style()
    figScat, ax = plt.subplots(4,sharex=True,figsize = (9,9))
    
    ax[3].scatter(df.index.values,df['flux'],color='r',s=3)
    ax[3].set_ylabel('GEM Flux (ng m$\mathregular{^-}$$\mathregular{^2}$ h$\mathregular{^-}$$\mathregular{^1}$)',
                      color = 'r')
    ax[0].set_xlim(df.index.values.min(),df.index.values.max())
    ax[0].scatter(df.index.values,df['H'],color='orange',s=1)
    ax[0].yaxis.set_label_position("right")
    ax[1].set_ylabel('Air Temperature (K)',color = 'purple')
    ax[1].scatter(df.index.values,df['T_K'],color='purple',s=1)
    ax[2].set_ylabel('GEM Concentration (ng m$\mathregular{^-}$$\mathregular{^3}$)',color = 'darkgreen')
    ax[2].scatter(df.index.values,df['GEM_avg_conc'],color='darkgreen',s=1)
    ax[0].set_ylabel('Heat Flux (W m$\mathregular{^-}$$\mathregular{^2}$)',color = 'orange')
    ax[2].yaxis.set_label_position("right")
    figScat.autofmt_xdate()
    
    figScat.savefig('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/Plots/scatter_flux_micro.pdf')
 
#%%
#Boxplots
def flux_boxplot():
    set_style()
    figB, axB = plt.subplots()
    
    axB = sns.boxplot(x="hour", y="flux",
                data=df)
    axB.plot(df_hour.index.values,df_hour.flux,color = 'white',linestyle = 'dashed',
             linewidth = 3,marker = 'o')
    figB.savefig('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/Plots/box_flux_hourly.pdf')


#%%
#Plot plots
GEM_flux()
B_gradient_plots() 
diurnal_flux_plot()
diurnal_gradient_plot()
flux_precip()
windrose()
scatter_windspd()
scatter_preciprate()
flux_boxplot()
scatter_flux_micro()
weekly_fluxgradient()

mu = df['flux'].mean()
sigma2 = df['flux'].std()
num_bins = 50

fig, ax = plt.subplots()
# the histogram of the data
n, bins, patches = ax.hist(df['flux'], num_bins, density=1, range=(np.nanmin(df['flux']),np.nanmax(df['flux'])))
# add a 'best fit' line
y = ((1 / (np.sqrt(2 * np.pi) * sigma2)) *
     np.exp(-0.5 * (1 / sigma2 * (bins - mu))**2))
ax.plot(bins, y, '--')
ax.set_xlabel('GEM Flux [ng m-2 h-1]')
ax.set_ylabel('Probability density')
# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.show()




