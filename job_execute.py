# -*- coding: utf-8 -*-
'''
#=============================================================================
#       Author: Fushan.Guo
#        Email: 1031010310@qq.com
#      Version: 0.0.1
#   LastChange: 2023-11-16 03:03:03
#=============================================================================
'''
# from cmath import log
import datetime
import paramiko
from multiprocessing import Pool
import croniter
import pymysql
import os
import time
import logging
import configparser
import subprocess
# from settings import *

#定义log，记录程序日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s[line:%(lineno)d] -  %(levelname)s  %(message)s',
    filename='/tmp/crontab.log'
    )

# db_host=DB_CONFIG['host']
# db_port=DB_CONFIG['port']
# db_user=DB_CONFIG['user']
# db_password=DB_CONFIG['password']

cfg = configparser.ConfigParser()
cfg.read('/app/datastack.cfg')

db_host= cfg.get('section','mysqlip')
db_user= cfg.get('section','mysqluser')
db_port= cfg.get('section','mysqlport')
db_password= cfg.get('section','mysqlpwd')
db_port=int(db_port)

#get local ip
# cmd_3='''/usr/sbin/ip addr | awk '/^[0-9]+: / {}; /inet.*global/ {print gensub(/(.*)\/(.*)/, "\\\\1", "g", $2)}' '''
# hostip=os.popen(cmd_3).read()
# hostip=hostip.strip()
# lines = hostip.splitlines()
# hostip=lines[0]

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

def compute_next_time(ip,port,user,pwd):
  try:
    sql_1="SELECT id,cron,next_exec_time FROM yandi.`crontab` WHERE next_exec_time IS NULL AND deleted=0"
    res=execute(ip,port,user,pwd,'mysql',sql_1)
    now = datetime.datetime.now()
    for i in res:
          id=i["id"]
          i=i['cron']
          con=croniter.croniter(i,now)
          next_time= con.get_next(datetime.datetime)
          sql_2 = "update yandi.crontab set next_exec_time='{0}' where id={1}".format(next_time, id)
          execute(ip,port,user,pwd,'mysql',sql_2)

  except Exception as e:
    logging.info('compute_next_time err :{0}'.format(e))


def current_job(ip,port,user,pwd):
    try:
      sql_3="SELECT * FROM yandi.crontab WHERE next_exec_time<NOW() AND failed=0 AND deleted=0;"
      res_1=execute(ip,port,user,pwd,'mysql',sql_3)
      logging.info('current_job is :{0}'.format(res_1))
      return res_1
    except Exception as e:
      logging.info('current_job err :{0}'.format(e))

def execute_job(ip,user,pwd,command,id,cron):
  log_1='insert into yandi.crontab_log(job_id,log) values({0},"开始执行：{1}")'.format(id,command)
  execute(db_host,db_port,db_user,db_password,'mysql',log_1)
  try:
    # if ip==hostip:
    if ip=='127.0.0.1':
        # subprocess.run(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
        os.system(command)
        log_3='insert into yandi.crontab_log(job_id,log) values({0},"结束执行：{1}")'.format(id,command)
        execute(db_host,db_port,db_user,db_password,'mysql',log_3)
 
    now = datetime.datetime.now()
    con=croniter.croniter(cron,now)
    next_time= con.get_next(datetime.datetime)
    sql_4="UPDATE yandi.`crontab` SET last_run=NOW(),next_exec_time='{0}' WHERE id={1}".format(next_time,id)
    execute(db_host,db_port,db_user,db_password,'mysql',sql_4)
  except Exception as e:
    logging.info('execute_job err :{0}'.format(e))
    sql_err="update yandi.crontab set failed=1 where id={0}".format(id)
    execute(db_host,db_port,db_user,db_password,'mysql',sql_err)
    log_100='insert into yandi.crontab_log(job_id,log) values({0},"执行execute_job函数报错")'.format(id)
    execute(db_host,db_port,db_user,db_password,'mysql',log_100)

def send_mail_fail():
  sql_err="SELECT id,ip,cron,command,failed FROM yandi.`crontab` WHERE deleted=0  AND failed=1 AND date_updated >DATE_ADD(NOW(), INTERVAL - 2 MINUTE)"
  sql_err_res=execute(db_host,db_port,db_user,db_password,'mysql',sql_err)
  # print(sql_err_res)
  if sql_err_res==():
    pass
  else:
    msg='''定时任务执行失败'''
    # send_mail(msg,['1031010310@qq.com'],'定时任务失败')
    print(msg)
  
def run():
  while True:
    try:
      # logging.info('send_report err :{0}'.format(cc))
      logging.info('start work.')
      compute_next_time(db_host,db_port,db_user,db_password)
      res_5=current_job(db_host,db_port,db_user,db_password)
      now = datetime.datetime.now()
    
      pool = Pool(processes =5)  # 可以同时跑10个进程
      for i in res_5:
        id=i['id']
        cron=i["cron"]
        command=i["command"]
        ip=i["ip"]
        user='mysql'
        pwd='testpwd6'
        pool.apply_async(execute_job,args=(ip,user,pwd,command,id,cron,))
      pool.close()
      pool.join()
      logging.info('end work.')
      send_mail_fail()
      time.sleep(30)
    except Exception as e:
      msg='''定时任务脚本执行报错'''
      # send_mail(msg,['1031010310@qq.com'],'定时任务报错')
      logging.info('run err :{0}'.format(e))

run()

