# -*- coding: utf-8 -*-
"""
Created on Tue May  1 11:24:29 2018

@author: Timothy_Richards
"""
#%%
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
username = os.getlogin()
def merge_csv_files():
    source_path = r'C://Users/'+username+'/Dropbox/Obrist Lab/Tekran/Raw Data/2537B_Gradient/'
    dest_path = r'C://Users/'+username+'/Dropbox/Obrist Lab/Tekran/Raw Data/2537B_Gradient/csvTK/'
    
    for file in os.listdir(source_path):
        if file.startswith("TK"):
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
                        
    ##Merge csv files
    ext = ".csv"
    dir_path = 'C://Users/'+username+'/Dropbox/Obrist Lab/Tekran/Raw Data/2537B_Gradient/csvTK/'
    results = 'C://Users/'+username+'/Documents/Hg/HgData.csv'
    
    #os.remove('C://Users/'+username+'/Documents/Hg/HgData.csv')
    os.chdir(dir_path)
    files = os.listdir(dir_path)
    for f in files:
        if f.startswith("TK"):
            if f.endswith(ext):
                data = open(f)
                out = open(results,'a')
                for l in data:
                    print(l, file=out)
                data.close()
                out.close()
                
    ##Cleanup csv file and create final HgData file
    HgData = pd.read_csv('C://Users/'+username+'/Documents/Hg/HgData.csv',header = 0,
                         names = ['date','time','type','cart','stat','flag','stime','vol',
                                  'bl','bldev','maxpk','area','conc'])
    HgData['qc_flag'] = np.where(HgData['date']=="Date",'1',
                                      (np.where(HgData['date']=='-','1',
                                         (np.where(HgData['flag']=='3','1','0')))))
    HgData = HgData[HgData.qc_flag == '0']
    HgData['datetime'] = pd.to_datetime(HgData['date'] +' '+ HgData['time'],yearfirst = True)
    HgData.set_index('datetime',inplace=True)
    
    HgData.to_csv('C://Users/'+username+'/Dropbox/Obrist Lab/Tekran/Raw Data/2537B_Gradient/HgQADataSet.csv')
    HgData.to_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/TK2537BData.csv')
    
    #Find last date read in, and use that to create an empty dataframe w/complete 5 min. intervals
    lastDate = row[0]
    lastTime = row[1]
    
    index = pd.date_range('2018-04-17 10:05:00','20'+lastDate+' '+lastTime,freq = '5min') ##UPDATE DATE RANGE EACH TIME
    columns = ['column']
    HgDataSet = pd.DataFrame(index = index, columns = columns)
    HgDataSet = HgDataSet.join(HgData)
    HgDataSet = HgDataSet.drop(['column','qc_flag'],axis=1)
    
    HgDataSet.to_csv('C://Users/'+username+'/Dropbox/Obrist Lab/Tekran/Raw Data/2537B_Gradient/HgCompleteDataSet.csv')
    return row
###############################################################################
##Email Latest status/file
#%%
if __name__ == "__main__":
    lastDate = merge_csv_files()
    latestFile = "C://Users/"+username+"/Dropbox/Obrist Lab/Tekran/Raw Data/2537B_Gradient/csvTK/"+"TK"+lastDate[0].replace("-","")+".csv"
    
    latestHgData = pd.read_csv("C://Users/"+username+"/Dropbox/Obrist Lab/Tekran/Raw Data/2537B_Gradient/csvTK/"+"TK"+lastDate[0].replace("-","")+".csv",header=0,
                               names = ['Date','Time','Typ','C','Stat','Stat.1','AdTim','Vol',
                                  'Bl','Bldev','MaxV','Area','ng/m3'])
    latestHgData = latestHgData.to_html()
     
    today = date.today()
    today = today.strftime("%y-%m-%d")
    if lastDate[0] == today:
        status = "RUNNING"
    else:
        status = "DOWN"
     
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    username = 'hffluxmonitor@gmail.com'  # Email Address from the email you want to send an email
    password = 'vssapffsdgrauqlp'  # App Password
    server = smtplib.SMTP('')
    
    # Create the body of the message (a HTML version for formatting).
    html = latestHgData


    # Function that sends email.
    def send_mail(username, password, from_addr, to_addrs, msg):
        server = smtplib.SMTP('smtp.gmail.com','587')
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(username, password)
        server.sendmail(from_addr, to_addrs, msg.as_string())
        server.quit()
    
    email_list = ['trichards1935@gmail.com','timothy_richards@student.uml.edu',
                  'Dean_Howard@uml.edu']
    
    for to_addrs in email_list:
        msg = MIMEMultipart()
    
        from_addr = "hffluxmonitor@gmail.com"
        msg['Subject'] = "Tekcap Status: "+status+"     Last Date Read: "+lastDate[0]+" "+lastDate[1]
        msg['From'] = from_addr
        msg['To'] = to_addrs
    
        # Attach HTML to the email
        body = MIMEText(html, 'html')
        msg.attach(body)
    
        try:
            send_mail(username, password, from_addr, to_addrs, msg)
            print("Email successfully sent to "+ to_addrs)
        except:
            print("Failed")
#%%