import pymysql
import time
import os
import datetime
from db_driver import mysql_driver

class add_monitor(mysql_driver):

    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request
            
    def get_privilege(self):
        mysql_ip = self.request.form['mysql_ip']
        
        if mysql_ip=='':
            msg="请填写IP"
            data=''           
        else:
            sql_a=f"SELECT monitor FROM yandi.`inventory` WHERE ip='{mysql_ip}';"
            v_1=self.exe_sql(sql_a)[0]['monitor']
            if v_1==1:
                msg='已部署监控'
                sql_2=f"SELECT ip,(CASE monitor WHEN '0' THEN '未监控' WHEN '1' THEN '已监控'  END) AS monitor  FROM yandi.inventory ORDER BY monitor desc;"
                data=self.exe_sql(sql_2)
            else:
                msg=mysql_ip
                v_2=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                cmd_mv=f"sudo sh -c 'mv /app/jiankong /app/jiankong_{v_2}'"
                self.remote_ssh(cmd_mv,mysql_ip,'ywuser','testpwd2')
                cmd_3="sudo sh -c 'mkdir /app/jiankong'"
                cmd_4="sudo sh -c 'chown -R ywuser.ywuser /app/jiankong'"
                self.remote_ssh(cmd_3,mysql_ip,'ywuser','testpwd2')
                self.remote_ssh(cmd_4,mysql_ip,'ywuser','testpwd2')
            
                self.remote_ssh_put('/app/jiankong/node_exporter.tar.gz','/app/jiankong/node_exporter.tar.gz',mysql_ip,'ywuser','testpwd2')
                self.remote_ssh_put('/app/jiankong/mysqld_exporter.tar.gz','/app/jiankong/mysqld_exporter.tar.gz',mysql_ip,'ywuser','testpwd2')
                #unzip
                cmd_5="sudo sh -c 'tar -xvf /app/jiankong/node_exporter.tar.gz -C /app/jiankong/'"
                cmd_6="sudo sh -c 'tar -xvf /app/jiankong/mysqld_exporter.tar.gz -C /app/jiankong/'"
                self.remote_ssh(cmd_5,mysql_ip,'ywuser','testpwd2')
                self.remote_ssh(cmd_6,mysql_ip,'ywuser','testpwd2')
                #start monitor
                cmd_7="sudo sh -c 'source /app/jiankong/node_exporter/start.sh'"
                cmd_8="sudo sh -c 'source /app/jiankong/mysqld_exporter/start.sh'"
                self.remote_ssh(cmd_7,mysql_ip,'ywuser','testpwd2')
                self.remote_ssh(cmd_8,mysql_ip,'ywuser','testpwd2')
                cmd_9=f"sed -i '3a\  - {mysql_ip}' /app/jiankong/prometheus/host.yml"
                cmd_10=f"sed -i '3a\  - {mysql_ip}' /app/jiankong/prometheus/mysql.yml"
                os.system(cmd_9)
                os.system(cmd_10)
                cmd_11=" /app/jiankong/prometheus/promtool check config /app/jiankong/prometheus/prometheus.yml"
                os.system(cmd_11)
                sql_1=f"update yandi.inventory set monitor=1 where ip='{mysql_ip}';"
                self.exe_sql(sql_1)
                sql_2=f"SELECT ip,(CASE monitor WHEN '0' THEN '未监控' WHEN '1' THEN '已监控'  END) AS monitor  FROM yandi.inventory ORDER BY monitor desc;"
                data=self.exe_sql(sql_2)

        return {
            'status':True,
            'msg':msg,
            'data':data
        }
        

        

    def get_mysqlip(self):
        sql = f"SELECT DISTINCT(ip) AS mysqlip FROM yandi.inventory;"

        return {
            'status':True,
            'msg':'成功获取数据',
            'data':self.exe_sql(sql)
        }
        

    def get_monitor(self):
        sql_2=f"SELECT ip,(CASE monitor WHEN '0' THEN '未监控' WHEN '1' THEN '已监控'  END) AS monitor  FROM yandi.inventory ORDER BY monitor desc;"
        data=self.exe_sql(sql_2)
        msg='OK'
        return {
            'status':True,
            'msg':msg,
            'data':data
        }


