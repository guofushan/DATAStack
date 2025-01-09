import pymysql
import time
import logging
# import json
from db_driver import mysql_driver

class mysql_adduser(mysql_driver):

    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request
            
    def get_privilege(self):
        vip=self.request.form['vip']

        msg="success"
        # sql=f''' SELECT  SUBSTRING_INDEX(grantee, "@", 1) AS users,SUBSTRING_INDEX(grantee, "@", - 1) AS ip,passwd,privilege AS grante,table_schema FROM `user_privilege` WHERE vip='{vip}' AND is_delete=0 ORDER BY create_date;'''
        sql=f'''SELECT
  grantee,
  table_schema,
  passwd,
  (CASE WHEN privilege='SELECT' THEN '只读' WHEN privilege='SELECT,UPDATE,INSERT,DELETE' THEN '仅DML' WHEN privilege='SELECT,UPDATE,CREATE,INDEX,EXECUTE,ALTER ROUTINE,INSERT,DELETE,DROP,ALTER,CREATE ROUTINE' THEN '读写（DDL+DML）' ELSE '暂无' END) AS grante
  
FROM
  `user_privilege`
WHERE vip = '{vip}'
  AND is_delete = 0
ORDER BY create_date;'''
        data=self.exe_sql(sql)
    
        return {
            'status':True,
            'msg':msg,
            'data':data
        }
   
    def get_dbname(self):
        vip=self.request.form['vip']
        # sql = f"SELECT dbname AS dbs FROM yandi.db_name WHERE ip='{vip}' AND is_delete=0;"    
        sql=f"SELECT schema_name AS dbs  FROM information_schema.SCHEMATA WHERE schema_name NOT IN('information_schema','mysql','performance_schema','sys');"
        msg='获取成功'
        # data=self.exe_sql(sql)
        data=self.remote_excute(vip,35972,'yunwei','testpwd','mysql',sql)

        return {
            'status':True,
            'msg':msg,
            'data':data
        }
        
          
    def create_user(self):
    #   try:
        user_name = self.request.form['user_name']
        db_ip = self.request.form['db_ip']
        user_passwd = self.request.form['user_passwd']
        dbname = self.request.form['db_name']
        role_name = self.request.form['role_name']
        vip=self.request.form['vip']
        logging.warning('create_user db: {0}'.format(dbname))
        
        if user_name=='' or db_ip=='' or user_passwd=='' or dbname=='' or role_name == '':
            msg='警告：请填写完整信息'
            data=''
    
        else:
            sql_pri=f"SELECT  DISTINCT(privilege) FROM yandi.`user_privilege` WHERE role ='{role_name}' LIMIT 1;"
            privile=self.exe_sql(sql_pri)[0]['privilege']
         
            #grant
            sql_4=f"create user '{user_name}'@'{db_ip}' identified by '{user_passwd}';"
            
            get_port=f"SELECT port FROM yandi.a_inventory  WHERE vip='{vip}' AND deleted=0 LIMIT 1;"
            port=self.exe_sql(get_port)[0]['port']
            port=int(port)
            #判断user是否存在
            judge_user_1=f'''select user,host from mysql.user where user='{user_name}' and host='{db_ip}';'''
            res_judge_user_1=self.remote_excute(vip,port,'yunwei','testpwd','mysql',judge_user_1)
            if res_judge_user_1==():
                res_3=self.remote_excute(vip,port,'yunwei','testpwd','mysql',sql_4)
            else:
                pass
            dbname_1 = dbname.split(',')
            logging.warning('create_user dbname_1: {0}'.format(dbname_1))
            for i_db in dbname_1:
                    #revoke grant
                    # try:
                    #     revoke_sql1=f'''revoke select on {i_db}.* from '{user_name}'@'{db_ip}';'''
                    #     self.remote_excute(vip,port,'yunwei','testpwd','mysql',revoke_sql1)
                    # except Exception as e:
                    #     revoke_sql2=f'''revoke SELECT,UPDATE,INSERT,DELETE on {i_db}.* from '{user_name}'@'{db_ip}';'''
                    #     self.remote_excute(vip,port,'yunwei','testpwd','mysql',revoke_sql2)
                    # finally:
                    #     revoke_sql3=f'''revoke SELECT,UPDATE,CREATE,INDEX,EXECUTE,ALTER ROUTINE,INSERT,DELETE,DROP,ALTER,CREATE ROUTINE on {i_db}.* from '{user_name}'@'{db_ip}';'''
                    #     self.remote_excute(vip,port,'yunwei','testpwd','mysql',revoke_sql3)
                    re_sql_1=f'''SELECT privilege FROM user_privilege WHERE grantee='{user_name}@{db_ip}' AND table_schema='{i_db}' AND is_delete=0 and vip='{vip}';'''
                    # data_re_sql_1=self.exe_sql(re_sql_1)[0]['privilege']
                    data_re_sql_1=self.exe_sql(re_sql_1)
                    if data_re_sql_1==():
                        pass
                    else:
                        data_re_sql_1=data_re_sql_1[0]['privilege']
                        drop_1=f'''revoke {data_re_sql_1} on {i_db}.* from '{user_name}'@'{db_ip}';'''
                        self.remote_excute(vip,port,'yunwei','testpwd','mysql',drop_1)
                    #update  yandi.user_privilege table
                    update_1=f'''update yandi.user_privilege set is_delete=1 where vip='{vip}' and table_schema='{i_db}' and grantee='{user_name}@{db_ip}';'''
                    self.exe_sql(update_1)
                    sql_6=f"INSERT INTO yandi.user_privilege(grantee,table_schema,privilege,vip,passwd) VALUES('{user_name}@{db_ip}','{i_db}','{privile}','{vip}','{user_passwd}')"
                    self.exe_sql(sql_6)
                    #new grant
                    sql_3=f"grant {privile} on {i_db}.* to '{user_name}'@'{db_ip}';"
                    res_4=self.remote_excute(vip,port,'yunwei','testpwd','mysql',sql_3)
                    
            sql_2="flush privileges;"  
            self.remote_excute(vip,port,'yunwei','testpwd','mysql',sql_2)
            msg='用户创建成功'
            sql=f'''SELECT
            grantee,
            table_schema,
            passwd,
            (CASE WHEN privilege='SELECT' THEN '只读' WHEN privilege='SELECT,UPDATE,INSERT,DELETE' THEN '仅DML' WHEN privilege='SELECT,UPDATE,CREATE,INDEX,EXECUTE,ALTER ROUTINE,INSERT,DELETE,DROP,ALTER,CREATE ROUTINE' THEN '读写（DDL+DML）' ELSE '暂无' END) AS grante
            
            FROM
            `user_privilege`
            WHERE vip = '{vip}'
            AND is_delete = 0
            ORDER BY create_date;'''
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
        logging.warning('{0},{1}'.format(grantee,passwd))
        
        if passwd=='':
            msg='警告：请填写完整信息'
            # data=''
        else:
            ##modify mysql user pwd
            msg='success'
            # aa='yhuj@1%'
            bb=grantee.replace('@',"'@'")
            cc="'" + bb + "'"
            modify_sql_1=f'''SET PASSWORD FOR {cc} = PASSWORD('{passwd}');''' 
            self.remote_excute(vip,35972,'yunwei','testpwd','mysql',modify_sql_1)
            
            
            sql = f'''update yandi.user_privilege set passwd='{passwd}' where vip='{vip}' and grantee='{grantee}' and is_delete=0;'''
            self.exe_sql(sql)
       
        return {
            'status': True,
            'msg': msg,
            'data': self.get_privilege()['data']
        }


    def delete_inventory(self):
        vip = self.request.form['vip']
        grantee = self.request.form['grantee']
        bb=grantee.replace('@',"'@'")
        cc="'" + bb + "'"
        ##delete mysql user
        drop_sql_1=f'''drop user {cc};'''
        logging.warning('drop user sql: {0}'.format(drop_sql_1))
        self.remote_excute(vip,35972,'yunwei','testpwd','mysql',drop_sql_1)
        
        sql = f'''UPDATE yandi.user_privilege SET is_delete =1 WHERE vip='{vip}' and grantee='{grantee}';'''
        self.exe_sql(sql)
        return {
            'status': True,
            'msg': '删除成功',
            'data': self.get_privilege()['data']
        }


