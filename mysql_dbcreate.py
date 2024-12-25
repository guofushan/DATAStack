import pymysql
import logging
import time
from db_driver import mysql_driver

class mysql_dbcreate(mysql_driver):

    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request
            
    def get_dbinfo(self):
        vip = self.request.form['vip']

        # sql = f'''SELECT vip,GROUP_CONCAT(DISTINCT(ip)) AS ip,PORT,GROUP_CONCAT(DISTINCT(dbname)) AS db FROM (SELECT b.vip,b.ip,a.port,a.dbname FROM yandi.`db_name` a,yandi.`a_inventory` b WHERE a.ip=b.vip AND b.vip='{vip}') aa GROUP BY vip,PORT'''  
        sql='''SELECT
  `schema_name` AS `schema_name`,
  DEFAULT_CHARACTER_SET_NAME,
  GROUP_CONCAT(users) AS grant_users
FROM
  (SELECT
    sche.schema_name,
    sche.DEFAULT_CHARACTER_SET_NAME,
    oo.users,
    oo.ip
  FROM
    information_schema.`SCHEMATA` sche
    LEFT JOIN
      (SELECT
        SUBSTRING_INDEX(users, "'", - 1) AS users,
        SUBSTRING_INDEX(ip, "'", 1) AS ip,
        table_schema,
        grante
      FROM
        (SELECT
          SUBSTRING_INDEX(grantee, "'", 2) AS users,
          SUBSTRING_INDEX(grantee, "'", - 2) AS ip,
          table_schema,
          GROUP_CONCAT(PRIVILEGE_TYPE) AS grante
        FROM
          information_schema.`SCHEMA_PRIVILEGES`
        WHERE grantee NOT LIKE '%mysql.session%'
          AND grantee NOT LIKE '%mysql.sys%'
        GROUP BY grantee,
          table_schema) a) oo
      ON sche.schema_name = oo.table_schema
      WHERE sche.schema_name NOT IN (
        'information_schema',
        'mysql',
        'performance_schema',
        'sys'
      )) kk
GROUP BY schema_name
ORDER BY grant_users DESC;'''

        return {
            'status':True,
            'msg':'成功获取数据',
            'data':self.remote_excute(vip,35972,'yunwei','testpwd','mysql',sql)
        }

    def save_db(self):
        vip = self.request.form['vip']
        dbname = self.request.form['dbname']
        
        if dbname =="" :
            msg='警告:请填写完整信息'
            sql='''SELECT
  schema_name,
  DEFAULT_CHARACTER_SET_NAME,
  GROUP_CONCAT(users) AS grant_users
FROM
  (SELECT
    sche.schema_name,
    sche.DEFAULT_CHARACTER_SET_NAME,
    oo.users,
    oo.ip
  FROM
    information_schema.`SCHEMATA` sche
    LEFT JOIN
      (SELECT
        SUBSTRING_INDEX(users, "'", - 1) AS users,
        SUBSTRING_INDEX(ip, "'", 1) AS ip,
        table_schema,
        grante
      FROM
        (SELECT
          SUBSTRING_INDEX(grantee, "'", 2) AS users,
          SUBSTRING_INDEX(grantee, "'", - 2) AS ip,
          table_schema,
          GROUP_CONCAT(PRIVILEGE_TYPE) AS grante
        FROM
          information_schema.`SCHEMA_PRIVILEGES`
        WHERE grantee NOT LIKE '%mysql.session%'
          AND grantee NOT LIKE '%mysql.sys%'
        GROUP BY grantee,
          table_schema) a) oo
      ON sche.schema_name = oo.table_schema
      WHERE sche.schema_name NOT IN (
        'information_schema',
        'mysql',
        'performance_schema',
        'sys'
      )) kk
GROUP BY schema_name
ORDER BY grant_users DESC;'''
            data=self.remote_excute(vip,35972,'yunwei','testpwd','mysql',sql)
        else:
            sql_1=f"create database {dbname};"
            res_4=self.remote_excute(vip,35972,'yunwei','testpwd','mysql',sql_1)
            sql_6=f"INSERT INTO yandi.db_name(dbname,ip,port) VALUES('{dbname}','{vip}','35972')"
            vip=self.exe_sql(sql_6)
            msg='DB创建成功'
     
            data=self.get_dbinfo()['data']
            
        # logging.warning('save_db vip: {0}'.format(vip))
        # logging.warning('save_db data: {0}'.format(data))
        
        return {
            'status': True,
            'msg': msg,
            'data': data
        }
