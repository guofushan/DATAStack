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
cluster_ip=cluster_ip
cluster_ip=eval(cluster_ip)
instance_max=666666

class pg_addinstance(mysql_driver):

    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request

    def getinventory(self):
        sql='''SELECT
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
        data_ip=self.exe_sql(sql)
        for i in data_ip:
            ip=i['vip']
            run_status=i['status']
            try:
                sql_check='''SELECT NOW();'''
                res_sql_check = self.remote_excute(ip,35972,'yunwei','so3evA1CWy','mysql',sql_check)
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


    def get_inventory_all(self):
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
        data_ip=self.exe_sql(sql_1)
        return  data_ip

    

    def delete_inventory(self):
        #输入参数
        vip = self.request.form['vip']
        ips =self.request.form['ips']
        port =self.request.form['port']

        #更新cmdb
        sql = f'''update yandi.pg_inventory set deleted=1 where vip='{vip}' and port='{port}';'''
        self.exe_sql(sql)
        sql_user = f'''UPDATE yandi.pg_user_privilege SET is_delete=1 WHERE vip='{vip}' and port='{port}';'''
        self.exe_sql(sql_user)
           
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
        #输入信息
        ip_one = self.request.form['ip_one']
        ip_two = self.request.form['ip_two']
        dbport = self.request.form['dbport']
        description = self.request.form['description']
        bufpool = self.request.form['bufpool']
     
        rand_str = ''.join(random.choices(string.ascii_lowercase , k=10))
        rand_vip=f"master.{rand_str}.service.consul"
        
        sql_check_one=f"select * from yandi.pg_inventory where ip='{ip_one}' and port='{dbport}' and deleted = 0;"
        res_check_one=self.exe_sql(sql_check_one)
        sql_check_two=f"select * from yandi.pg_inventory where ip='{ip_two}' and port='{dbport}' and deleted = 0;"
        res_check_two=self.exe_sql(sql_check_two)       
        
        cmd_os='''if [ -e /app/ ]; then echo "exist"; fi'''
        res_cmd_os_one=self.remote_ssh(cmd_os,ip_one,rootuser,rootpwd)
        res_cmd_os_two=self.remote_ssh(cmd_os,ip_two,rootuser,rootpwd)
        logging.warning('res_cmd_os_one:{0},res_cmd_os_two:{1}'.format(res_cmd_os_one,res_cmd_os_two))
        #判断/app/postgresql是否存在
        cmd_appmysql1=f'''if [ -e /app/postgresql/data/data{dbport} ]; then echo "exist"; fi'''
        res_appmysql1=self.remote_ssh(cmd_appmysql1,ip_one,rootuser,rootpwd)
        
        cmd_appmysql2=f'''if [ -e /app/postgresql/data/data{dbport} ]; then echo "exist"; fi'''
        res_appmysql2=self.remote_ssh(cmd_appmysql2,ip_two,rootuser,rootpwd)
        
        #python check
        pcmd1='''python3 --version'''
        res_pcmd1=self.remote_ssh(pcmd1,ip_one,rootuser,rootpwd)
        res_pcmd2=self.remote_ssh(pcmd1,ip_two,rootuser,rootpwd)
        logging.warning('master python vesion:{0}, slave python vesion:{1}'.format(res_pcmd1,res_pcmd2))
        if res_pcmd1== None or res_pcmd2==None:
            status='False'
            msg="Python版本异常"
        else:
            if (res_pcmd1.count('Python 3.9') == 1 and res_pcmd2.count('Python 3.9')==1) or (res_pcmd1.count('Python 3.1') == 1 and res_pcmd2.count('Python 3.1')==1):
                sql_select='''SELECT COUNT(vip) AS instacnce_count FROM (SELECT vip FROM yandi.pg_inventory WHERE deleted = 0 GROUP BY vip) aa;'''
                instacnce_count=self.exe_sql(sql_select)[0]['instacnce_count']
                #验证实例个数限制
                if instacnce_count<instance_max: 
                    if res_check_one==() and res_check_two==() and res_cmd_os_one is not None and res_cmd_os_two is not None and ip_one!=ip_two and res_appmysql1 is None and res_appmysql2 is None:
                        sql_1=f"INSERT INTO pg_inventory(vip,`port`,ip,ms,description) VALUES('{rand_vip}','{dbport}','{ip_one}','master','{description}'); "
                        sql_2=f"INSERT INTO pg_inventory(vip,`port`,ip,ms,description) VALUES('{rand_vip}','{dbport}','{ip_two}','slave','{description}'); "
                        self.exe_sql(sql_1)
                        self.exe_sql(sql_2)
                        status=True
                        msg="success"
                    #add postgres user
                        cmd_groupadd="groupadd postgres"
                        cmd_useradd="useradd postgres -g postgres"
                        cmd_chpasswd="echo postgres:zmzqruq6 | chpasswd"
                        self.remote_ssh(cmd_groupadd,ip_one,root_user,root_pwd)
                        self.remote_ssh(cmd_useradd,ip_one,root_user,root_pwd)
                        self.remote_ssh(cmd_chpasswd,ip_one,root_user,root_pwd)
                        
                        self.remote_ssh(cmd_groupadd,ip_two,root_user,root_pwd)
                        self.remote_ssh(cmd_useradd,ip_two,root_user,root_pwd)
                        self.remote_ssh(cmd_chpasswd,ip_two,root_user,root_pwd)
                
                        time.sleep(3)
                        
                        executor = ThreadPoolExecutor(3)    # 参数设置线程池大小
                        # 交由线程去执行耗时任务
                        t1=executor.submit(self.install_ha_pg,ip_one,ip_two,rootuser,rootpwd,'master',bufpool,dbport,rand_str)
                        time.sleep(1)
                        t2=executor.submit(self.install_ha_pg,ip_two,ip_one,rootuser,rootpwd,'slave',bufpool,dbport,rand_str)
                    
                        #添加consul到dns
                        logging.warning('start dns_modify_pg')
                        for cluster1 in cluster_ip:
                            dns_modify_1=f'''sed -i '1a server=/{rand_vip}/{cluster1}#8600' /etc/dnsmasq.conf'''
                            logging.warning('dnsmasq cmd :{dns_modify_1}')
                            if datastack_ip=='10.88.28.3':
                                # os.system(dns_modify_1)
                                # os.system(dns_restart)
                                self.remote_ssh_noresult(dns_modify_1,datastack_ip,rootuser,rootpwd)
                                # self.remote_ssh_noresult(dns_restart,datastack_ip,rootuser,rootpwd)
                            else:
                                self.remote_ssh_noresult(dns_modify_1,datastack_ip,rootuser,rootpwd)
                                # self.remote_ssh_noresult(dns_restart,datastack_ip,rootuser,rootpwd)
                    #dnsmasq restart
                        dns_restart='''service dnsmasq restart'''
                        self.remote_ssh_noresult(dns_restart,datastack_ip,rootuser,rootpwd)
                        logging.warning('dnsmasq restart.')

                    else:
                        status='False'
                        msg="实例已存在或/app目录异常"
                else:
                    status='False'
                    msg="已达到最大实例数"
            else:
                status='False'
                msg="Python版本异常"
        


        return {
            'status':status,
            'msg': msg,
            'data':self.get_inventory_all()
        }
    
    
    def install_ha_pg(self,ip,ip_master,root_user,root_pwd,ms,bufpoolsize,dbport,rand_str):
      try:
        #上传安装包
        exist_pg1=f'''if [ -e /app/postgresql/app/pg/bin ]; then echo "exist"; fi'''
        res_exist_pg1=self.remote_ssh(exist_pg1,ip,rootuser,rootpwd)
        logging.warning(f'{ip} res_exist_pg1:{res_exist_pg1}')
        if res_exist_pg1 is None:
            res_1=self.remote_ssh_put('/app/yandi/pg.tar.gz','/tmp/pg.tar.gz',ip,root_user,root_pwd)
            if res_1==1 :
              sql_11=f"update pg_inventory set status='上传失败' where ip='{ip}' and port='{dbport}' and deleted=0;"
              self.exe_sql(sql_11)
            else:
              sql_11=f"update pg_inventory set status='上传成功' where ip='{ip}' and port='{dbport}' and deleted=0;"
              self.exe_sql(sql_11)
              #unzip 
              cmd_tar="tar -xvf /tmp/pg.tar.gz -C /app/"
              self.remote_ssh(cmd_tar,ip,root_user,root_pwd)
              unzip_patroni="tar -xvf /app/postgresql/app/pg_extention/patroni.tar.gz -C /app/postgresql/app/pg_extention/"
              self.remote_ssh(unzip_patroni,ip,root_user,root_pwd)
              logging.warning(f'unzip_patroni:{unzip_patroni}')
            #修改buffer pool
            #   cmd_buffer=f'''sed -i 's/shared_buffers = 438MB/shared_buffers = {bufpoolsize}GB/' /app/postgresql/data/pg/pgdata/postgresql.conf'''
            #   self.remote_ssh(cmd_buffer,ip,root_user,root_pwd)
              #chown postgres
              cmd_change="chown -R postgres.postgres /app/postgresql"
              self.remote_ssh(cmd_change,ip,root_user,root_pwd)
              logging.warning(f'cmd_change:{cmd_change}')
              #rpm yum
              rpm_1='''yum  install -y readline-devel zlib-devel make gcc bzip2 perl perl-ExtUtils-Embed  openssl-devel libxml2-devel pam-devel libxslt-devel openldap-devel gcc-c++ cmake libuuid-devel uuid uuid-devel-1.6.2-26.el7.x86_64.rpm openssl libicu-devel unzip uuid-devel glibc-headers kernel-headers pam libxml2 libxslt tcl tcl-devel openldap expect'''
              # self.remote_ssh_noresult(rpm_1,ip,root_user,root_pwd)
              self.remote_ssh(rpm_1,ip,root_user,root_pwd)
              logging.warning(f'rpm_1:{rpm_1}')
              
              #install patroni
              pat_1='''pip3 install --no-index --find-links=/app/postgresql/app/pg_extention/patroni patroni[consul] psycopg2-binary urllib3==1.26.18'''  
              # self.remote_ssh_noresult(pat_1,ip,root_user,root_pwd)
              self.remote_ssh(pat_1,ip,root_user,root_pwd)
              logging.warning(f'pat_1:{pat_1}')
              
              consul_ips = ','.join(f"{consulip}:8500" for consulip in cluster_ip)
              patronifile=f'''
    scope: {rand_str}
    name: {ip}
    restapi:
      listen: 0.0.0.0:8{dbport}
      connect_address: {ip}:8{dbport}

    consul:
      host: {consul_ips}
      register_service: true
      service_name: bbbb
      service_check_interval: 10s
      service_tags:
        - "postgresql"
        - "primary"  # 或 "replica"，根据角色动态调整
    bootstrap:
      dcs:
        ttl: 30
        loop_wait: 10
        retry_timeout: 10
        maximum_lag_on_failover: 1048576
        postgresql:
          use_pg_rewind: true
          use_slots: true
          parameters:
            wal_level: logical
            hot_standby: "on"
            max_wal_senders: 10
            max_replication_slots: 10
            wal_log_hints: "on"
            archive_command: 'pgbackrest --stanza=db1 archive-push %p'
            archive_mode: on  
            wal_log_hints: on
            wal_compression: on
            wal_writer_delay: 10ms
            wal_writer_flush_after: 1MB
            commit_delay: 10
            commit_siblings: 5
            checkpoint_timeout: 30min
            max_wal_size: 32GB
            min_wal_size: 16GB
            max_wal_senders: 64
            wal_keep_size: 128MB
            wal_sender_timeout: 60s
            max_replication_slots: 64
            effective_cache_size: 877MB
            log_destination: 'csvlog'
            logging_collector: on
            log_directory: '/app/postgresql/logs/pg/pglog{dbport}'
            log_filename: 'postgresql-%Y-%m-%d_%H%M%S.log'
            log_file_mode: 0600 
            log_truncate_on_rotation: off
            log_rotation_age: 1d
            log_rotation_size: 1GB
            log_min_duration_statement: 1s
            log_checkpoints: on
            log_connections: on
            log_disconnections: on
            log_error_verbosity: verbose
            log_line_prefix: '%m %p %u %d %r %e'
            log_lock_waits: on
            log_statement: 'all'
            log_timezone: 'Asia/Shanghai'
            timezone: 'Asia/Shanghai'
            track_io_timing: on
            track_activity_query_size: 102400
            autovacuum: on
            vacuum_cost_delay: 0
            log_autovacuum_min_duration: 0
            autovacuum_max_workers: 8
            autovacuum_vacuum_scale_factor: 0.02
            autovacuum_analyze_scale_factor: 0.01
            autovacuum_freeze_max_age: 1200000000
            autovacuum_multixact_freeze_max_age: 1250000000
            autovacuum_vacuum_cost_delay: 0ms
            datestyle: 'iso, mdy'
            timezone: 'Asia/Shanghai'
            lc_messages: 'en_US.utf8'
            lc_monetary: 'en_US.utf8'
            lc_numeric: 'en_US.utf8'
            lc_time: 'en_US.utf8'
            default_text_search_config: 'pg_catalog.english'
            shared_preload_libraries: 'pg_stat_statements'
            cron.database_name: 'postgres'
            pg_stat_statements.max: 10000
            pg_stat_statements.track: all
            pg_stat_statements.track_utility: off
            pg_stat_statements.save: on
            deadlock_timeout: 10s
            max_connections: 2000
            superuser_reserved_connections: 10
            unix_socket_directories: '/app/postgresql/data/data{dbport}'
            tcp_keepalives_idle: 60
            tcp_keepalives_interval: 10
            tcp_keepalives_count: 10
            password_encryption: md5
            shared_buffers: 1GB
            max_prepared_transactions: 2000
            work_mem: 8MB
            maintenance_work_mem: 2GB
            autovacuum_work_mem: 1GB
            dynamic_shared_memory_type: posix
            max_files_per_process: 204800
            vacuum_cost_delay: 0
            bgwriter_delay: 10ms
            bgwriter_lru_maxpages: 1000
            bgwriter_lru_multiplier: 10.0
            bgwriter_flush_after: 512kB
            effective_io_concurrency: 0
            max_worker_processes: 256
            max_parallel_maintenance_workers: 6
            max_parallel_workers_per_gather: 4
            max_parallel_workers: 28
            old_snapshot_threshold: 6h

      initdb:
        - encoding: UTF8
        - data-checksums
      pg_hba:
        - host replication all 0.0.0.0/0 md5
        - host all all 0.0.0.0/0 md5 
    postgresql:
      listen: 0.0.0.0:{dbport}
      connect_address: {ip}:{dbport}
      data_dir: /app/postgresql/data/data{dbport}
      bin_dir: /app/postgresql/app/pg/bin
      pgpass: /tmp/pgpass
      authentication:
        replication:
          username: repl
          password: co5tvA1CWy
        superuser:
          username: postgres
          password: so3evA1CWy
    tags:
      nofailover: false
      noloadbalance: false
      clonefrom: false
      nosync: false
    watchdog:
      mode: automatic  # 或 off, required
      device: /dev/watchdog  # watchdog 设备路径
      timeout: 30  # 超时时间（秒）  
    log:
      level: INFO          # 日志级别（DEBUG, INFO, WARNING, ERROR, CRITICAL）
      dir: /app/postgresql/logs/pg/patroni{dbport}   
      file_num: 10         # 日志文件数量（轮转）
      file_size: 50000000  # 每个日志文件的大小（字节，50MB）
      format: "%(asctime)s %(levelname)s: %(message)s"  # 日志格式
    '''       
              self.remote_createfile(f"/app/postgresql/data/patroni{dbport}.yml",patronifile,ip,'postgres','zmzqruq6',22)
              logging.warning(f'touch patroni yml success.')
              #mkdir log dir
              dir_1=f'''mkdir -p /app/postgresql/logs/pg/patroni{dbport}'''
              self.remote_ssh(dir_1,ip,'postgres','zmzqruq6')
              #add /etc/bashrc
              bashrc_1=f'''echo 'export PGHOME=/app/postgresql/app/pg' >> /home/postgres/.bash_profile'''
              self.remote_ssh(bashrc_1,ip,'postgres','zmzqruq6')
              bashrc_2=f'''echo 'export PATH=$PGHOME/bin:$PATH:$HOME/bin' >> /home/postgres/.bash_profile'''
              self.remote_ssh(bashrc_2,ip,'postgres','zmzqruq6')
              
              add_bashrc_2=f'''echo 'export LD_LIBRARY_PATH=$PGHOME/lib:$LD_LIBRARY_PATH' >> /home/postgres/.bash_profile'''
              self.remote_ssh(add_bashrc_2,ip,'postgres','zmzqruq6')
              
              bashrc_3=f'''echo 'alias pg_start="/app/postgresql/app/pg/bin/pg_ctl -D /app/postgresql/data/pg/pgdata start &"' >> /home/postgres/.bash_profile'''
              self.remote_ssh(bashrc_3,ip,root_user,root_pwd)
        
              bashcmd1=f'''echo 'alias pg_stop="/app/postgresql/app/pg/bin/pg_ctl -D /app/postgresql/data/pg/pgdata stop"' >> /home/postgres/.bash_profile'''
              bashcmd2=f'''echo 'alias pgdba="/app/postgresql/app/pg/bin/psql -Upostgres  -p5432 -h127.0.0.1"' >> /home/postgres/.bash_profile'''
              bashcmd3=f'''echo 'alias pglog="cd /app/postgresql/logs/pg"' >> /home/postgres/.bash_profile'''
              bashcmd4=f'''echo 'alias pgdata="cd /app/postgresql/data"' >> /home/postgres/.bash_profile'''
              bashcmd5=f'''echo 'alias pgdir="cd /app/postgresql/app/pg"' >> /home/postgres/.bash_profile'''
              bashcmd9=f'''echo 'alias patroni_start="nohup patroni  /etc/patroni.yml > /tmp/patroni_log.output 2>&1 &"' >> /home/postgres/.bash_profile'''
              self.remote_ssh(bashcmd1,ip,root_user,root_pwd)
              self.remote_ssh(bashcmd2,ip,root_user,root_pwd)
              self.remote_ssh(bashcmd3,ip,root_user,root_pwd)
              self.remote_ssh(bashcmd4,ip,root_user,root_pwd)
              self.remote_ssh(bashcmd5,ip,root_user,root_pwd)
              self.remote_ssh(bashcmd9,ip,root_user,root_pwd)
              bashcmd6=f'''source /home/postgres/.bash_profile'''
              self.remote_ssh(bashcmd6,ip,'postgres','zmzqruq6')
              logging.warning(f'.bash_profile success.')
              #添加patroni命令
              find1='''find / -name patroni_raft_controller'''
              res_find1=self.remote_ssh(find1,ip,rootuser,rootpwd)
              logging.warning(f'find / -name patroni_raft_controller res is:{res_find1}')

              find1_path = res_find1.rsplit('/', 1)[0]
              bashcmd7=f'''echo 'export PATH=$PATH:{find1_path}' >> /etc/profile'''
              self.remote_ssh(bashcmd7,ip,root_user,root_pwd)
              bashcmd8=f'''source /etc/profile'''
              self.remote_ssh(bashcmd8,ip,root_user,root_pwd)
              logging.warning(f'add patroni {find1_path}to  /etc/profile success.')

              if ms=='master':
                  bashcmd6=f'''source /home/postgres/.bash_profile'''
                  self.remote_ssh(bashcmd6,ip,'postgres','zmzqruq6')
                  # cmd_start1=f'''nohup {find1_path}/patroni  /app/postgresql/data/patroni{dbport}.yml > /app/postgresql/logs/pg/patroni{dbport}/patroni_log{dbport}.output 2>&1 &'''
                  cmd_start1=f'''nohup bash -c "LD_LIBRARY_PATH=/app/postgresql/app/pg/lib {find1_path}/patroni  /app/postgresql/data/patroni{dbport}.yml > /app/postgresql/logs/pg/patroni{dbport}/patroni_log{dbport}.output 2>&1" &'''
                  self.remote_ssh_noresult(cmd_start1,ip,'postgres','zmzqruq6')
                  logging.warning(f'cmd_start patroni:{cmd_start1}')
              elif ms=='slave':
                  time.sleep(60)
                  #判断主库是否已经启动
                  while True:
                    try:
                        time.sleep(10)
                        sql_judge='''select * from pg_user;'''
                        res_sql_judge=self.pg_execute(sql_judge,ip_master,'postgres','postgres','so3evA1CWy',dbport)
                        #启动slave
                        # cmd_start1=f'''nohup {find1_path}/patroni  /app/postgresql/data/patroni{dbport}.yml > /app/postgresql/logs/pg/patroni{dbport}/patroni_log{dbport}.output 2>&1 &'''
                        cmd_start1=f'''nohup bash -c "LD_LIBRARY_PATH=/app/postgresql/app/pg/lib {find1_path}/patroni  /app/postgresql/data/patroni{dbport}.yml > /app/postgresql/logs/pg/patroni{dbport}/patroni_log{dbport}.output 2>&1" &'''

                        self.remote_ssh_noresult(cmd_start1,ip,'postgres','zmzqruq6')
                        break
                    except Exception as cc:
                        logging.warning('pg master is stop.')
              else:
                  logging.warning('pg start err.')
                
              sql_modify_bashrc=f"update pg_inventory set status='patroni start' where ip='{ip}' and port='{dbport}' and deleted=0;"
              self.exe_sql(sql_modify_bashrc) 

        else:  
            
              consul_ips = ','.join(f"{consulip}:8500" for consulip in cluster_ip)
              patronifile=f'''
    scope: {rand_str}
    name: {ip}
    restapi:
      listen: 0.0.0.0:8{dbport}
      connect_address: {ip}:8{dbport}

    consul:
      host: {consul_ips}
      register_service: true
      service_name: bbbb
      service_check_interval: 10s
      service_tags:
        - "postgresql"
        - "primary"  # 或 "replica"，根据角色动态调整
    bootstrap:
      dcs:
        ttl: 30
        loop_wait: 10
        retry_timeout: 10
        maximum_lag_on_failover: 1048576
        postgresql:
          use_pg_rewind: true
          use_slots: true
          parameters:
            wal_level: logical
            hot_standby: "on"
            max_wal_senders: 10
            max_replication_slots: 10
            wal_log_hints: "on"
            archive_command: 'pgbackrest --stanza=db1 archive-push %p'
            archive_mode: on  
            wal_log_hints: on
            wal_compression: on
            wal_writer_delay: 10ms
            wal_writer_flush_after: 1MB
            commit_delay: 10
            commit_siblings: 5
            checkpoint_timeout: 30min
            max_wal_size: 32GB
            min_wal_size: 16GB
            max_wal_senders: 64
            wal_keep_size: 128MB
            wal_sender_timeout: 60s
            max_replication_slots: 64
            effective_cache_size: 877MB
            log_destination: 'csvlog'
            logging_collector: on
            log_directory: '/app/postgresql/logs/pg/pglog{dbport}'
            log_filename: 'postgresql-%Y-%m-%d_%H%M%S.log'
            log_file_mode: 0600 
            log_truncate_on_rotation: off
            log_rotation_age: 1d
            log_rotation_size: 1GB
            log_min_duration_statement: 1s
            log_checkpoints: on
            log_connections: on
            log_disconnections: on
            log_error_verbosity: verbose
            log_line_prefix: '%m %p %u %d %r %e'
            log_lock_waits: on
            log_statement: 'all'
            log_timezone: 'Asia/Shanghai'
            timezone: 'Asia/Shanghai'
            track_io_timing: on
            track_activity_query_size: 102400
            autovacuum: on
            vacuum_cost_delay: 0
            log_autovacuum_min_duration: 0
            autovacuum_max_workers: 8
            autovacuum_vacuum_scale_factor: 0.02
            autovacuum_analyze_scale_factor: 0.01
            autovacuum_freeze_max_age: 1200000000
            autovacuum_multixact_freeze_max_age: 1250000000
            autovacuum_vacuum_cost_delay: 0ms
            datestyle: 'iso, mdy'
            timezone: 'Asia/Shanghai'
            lc_messages: 'en_US.utf8'
            lc_monetary: 'en_US.utf8'
            lc_numeric: 'en_US.utf8'
            lc_time: 'en_US.utf8'
            default_text_search_config: 'pg_catalog.english'
            shared_preload_libraries: 'pg_stat_statements'
            cron.database_name: 'postgres'
            pg_stat_statements.max: 10000
            pg_stat_statements.track: all
            pg_stat_statements.track_utility: off
            pg_stat_statements.save: on
            deadlock_timeout: 10s
            max_connections: 2000
            superuser_reserved_connections: 10
            unix_socket_directories: '/app/postgresql/data/data{dbport}'
            tcp_keepalives_idle: 60
            tcp_keepalives_interval: 10
            tcp_keepalives_count: 10
            password_encryption: md5
            shared_buffers: 1GB
            max_prepared_transactions: 2000
            work_mem: 8MB
            maintenance_work_mem: 2GB
            autovacuum_work_mem: 1GB
            dynamic_shared_memory_type: posix
            max_files_per_process: 204800
            vacuum_cost_delay: 0
            bgwriter_delay: 10ms
            bgwriter_lru_maxpages: 1000
            bgwriter_lru_multiplier: 10.0
            bgwriter_flush_after: 512kB
            effective_io_concurrency: 0
            max_worker_processes: 256
            max_parallel_maintenance_workers: 6
            max_parallel_workers_per_gather: 4
            max_parallel_workers: 28
            old_snapshot_threshold: 6h

      initdb:
        - encoding: UTF8
        - data-checksums
      pg_hba:
        - host replication all 0.0.0.0/0 md5
        - host all all 0.0.0.0/0 md5 
    postgresql:
      listen: 0.0.0.0:{dbport}
      connect_address: {ip}:{dbport}
      data_dir: /app/postgresql/data/data{dbport}
      bin_dir: /app/postgresql/app/pg/bin
      pgpass: /tmp/pgpass
      authentication:
        replication:
          username: repl
          password: co5tvA1CWy
        superuser:
          username: postgres
          password: so3evA1CWy
    tags:
      nofailover: false
      noloadbalance: false
      clonefrom: false
      nosync: false
    watchdog:
      mode: automatic  # 或 off, required
      device: /dev/watchdog  # watchdog 设备路径
      timeout: 30  # 超时时间（秒）  
    log:
      level: INFO          # 日志级别（DEBUG, INFO, WARNING, ERROR, CRITICAL）
      dir: /app/postgresql/logs/pg/patroni{dbport}   
      file_num: 10         # 日志文件数量（轮转）
      file_size: 50000000  # 每个日志文件的大小（字节，50MB）
      format: "%(asctime)s %(levelname)s: %(message)s"  # 日志格式
    '''       
              self.remote_createfile(f"/app/postgresql/data/patroni{dbport}.yml",patronifile,ip,'postgres','zmzqruq6',22)
              logging.warning(f'touch patroni yml success.')

              if ms=='master':
                  # cmd_start1=f'''nohup {find1_path}/patroni  /app/postgresql/data/patroni{dbport}.yml > /app/postgresql/logs/pg/patroni{dbport}/patroni_log{dbport}.output 2>&1 &'''
                  cmd_start1=f'''nohup bash -c "LD_LIBRARY_PATH=/app/postgresql/app/pg/lib {find1_path}/patroni  /app/postgresql/data/patroni{dbport}.yml > /app/postgresql/logs/pg/patroni{dbport}/patroni_log{dbport}.output 2>&1" &'''
                  self.remote_ssh_noresult(cmd_start1,ip,'postgres','zmzqruq6')
              elif ms=='slave':
                  time.sleep(30)
                  #判断主库是否已经启动
                  while True:
                    try:
                        time.sleep(10)
                        sql_judge='''select * from pg_user;'''
                        res_sql_judge=self.pg_execute(sql_judge,ip_master,'postgres','postgres','so3evA1CWy',dbport)
                        #启动slave
                        # cmd_start1=f'''nohup {find1_path}/patroni  /app/postgresql/data/patroni{dbport}.yml > /app/postgresql/logs/pg/patroni{dbport}/patroni_log{dbport}.output 2>&1 &'''
                        cmd_start1=f'''nohup bash -c "LD_LIBRARY_PATH=/app/postgresql/app/pg/lib {find1_path}/patroni  /app/postgresql/data/patroni{dbport}.yml > /app/postgresql/logs/pg/patroni{dbport}/patroni_log{dbport}.output 2>&1" &'''

                        self.remote_ssh_noresult(cmd_start1,ip,'postgres','zmzqruq6')
                        break
                    except Exception as cc:
                        logging.warning('pg master is stop.')
              else:
                  logging.warning('pg start err.')
                
              sql_modify_bashrc=f"update pg_inventory set status='patroni start' where ip='{ip}' and port='{dbport}' and deleted=0;"
              self.exe_sql(sql_modify_bashrc) 
                  

      except Exception as e:
            sql_11=f"update pg_inventory set status='部署失败' where ip='{ip}' and port='{dbport}' and deleted=0;"
            self.exe_sql(sql_11)
            logging.warning('install_ha_pg err:{0}'.format(e))

        
        
        
        
        