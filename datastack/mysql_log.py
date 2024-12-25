import pymysql
import time
import logging
from settings import *
from datetime import datetime, timedelta
from db_driver import mysql_driver

datastack_ip=datastack_ip

class mysql_log(mysql_driver):

    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request
            
    def get_slow_log(self):
            start_time = self.request.form['start_time']
            stop_time = self.request.form['stop_time']
            vip=self.request.form['vip']
            logging.warning('start_time: {0},stop_time:{1}'.format(start_time,stop_time))

            # if start_time is None or stop_time is None:
            if start_time=='' or stop_time=='':
                msg='警告:请填写完整信息'
                data=''
            else:
                msg='成功获取慢日志数据'
                sql=f"""SELECT start_time,user_host,query_time,lock_time,rows_sent,rows_examined,db,LAST_INSERT_ID,INSERT_ID,server_id,LEFT(sql_text,3000) AS sql_text,thread_id FROM mysql.`slow_log` WHERE start_time >= '{start_time}' AND start_time <= '{stop_time}';"""
                data=self.remote_excute(vip,35972,'yunwei','testpwd','mysql',sql)

            return {
                'status':True,
                'msg':msg,
                'data':data
            }
    
    def first_slow_log(self):
            vip=self.request.form['vip']
            # if start_time is None or stop_time is None:
            msg='成功获取慢日志数据'
            # sql=f"""SELECT * FROM mysql.`slow_log`  LIMIT 20;"""
            sql=f'''SELECT
  start_time,
  user_host,
  query_time,
  lock_time,
  rows_sent,
  rows_examined,
  db,
  LAST_INSERT_ID,
  INSERT_ID,
  server_id,
  LEFT(sql_text,3000) AS sql_text ,
  thread_id
FROM
  mysql.`slow_log`
LIMIT 20;
'''
            data=self.remote_excute(vip,35972,'yunwei','testpwd','mysql',sql)

            return {
                'status':True,
                'msg':msg,
                'data':data
            }

    def granafa_ip(self):
            vip=self.request.form['vip']
            sql_single=f'''SELECT ip FROM yandi.`a_inventory` WHERE vip='{vip}' AND deleted=0 LIMIT 1;'''
            ip_single=self.exe_sql(sql_single)[0]['ip']

            msg='success'
            # url=f'''http://{datastack_ip}:3001/d/rYdddlPWk/linux?orgId=1&refresh=10s'''
            url=f'''http://{datastack_ip}:3001/d/rYdddlPWk/linux?orgId=1&refresh=10s&var-DS_PROMETHEUS=default&var-job=Host&var-node={ip_single}&var-diskdevices=%5Ba-z%5D%2B%7Cnvme%5B0-9%5D%2Bn%5B0-9%5D%2B%7Cmmcblk%5B0-9%5D%2B'''
            logging.warning('monitor url: {0}'.format(url))

            return {
                'status':True,
                'msg':msg,
                'data':url
            }
            
    def redis_granafa_ip(self):
            ip=self.request.form['ip']
            msg='success'
            # url=f'''http://{datastack_ip}:3001/d/rYdddlPWk/linux?orgId=1&refresh=10s'''
            url=f'''http://{datastack_ip}:3001/d/rYdddlPWk/linux?orgId=1&refresh=10s&var-DS_PROMETHEUS=default&var-job=Host&var-node={ip}&var-diskdevices=%5Ba-z%5D%2B%7Cnvme%5B0-9%5D%2Bn%5B0-9%5D%2B%7Cmmcblk%5B0-9%5D%2B'''
            # data=f''''iframeUrl':"{url}" '''
            logging.warning('monitor url: {0}'.format(url))

            return {
                'status':True,
                'msg':msg,
                'data':url
            }
        