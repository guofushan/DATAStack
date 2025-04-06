from db_driver import mysql_driver
from user import User
import random
from datetime import datetime,timedelta
from flask import send_from_directory, send_file
import os
import logging
from settings import *
import time

script_dir=script_dir
host_yandi=DB_CONFIG['host']
port_yandi=DB_CONFIG['port']
user_yandi=DB_CONFIG['user']
password_yandi=DB_CONFIG['password']

class mysql_binlog2sql(mysql_driver):
    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request
    
    def auto_complete(self):
            schema_lists = []
            binlog_lists = []
            table_lists = []
            host = self.request.form['host']
            only_schemas = self.request.form['only_schemas']
            schema_sql = '''select SCHEMA_NAME from information_schema.SCHEMATA where SCHEMA_NAME not in ('mysql','information_schema','performance_schema','sys')'''
            table_sql = """select TABLE_NAME from information_schema.`TABLES` where TABLE_SCHEMA = '{0}'""".format(only_schemas)
            binlog_sql = 'show binary logs'
            # 获取数据库名
            schema_results = self.remote_excute(host,35972,'yunwei','testpwd','mysql',schema_sql)
            for schema in schema_results:
                schema_lists.append(schema['SCHEMA_NAME'])

            # 获取主机的binlog
            binlog_results = self.remote_excute(host,35972,'yunwei','testpwd','mysql',binlog_sql)
            for binlog in binlog_results:
                binlog_lists.append(binlog['Log_name'])
            if len(only_schemas) != 0:
                # 获取表名
                table_results = self.remote_excute(host,35972,'yunwei','testpwd','mysql',table_sql)
                for table in table_results:
                    table_lists.append(table['TABLE_NAME'])
                if len(table_lists) == 0:
                    table_lists = ['该库无表']
            return {
                'status': True,
                'data': {'schemas': schema_lists, 'tables': table_lists, 'binlog': binlog_lists}
            }
            
    def get_binlog_info(self):
          host = self.request.form['host']
          logging.warning('get_binlog_info host: {0}'.format(host))

          start_file = self.request.form['start_file']
          only_schemas = self.request.form['only_schemas']
          only_tables = self.request.form['only_tables']
          if only_tables == '该库无表':
              only_tables = ''
          # 将UTC时间转化为本地时间
          if len(self.request.form['start_time']) == 0:
              start_time = ''
          else:
              start_time = str(datetime.strptime(self.request.form['start_time'][:19], '%Y-%m-%dT%H:%M:%S') + timedelta(hours=8))
          if len(self.request.form['stop_time']) == 0:
              stop_time = ''
          else:
              stop_time = str(datetime.strptime(self.request.form['stop_time'][:19], '%Y-%m-%dT%H:%M:%S') + timedelta(hours=8))
          #sql_type = self.request.form['sql_type']
          sql_type = eval(self.request.form['sql_type'])
        #   sql_type = self.request.form['sql_type']
          # sql_type = eval(self.request.form['sql_type'][0])
          # 未选择类型，则解析所有类型的DML
          if sql_type == []:
            #   sql_type = ['INSERT', 'DELETE', 'UPDATE']
              sqltype=''     
          else:
              aa=f'''"{sql_type}"'''
              bb=aa.replace('[','').replace(']','').replace("'",'').replace(' ','').replace('"','')
              sqltype=f"-sql {bb}"
              
          flashback = self.request.form['flashback']
          if flashback == 'true':
                work_type='rollback'
          else:
                work_type='2sql'
          print(host,start_file,only_schemas,only_tables,start_time,stop_time,flashback,sql_type)
          #执行my2sql
          cmd_2=f"chmod 777 {script_dir}/my2sql"
          os.system(cmd_2)
          
          if only_schemas=='':
              only_schemas=''
          else:
              only_schemas=f" -databases {only_schemas}"
          
          if only_tables=='':
              only_tables=''
          else:
              only_tables=f" -tables {only_tables}"
          
          if start_time=='':
              start_time=''
          else:
              start_time=f''' -start-datetime "{start_time}" ''' 
              
          if stop_time=='':
              stop_time=''
          else:
              stop_time=f''' -stop-datetime "{stop_time}" ''' 
          

          v_1=sqltype + only_schemas + only_tables + start_time + stop_time

          cmd_2=f'''rm -rf /tmp/rollback*.sql'''
          cmd_3=f'''rm -rf /tmp/forward*.sql'''
          cmd_4=f'''rm -rf /tmp/binlog.sql'''
          os.system(cmd_2)
          os.system(cmd_3)
          os.system(cmd_4)
          cmd_1=f'''{script_dir}/my2sql -user {user_yandi} -password '{password_yandi}' -host '{host}' -port {port_yandi} -mode repl -work-type {work_type}  -start-file {start_file} {v_1} -output-dir /tmp/'''
          os.system(cmd_1)
          
          return {
                    'status': True,
                    'msg': '解析成功'
                    # 'msg': cmd_1
                }



    def download(self):
        cmd_1="mv /tmp/rollback*.sql /tmp/binlog.sql"
        cmd_2="mv /tmp/forward*.sql /tmp/binlog.sql"
        cmd_3="chmod 777 /tmp/binlog.sql"
        
        os.system(cmd_1)
        os.system(cmd_2)
        os.system(cmd_3)
        # return send_from_directory("/root",filename="forward.108.sql",as_attachment=True)
        return send_file('/tmp/binlog.sql', as_attachment=True)

        # return send_from_directory(r"C:\Users\86131\Desktop\ue",filename="binlog.sql",as_attachment=True)
