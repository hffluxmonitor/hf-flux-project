# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 15:52:05 2018

@author: Timothy_Richards
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

username = os.getlogin()

data = pd.read_csv('C://Users/'+username+'/Dropbox/Obrist Lab/HarvardForestData/TK2537XData.csv')
data['datetime'] = pd.to_datetime(data['date'] +' '+ data['time'],yearfirst = True)
data.set_index('datetime',inplace=True)

#Slice dataframe to use only last 30 days
today = pd.datetime.today().date()
cut_off = today - pd.offsets.Day(29)
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
data = data.drop('flag2',axis=1)

#BlDev: plot bldev against timestamp
data['flag2'] = np.where(np.logical_and(data.type == "CONT",data.stat == "OK"),1,0)
bldev = data[data.flag2 == 1]
ax[1].plot(bldev.index.values,bldev.bldev,color="blue",label = 'bldev')
ax[1].legend()
ax[0].set_title('Tekran variables vs. time')
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



fig1.savefig('C://Users/'+username+'/Documents/figConcABX.png')
figCal.savefig("C://Users/"+username+"/Documents/figCalX.png")
fig.savefig("C://Users/"+username+"/Documents/fig2537XQA.png")
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
    msg['Subject'] = 'QA - 2537X'
    msg['From'] = strFrom
    msg['To'] = strTo
    msg.preamble = 'This is a multi-part message in MIME format'
    
    #Encapsulate plain and HTML versions in "alterntive" part
    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)
    
    msgText = MIMEText('This is the alternative plain text message')
    msgAlternative.attach(msgText)
    
    #Reference the image in the IMG SRC attribute by ID
    msgText = MIMEText('<b>Tekran 2537X QA over last 30 days</b><br><img src="cid:image1"><br><br><img src="cid:image2"><br><br><img src="cid:image3"><br>','html')
    msgAlternative.attach(msgText)
    
    #Open Images
    fp = open('C://Users/Timothy_Richards/Documents/figConcABX.png','rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    
    fp = open('C://Users/Timothy_Richards/Documents/fig2537XQA.png','rb')
    msgImage2 = MIMEImage(fp.read())
    fp.close()
    
    fp = open('C://Users/Timothy_Richards/Documents/figCalX.png','rb')
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
                      
