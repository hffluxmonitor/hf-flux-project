# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 11:56:36 2018

@author: Timothy_Richards

Description:
"""
#Program to monitor QA of flux system. Email status every Monday morning.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime,timedelta

username1 = os.getlogin()

data = pd.read_csv('C://Users/'+username1+'/Dropbox/Obrist Lab/Tekran/Raw Data/2537B_Gradient/HgQADataSet.csv')

data['datetime'] = pd.to_datetime(data['datetime'],yearfirst=True)
data = data.set_index('datetime')
data.index = pd.to_datetime(data.index)

#Slice dataframe to use only last 30 days
today = pd.datetime.today().date()
cut_off = pd.to_datetime(today - pd.offsets.Day(29))
data = data[cut_off:]


#plot conc(where type == 'CONT' and stat == 'OK' and cart == 'A') against timestamp
fig1, ax1 = plt.subplots()
data['flag2'] = np.where(np.logical_and(np.logical_and(data.type == "CONT",data.stat == "OK"),data.cart == "A"),1,0)
data['conc'] = np.where(data.conc > 5,np.nan,data.conc)
concCartA = data[data.flag2 == 1]
ax1.plot(concCartA.index.values,concCartA.conc,label = "[Cart A]")
data = data.drop('flag2',axis=1)


#plot conc(where type == 'CONT' and stat == 'OK' and cart == 'B') against timestamp
data['flag2'] = np.where(np.logical_and(np.logical_and(data.type == "CONT",data.stat == "OK"),data.cart == "B"),1,0)
data['conc'] = np.where(data.conc > 5,np.nan,data.conc)
concCartB = data[data.flag2 == 1]
ax1.plot(concCartB.index.values,concCartB.conc,label = "[Cart B]")
data = data.drop('flag2',axis=1)
ax1.legend()
fig1.autofmt_xdate()
locs, labels = plt.xticks()
plt.xticks(np.arange(locs[0], locs[-1], step=3))
plt.ylabel(r'GEM [ng $\mathrm{m^{-3}]}$')
plt.title('GEM conc. vs. time')
fig1.tight_layout()

#Bl: plot bl against timestamp
data['flag2'] = np.where(np.logical_and(data.type == "CONT",data.stat == "OK"),1,0)
bl = data[data.flag2 == 1]
fig, ax = plt.subplots(4,1,sharex=True)
fig.autofmt_xdate()
fig.tight_layout()
ax[0].plot(bl.index.values,bl.bl,color = "red",label = 'bl')
ax[0].legend()
ax[0].set_title('Tekran variables vs. time')
data = data.drop('flag2',axis=1)

#BlDev: plot bldev against timestamp
data['flag2'] = np.where(np.logical_and(data.type == "CONT",data.stat == "OK"),1,0)
bldev = data[data.flag2 == 1]
ax[1].plot(bldev.index.values,bldev.bldev,color="blue",label = 'bldev')
ax[1].legend()
fig.tight_layout()
data = data.drop('flag2',axis=1)

#Volume: plot vol(where type == 'CONT') against timestamp
data['flag2'] = np.where(data.type == "CONT",1,0)
cont = data[data.flag2 == 1]
ax[2].plot(cont.index.values,cont.vol, color = "green", label = 'volume')
ax[2].legend()
data = data.drop('flag2',axis=1)

#Sample time: plot stime(where type == 'CONT') against timestamp
ax[3].plot(cont.index.values,cont.stime, color = 'purple', label = 'stime')
ax[3].legend()
locs, labels = plt.xticks()
plt.xticks(np.arange(locs[0], locs[-1], step=3))

#Calibrations: plot area(where type == 'SPAN' and cart == 'A') against timestamp
figCal, axCal = plt.subplots(2,1,sharex=True)
data['flag2'] = np.where(np.logical_and(data.type == 'SPAN',data.cart == 'A'),1,0)
spanA = data[data.flag2 == 1]
axCal[0].plot(spanA.index.values,spanA.area,color = 'red',label = 'SPAN: A')
axCal[0].set_title('Area vs. time')
data = data.drop('flag2',axis=1)


##plot area(where type == 'SPAN' and cart =='B') against timestamp
data['flag2'] = np.where(np.logical_and(data.type == 'SPAN',data.cart == 'B'),1,0)
spanB = data[data.flag2 == 1]
data = data.drop('flag2',axis=1)
axCal[0].plot(spanB.index.values, spanB.area,color = 'green', label = 'SPAN: B')
axCal[0].legend()
figCal.autofmt_xdate()

##plot area(where type == 'ZERO' and cart =='A') against timestamp
data['flag2'] = np.where(np.logical_and(data.type == 'ZERO',data.cart == 'A'),1,0)
zeroA = data[data.flag2 == 1]
axCal[1].plot(zeroA.index.values,zeroA.area,color = 'red',label = 'ZERO: A')
data = data.drop('flag2',axis=1)

##plot area(where type == 'ZERO' and cart =='B') against timestamp
data['flag2'] = np.where(np.logical_and(data.type == 'ZERO',data.cart == 'B'),1,0)
zeroB = data[data.flag2 == 1]
data = data.drop('flag2',axis=1)
axCal[1].plot(zeroB.index.values, zeroB.area,color = 'green', label = 'ZERO: B')
axCal[1].legend()
figCal.autofmt_xdate()
figCal.tight_layout()
locs, labels = plt.xticks()
plt.xticks(np.arange(locs[0], locs[-1], step=3))
#%%
##Calculate RPD for each intake and plot
#now = datetime.now()
#now_minus_90 = now - datetime.timedelta(minutes = 90)
#data = data.reset_index()
#
#data0 = data[(data.type == 'CONT') & (data.stat == 'OK') & (data.flag == 0) & (data.datetime > now_minus_90)]
#data1 = data[(data.type == 'CONT') & (data.stat == 'OK') & (data.flag == 1) & (data.datetime > now_minus_90)]
#
#a_data = data0[data0.cart == 'A']
#b_data = data0[data0.cart == 'B']
#
#a_data = np.mean(a_data.conc)
#b_data = np.mean(b_data.conc)
#
#rpd = np.abs(a_data - b_data)/np.mean([a_data,b_data])*100
#%%
timespan = 90 #minutes
timespan = timespan/1440 #days
timespan = datetime.now() - timedelta(minutes = 90)
now = datetime.now()
data = data.reset_index()

Inlet_flags = [0,1] #B Unit

#Run through each inlet
for v in range(len(Inlet_flags)):
    #set inlet flag
    inlet = Inlet_flags[v]
            
    #Create temp array to hold RPD data
    rpd_temp = pd.DataFrame(index = range(0,len(data)),columns = ['A'])
    
    #Run through each measurement in dataframe
    for i in range(len(data)):
        #Only calculate for valid measurements
        if data.type[i] == 'CONT':
            #find all valid A data
            a_data = data.conc[(data.cart == 'A') & (data.type == 'CONT') & (data.stat == 'OK') & (data.flag == inlet) & (data.datetime > timespan)]
            #find all valid B data
            b_data = data.conc[(data.cart == 'B') & (data.type == 'CONT') & (data.stat == 'OK') & (data.flag == inlet) & (data.datetime > timespan)]
            
            #calculate means of A and B over the time period
            a_data = np.nanmean(a_data)
            b_data = np.nanmean(b_data)
            
            #Calculate RPD from mean values
            rpd_temp.A[i] = np.abs(a_data-b_data)/np.mean([a_data,b_data])
            
#Maybe assign rpd_temp back to data using timestamp as index? Then plot would 
#change over time
        
    
    


    




#%%
fig1.savefig("C://Users/"+username1+"/Documents/figConcAB.png")
figCal.savefig("C://Users/"+username1+"/Documents/figCal.png")
fig.savefig("C://Users/"+username1+"/Documents/fig2537BQA.png")
#%%
#Email Plots
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

username = 'hffluxmonitor@gmail.com'  # Email Address from the email you want to send an email
password = 'vssapffsdgrauqlp'  # App Password

# Function that sends email.
strFrom = 'hffluxmonitor@gmail.com'
email_list = ['trichards1935@gmail.com','timothy_richards@student.uml.edu',
              'Dean_Howard@uml.edu']


def send_mail(username, password, strFrom, strTo, msg):
    smtp = smtplib.SMTP('smtp.gmail.com','587')
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(username,password)
    smtp.sendmail(strFrom, strTo, msg.as_string())
    smtp.quit()

#Create message
for strTo in email_list:
    msg = MIMEMultipart('related')
    msg['Subject'] = 'QA - 2537B'
    msg['From'] = strFrom
    msg['To'] = strTo
    msg.preamble = 'This is a multi-part message in MIME format'
    
    #Encapsulate plain and HTML versions in "alterntive" part
    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)
    
    msgText = MIMEText('This is the alternative plain text message')
    msgAlternative.attach(msgText)
    
    #Reference the image in the IMG SRC attribute by ID
    msgText = MIMEText('<b>Tekran 2537B QA over last 30 days</b><br><img src="cid:image1"><img src="cid:image2"><br><br><img src="cid:image3"><br>','html')
    msgAlternative.attach(msgText)
    
    #Open Images
    fp = open('C://Users/'+username1+'/Documents/figConcAB.png','rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    
    fp = open('C://Users/'+username1+'/Documents/fig2537BQA.png','rb')
    msgImage2 = MIMEImage(fp.read())
    fp.close()
    
    fp = open('C://Users/'+username1+'/Documents/figCal.png','rb')
    msgImage3 = MIMEImage(fp.read())
    fp.close()
    
    #Define Image ID
    msgImage.add_header('Content-ID', '<image1>')
    msgImage2.add_header('Content-ID', '<image2>')
    msgImage3.add_header('Content-ID', '<image3>')
    msg.attach(msgImage)
    msg.attach(msgImage2)
    msg.attach(msgImage3)
    
    #Send the email
    try:
        send_mail(username, password, strFrom, strTo, msg)
        print("Success!")
    except:
        print("Failed")
                      
