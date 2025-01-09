import pymysql
import time
import os
import datetime
from concurrent.futures import ThreadPoolExecutor
from settings import *
import random
import logging
import string
import redis
from db_driver import mysql_driver

script_dir=script_dir
rootuser=root_user
rootpwd=root_pwd
datastack_ip=datastack_ip
instance_max=666666

class add_redis(mysql_driver):

    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request

    def install_redis(self):
        ip = self.request.form['ip']
        description = self.request.form['description']
        buffer_pool_size = self.request.form['buffer_pool_size']
        pwd = self.request.form['pwd']
        port = self.request.form['port']
        
        sql_check_one=f"select * from yandi.redis_ins where ip='{ip}' and deleted = 0;"
        res_check_one=self.exe_sql(sql_check_one)   
        
        cmd_os='''if [ -e /app/redis/ ]; then echo "exist"; fi'''
        res_cmd_os=self.remote_ssh(cmd_os,ip,rootuser,rootpwd)
        cmd_os_app='''if [ -e /app/ ]; then echo "exist"; fi'''
        res_cmd_os_app=self.remote_ssh(cmd_os_app,ip,rootuser,rootpwd)
        logging.warning('res_cmd_os:{0},res_cmd_os_app:{1}'.format(res_cmd_os,res_cmd_os_app))

        sql_select='''SELECT COUNT(*)  AS instacnce_count  FROM yandi.`redis_ins` WHERE deleted=0;'''
        instacnce_count=self.exe_sql(sql_select)[0]['instacnce_count']
        #验证实例个数限制
        if instacnce_count<instance_max:  
            if res_check_one==() and res_cmd_os is None and res_cmd_os_app is not None:
                sql_1=f"INSERT INTO yandi.redis_ins(ip,`port`,description,pwd,buffer) VALUES('{ip}','{port}','{description}','{pwd}','{buffer_pool_size}'); "
                self.exe_sql(sql_1)
                status=True
                msg="success"
            #add mysql user
                cmd_groupadd="groupadd mysql"
                cmd_useradd="useradd mysql -g mysql"
                cmd_chpasswd="echo mysql:testpwd6 | chpasswd"
                self.remote_ssh(cmd_groupadd,ip,root_user,root_pwd)
                self.remote_ssh(cmd_useradd,ip,root_user,root_pwd)
                self.remote_ssh(cmd_chpasswd,ip,root_user,root_pwd)
            #修改app属组
                cmd_change_app="chown -R mysql.mysql /app"
                self.remote_ssh(cmd_change_app,ip,root_user,root_pwd)
                time.sleep(5)
                executor = ThreadPoolExecutor(3)    # 参数设置线程池大小
                # 交由线程去执行耗时任务
                t1=executor.submit(self.install_single_redis,ip,rootuser,rootpwd,buffer_pool_size,pwd,port)                
            
            else:
                status='False'
                msg="实例已存在或/app目录异常"
        else:
            status='False'
            msg="已达到最大实例数"
        
        sql="SELECT `description`,vip,`port`,GROUP_CONCAT(ip)  AS ips,date_created  FROM redis_ins  WHERE deleted=0 GROUP BY vip;"
            
        return {
            'status':status,
            'msg': msg,
            # 'data':self.exe_sql(sql)
            'data':self.get_inventory()['data']
        }
  

    def install_single_redis(self,ip,root_user,root_pwd,buffer_pool_size,pwd,port):
      try:
        #上传安装包
        res_1=self.remote_ssh_put('/app/yandi/redis.tar.gz','/tmp/redis.tar.gz',ip,root_user,root_pwd)
        if res_1==1 :
          sql_11=f"update redis_ins set status='上传失败' where ip='{ip}' and deleted=0;"
          self.exe_sql(sql_11)
        else:
          sql_11=f"update redis_ins set status='上传成功' where ip='{ip}' and deleted=0;"
          self.exe_sql(sql_11)
          cmd_tar="tar -xvf /tmp/redis.tar.gz -C /app/"
          self.remote_ssh(cmd_tar,ip,root_user,root_pwd)
          #修改pwd
          sql_serverid=f"update redis_ins set status='修改pwd' where ip='{ip}' and deleted=0;"
          self.exe_sql(sql_serverid) 
        #   cmd_serverid=f'''sed -i 's/s33rt68nh/{pwd}/' /app/redis_data/redis.conf'''
          cmd_serverid=f'''sed -i 's/testpwd6/{pwd}/' /app/redis_data/users.acl'''
          self.remote_ssh(cmd_serverid,ip,root_user,root_pwd)
          #修改buffer pool
          cmd_buffer=f'''sed -i 's/1024m/{buffer_pool_size}GB/' /app/redis_data/redis.conf'''
          self.remote_ssh(cmd_buffer,ip,root_user,root_pwd)
          #修改port
          cmd_buffer=f'''sed -i 's/port 10000/port {port}/' /app/redis_data/redis.conf'''
          self.remote_ssh(cmd_buffer,ip,root_user,root_pwd)
          #start mysql 
          sql_startmysql=f"update redis_ins set status='启动redis' where ip='{ip}' and deleted=0;"
          self.exe_sql(sql_startmysql) 
          cmd_start="/app/redis/src/redis-server /app/redis_data/redis.conf"
          self.remote_ssh_noresult(cmd_start,ip,root_user,root_pwd)
          sql_startmysqlend=f"update redis_ins set status='启动redis成功' where ip='{ip}' and deleted=0;"
          self.exe_sql(sql_startmysqlend) 

          #modify /etc/bashrc
          bashcmd1=f'''echo 'alias redistart="/app/redis/src/redis-server /app/redis_data/redis.conf"' >> /etc/bashrc'''
          bashcmd2=f'''echo 'alias redistop="pkill redis-server"' >> /etc/bashrc'''
          bashcmd3=f'''echo 'alias myredis="/app/redis/src/redis-cli -p 10000"' >> /etc/bashrc'''
          bashcmd4=f'''echo 'alias redata="cd /app/redis_data"' >> /etc/bashrc'''
          bashcmd5=f'''echo 'alias recmd="cd /app/redis/src"' >> /etc/bashrc'''
          self.remote_ssh(bashcmd1,ip,root_user,root_pwd)
          self.remote_ssh(bashcmd2,ip,root_user,root_pwd)
          self.remote_ssh(bashcmd3,ip,root_user,root_pwd)
          self.remote_ssh(bashcmd4,ip,root_user,root_pwd)
          self.remote_ssh(bashcmd5,ip,root_user,root_pwd)
          self.install_monitor(ip)
      except Exception as e:
        # sql_11=f"update redis_ins set status='部署失败' where ip='{ip}' and deleted=0;"
        # self.exe_sql(sql_11)
        logging.warning('install_single_redis err:{0}'.format(e))
           
  
    def get_inventory(self):
        sql='''SELECT ip,`port`,redis_type,description,date_created,pwd FROM yandi.`redis_ins` WHERE deleted=0;'''
        data_ip=self.exe_sql(sql)
        for i in data_ip:
            ip=i['ip']
            port=i['port']
            pwd=i['pwd']
            try:
                pool = redis.ConnectionPool(host=ip, port=port, db=0,password=pwd)
                r = redis.Redis(connection_pool=pool)
                # slowlog = r.slowlog_get()
                info_memory = r.info('memory')
                use_mem=info_memory['used_memory_human']
                totle_meme=info_memory['maxmemory_human']
                details=use_mem + '/' + totle_meme
                i['status'] = '运行中'
                i['details'] = details
            except Exception as e:
                i['status'] = '等待中'
                i['details'] = '等待中'
        return {
            'status':True,
            'msg':'success',
            'data':data_ip
        }
    
    def install_monitor(self,ip):
      try:
 
                mysql_ip=ip
                logging.warning('install monitor:{0}'.format(mysql_ip))
                cmd_os='''if [ -e /app/jiankong/ ]; then echo "exist"; fi'''
                res_cmd_os=self.remote_ssh(cmd_os,ip,rootuser,rootpwd)
                if res_cmd_os is None:
                    self.remote_ssh_put('/app/jiankong/node_exporter.tar.gz','/app/jiankong/node_exporter.tar.gz',mysql_ip,'mysql','testpwd6')
                    #unzip
                    cmd_5="tar -xvf /app/jiankong/node_exporter.tar.gz -C /app/jiankong/"
                    self.remote_ssh(cmd_5,mysql_ip,'mysql','testpwd6')
                    #start monitor
                    cmd_7="source /app/jiankong/node_exporter/start.sh"
                    self.remote_ssh(cmd_7,mysql_ip,'mysql','testpwd6')
                    cmd_9=f"sed -i '3a\  - {mysql_ip}' /app/jiankong/prometheus/host.yml"
                    os.system(cmd_9)
                    cmd_11=" /app/jiankong/prometheus/promtool check config /app/jiankong/prometheus/prometheus.yml"
                    os.system(cmd_11)
                    sql_1=f"update yandi.redis_ins set monitor=1 where ip='{mysql_ip}';"
                    self.exe_sql(sql_1)
                    logging.warning('end install monitor:{0}'.format(mysql_ip))
      except Exception as e:
                logging.warning('install monitor err:{0}'.format(e))

    

    def delete_inventory(self):
        ip =self.request.form['ip']
    
        sql = f'''update yandi.redis_ins set deleted=1 where ip='{ip}';'''
        self.exe_sql(sql)
              
        return {
            'status': True,
            'msg': '删除成功',
            'data': self.get_inventory()['data']
        }

    def modify_rds(self):
        ip = self.request.form['ip']
        description = self.request.form['description']
        sql_1 = f"update yandi.redis_ins set description='{description}' where ip = '{ip}' and  deleted = 0;"
        self.exe_sql(sql_1)
        
        return {
            'status':True,
            'msg': 'success',
            # 'data':self.exe_sql(sql)
            'data':self.get_inventory()['data']
        }
        
   
        
        