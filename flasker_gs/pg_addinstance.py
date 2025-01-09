import pymysql
import time
import os
import datetime
from concurrent.futures import ThreadPoolExecutor
from settings import *
import random
import logging
import string
from db_driver import mysql_driver

script_dir=script_dir
rootuser=root_user
rootpwd=root_pwd
datastack_ip=datastack_ip
instance_max=666666

class pg_addinstance(mysql_driver):

    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request

    def getinventory(self):
        sql='''SELECT `description`,vip,`port`,GROUP_CONCAT(ip)  AS ips,run_status ,date_created,(CASE mysql_type WHEN '1' THEN 'MySQL5.7' WHEN '2' THEN 'MySQL8' END) AS mysql_type FROM yandi.pg_inventory  WHERE deleted=0 GROUP BY vip;'''
        data_ip=self.exe_sql(sql)
        for i in data_ip:
            ip=i['vip']
            run_status=i['run_status']
            try:
                sql_check='''SELECT NOW();'''
                res_sql_check = self.remote_excute(ip,35972,'yunwei','testpwd','mysql',sql_check)
                if run_status=='运行中':
                    pass
                else:
                    sql_update_1=f'''update yandi.pg_inventory set run_status='运行中' where vip='{ip}';'''
                    logging.warning('getinventory sql:{0}'.format(sql_update_1))
                    self.exe_sql(sql_update_1)
            except Exception as e:
                sql_update_1=f'''update yandi.pg_inventory set run_status='等待中' where vip='{ip}';'''
                logging.warning('getinventory sql:{0}'.format(sql_update_1))
                self.exe_sql(sql_update_1)
                        

    def get_inventory(self):
        sql_1='''SELECT
  `description`,
  vip,
  `port`,
  GROUP_CONCAT(ip) AS ips,
  run_status AS `status`,
  date_created,
  pg_version
FROM
  yandi.pg_inventory
WHERE deleted = 0
GROUP BY vip;'''
        data_ip_1=self.exe_sql(sql_1)
        # logging.warning('get_inventory res:{0}'.format(data_ip_1))
        return {
            'status':True,
            'msg':'success',
            'data':data_ip_1
        }
           
    
    def install_monitor(self):
      try:
        m_1='''SELECT DISTINCT(ip) AS ip FROM yandi.`pg_inventory` WHERE monitor=0 AND deleted=0;'''
        all_mysql_ip=self.exe_sql(m_1)
        logging.warning('start install monitor:{0}'.format(all_mysql_ip))
        if all_mysql_ip==():
            pass  
        else:
            for i in all_mysql_ip:
                mysql_ip=i['ip']
                logging.warning('install monitor:{0}'.format(mysql_ip))
                v_2=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                cmd_mv=f'''mv /app/jiankong /app/jiankong_{v_2}'''
                self.remote_ssh(cmd_mv,mysql_ip,'mysql','testpwd6')
                cmd_3="mkdir /app/jiankong"
                self.remote_ssh(cmd_3,mysql_ip,'mysql','testpwd6')
            
                self.remote_ssh_put('/app/jiankong/node_exporter.tar.gz','/app/jiankong/node_exporter.tar.gz',mysql_ip,'mysql','testpwd6')
                self.remote_ssh_put('/app/jiankong/mysqld_exporter.tar.gz','/app/jiankong/mysqld_exporter.tar.gz',mysql_ip,'mysql','testpwd6')
                #unzip
                cmd_5="tar -xvf /app/jiankong/node_exporter.tar.gz -C /app/jiankong/"
                cmd_6="tar -xvf /app/jiankong/mysqld_exporter.tar.gz -C /app/jiankong/"
                self.remote_ssh(cmd_5,mysql_ip,'mysql','testpwd6')
                self.remote_ssh(cmd_6,mysql_ip,'mysql','testpwd6')
                #start monitor
                cmd_7="source /app/jiankong/node_exporter/start.sh"
                cmd_8="source /app/jiankong/mysqld_exporter/start.sh"
                self.remote_ssh(cmd_7,mysql_ip,'mysql','testpwd6')
                self.remote_ssh(cmd_8,mysql_ip,'mysql','testpwd6')
                cmd_9=f"sed -i '3a\  - {mysql_ip}' /app/jiankong/prometheus/host.yml"
                cmd_10=f"sed -i '3a\  - {mysql_ip}' /app/jiankong/prometheus/mysql.yml"
                os.system(cmd_9)
                os.system(cmd_10)
                cmd_11=" /app/jiankong/prometheus/promtool check config /app/jiankong/prometheus/prometheus.yml"
                os.system(cmd_11)
                sql_1=f"update yandi.pg_inventory set monitor=1 where ip='{mysql_ip}';"
                self.exe_sql(sql_1)
                logging.warning('end install monitor:{0}'.format(mysql_ip))
      except Exception as e:
        logging.warning('install monitor err:{0}'.format(e))

        

    def get_inventory_all(self):
        executor = ThreadPoolExecutor(2)  # 参数设置线程池大小
            # 交由线程去执行耗时任务
        t1=executor.submit(self.install_monitor)
        sql_1='''SELECT `description`,vip,`port`,GROUP_CONCAT(ip)  AS ips,run_status AS `status`,date_created,(CASE mysql_type WHEN '1' THEN 'MySQL5.7' WHEN '2' THEN 'MySQL8' END) AS mysql_type FROM yandi.pg_inventory  WHERE deleted=0 GROUP BY vip;'''
        data_ip=self.exe_sql(sql_1)
        return  data_ip

    

    def delete_inventory(self):
   
        vip = self.request.form['vip']
        ips =self.request.form['ips']
        #delete dir
        cmd_1="rm -rf /app/mysql"
        cmd_2="service mysql stop"
        cmd_3="service mysqld stop"
        # self.remote_ssh(cmd_2,ip,rootuser,rootpwd)
        # self.remote_ssh(cmd_3,ip,rootuser,rootpwd)
        # self.remote_ssh(cmd_1,ip,rootuser,rootpwd)
        sql = f'''update yandi.pg_inventory set deleted=1 where vip='{vip}';'''
        self.exe_sql(sql)
        #delete user_privilege user
        sql_user = f'''UPDATE yandi.`user_privilege` SET is_delete=1 WHERE vip='{vip}';'''
        self.exe_sql(sql_user)
        #delete yandi.db_name
        sql_db = f'''UPDATE  yandi.db_name  SET is_delete=1 WHERE ip='{vip}';'''
        self.exe_sql(sql_db)
        # sql = 'select id,ip,description,vip,port from yandi.pg_inventory where deleted = 0 ORDER BY vip;'
        sql="SELECT `description`,vip,`port`,GROUP_CONCAT(ip)  AS ips,date_created  FROM pg_inventory  WHERE deleted=0 GROUP BY vip;"
        
        return {
            'status': True,
            'msg': '删除成功',
            'data': self.get_inventory_all()
        }

    def modify_rds(self):
        vip = self.request.form['vip']
        description = self.request.form['description']
        sql_1 = f"update yandi.pg_inventory set description='{description}' where vip = '{vip}' and  deleted = 0;"
        self.exe_sql(sql_1)
        # sql = 'select id,ip,description,vip,port from yandi.pg_inventory where deleted = 0 ORDER BY vip;'        
        sql="SELECT `description`,vip,`port`,GROUP_CONCAT(ip)  AS ips,date_created  FROM pg_inventory  WHERE deleted=0 GROUP BY vip;"
        
        return {
            'status':True,
            'msg': 'success',
            # 'data':self.exe_sql(sql)
            'data':self.get_inventory_all()
        }
        
    def save_ha(self):
        ip_one = self.request.form['ip_one']
        description = self.request.form['description']
        ip_two = self.request.form['ip_two']
        bufpool = self.request.form['bufpool']
     
        rand_str = ''.join(random.choices(string.ascii_lowercase , k=10))
        rand_vip=f"{rand_str}.service.consul"
        
        sql_check_one=f"select * from yandi.pg_inventory where ip='{ip_one}' and deleted = 0;"
        res_check_one=self.exe_sql(sql_check_one)
        sql_check_two=f"select * from yandi.pg_inventory where ip='{ip_two}' and deleted = 0;"
        res_check_two=self.exe_sql(sql_check_two)       
        
        cmd_os='''if [ -e /app/ ]; then echo "exist"; fi'''
        res_cmd_os_one=self.remote_ssh(cmd_os,ip_one,rootuser,rootpwd)
        res_cmd_os_two=self.remote_ssh(cmd_os,ip_two,rootuser,rootpwd)
        logging.warning('res_cmd_os_one:{0},res_cmd_os_two:{1}'.format(res_cmd_os_one,res_cmd_os_two))
        #判断/app/postgresql是否存在
        cmd_appmysql1='''if [ -e /app/postgresql/ ]; then echo "exist"; fi'''
        res_appmysql1=self.remote_ssh(cmd_appmysql1,ip_one,rootuser,rootpwd)
        
        cmd_appmysql2='''if [ -e /app/postgresql/ ]; then echo "exist"; fi'''
        res_appmysql2=self.remote_ssh(cmd_appmysql2,ip_two,rootuser,rootpwd)
        
        sql_select='''SELECT COUNT(vip) AS instacnce_count FROM (SELECT vip FROM yandi.pg_inventory WHERE deleted = 0 GROUP BY vip) aa;'''
        instacnce_count=self.exe_sql(sql_select)[0]['instacnce_count']
        #验证实例个数限制
        if instacnce_count<instance_max: 
            if res_check_one==() and res_check_two==() and res_cmd_os_one is not None and res_cmd_os_two is not None and ip_one!=ip_two and res_appmysql1 is None and res_appmysql2 is None:
                sql_1=f"INSERT INTO pg_inventory(vip,`port`,ip,ms,description) VALUES('{rand_vip}','35972','{ip_one}','master','{description}'); "
                sql_2=f"INSERT INTO pg_inventory(vip,`port`,ip,ms,description) VALUES('{rand_vip}','35972','{ip_two}','slave','{description}'); "
                self.exe_sql(sql_1)
                self.exe_sql(sql_2)
                status=True
                msg="success"
            #add postgres user
                cmd_groupadd="groupadd postgres"
                cmd_useradd="useradd postgres -g postgres"
                cmd_chpasswd="echo postgres:testpwd6 | chpasswd"
                self.remote_ssh(cmd_groupadd,ip_one,root_user,root_pwd)
                self.remote_ssh(cmd_useradd,ip_one,root_user,root_pwd)
                self.remote_ssh(cmd_chpasswd,ip_one,root_user,root_pwd)
                
                self.remote_ssh(cmd_groupadd,ip_two,root_user,root_pwd)
                self.remote_ssh(cmd_useradd,ip_two,root_user,root_pwd)
                self.remote_ssh(cmd_chpasswd,ip_two,root_user,root_pwd)
            #修改app属组
                # cmd_change_app="chown -R mysql.mysql /app"
                # self.remote_ssh(cmd_change_app,ip_one,root_user,root_pwd)
                # self.remote_ssh(cmd_change_app,ip_two,root_user,root_pwd)
                time.sleep(3)
                
                executor = ThreadPoolExecutor(3)    # 参数设置线程池大小
                # 交由线程去执行耗时任务
                t1=executor.submit(self.install_ha_mysql,ip_one,ip_two,rootuser,rootpwd,'master',bufpool,db_version)
                time.sleep(1)
                t2=executor.submit(self.install_ha_mysql,ip_two,ip_one,rootuser,rootpwd,'slave',bufpool,db_version)
            
                #添加consul到dns
                logging.warning('start dns_modify_1')
                dns_modify_1=f'''sed -i '1a server=/{rand_vip}/{ip_one}#8600' /etc/dnsmasq.conf'''
                dns_modify_2=f'''sed -i '1a server=/{rand_vip}/{ip_two}#8600' /etc/dnsmasq.conf'''
                dns_restart='''service dnsmasq restart'''
                
                if datastack_ip=='10.10.10.10':
                    # os.system(dns_modify_1)
                    # os.system(dns_modify_2)
                    # os.system(dns_restart)
                    self.remote_ssh_noresult(dns_modify_1,datastack_ip,rootuser,rootpwd)
                    self.remote_ssh_noresult(dns_modify_2,datastack_ip,rootuser,rootpwd)
                    self.remote_ssh_noresult(dns_restart,datastack_ip,rootuser,rootpwd)
                else:
                    self.remote_ssh_noresult(dns_modify_1,datastack_ip,rootuser,rootpwd)
                    self.remote_ssh_noresult(dns_modify_2,datastack_ip,rootuser,rootpwd)
                    self.remote_ssh_noresult(dns_restart,datastack_ip,rootuser,rootpwd)
                
            else:
                status='False'
                msg="实例已存在或/app目录异常"
        else:
            status='False'
            msg="已达到最大实例数"
    
