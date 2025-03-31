import pymysql
import logging
import time
from db_driver import mysql_driver

class pg_dbcreate(mysql_driver):

    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request
        
    def get_dbinfo(self):
        vip = self.request.form['vip']
        port = self.request.form['port']

        # sql='''SELECT a.datname,pg_encoding_to_char(a.encoding),b.usename  FROM pg_database a,pg_user b where datname not in ('template1','template0') and a.datdba =b.usesysid ;'''
        sql='''SELECT a.datname,pg_encoding_to_char(a.encoding) as char_set,b.usename  FROM pg_database a,pg_user b where datname not in ('template1','template0') and a.datdba =b.usesysid ;'''
        return {
            'status':True,
            'msg':'成功获取数据',
            'data':self.pg_execute(sql,vip,'postgres','postgres','so3evA1CWy',port)
            # pg_execute(self,sql_text,ip,db,user,pwd,port)
        }
        
    def get_owners(self):
        vip = self.request.form['vip']
        port = self.request.form['port']
        sql='''select usename from pg_user;'''
        
        return {
            'status':True,
            'msg':'成功获取数据',
            'data':self.pg_execute(sql,vip,'postgres','postgres','so3evA1CWy',port)
        }

    def save_db(self):
        vip = self.request.form['vip']
        port = self.request.form['port']
        dbname = self.request.form['dbname']
        ownername = self.request.form['ownername']
        logging.warning('{0},{1}'.format(dbname,ownername))
        
        if dbname =="" or ownername =="":
            msg='警告:请填写完整信息'
            sql='''SELECT a.datname,pg_encoding_to_char(a.encoding) as char_set,b.usename  FROM pg_database a,pg_user b where datname not in ('template1','template0') and a.datdba =b.usesysid ;'''
            data=self.pg_execute(sql,vip,'postgres','postgres','so3evA1CWy',port)
        else:
            sql_1=f" create database  {dbname} with owner  {ownername}; "
            res_4=self.pg_ddl_execute(sql_1,vip,'postgres','postgres','so3evA1CWy',port)
            msg='DB创建成功'
     
            sql='''SELECT a.datname,pg_encoding_to_char(a.encoding) as char_set,b.usename  FROM pg_database a,pg_user b where datname not in ('template1','template0') and a.datdba =b.usesysid ;'''
            data=self.pg_execute(sql,vip,'postgres','postgres','so3evA1CWy',port)
             
        
        return {
            'status': True,
            'msg': msg,
            'data': data
        }
