# -*- coding: utf-8 -*-
"""
Created on Tue May  1 14:49:42 2018

@author: Timothy_Richards
"""

import os
from ftplib import FTP
import pandas as pd
import numpy as np

def sonic_ftp():
    ftp = FTP("ftp.as.harvard.edu")
    ftp.login()
    ftp.retrlines("LIST")
     
    ftp.cwd("pub/index/exchange/jwm")
     
    listing = []
    ftp.retrlines("LIST", listing.append)
    words = listing[0].split(None, 8)
    filename = words[-1].lstrip()
    filename2 = os.path.basename
    filenames = ftp.nlst()
    username = os.getlogin()
    # 
    # download the files
    for filename in filenames:
        if filename.startswith("micromet"):
            local_filename = os.path.join(r'C://Users/'+username+'/Dropbox/Obrist Lab/Tekran/Raw Data/sonic_data', filename)
            lf = open(local_filename, "wb")
            ftp.retrbinary("RETR " + filename, lf.write, 8*1024)
            lf.close()
    
    ftp.quit()
    
    #Merge .dat files into one
    ext = ".dat"
    dir_path = 'C://Users/'+username+'/Dropbox/Obrist Lab/Tekran/Raw Data/sonic_data'
    results = 'C://Users/'+username+'/Dropbox/Obrist Lab/Tekran/Raw Data/sonic_data/sonicDataRaw.csv'
    
    os.remove('C://Users/'+username+'/Dropbox/Obrist Lab/Tekran/Raw Data/sonic_data/sonicDataRaw.csv')
    os.chdir(dir_path)
    files = os.listdir(dir_path)
    for f in files:
        if f.startswith("micromet"):
            if f.endswith(ext):
                data = open(f)
                out = open(results,'a')
                for l in data:
                    print(l, file=out)
                data.close()
                out.close()
                
    #Cleanup file
    sonicData = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/Tekran/Raw Data/sonic_data/sonicDataRaw.csv',header=0,
                            names = ['day.EST','Wspd.m/s','Wdir.deg','sigmaU.m2/s2','cov(u,v).m2/s2',
                                     'cov(uw).m2/s2','sigmaV.m2/s2','sigmaW.m2/s2','T.sonic.C','sigmaT.C2','Fheat.W.m2'])
        
    sonicData['FlagDelete'] = np.where(sonicData['day.EST']=='day.EST','1','0')
    sonicData = sonicData[sonicData.FlagDelete == '0']
    sonicData['Datetime'] = pd.to_datetime(sonicData['day.EST'],unit='d')
    sonicData['Datetime'] = sonicData['Datetime'] + pd.DateOffset(years=48, days = -1)
    sonicData.set_index('Datetime',inplace=True)
    sonicData = sonicData.drop('FlagDelete',axis=1)
    
    os.remove('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/sonicData.csv')
    sonicData.to_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/sonicData.csv')
    return