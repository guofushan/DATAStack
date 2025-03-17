# -*- coding:UTF-8
"""
Created on 2020-08-10

@author: GFS
"""

import pymysql
import time
import datetime
import os
import sys
import smtplib
# from pymysql import escape_string
# from pymysql.converters import escape_string
import logging
from email.mime.text import MIMEText
from email.header import Header
import requests
import json
import base64

#sql执行模块
def execute(ip,port,user,pwd,db,sql_text):
    try:
        connection = pymysql.connect(host=ip, user=user, passwd=pwd, db=db,port=port,autocommit = True,charset='utf8mb4')
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql_text)
        connection.commit()
        result = cursor.fetchall()
        return result
    finally:
        connection.close()

#邮件通知模块
def send_mail(msg,reciver,subject_text):
 try:
    mail_user="1031010310@qq.com"   
    mail_pass="testpwd8"
    mail_body=msg
    # message = MIMEText(mail_body)
    message = MIMEText(mail_body, 'html', 'utf-8')

    # message['From'] = Header("DBA")
    message['From'] = Header(f'=?utf-8?B?{base64.b64encode("python自动发送".encode()).decode()}=?= <1031010310@qq.com>')      #必须填发送者邮箱
    message['To'] =  Header("receiver")
    subject = subject_text  #MySQL工单 or slow log告警
    message['Subject'] = Header(subject, 'utf-8')

    try:
        mailhost = 'smtp.qq.com'
        smtpObj = smtplib.SMTP_SSL(mailhost,465)
        
        smtpObj.connect("smtp.qq.com", 465)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(mail_user, reciver, message.as_string())
        print ("邮件发送成功")
    except Exception as bb:
        print ("Error: 无法发送邮件")
        print(bb)
 except Exception as cc:
    print(cc)
        

