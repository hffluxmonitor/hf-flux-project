# -*- coding: utf-8 -*-
"""
Created on Tue May 22 10:13:47 2018

@author: Timothy_Richards
"""
import numpy as np
import pandas as pd
import os

username = os.getlogin()

#%%
def qc_spike_removal(data):
    
    week_window = 2 #moving average window in weeks
    s_per_hour = 2 #Samples taken per hour
    index_window = week_window*7*24*s_per_hour #weeks*days/week*hours/day
    index_window = int(index_window/2) #Split in half (half before, half after)
    
    #Run spike removal for all columns in dataframe
    #for s in range(len(data.columns)):
    for s in range(25,26):
        f = 3.5 #want to start at 3.6, so back off one*d_step
        f_step = 0.1
        num_spikes = [1] #number to kick off loop
        print(s)
        
        #Skip "StabilityClass" and "Datetime" columns
        if np.logical_or(s == 0,s == 23):
            continue
    
        while len(num_spikes)>0:
            f+=f_step
            num_spikes = []
        
            for i in range(index_window,len(data)-index_window):
                #Compute mean and std deviation
                mean = np.nanmean(data.iloc[i-index_window:i+index_window,s])
                std = np.nanstd(data.iloc[i-index_window:i+index_window,s])
            
                for j in range(i-index_window,i+index_window):
                    if data.iloc[j,s] < mean - f*std or data.iloc[j,s]>mean + f*std:
                        num_spikes.append([j])
        
            num_spikes = np.array(num_spikes)           
            num_spikes = np.unique(num_spikes)
            num_spikes = num_spikes.astype(int)
            data.iloc[num_spikes,s] = np.nan
        
    return(data)
#%%
#Read full Hg dataset
HgData = pd.read_csv('C://Users/Timothy_Richards/Dropbox/Obrist Lab/Tekran/Raw Data/2537B_Gradient/HgCompleteDataSet.csv')
HgData.set_index('Unnamed: 0',inplace=True)

Hg01 = HgData.pivot(columns = 'flag',values = 'conc')
Hg01 = Hg01.drop(np.nan,axis=1)
Hg01.columns = ['0','1']
Hg01 = Hg01.astype(float)


#Create new dataframe with 5 min intervals over entire study period
index = Hg01.index.values
columns = ['date']
HgMA = pd.DataFrame(index = index, columns = columns)
HgMA = HgMA.join(Hg01)
HgMA.index = pd.to_datetime(HgMA.index)
HgMA = HgMA.drop('date',axis=1)
HgMA.columns = ['Lower','Upper']

#Apply moving average to fill in gaps - window = 4 (20 minutes)
HgMA['Lower'] = HgMA['Lower'].rolling(window = 4,min_periods=1).mean()
HgMA['Upper'] = HgMA['Upper'].rolling(4,min_periods=1).mean()
HgMA['Gradient'] = HgMA['Upper']-HgMA['Lower']
HgMA['dC/dz'] = HgMA['Gradient']/5 #Divide by delta-z, which is 5 m

#Resample to create 30 minute averages to apply to sonic data
Hg30min = HgMA.resample('30min').mean()
Hg30minStd = HgMA.resample('30min').std()
Hg30minStd.columns = ['0std','1std','GradientStd','dC/dzStd']
Hg30minFinal = Hg30min.join(Hg30minStd)

#FLUX CALCULATIONS (using equation from  Edwards (2005))

c = 23 #m height of canopy
z = 27.9 #m height of sonic
d = (2/3)*c #m 
rho = 1.225 #kg/m3
c_p = 1005 #J/kgK
k = 0.4
g = 9.81 #m/s2
z1 = 24.1 #m
z2 = 29 #m


sonic = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/sonicData.csv')
sonic.index = pd.to_datetime(sonic['Datetime'])
sonic = sonic.drop('Datetime',axis=1)
sonic.columns = ['day.EST','Wspd.m/s','Wdir.deg','sigmaU','cov(u,v)',
                 'cov(uw)','sigmaV','sigmaW','T','sigmaT','Fheat']

sonicInitial = sonic

#qc_spike_removal(sonic)

#Drop flux values where T>100 C (bad data)
#sonic['T'] = np.where(sonic['T']>100,np.NaN,sonic['T'])
sonic[sonic['T'] > 100] = np.nan

#friction velocity and drop data when u* < 0.17 (poorly developed turbulent cond)
sonic['u*'] = np.sqrt(-1*sonic['cov(uw)']) #m/sec

#convert T to Kelvin
sonic['T_K'] = sonic['T']+273

sonic['H'] = sonic['Fheat']*rho*c_p #Foken 2006 (Fheat is sonic heat flux in Km/s, need to convert to sensible heat flux)

#Calculate L
sonic['L'] = ((-(sonic['u*']**3)*sonic['T_K']*rho*c_p)/(k*g*(sonic['H'])))

#Calculate (z-d)/L
sonic['(z-d)/L'] = (z-d)/sonic['L']

sonic['StabilityClass'] = np.where(sonic['(z-d)/L']<-0.02,'U',
                                          (np.where(sonic['(z-d)/L']>0.02,'S',
                                               (np.where(np.logical_and(sonic['(z-d)/L']>-0.02,sonic['(z-d)/L']<0.02),'N',np.NaN)))))

##Using Edwards Flux equation
s1 = lambda x:-4.7*((z1-d)/x)
s2 = lambda x:-4.7*((z2-d)/x)
y1 = lambda x:(((1-15*((z1-d)/x)))**0.25)**2
y2 = lambda x:(((1-15*((z2-d)/x)))**0.25)**2
u1 = lambda x:2*np.log((1+y1(sonic['L']))/2)
u2 = lambda x:2*np.log((1+y2(sonic['L']))/2)

sonic['psi1'] = np.where(sonic['StabilityClass']=="S",s1(sonic['L']),
                                  (np.where(sonic['StabilityClass']=="U",u1(sonic['L']),'0')))
sonic['psi2'] = np.where(sonic['StabilityClass']=="S",s2(sonic['L']),
                                  (np.where(sonic['StabilityClass']=="U",u2(sonic['L']),'0')))
sonic['psi1'] = sonic['psi1'].astype(float)
sonic['psi2'] = sonic['psi2'].astype(float)


#Resample with 30 min means to use with Hg data
sonic30min = sonic.resample('30min').mean()

#Reclassify stability
##Stable: > 0.02
##Unstable < -0.02
##Neutral -0.02<z-d/L<0.02   
sonic30min['StabilityClass'] = np.where(sonic30min['(z-d)/L']<-0.02,'U',
                                          (np.where(sonic30min['(z-d)/L']>0.02,'S',
                                               (np.where(np.logical_and(sonic30min['(z-d)/L']>-0.02,sonic30min['(z-d)/L']<0.02),'N',np.NaN)))))                        
          
#join with Hg data
sonicHg30min = Hg30min.join(sonic30min)

sonicHg30min['GEMAvgConc'] = (sonicHg30min['Lower']+sonicHg30min['Upper'])/2

#Calculate flux using Edwards equation
a = (z2-d)/(z1-d)
sonicHg30min['Flux'] = (-(sonicHg30min['u*']*k*sonicHg30min['Gradient'])/(np.log(a)-sonicHg30min['psi2']+sonicHg30min['psi1']))*60*60

sonicHg30min = sonicHg30min.reset_index()

#%%    
sonicHg30min = qc_spike_removal(sonicHg30min)
sonicHg30min.to_csv('C://Users/Timothy_Richards/Documents/sonicHg30min.csv')
#%%
sonicHg30min['Flux'].plot()