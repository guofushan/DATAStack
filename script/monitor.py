from prometheus_client import Gauge, start_http_server
import random
import time
import subprocess
import logging
import pymysql
import configparser
import paramiko

cfg = configparser.ConfigParser()
cfg.read('/app/datastack.cfg')
db_host= cfg.get('section','mysqlip')
db_user= cfg.get('section','mysqluser')
db_port= cfg.get('section','mysqlport')
db_password= cfg.get('section','mysqlpwd')
db_port=int(db_port)

logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(filename)s[line:%(lineno)d] -  %(levelname)s  %(message)s',
        filename='/tmp/prome_monitor.log')

#sql执行模块
def execute(ip,port,user,pwd,db,sql_text):
    try:
        connection = pymysql.connect(host=ip, user=user, passwd=pwd, db=db,port=port,autocommit = True,charset='utf8mb4')
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql_text)
        connection.commit()
        result = cursor.fetchall()
        return result
    finally:
        connection.close()
        
# 定义和注册指标
datastack_1 = Gauge('datastack_1', '随机数指标',labelnames=["label"])

# 启动 HTTP 服务器，暴露 metrics 接口
start_http_server(9097)

def get_orch_status():
    cmd_1="ps -ef | grep orchestrator | grep -v grep | wc -l"
    r_1=subprocess.getoutput(cmd_1)
    if r_1=='0':
        v_1='orchestrator_status'
        v_2=0
    else:
        v_1='orchestrator_status'
        v_2=1
    return(v_1,v_2)

def get_consul_status():
    cmd_1="/app/consul/consul catalog services"
    r_1=subprocess.getoutput(cmd_1)
    sql_1='''SELECT * FROM `a_inventory` WHERE deleted=0 AND ms<>'';'''
    res_1=execute(db_host,db_port,db_user,db_password,'yandi',sql_1)
    for i in res_1:
            ip=i['ip']
            print(ip)
            user='mysql'
            password='zmzqruq6'
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip,22,user,password)
            stdin, stdout, stderr = ssh.exec_command(cmd_1)
            cmd_result=stdout.read()
            cmd_error=stderr.read()
            print(cmd_result)
            print(cmd_error)
    
while True:
    cc=get_orch_status()
    name_1=cc[0]
    staus_1=cc[1]

    datastack_1.labels(name_1).set(staus_1)
    logging.info('data insert ok.')
    get_consul_status()

    # 等待 5 秒钟，再次进行收集
    time.sleep(5)
