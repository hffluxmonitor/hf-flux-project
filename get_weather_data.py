# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 07:10:48 2018
@author: FluxMonitor
Description: Uses Dark Sky API to request historical weather data
"""
import pandas as pd
import numpy as np
from rapidconnect import RapidConnect
import datetime as dt
import os

username = os.getlogin()
rapid = RapidConnect("default-application_5b72b75fe4b02799e7f62892", "4df23935-0f28-4bd5-9eb1-0e8d7b021f78")

today = pd.to_datetime(dt.datetime.now().strftime('%y-%m-%d 00:00:00'),yearfirst = True)
today = today
date_range = pd.date_range('2018-04-17 00:00:00',today)
date_range_hourly = pd.date_range('2018-04-17 00:00:00','2018-04-20 00:00:00',freq = '1h')
precip = pd.DataFrame(index = date_range,columns = ['date','precip_rate_mm_hour','precip_type'])
daily_precip = pd.DataFrame(index = date_range,columns = ['precip_avg_rate_mm_hour','precip_type'])
hourly_precip = pd.DataFrame(index = date_range_hourly, columns = ['precip_rate_mm_hour','precip_type'])

for i in date_range:
    print(i)

for d in date_range:
    result = rapid.call('Darksky', 'getTimeMachineRequest', { 
    	'apiKey': 'c230f720cf53566b8f33657451e694d3',
    	'time': d,
    	'coordinates': '42.5315, -72.1899',
       'units': 'si'
    })
    
    #Get hourly precip data from date
    df = pd.DataFrame(index = range(0,24),columns = ['date','precip_rate_mm_hour','precip_type'])
    unix_date = result.get('currently').get('time')
    
    for item in result['hourly'].items():
        h_data = item
    
    for item in result['daily'].items():
        d_data = item
    
    i = 0 #initialize loop
    for i in range(0,24):
        df.loc[i,'precip_rate_mm_hour'] = h_data[1][i].get('precipIntensity')
        df.loc[i,'precip_type'] = d_data[1][0].get('precipType')
        df.loc[i,'sunrise'] = d_data[1][0].get('sunriseTime')
        df.loc[i,'sunset'] = d_data[1][0].get('sunsetTime')
        df.loc[i,'date'] = (pd.to_datetime(unix_date,unit = 's'))
        
        #precip.loc[d,'date'] = np.unique(df.loc[0,'date'])
        precip.loc[d,'precip_rate_mm_hour'] = np.mean(df['precip_rate_mm_hour'])
        precip.loc[d,'precip_type'] = df.loc[0,'precip_type']
        precip.loc[d,'sunrise'] = df.loc[0,'sunrise']
        precip.loc[d,'sunset'] = df.loc[0,'sunset']
    
        daily_precip.loc[d,'precip_avg_rate_mm_hour'] = precip.loc[d,'precip_rate_mm_hour']
        daily_precip.loc[d,'precip_type'] = precip.loc[d,'precip_type']
        daily_precip.loc[d,'sunrise'] = precip.loc[d,'sunrise']
        daily_precip.loc[d,'sunset'] = precip.loc[d,'sunset']
       
daily_precip['sunrise'] = pd.to_datetime(daily_precip['sunrise'].astype(int),unit = 's')
daily_precip['sunrise'] = daily_precip['sunrise'].dt.time - pd.Timedelta('04:00:00')
daily_precip['sunset'] = pd.to_datetime(daily_precip['sunrise'].astype(int),unit = 's')
daily_precip['sunset'] = daily_precip['sunset'].dt.time
        
daily_precip.to_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/PrecipData/DailyPrecip/MeanDailyPrecipRates.csv')
        

#Create dataframe of entire dataset hourly
#Check if time is in correct timezone (check result[currenttime] and make sure it's correct)
