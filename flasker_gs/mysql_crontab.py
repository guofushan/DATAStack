import pymysql
from db_driver import mysql_driver

class mysql_crontab(mysql_driver):

    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request
            
    def get_crontab(self):
        sql = f"SELECT id,ip,cron,`comment`,command,last_run,next_exec_time,date_created,(CASE failed WHEN '1' THEN '失败' WHEN '0' THEN '成功'  WHEN '2' THEN '取消' END) AS failed FROM yandi.`a_crontab` WHERE deleted=0 ORDER BY failed"    

        return {
            'status':True,
            'msg':'成功获取数据',
            'data':self.exe_sql(sql)
        }

    
    def save_crontab(self):
        id = self.request.form['id']
        ip = self.request.form['ip']
        command = self.request.form['command']
        comment = self.request.form['comment']
        cron = self.request.form['cron']
        failed = self.request.form['failed']
        
        if failed=='成功':
            failed=0
        elif failed=='失败':
            failed=1    
        elif failed=='取消':
            failed=2   
                
        if id == '':
            sql_1=f"insert into yandi.crontab(ip,cron,command,comment) values('{ip}','{cron}','{command}','{comment}')"
            self.exe_sql(sql_1)
        else:
            sql_1=f"update yandi.crontab set ip='{ip}',cron='{cron}',command='{command}',comment='{comment}',failed={failed} where id={id}"
            self.exe_sql(sql_1)
        sql = f"SELECT id,ip,cron,`comment`,command,last_run,next_exec_time,date_created,(CASE failed WHEN '1' THEN '失败' WHEN '0' THEN '成功' WHEN '2' THEN '取消' END) AS failed FROM yandi.`crontab` WHERE deleted=0 ORDER BY failed"    

        return {
            'status':True,
            'msg':'成功获取数据',
            'data':self.exe_sql(sql)
        }
        
    def delete_crontab(self):
        id = self.request.form['id']
        sql_1=f"update yandi.crontab set deleted=1 where id={id}"
        self.exe_sql(sql_1)
        sql = f"SELECT id,ip,cron,`comment`,command,last_run,next_exec_time,date_created,(CASE failed WHEN '1' THEN '失败' WHEN '0' THEN '成功' WHEN '2' THEN '取消' END) AS failed FROM yandi.`crontab` WHERE deleted=0 ORDER BY failed"    

        return {
            'status':True,
            'msg':'成功获取数据',
            'data':self.exe_sql(sql)
        }
   
    def get_log(self):
        id = self.request.form['id']
        sql_1=f"SELECT LOG FROM yandi.crontab_log WHERE job_id={id} ORDER BY id DESC LIMIT 1"
        # self.exe_sql(sql_1)
        
        return {
            'status':True,
            'msg':'成功获取数据',
            'data':self.exe_sql(sql_1)
        }     