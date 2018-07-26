#/bin/env python
#-*-coding:utf-8-*-
import socket
import time
import smtplib
import urllib.request as ul
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import xml.etree.ElementTree as ET  
 
#发送邮件的基本函数，参数依次如下
# smtp服务器地址、邮箱用户名，邮箱秘密，发件人地址，收件人地址（列表的方式），邮件主题，邮件html内容
def sendEmail(smtpserver,username,password,sender,receiver,subject,msghtml):
    msgRoot = MIMEMultipart('related')
    msgRoot["To"] = ','.join(receiver)
    msgRoot["From"] = sender
    msgRoot['Subject'] =  subject
    msgText = MIMEText(msghtml,'html','utf-8')
    msgRoot.attach(msgText)
    #sendEmail
    smtp = smtplib.SMTP(smtpserver,587)
    smtp.connect(smtpserver,587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msgRoot.as_string())
    smtp.quit()
 
# 检查网络连通性
def check_network(try_times):
    isConnected = False
    i = 0    
    while i<try_times:
        try:
            result=ul.urlopen('http://baidu.com').read()
            print(result)
            print("Network is Ready!")
            isConnected = True
            break
        except Exception as e:
            print(e)
            print("Network is not ready,Sleep 5s....")
            time.sleep(5)
        i = i+1
    return isConnected
 
# 获得本级制定接口的ip地址
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("1.1.1.1",80))
    ipaddr=s.getsockname()[0]
    s.close()
    return ipaddr
 
if __name__ == '__main__':
    if check_network(10):
        ipaddr=get_ip_address()
        email_add = 'jhcai11.thu@gmail.com'
        tree = ET.parse('send_ip.xml')
        root = tree.getroot()
        pwd = root[0][0].text
        sendEmail('smtp.gmail.com',email_add,pwd,email_add,[email_add],'IP Address Of Raspberry Pi',ipaddr)
