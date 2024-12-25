import pymysql
import time
import logging
# import json
from db_driver import mysql_driver

class redis_adduser(mysql_driver):

    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request
            
    def get_privilege(self):
        ip=self.request.form['ip']

        msg="success"
        sql=f'''SELECT role,user_name,passwd,create_date FROM yandi.`redis_privilege`	 WHERE is_delete=0 AND ip='{ip}';'''
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
        user_passwd = self.request.form['user_passwd']
        role_name = self.request.form['role_name']
        ip=self.request.form['ip']
        
        if user_name=='' or user_passwd=='' or role_name == '':
            msg='警告：请填写完整信息'
            data=''
        else: 
            adduser_1=f'''SELECT pwd,port FROM `redis_ins` WHERE ip='{ip}' AND deleted=0;'''
            pwd_1=self.exe_sql(adduser_1)[0]['pwd']
            redis_port=self.exe_sql(adduser_1)[0]['port']
            logging.warning('redis add user: {0},{1},{2}'.format(pwd_1,redis_port,role_name))
            
            # adduser_2=f'''/app/redis/src/redis-cli -p {redis_port} -a {pwd_1} acl setuser {user_name} >{user_passwd}'''
            # adduser_rd=f'''/app/redis/src/redis-cli -p {redis_port} -a {pwd_1} acl setuser {user_name} on +get>{user_passwd}'''
            adduser_2=f'''sed -i '1a user {user_name} on >{user_passwd} ~* +@all' /app/redis_data/users.acl'''
            adduser_rd=f'''sed -i '1a user {user_name} on >{user_passwd} ~* +get' /app/redis_data/users.acl'''
            adduser_load=f'''/app/redis/src/redis-cli -p {redis_port} -a {pwd_1} acl load'''

            if role_name=='读写':
                sql_user1=f'''select * from yandi.`redis_privilege` where is_delete=0 and ip='{ip}' and user_name='{user_name}';'''
                res_user1=self.exe_sql(sql_user1)
                logging.warning('res_user1: {0}'.format(res_user1))
                if res_user1==():
                    self.remote_ssh(adduser_2,ip,'mysql','testpwd6')
                    msg='用户创建成功'
                    sql_1=f'''INSERT INTO yandi.`redis_privilege`(role,ip,user_name,passwd) VALUES('{role_name}','{ip}','{user_name}','{user_passwd}');'''
                    self.exe_sql(sql_1)
                else:
                    msg='用户已存在'
            else:
                sql_user1=f'''select * from yandi.`redis_privilege` where is_delete=0 and ip='{ip}' and user_name='{user_name}';'''
                res_user1=self.exe_sql(sql_user1)
                logging.warning('res_user1: {0}'.format(res_user1))
                if res_user1==():
                    self.remote_ssh(adduser_rd,ip,'mysql','testpwd6')
                    msg='用户创建成功'
                    sql_1=f'''INSERT INTO yandi.`redis_privilege`(role,ip,user_name,passwd) VALUES('{role_name}','{ip}','{user_name}','{user_passwd}');'''
                    self.exe_sql(sql_1)
                else:
                    msg='用户已存在'
                    
            self.remote_ssh(adduser_load,ip,'mysql','testpwd6')
            
            # msg='用户创建成功'
            sql=f'''SELECT role,user_name,passwd,create_date FROM yandi.`redis_privilege`	 WHERE is_delete=0 AND ip='{ip}';'''
            data=self.exe_sql(sql)
        
        return {
            'status':True,
            'msg':msg,
            'data':data
        }
      

    # get_role      
    def get_role(self):
        sql = f"SELECT   (     CASE       WHEN role = '读写（DDL+DML）'       THEN '读写'       ELSE '只读'     END   ) AS role FROM   (SELECT DISTINCT     (role) role   FROM     yandi.`user_privilege`   WHERE role <> ''     AND role LIKE '%读%' ) aa;"    

        return {
            'status':True,
            'msg':'成功获取数据',
            'data':self.exe_sql(sql)
        }    
        

    def save_inventory(self):
        user_name = self.request.form['user_name']
        passwd = self.request.form['passwd']
        ip = self.request.form['ip']
        logging.warning('{0},{1}'.format(user_name,passwd))
        
        if passwd=='':
            msg='警告：请填写完整信息'
            # data=''
        else:
            old_passwd=f'''SELECT passwd FROM redis_privilege WHERE ip='{ip}' AND is_delete=0 and user_name='{user_name}';'''
            old_passwd=self.exe_sql(old_passwd)[0]['passwd']
            # mdf_1=f'''user {user_name} on >rootroot'''
            mdf_1=f'''sed -i 's/user {user_name} on >{old_passwd}/user {user_name} on >{passwd}/' /app/redis_data/users.acl'''
            self.remote_ssh(mdf_1,ip,'mysql','testpwd6')
            
            adduser_1=f'''SELECT pwd,port FROM `redis_ins` WHERE ip='{ip}' AND deleted=0;'''
            pwd_1=self.exe_sql(adduser_1)[0]['pwd']
            redis_port=self.exe_sql(adduser_1)[0]['port']
            
            adduser_load=f'''/app/redis/src/redis-cli -p {redis_port} -a {pwd_1} acl load'''
            self.remote_ssh(adduser_load,ip,'mysql','testpwd6')

            sql = f'''update yandi.redis_privilege set passwd='{passwd}' where ip='{ip}' and is_delete=0 and user_name='{user_name}';'''
            self.exe_sql(sql)
            msg='success'
       
        return {
            'status': True,
            'msg': msg,
            'data': self.get_privilege()['data']
        }


    def delete_inventory(self):
        ip = self.request.form['ip']
        user_name = self.request.form['user_name']
        del_cmd1=f'''sed -i '/user {user_name} on/d' /app/redis_data/users.acl '''
        
        adduser_1=f'''SELECT pwd,port FROM `redis_ins` WHERE ip='{ip}' AND deleted=0;'''
        pwd_1=self.exe_sql(adduser_1)[0]['pwd']
        redis_port=self.exe_sql(adduser_1)[0]['port']
        
        adduser_load=f'''/app/redis/src/redis-cli -p {redis_port} -a {pwd_1} acl load'''
        self.remote_ssh(del_cmd1,ip,'mysql','testpwd6')
        self.remote_ssh(adduser_load,ip,'mysql','testpwd6')
        
        sql = f'''UPDATE yandi.redis_privilege SET is_delete =1 WHERE ip='{ip}' and user_name='{user_name}' and is_delete=0;'''
        self.exe_sql(sql)
        return {
            'status': True,
            'msg': '删除成功',
            'data': self.get_privilege()['data']
        }


