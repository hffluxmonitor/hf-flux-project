# -*- coding: utf-8 -*-
"""
Created on Fri May 11 13:31:12 2018

@author: Timothy_Richards

Description: Program will monitor status of TekCap every half hour. If determined to be
down, an email will be sent out stating that TekCap is down. If user replies to email with
a message containing 'stop', the monitor emails will cease to send. The check for whether or
not to stop the emails is if there is an email in the hffluxmonitor inbox from "today". Emails
can be continued by replying to hffluxmonitor with any message, as the readmail function only 
checks the latest email.
"""

#%%
import imaplib
import email
from datetime import datetime
import datetime
import os

ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "hffluxmonitor" + ORG_EMAIL
FROM_PWD = "vssapffsdgrauqlp"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993
string = "stop"
username = os.getlogin()


def readmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')
        stop = 0
        local_date = "0"
        
        typ, data = mail.search(None, 'ALL')
        mail_ids = data[0]
        
        id_list = mail_ids.split()
        latest_email_id = int(id_list[-1])
        
        typ, data = mail.fetch(str.encode(str(latest_email_id)), '(RFC822)')
            
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1].decode('utf-8'))
                email_subject = msg['subject']
                email_from = msg['from']
                email_date = msg['date']
                date_tuple = email.utils.parsedate_tz(email_date)
                if date_tuple:
                    local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple)).strftime("%a, %d %b %Y")                     
                print('From : ' + email_from + '\n')
                print('Subject :' + email_subject + '\n')
                print('Date : '+email_date+'\n')
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = str(part.get_payload(decode=True))
                        if string in body:
                            stop = 1
                    else:
                        continue
                    
    except Exception as e:
        print(str(e))
    return stop,local_date
#%%
# Function that sends email.
def send_mail(username, password, from_addr, to_addrs, msg):
    server = smtplib.SMTP('smtp.gmail.com','587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    server.sendmail(from_addr, to_addrs, msg.as_string())
    server.quit()
#%%
import os
import time

basepath = 'C://Users/'+username+'/Dropbox/Obrist Lab/Tekran/Raw Data/2537B_Gradient/'
for fname in os.listdir(basepath):
    path = os.path.join(basepath, fname)
    if os.path.isdir(path):
        # skip directories
        continue

latest_file = path #path is last file in directory

t = os.path.getmtime(latest_file)
modTime = datetime.datetime.fromtimestamp(t).strftime('%y-%m-%d %H:%M:%S')
now = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
now2 = time.time()
dif = now2-t

if dif <= 1800:
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
text = "Tekcap is currently down. Do something about it."


#%%
email_list = ['trichards1935@gmail.com','timothy_richards@student.uml.edu',
              'Dean_Howard@uml.edu']
today = datetime.datetime.now().strftime("%a, %d %b %Y")

if status == "RUNNING":
    print('TekCap is running')
else:
    z = readmail()
    if z[1] == today:
        if z[0] == 1:
            print("TekMonitor Stopped")
    else:         
        for to_addrs in email_list:
            msg = MIMEMultipart()

            from_addr = "trichards1935@gmail.com"
            msg['Subject'] = "Tekcap Status: "+status+"     Last Date Read: "+ modTime
            msg['From'] = from_addr
            msg['To'] = to_addrs
    
            # Attach HTML to the email
            body = MIMEText(text, 'text')
            msg.attach(body)
    
            try:
                send_mail(username, password, from_addr, to_addrs, msg)
                print("Email successfully sent to "+ to_addrs)
            except:
                print("Failed")
