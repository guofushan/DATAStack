import pymysql
from db_driver import mysql_driver
import datetime

class table_size(mysql_driver):

    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request
            
    def get_tableinfo(self):
        sql='''SELECT
  CONCAT(a.TABLE_SCHEMA, '.', a.TABLE_NAME) AS tablename,
  a.hostip,
  MAX(a.TABLE_ROWS) AS TABLE_ROWS,
  ROUND(
    (
      MAX(a.INDEX_LENGTH) + MAX(a.DATA_FREE) + MAX(a.DATA_LENGTH)
    ) / 1024 / 1024 / 1024,
    2
  ) AS tablesize
FROM
  yandi.tables a 
WHERE a.CREATE_date > CURRENT_DATE
GROUP BY a.TABLE_SCHEMA,
  a.TABLE_NAME
ORDER BY tablesize DESC
LIMIT 30;'''
        # sql="SELECT CONCAT(TABLE_SCHEMA,'.',TABLE_NAME) AS tablename,hostip,MAX(TABLE_ROWS) AS TABLE_ROWS,ROUND((MAX(INDEX_LENGTH)+MAX(DATA_FREE)+MAX(DATA_LENGTH))/1024/1024/1024,2) AS tablesize FROM yandi.tables WHERE CREATE_date >CURRENT_DATE GROUP BY TABLE_SCHEMA,TABLE_NAME ORDER BY tablesize DESC LIMIT 30;"
        return {
            'status':True,
            'msg':'成功获取数据',
            'data':self.exe_sql(sql)
        }
        
    def get_insinfo(self):
        sql='''
SELECT cc.*,GROUP_CONCAT(DISTINCT(dd.ip)) AS ip FROM (SELECT
  vip,
  ROUND((
    SUM(INDEX_LENGTH) + SUM(DATA_FREE) + SUM(DATA_LENGTH)
  ) / 1024 / 1024 / 1024,2) AS ins_size
FROM
  (SELECT
    c.vip,
    c.TABLE_SCHEMA,
    c.TABLE_NAME,
    MAX(TABLE_ROWS) AS TABLE_ROWS,
    MAX(INDEX_LENGTH) AS INDEX_LENGTH,
    MAX(DATA_FREE) AS DATA_FREE,
    MAX(DATA_LENGTH) AS DATA_LENGTH
  FROM
    (SELECT
      b.vip,
      a.*
    FROM
      yandi.tables a,
      yandi.`a_inventory` b
    WHERE b.vip = a.hostip
      AND CREATE_date > CURRENT_DATE) c
  GROUP BY c.vip,
    c.TABLE_SCHEMA,
    c.TABLE_NAME
    
    ) d
GROUP BY d.vip
) cc, yandi.`a_inventory`  dd WHERE cc.vip=dd.vip GROUP BY dd.vip ORDER BY ins_size DESC
'''
        return {
            'status':True,
            'msg':'成功获取数据',
            'data':self.exe_sql(sql)
        }
        
    def get_ip(self):
        # sql = f"SELECT distinct(vip) FROM yandi.`inventory` WHERE deleted=0;"   
        sql=f"SELECT DISTINCT(vip) FROM yandi.`a_inventory` WHERE deleted=0;" 

        return {
            'status':True,
            'msg':'成功获取数据',
            'data':self.exe_sql(sql)
        }
        
    def get_detail(self):
        db_ips = self.request.form['db_ips']
        s1 = db_ips.split(',')
        str1 =str(s1)
        bb=str1[1:][:-1]
        
    
        sql=f"""SELECT CONCAT(TABLE_SCHEMA,'.',TABLE_NAME) AS tablename,hostip,MAX(TABLE_ROWS) AS TABLE_ROWS,ROUND((MAX(INDEX_LENGTH)+MAX(DATA_FREE)+MAX(DATA_LENGTH))/1024/1024/1024,2) AS tablesize FROM yandi.`tables` WHERE hostip IN ({bb})
 AND CREATE_date >CURRENT_DATE GROUP BY TABLE_SCHEMA,TABLE_NAME ORDER BY tablesize DESC LIMIT 30;
"""
        return {
            'status':True,
            'msg':'成功获取数据',
            
            'data':self.exe_sql(sql)
        }
   
          
          