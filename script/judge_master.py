# -*- coding: utf-8 -*-
'''
#=============================================================================
#       Author: Fushan.Guo
#        Email: 1031059192@qq.com
#      Version: 0.0.1
#   LastChange: 2023-12-26
#=============================================================================
'''
import datetime
import pymysql
import time
import logging
import requests
import json
import os
import sys
import argparse
 
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

#define  parse help
def parse():
    parser = argparse.ArgumentParser(description='example: pchkmaster -h 192.168.1.1 -p 3306')
    parser.add_argument('-i',"--mysqlip",type=str,help='mysql ip.')
    parser.add_argument('-p',"--mysqlport",type=str,help='mysql port.')

    args = parser.parse_args()
    if not args.mysqlip or not args.mysqlport:
        parser.print_help()
        sys.exit(0)

    return args
         
def getmaster(mysqlip,mysqlport,user,pwd):
  sql_1="show variables like 'read_only';"
  res_1=execute(mysqlip,mysqlport,user,pwd,'mysql',sql_1)
  only=res_1[0]['Value']
  
  if only=='ON':
        msg=f"{mysqlip} readonly is {only},is slave node."
        print(msg)
        sys.exit(1)
  else:  
        sql_2="SELECT DISTINCT(SUBSTRING_INDEX(HOST, ':', 1)) AS slave_hostname FROM information_schema.processlist WHERE USER='zy_repl' AND command IN ('Binlog Dump', 'Binlog Dump GTID');"
        res_2=execute(mysqlip,mysqlport,user,pwd,'mysql',sql_2)
        if res_2==():
              sql_6="SHOW SLAVE status;"
              res_6=execute(mysqlip,mysqlport,user,pwd,'mysql',sql_6)
              if res_6 ==():
                    msg=f"{mysqlip} readonly is {only},is master node."
                    print(msg)                   
                    sys.exit(0)
              else:
                  #   print(mysqlip)
                  #   print("is slave node.")
                    msg=f"{mysqlip} readonly is {only},is slave node."
                    print(msg)    
                    sys.exit(1)
        else:
            slaveip=res_2[0]['slave_hostname']
            sql_3="SHOW SLAVE status;"
            res_3=execute(slaveip,mysqlport,user,pwd,'mysql',sql_3)
            masterip=res_3[0]['Master_Host']
            if masterip==mysqlip:
                  # print(mysqlip)
                  # print("is master node.")
                  msg=f"{mysqlip} readonly is {only},is master node."
                  print(msg)
                  sys.exit(0)
            else:
                  # print(mysqlip)
                  # print("is slave node.")
                  msg=f"{mysqlip} readonly is {only},is slave node."
                  print(msg)
                  sys.exit(1)
              


def judge():
      try:
            args=parse()
            mysqlip=args.mysqlip
            mysqlport=args.mysqlport
            mysqlport=int(mysqlport)
            getmaster(mysqlip,mysqlport,'zy_repl','co5tvA1CWy')

      except Exception as exec_error:
            print(exec_error)
            sys.exit(1)

judge()
