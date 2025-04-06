import pymysql
import time
import json
import logging
from datetime import datetime, timedelta
from db_driver import mysql_driver
from settings import *

datastack_ip=datastack_ip

class pg_detail(mysql_driver):

    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request
            
    def get_detail(self):
            vip=self.request.form['vip']
            # sql=f"""SELECT `description`,vip,`port`,GROUP_CONCAT(ip)  AS ips,date_created  FROM a_inventory  WHERE vip='{vip}' AND deleted=0 GROUP BY vip;"""
            sql=f"""SELECT `description`,vip,`port`,GROUP_CONCAT(ip)  AS ips,date_created  FROM pg_inventory  WHERE vip='{vip}' AND deleted=0 GROUP BY vip;"""
            msg='success'
            data=self.exe_sql(sql)
            # logging.warning('get_detail data1: {0}'.format(data))
            sql_c=f'''SELECT COUNT(*) AS count_ms FROM  `a_inventory` WHERE vip='{vip}' AND deleted=0;'''
            data_c=self.exe_sql(sql_c)[0]['count_ms']

            sql1=f'''SELECT CONCAT('http://','{datastack_ip}',":",'3000') as orch,b.consul1,c.consul2 FROM 
(SELECT  CONCAT('http://',ip,":",'8500') AS consul1,vip FROM a_inventory  WHERE vip='{vip}' AND deleted=0 ORDER BY consul1  ASC LIMIT 1
) b,
(SELECT  CONCAT('http://',ip,":",'8500') AS consul2,vip FROM a_inventory  WHERE vip='{vip}' AND deleted=0 ORDER BY consul2 DESC LIMIT 1
) c WHERE  b.vip=c.vip;'''
            
            if data_c==1:
                data1={'orch':'单节点实例不支持','consul1':'单节点实例不支持','consul2':'单节点实例不支持'}
                j = json.dumps(data1)
                data1 = json.loads(j)
                data1=[data1]
            else:
                data1=self.exe_sql(sql1)
                
            return {
                'status':True,
                'msg':msg,
                'data':data,
                'data1':data1
                }
    
    
    
        