import pymysql
import time
import logging
from settings import *
from datetime import datetime, timedelta
from db_driver import mysql_driver

datastack_ip=datastack_ip

class pg_log(mysql_driver):

    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request
            
    def get_slow_log(self):
            start_time = self.request.form['start_time']
            stop_time = self.request.form['stop_time']
            vip=self.request.form['vip']
            port=self.request.form['port']
            logging.warning('start_time: {0},stop_time:{1}'.format(start_time,stop_time))

            # if start_time is None or stop_time is None:
            if start_time=='' or stop_time=='':
                msg='警告:请填写完整信息'
                data=''
            else:
                msg='SUCCESS'
                sql=f'''select
	ts,
	userid::regrole,
	b.datname ,
	query,
	round(cast((total_exec_time + total_plan_time) as numeric),1) as total_exec_time,
	round(cast((total_exec_time + total_plan_time)/calls as numeric),1) as avg_exec_time,
	calls,
	rows / calls as rows,
	round(cast(min_exec_time as numeric),1) as min_exec_time,
	round(cast(max_exec_time as numeric),1) as max_exec_time
from
	stat_statements_snapshots a,
	pg_catalog.pg_database b
where
	a.ts>'{start_time}' and a.ts<'{stop_time}'
	and a.dbid = b.oid
order by
	max_exec_time desc limit 1000;
'''
                data=self.pg_execute(sql,vip,'postgres','postgres','so3evA1CWy',port)

            return {
                'status':True,
                'msg':msg,
                'data':data
            }
    
    def first_slow_log(self):
            vip=self.request.form['vip']
            port=self.request.form['port']
            msg='SUCCESS'
            sql=f'''select
	ts,
	userid::regrole,
	b.datname ,
	query,
	round(cast((total_exec_time + total_plan_time) as numeric),1) as total_exec_time,
	round(cast((total_exec_time + total_plan_time)/calls as numeric),1) as avg_exec_time,
	calls,
	rows / calls as rows,
	round(cast(min_exec_time as numeric),1) as min_exec_time,
	round(cast(max_exec_time as numeric),1) as max_exec_time
from
	stat_statements_snapshots a,
	pg_catalog.pg_database b
where
	a.ts<now()-interval '1 hours'
	and a.dbid = b.oid
order by
	max_exec_time desc limit 1000;
'''
            data=self.pg_execute(sql,vip,'postgres','postgres','so3evA1CWy',port)

            return {
                'status':True,
                'msg':msg,
                'data':data
            }

    def granafa_ip(self):
            vip=self.request.form['vip']
            sql_single=f'''SELECT ip FROM yandi.`pg_inventory` WHERE vip='{vip}' AND deleted=0 LIMIT 1;'''
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
            
    
        