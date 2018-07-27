# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 11:26:20 2018

@author: Timothy_Richards

Purpose: Merge all files from TK2537X and create a csv file with headers and cal logs
removed
"""
import csv
import os
import pandas as pd
import numpy as np
from datetime import date

###Should update this script to append new files onto final file instead of 
###concatinating every file every time
#-----------------------------------
#This script will replace the space delimiter in the files and save them in csv format.
#-----------------------------------
"""
Set up paths
"""
def merge_csv_files():
    username = os.getlogin()
    source_path = r'C://Users/'+username+'/Dropbox/Obrist Lab/Tekran/Raw_Data/2537X_Gradient'
    dest_path = r'C://Users/'+username+'/Dropbox/Obrist Lab/Tekran/Raw_Data/2537X_Gradient/csvX/'
    
    for file in os.listdir(source_path):
        if file.startswith("GR"):
            #get filename without file extension
            filename_no_extension = os.path.splitext(file)[0]
    
            #concatenate filename amd paths
            dest_csv_file = str(filename_no_extension) + ".csv"
            dest_file = os.path.join(dest_path,dest_csv_file)
            source_file = os.path.join(source_path,file)
    
            #open the original file and create reader object
            with open(source_file, "r") as infile:
                reader = csv.reader(infile, delimiter = " ",skipinitialspace = True)
                with open(dest_file, "w") as outfile:
                    writer = csv.writer(outfile, delimiter = ',')
                    for row in reader:
                        writer.writerow(row)
                        
    ext = ".csv"
    dir_path = 'C://Users/'+username+'/Dropbox/Obrist Lab/Tekran/Raw_Data/2537X_Gradient/csvX/'
    results = 'C://Users/'+username+'/Dropbox/Obrist Lab/Tekran/Raw_Data/2537X_Gradient/csvX/TK2537XRawData.csv'
    
    os.remove('C://Users/'+username+'/Dropbox/Obrist Lab/Tekran/Raw_Data/2537X_Gradient/csvX/TK2537XRawData.csv')
    os.chdir(dir_path)
    files = os.listdir(dir_path)
    for f in files:
        if f.startswith("GR"):
            if f.endswith(ext):
                data = open(f)
                out = open(results,'a')
                for l in data:
                    print(l, file=out)
                data.close()
                out.close()
                
    HgData = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/Tekran/Raw_Data/2537X_Gradient/csvX/TK2537XRawData.csv',header = 0,
                         names = ['date','time','type','cart','stat','flag','stime','vol',
                                  'bl','bldev','maxpk','area','conc'])
    
    words = ["-","Date","CALIBRATION","ZERO","ZERO:","Zero-Sub","Sample","Volume","Baseline","Bl","Start","SPAN","SPAN:",
             "Round","METHOD:","Low","Intg-dly","HtrBOn","HtrBHold","HtrBCoolDu:","HtrAOn","HtrAHold","HtrACoolDu:",
             "Hg","Car-Meas","Car-Idle","Calib","Cal-Conc","CALIBRATION:","AutoCal"]
    
    HgData['QC'] = HgData.date.isin(words) #Creates column of boolean values
    HgData = HgData[HgData.QC == False] #Drop rows where QC is true
    HgData = HgData.drop(['QC'],axis=1)
    
    HgData.to_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/TK2537XData.csv')
    return


