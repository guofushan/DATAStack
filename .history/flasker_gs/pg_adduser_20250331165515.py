import pymysql
import time
import logging
# import json
from db_driver import mysql_driver

class pg_adduser(mysql_driver):

    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request
            
    def get_privilege(self):
        vip=self.request.form['vip']
        port=self.request.form['port']
        
        msg="success"
        sql=f'''SELECT
  grantee,
  table_schema,
  passwd,
  (CASE WHEN privilege='SELECT' THEN '只读' WHEN privilege='SELECT,UPDATE,INSERT,DELETE' THEN '仅DML' WHEN privilege='ALL' THEN '读写（DDL+DML）' ELSE '暂无' END) AS grante
  
FROM
  `pg_user_privilege`
WHERE vip = '{vip}' AND PORT={port}
  AND is_delete = 0
ORDER BY grantee;'''
        data=self.exe_sql(sql)
    
        return {
            'status':True,
            'msg':msg,
            'data':data
        }
   
        
    def get_dbname(self):
        vip=self.request.form['vip']
        port=self.request.form['port']
        sql=f"select datname  AS dbs from pg_database where datname not in ('template1','template0');"
        msg='获取成功'
        data= self.pg_execute(sql,vip,'postgres','postgres','so3evA1CWy',port)
        #拼接schema
        aa=[]
        for i in data:
            dbs=i['dbs']
            sql_1="SELECT nspname AS schema_name FROM pg_catalog.pg_namespace where nspname not in ('pg_toast','pg_catalog','information_schema'); "
            # data1=self.pg_execute(sql_1,vip,'postgres','postgres','so3evA1CWy',port)
            data1=self.pg_execute(sql_1,vip,dbs,'postgres','so3evA1CWy',port)
            for ii in data1:
                schemas=ii['schema_name']
                schemaname=f'''{dbs}.{schemas}'''
                aa.append(schemaname) 
        
        return {
            'status':True,
            'msg':msg,
            'data':aa
        }
        
          
    def create_user(self):
    #   try:
        user_name = self.request.form['user_name']
        user_passwd = self.request.form['user_passwd']
        vip=self.request.form['vip']
        # logging.warning('create_user db: {0}'.format(dbname))
        port=self.request.form['port']
        db_name=self.request.form['db_name']
        role_name=self.request.form['role_name']

        if user_name=='' or user_passwd=='':
            msg='警告：请填写完整信息'

        elif user_name!='' and user_passwd!='' and role_name!='' and db_name!='':
             #create user sql
            msg='用户授权成功'
            sql_4=f"create user {user_name} password '{user_passwd}';"
            #判断user是否存在
            judge_user_1=f'''select * from pg_user where usename='{user_name}';'''
            res_judge_user_1=self.pg_execute(judge_user_1,vip,'postgres','postgres','so3evA1CWy',port)
            if res_judge_user_1==[]:
                self.pg_ddl_execute(sql_4,vip,'postgres','postgres','so3evA1CWy',port)
             
            else:
                pass
            #grant
            logging.warning('grant db =: {0}'.format(db_name))
            dbname_1 = db_name.split(',')
            logging.warning('create_user dbname_1: {0}'.format(dbname_1))
            sql_pri=f"SELECT  DISTINCT(privilege) FROM yandi.pg_user_privilege WHERE role ='{role_name}' LIMIT 1;"
            privile=self.exe_sql(sql_pri)[0]['privilege']
            sql_update1=f'''update pg_user_privilege set is_delete=1 where grantee='{user_name}' and vip='{vip}' and port={port} ;''' 
            self.exe_sql(sql_update1)
            
            for str1 in dbname_1:
                str2 = "."
                str_db=str1[:str1.index(str2)]
                str_schema=str1[str1.index(str2):][1:]
                logging.warning('str_db : {0},str_schema : {1}'.format(str_db,str_schema))
                grantsql_1=f'''REVOKE  CREATE  ON SCHEMA public from public;'''
                grantsql_2=f'''grant usage on schema {str_schema} to {user_name};'''
                grantsql_3=f'''grant {privile} on all tables in schema {str_schema} to {user_name};'''
                grantsql_4=f'''alter default privileges in schema {str_schema} grant {privile} on tables to {user_name};'''
                self.pg_ddl_execute(grantsql_1,vip,str_db,'postgres','so3evA1CWy',port)
                self.pg_ddl_execute(grantsql_2,vip,str_db,'postgres','so3evA1CWy',port)
                self.pg_ddl_execute(grantsql_3,vip,str_db,'postgres','so3evA1CWy',port)
                self.pg_ddl_execute(grantsql_4,vip,str_db,'postgres','so3evA1CWy',port)
                sql_i_1=f'''replace into `pg_user_privilege`(grantee,passwd,vip,port,table_schema,privilege) VALUES('{user_name}','{user_passwd}','{vip}',{port},'{str1}','{privile}')'''
                self.exe_sql(sql_i_1)
        else:
            #create user sql
            sql_4=f"create user {user_name} password '{user_passwd}';"
            #判断user是否存在
            judge_user_1=f'''select * from pg_user where usename='{user_name}';'''
            res_judge_user_1=self.pg_execute(judge_user_1,vip,'postgres','postgres','so3evA1CWy',port)
            if res_judge_user_1==[]:
                self.pg_ddl_execute(sql_4,vip,'postgres','postgres','so3evA1CWy',port)
                msg='用户创建成功'
                sql_i_1=f'''INSERT INTO `pg_user_privilege`(grantee,passwd,vip,port) VALUES('{user_name}','{user_passwd}','{vip}',{port})'''
                self.exe_sql(sql_i_1)
            else:
                msg='用户已存在'
                    
           
        
        sql=f'''SELECT
  grantee,
  table_schema,
  passwd,
  (CASE WHEN privilege='SELECT' THEN '只读' WHEN privilege='SELECT,UPDATE,INSERT,DELETE' THEN '仅DML' WHEN privilege='ALL' THEN '读写（DDL+DML）' ELSE '暂无' END) AS grante
  
FROM
  `pg_user_privilege`
WHERE vip = '{vip}' AND PORT={port}
  AND is_delete = 0
ORDER BY grantee;'''
        data=self.exe_sql(sql)
        
        return {
            'status':True,
            'msg':msg,
            'data':data
        }
      

    # get_role      
    def get_role(self):
        sql = f"SELECT DISTINCT(role) role FROM yandi.`user_privilege` WHERE role <>'';"    

        return {
            'status':True,
            'msg':'成功获取数据',
            'data':self.exe_sql(sql)
        }    
        

    def save_inventory(self):
        grantee = self.request.form['grantee']
        passwd = self.request.form['passwd']
        vip = self.request.form['vip']
        port = self.request.form['port']
        logging.warning('{0},{1}'.format(grantee,passwd))
        
        if passwd=='':
            msg='警告：请填写完整信息'
            # data=''
        else:
            ##modify pg user pwd
            msg='success'
            # aa='yhuj@1%'
            # bb=grantee.replace('@',"'@'")
            # cc="'" + bb + "'"
            # modify_sql_1=f'''SET PASSWORD FOR {cc} = PASSWORD('{passwd}');''' 
            # self.remote_excute(vip,35972,'yunwei','so3evA1CWy','mysql',modify_sql_1)
            mdfy_1=f'''alter user {grantee} password '{passwd}';'''
            self.pg_ddl_execute(mdfy_1,vip,'postgres','postgres','so3evA1CWy',port)

            sql = f'''update yandi.pg_user_privilege set passwd='{passwd}' where vip='{vip}' and port={port} and grantee='{grantee}' and is_delete=0;'''
            self.exe_sql(sql)
       
        return {
            'status': True,
            'msg': msg,
            'data': self.get_privilege()['data']
        }


    def delete_inventory(self):
        vip = self.request.form['vip']
        port = self.request.form['port']
        grantee = self.request.form['grantee']
        privilege_1 = self.request.form['grante']
        table_schema = self.request.form['table_schema']
    #revoke 
        if table_schema=='':
            ##delete mysql user
            drop_sql_1=f'''ALTER ROLE {grantee} NOLOGIN;'''
            logging.warning('drop user sql: {0}'.format(drop_sql_1))
            self.pg_ddl_execute(drop_sql_1,vip,'postgres','postgres','so3evA1CWy',port)
            #update yandi
            sql = f'''UPDATE yandi.pg_user_privilege SET is_delete =1 WHERE vip='{vip}' and port= {port} and grantee='{grantee}';'''
            self.exe_sql(sql)
        else:
            if privilege_1=='仅DML':
                privilege_2='SELECT,UPDATE,INSERT,DELETE'
            elif privilege_1=='读写（DDL+DML）':
                privilege_2='ALL'
            elif privilege_1=='只读':
                privilege_2='SELECT'
            
            str2 = "."
            str_db=table_schema[:table_schema.index(str2)]
            str_schema=table_schema[table_schema.index(str2):][1:]
        #revoke sql
            revok_1=f'''revoke {privilege_2} on all tables in schema {str_schema} from {grantee};'''
            self.pg_ddl_execute(revok_1,vip,str_db,'postgres','so3evA1CWy',port)
            # revoke select on all tables in schema public from sel;
            sql = f'''UPDATE yandi.pg_user_privilege SET is_delete =1 WHERE vip='{vip}' and port= {port} and grantee='{grantee}' and table_schema='{table_schema}';'''
            self.exe_sql(sql)
             
        return {
            'status': True,
            'msg': '删除成功',
            'data': self.get_privilege()['data']
        }


