# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 11:59:00 2018

@author: Timothy_Richards

Description: Program merges all .txt data from Tekran B, Tekran X, and sonic into
.csv files. Also creates even spaced time series .csv files and joins GEM data with
sonic data.
"""

import TK2537B_csv_merge
import TK2537X_csv_merge
import getSonicData
import create_even_time_series
import merge_hg_sonic_data

#%%
#Merge all Tekran 2537B files into one csv and sends an email containing last
#file read in and instrument status
TK2537B_csv_merge.merge_csv_files()
TK2537B_csv_merge.mail_update()
#%%
#Merge all Tekran 2537X files into one csv and sends an email containing last
#file read in and instrument status
TK2537X_csv_merge.merge_csv_files()
TK2537X_csv_merge.mail_update()
#%%
#Retrieve sonic files and merges into one .csv file
getSonicData.sonic_ftp()
#%%
#Create evenly spaced time series csv files (5 min for B, 2.5 for X)
create_even_time_series.TKB_5_min_time_series()
create_even_time_series.TKX_2_5_min_time_series()
#%%
#Resample 5 min GEM data into 30 min means, and join with 30 min sonic data
merge_hg_sonic_data.merge_gemB_sonic_data()
merge_hg_sonic_data.merge_gemX_sonic_data()