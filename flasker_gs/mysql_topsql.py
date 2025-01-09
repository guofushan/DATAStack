from db_driver import mysql_driver
from user import User
import random
class mysql_topsql(mysql_driver):
    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request
      
    def auto_complete(self):
        schema_lists = []
        host = self.request.form['host']
        # host = host.split('_')[0]
        # only_schemas = self.request.form['only_schemas']
        # schema_sql = ''' SELECT DISTINCT(TABLE_SCHEMA) FROM yandi.tables WHERE hostip = '{0}';'''.format(host)
        schema_sql='''SELECT SCHEMA_NAME FROM information_schema.`SCHEMATA`;'''
        # 获取数据库名
        
        schema_results = self.remote_excute(host,35972,'yunwei','testpwd','mysql',schema_sql)
        for schema in schema_results:
                schema_lists.append(schema['SCHEMA_NAME'])

        # print(schema_lists)
        return {
            'status': True,
            'data': {'schemas': schema_lists}
        }
       
    def get_top_sql(self):
        start_time = self.request.form['start_time']
        stop_time = self.request.form['stop_time']
        hostip = self.request.form['hostip']
        # hostip = hostip.split('_')[0]
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
WHERE all_time > 0 limit 200'''     


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
WHERE all_time > 0 limit 200'''  

        
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