from db_driver import mysql_driver
from user import User
import random
class mysql(mysql_driver):
    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request
   
    def get_all_ips(self):
        return {
            'status':True,
            'data':self.get_all_ips_from_db()
        }

    def get_all_ips_from_db(self):
        sql = "SELECT CONCAT(ip,'_',description) AS hostip FROM yandi.inventory;"
        return self.exe_sql_one_col(sql)

    def get_all_db_ips(self):
        return {
            'status':True,
            'data':self.get_all_ips_from_db()
        }
        
    def get_all_db(self):
        hostip = self.request.form['hostip']
        
        sql = f"""'SELECT DISTINCT(schema_name) FROM events_statements_summary_by_digest WHERE hostip = '{hostip}'"""
        data_1=self.exe_sql_one_col(sql)
        
        return {
            'status':True,
            'data':data_1
        }

    def get_db_names(self):
        sql = 'select dbname,vip from yandi.db where deleted = false;'
        results = self.exe_sql(sql=sql)
        return {
            'status':True,
            'data':results
        }

    def get_slow_log(self):
        start_time = self.request.form['start_time']
        stop_time = self.request.form['stop_time']
        hostip = self.request.form['hostip']
        hostip = hostip.split('_')[0]

        sql = f"""SELECT
  DATE_FORMAT(start_time, '%Y-%m-%d %H:%i:%s') start_time,
  query_time,
  lock_time,
  rows_sent,
  rows_examined,
  LEFT(sql_text,500) as sql_text,
  db,
  user_host
FROM
  mysql.slow_log
WHERE start_time >= '{start_time}' and start_time <= '{stop_time}'  LIMIT 100;"""       
                
        
        if hostip == '':
            msg='警告:请填写IP信息'
            detail_slow_logs=''
        else:
            msg='获取成功'
            detail_slow_logs = self.remote_excute(hostip,35972,'yunwei','testpwd','mysql',sql)

            
        return {
            'status':True,
            'msg':msg,
            'data':{
                'detail':detail_slow_logs,
            }
        }
        
        
    def auto_complete(self):
        schema_lists = []
        host = self.request.form['host']
        host = host.split('_')[0]
        only_schemas = self.request.form['only_schemas']
        schema_sql = ''' SELECT DISTINCT(TABLE_SCHEMA) FROM yandi.tables WHERE hostip = '{0}';'''.format(host)

        # 获取数据库名
        schema_results = self.exe_sql_no_col(sql=schema_sql)
        for schema in schema_results:
            schema_lists.append(schema[0])

        print(schema_lists)
        return {
            'status': True,
            'data': {'schemas': schema_lists}
        }
       
    def get_top_sql(self):
        start_time = self.request.form['start_time']
        stop_time = self.request.form['stop_time']
        hostip = self.request.form['hostip']
        hostip = hostip.split('_')[0]
        schema= self.request.form['db_name']
        sql = f'''SELECT
  *
FROM
  (SELECT
    hostip,
    schema_name,
    digest,
    digest_text,
    MAX(count_star) AS last_time,
    MIN(count_star) AS first_time,
    MAX(count_star) - MIN(count_star) AS all_time,
    MIN(CREATE_date) as min_time,
    MAX(CREATE_date) as max_time
  FROM
    yandi.events_statements_summary_by_digest
  WHERE hostip = '{hostip}'
    AND schema_name = '{schema}'
    AND CREATE_date > '{start_time}'
    AND CREATE_date < '{stop_time}'
  GROUP BY digest,
    schema_name
  ORDER BY all_time DESC) a
WHERE all_time > 0'''     


        sql_1 = f'''SELECT
  *
FROM
  (SELECT
    hostip,
    schema_name,
    digest,
    digest_text,
    MAX(count_star) AS last_time,
    MIN(count_star) AS first_time,
    MAX(count_star) - MIN(count_star) AS all_time,
    MIN(CREATE_date) as min_time,
    MAX(CREATE_date) as max_time
  FROM
    yandi.events_statements_summary_by_digest
  WHERE hostip = '{hostip}'
    AND CREATE_date > '{start_time}'
    AND CREATE_date < '{stop_time}'
  GROUP BY digest,
    schema_name
  ORDER BY all_time DESC) a
WHERE all_time > 0'''  

        
        if schema=='':
            res=self.exe_sql(sql_1)
        else:
            res=self.exe_sql(sql)
            
        return {
            'status':True,
            'msg':'成功获取数据',
            # 'data':self.exe_sql(sql)
            'data':res
        }