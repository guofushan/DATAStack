# -*- coding: utf-8 -*-
'''
#=============================================================================
#       Author: Fushan.Guo
#        Email: 1031010310@qq.com
#      Version: 0.0.1
#   LastChange: 2023-8-22
#=============================================================================
'''
from tools import *
# from settings import *
import logging
import datetime
from multiprocessing import Pool
import paramiko
import time
import os, sys
import shutil
import pymysql
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import configparser

# db_host=DB_CONFIG['host']
# db_port=DB_CONFIG['port']
# db_user=DB_CONFIG['user']
# db_password=DB_CONFIG['password']
cfg = configparser.ConfigParser()
cfg.read('/app/datastack.cfg')
db_host= cfg.get('section','mysqlip')
db_user= cfg.get('section','mysqluser')
db_port= cfg.get('section','mysqlport')
db_password= cfg.get('section','mysqlpwd')
db_port=int(db_port)

#定义log，记录程序日志info
logdate= datetime.datetime.now().strftime("%Y%m%d_%H%M%S")       
log_name=f"/tmp/backup_{logdate}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s[line:%(lineno)d] -  %(levelname)s  %(message)s',
    filename=log_name)

#定义全备
def full_bak(ip):
    try:
        logging.info('begin backup {0}.'.format(ip))
        date_format=datetime.datetime.today().strftime("%Y_%m_%d")
#远程执行
        user='mysql'
        password='testpwd6'
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,user,password)
        cmd="""xtrabackup --defaults-file=/app/my.cnf --user=admin --password=testpwd --backup --compress --compress-threads=2 --target-dir=/app/backup/mysql/{0}_{1}_fullbackup""".format(date_format,ip)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        cmd_result=stdout.read()
        cmd_error=stderr.read()
        logging.info('{1}_log1:{0};{1}_log2:{2}'.format(cmd_result,ip,cmd_error))
#计算备份文件大小
        filesize="""cd /app/backup/mysql/{0}_{1}* && du -sm""".format(date_format,ip)
        stdin, stdout, stderr = ssh.exec_command(filesize)
        size=stdout.read()
        size=str(size)[2:][:-6]
        sql_3="""update yandi.backup_detail set backup_status=1,file_name='{0}_{1}_fullbackup',file_size='{2}' where ip='{1}' and DATE_FORMAT(create_time,'%Y_%m_%d')='{0}';""".format(date_format,ip,size)
        execute(db_host,db_port,db_user,db_password,'yandi',sql_3)

    except Exception as e:
        logging.info('full_bak err {0}.'.format(e))
        ssh.close()
        sys.exit(0)

def backup(ip,bak_store):
    try:
        before_date=(datetime.datetime.today() + datetime.timedelta(-1)).strftime("%Y_%m_%d")
        weekday=datetime.datetime.today().isoweekday()
#开始备份
        sql_1="""insert yandi.backup_detail(ip) values('{0}')""".format(ip)
        execute(db_host,db_port,db_user,db_password,'yandi',sql_1)  
#远程执行
        user='mysql'
        password='testpwd6'
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,user,password)
        full_bak(ip)
      
#删除历史备份集
        del_cmd=f'''find /app/backup/mysql -mtime +{bak_store}'''
        bb=''' -name "*backup" -exec rm -rf {} \;'''
        del_cmd=del_cmd + bb
        stdin, stdout, stderr = ssh.exec_command(del_cmd)
        ssh.close()

    except Exception as e:
        logging.info('backup err {0}.'.format(e))
        ssh.close()
        sys.exit(0)


if __name__ == '__main__':

    sql_ip='''SELECT ip,bak,bak_store FROM a_inventory WHERE deleted=0 AND bak='是' AND ms<>'master';'''
    ip_list=execute(db_host,db_port,db_user,db_password,'yandi',sql_ip)
    
    pool = Pool(processes =5)
    for i in ip_list:
        ip=i['ip']
        bak_store=i['bak_store']
        
        pool.apply_async(backup,args=(ip,bak_store,))
    pool.close()
    pool.join()
