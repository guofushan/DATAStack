import pymysql
import time
import json
import logging
from datetime import datetime, timedelta
import redis
from db_driver import mysql_driver

class redis_detail(mysql_driver):

    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request
            
    def get_detail(self):
            ip=self.request.form['ip']
            sql=f'''SELECT ip,`port`,redis_type,description,date_created,pwd FROM yandi.`redis_ins` WHERE deleted=0 and ip='{ip}';'''
            data_ip=self.exe_sql(sql)
            for i in data_ip:
                ip=i['ip']
                port=i['port']
                pwd=i['pwd']
                try:
                    pool = redis.ConnectionPool(host=ip, port=port, db=0,password=pwd)
                    r = redis.Redis(connection_pool=pool)
                    # slowlog = r.slowlog_get()
                    info_memory = r.info('memory')
                    use_mem=info_memory['used_memory_human']
                    totle_meme=info_memory['maxmemory_human']
                    details=use_mem + '/' + totle_meme
                    i['status'] = '运行中'
                    i['details'] = details
                except Exception as e:
                    i['status'] = '等待中'
                    i['details'] = '等待中'
            return {
                'status':True,
                'msg':'success',
                'data':data_ip
            }
    
    
        