# sql = 'select id,ip,description,vip,port from yandi.pg_inventory where deleted = 0 ORDER BY vip;'
        sql="SELECT `description`,vip,`port`,GROUP_CONCAT(ip)  AS ips,date_created  FROM pg_inventory  WHERE deleted=0 GROUP BY vip;"


        return {
            'status':status,
            'msg': msg,
            # 'data':self.exe_sql(sql)
            'data':self.get_inventory_all()
        }
    
    
    def install_ha_mysql(self,ip,ip_master,root_user,root_pwd,ms,bufpoolsize,db_version):
      try:
        #上传安装包
        res_1=self.remote_ssh_put('/app/yandi/pg.tar.gz','/tmp/pg.tar.gz',ip,root_user,root_pwd)
        if res_1==1 :
          sql_11=f"update pg_inventory set status='上传失败' where ip='{ip}' and deleted=0;"
          self.exe_sql(sql_11)
        else:
          sql_11=f"update pg_inventory set status='上传成功' where ip='{ip}' and deleted=0;"
          self.exe_sql(sql_11)
          #unzip 
          cmd_tar="tar -xvf /tmp/pg.tar.gz -C /app/"
          self.remote_ssh(cmd_tar,ip,root_user,root_pwd)

        #修改buffer pool
          cmd_buffer=f'''sed -i 's/shared_buffers = 438MB/shared_buffers = {bufpoolsize}GB/' /app/postgresql/data/pg/pgdata/postgresql.conf'''
          self.remote_ssh(cmd_buffer,ip,root_user,root_pwd)
          #chown postgres
          cmd_change="chown -R postgres.postgres /app/postgresql"
          self.remote_ssh(cmd_change,ip,root_user,root_pwd)
          #rpm yum
          rpm_1='''yum -y install readline-devel zlib-devel make gcc bzip2 perl perl-ExtUtils-Embed python python-devel openssl-devel libxml2-devel pam-devel libxslt-devel openldap-devel gcc-c++ cmake libuuid-devel uuid uuid-devel-1.6.2-26.el7.x86_64.rpm openssl libicu-devel unzip uuid-devel glibc-headers kernel-headers pam libxml2 libxslt tcl tcl-devel openldap expect'''
          self.remote_ssh_noresult(rpm_1,ip,root_user,root_pwd)

          #start pg 
          sql_startmysql=f"update pg_inventory set status='启动pg' where ip='{ip}' and deleted=0;"
          self.exe_sql(sql_startmysql) 
          cmd_start="/app/postgresql/app/pg/bin/pg_ctl -D /app/postgresql/data/pg/pgdata start &"
          self.remote_ssh_noresult(cmd_start,ip,'postgres','testpwd6')
          sql_startmysqlend=f"update pg_inventory set status='启动mysql成功' where ip='{ip}' and deleted=0;"
          self.exe_sql(sql_startmysqlend) 
          time.sleep(16)
          
          if ms=='slave':
              time.sleep(30)
              #判断主库是否已经启动
              while True:
                try:
                    # sql_judge='''SELECT NOW();'''
                    sql_judge='''SHOW VARIABLES LIKE 'server_uuid';'''
                    res_sql_judge= self.remote_excute(ip_master,35972,'yunwei','testpwd','mysql',sql_judge)[0]['Value']
                    logging.warning('mysql master server: {0}'.format(res_sql_judge))
                    if res_sql_judge=='9177ff20-b9ba-11ee-b8ae-fab77148ac00':
                        logging.warning('mysql master is stop: {0},serverid:{1}'.format(ip_master,res_sql_judge))
                    else:
                        logging.warning('mysql master is start: {0},serverid:{1}'.format(ip_master,res_sql_judge))
                        break
                    # logging.warning('mysql master is start: {0}'.format(ip_master))
                    # break
                except Exception as cc:
                    logging.warning('mysql master is stop.')
                    
              c_3='''reset slave all;'''
              c_4='''reset master;'''
              self.remote_excute(ip,35972,'yunwei','testpwd','mysql',c_3)
              self.remote_excute(ip,35972,'yunwei','testpwd','mysql',c_4)     
              logging.warning('{0},serverid:{1}'.format(c_3,ip))    
              c_1=f'''CHANGE MASTER TO MASTER_HOST='{ip_master}', MASTER_PORT=35972, MASTER_AUTO_POSITION=1, MASTER_USER='zy_repl', MASTER_PASSWORD='co5tvA1CWy';'''
              c_2="start slave;"
              self.remote_excute(ip,35972,'yunwei','testpwd','mysql',c_1)
              self.remote_excute(ip,35972,'yunwei','testpwd','mysql',c_2)
              #set readonly
              sql_rd='''set global read_only=1;'''
              self.remote_excute(ip,35972,'yunwei','testpwd','mysql',sql_rd)
              
              sql_starslave=f"update pg_inventory set status='start slave success.' where ip='{ip}' and deleted=0;"
              self.exe_sql(sql_starslave) 
            
              orch_2=f'''/app/orchestrator/orchestrator -config /app/orchestrator/orchestrator.conf.json -c discover -i {ip}:35972'''
              logging.warning('orch_register: {0}'.format(orch_2))
              os.system(orch_2)
              logging.warning('orch_register_end: {0}'.format(orch_2))
              sql_orch_discover=f"update pg_inventory set status='orch_discover' where ip='{ip}' and deleted=0;"
              self.exe_sql(sql_orch_discover)  
        
          else:
              pass
          #start consul
          #modify json file
          consul_1=f'''sed -i 's/1.1.1.1/{ip}/' /app/consul/server_data/server.json'''
          self.remote_ssh(consul_1,ip,root_user,root_pwd)
          consul_2=f'''sed -i 's/1.1.1.1/{ip}/' /app/consul/server_data/mysql.json'''
          self.remote_ssh(consul_2,ip,root_user,root_pwd)
          consul_3=f'''sed -i 's/2.2.2.2/{ip_master}/' /app/consul/server_data/mysql.json'''
          self.remote_ssh(consul_3,ip,root_user,root_pwd)
          
          c_sql1=f'''SELECT ip,PORT,vip,SUBSTRING_INDEX(vip, '.', 1) AS ser FROM pg_inventory WHERE ip='{ip}' AND deleted=0;'''
          ser=self.exe_sql(c_sql1)[0]['ser']
          logging.warning('ser: {0}'.format(ser))
          consul_4=f'''sed -i 's/mysql_rw/{ser}/' /app/consul/server_data/mysql.json'''
          self.remote_ssh(consul_4,ip,root_user,root_pwd)
 
          sql_modify_consul=f"update pg_inventory set status='modify consul' where ip='{ip}' and deleted=0;"
          self.exe_sql(sql_modify_consul)  
          #add /etc/bashrc
          bashrc_1=f'''echo 'alias consul="/app/consul/consul"' >> /etc/bashrc'''
          self.remote_ssh(bashrc_1,ip,root_user,root_pwd)
          bashrc_2=f'''echo 'alias consulstop="pkill consul&rm -rf /app/consul/server_data/server_metadata.json"' >> /etc/bashrc'''
          self.remote_ssh(bashrc_2,ip,root_user,root_pwd)
          bashrc_3=f'''echo 'alias consulstart="nohup /app/consul/consul agent -config-file=/app/consul/server_data/server.json -config-dir=/app/consul/server_data > /app/consul/server_data/consul.log &"' >> /etc/bashrc'''
          self.remote_ssh(bashrc_3,ip,root_user,root_pwd)
          
          bashcmd1=f'''echo 'alias dba="/app/mysql/dist/bin/mysql -uadmin -ptestpwd -S /tmp/35972.sock"' >> /etc/bashrc'''
          bashcmd2=f'''echo 'alias mysql_start="/app/mysql/dist/bin/mysqld_safe  --defaults-file=/app/my.cnf &"' >> /etc/bashrc'''
          bashcmd3=f'''echo 'alias mysql_stop="/app/mysql/dist/bin/mysqladmin -uadmin -ptestpwd -S /tmp/35972.sock shutdown"' >> /etc/bashrc'''
          bashcmd4=f'''echo 'alias mydata="cd /app/mysql/data"' >> /etc/bashrc'''
          bashcmd5=f'''echo 'alias mylog="cd /app/mysql/log"' >> /etc/bashrc'''
          self.remote_ssh(bashcmd1,ip,root_user,root_pwd)
          self.remote_ssh(bashcmd2,ip,root_user,root_pwd)
          self.remote_ssh(bashcmd3,ip,root_user,root_pwd)
          self.remote_ssh(bashcmd4,ip,root_user,root_pwd)
          self.remote_ssh(bashcmd5,ip,root_user,root_pwd)
            
          sql_modify_bashrc=f"update pg_inventory set status='modify bashrc' where ip='{ip}' and deleted=0;"
          self.exe_sql(sql_modify_bashrc) 
          #start consul
          start_consul="nohup /app/consul/consul agent -config-file=/app/consul/server_data/server.json -config-dir=/app/consul/server_data > /app/consul/server_data/consul.log &"
          self.remote_ssh_noresult(start_consul,ip,root_user,root_pwd)
          sql_start_consul=f"update pg_inventory set status='start consul' where ip='{ip}' and deleted=0;"
          self.exe_sql(sql_start_consul) 
        #install xtrabackup
          cmd_install='''yum localinstall -y /app/percona-xtrabackup* '''
          self.remote_ssh(cmd_install,ip,root_user,root_pwd)           

      except Exception as e:
        # sql_11=f"update pg_inventory set status='部署失败' where ip='{ip}' and deleted=0;"
        # self.exe_sql(sql_11)
            logging.warning('install_ha_mysql err:{0}'.format(e))

        
        
        
        
        