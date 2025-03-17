from db_driver import mysql_driver
from croniter import croniter

class scheduler(mysql_driver):
    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request


    def get_scheduler(self):
        return {
            'status':True,
            'msg':'获取定时任务列表成功',
            'data':self.get_schedulers_from_db()
        }

    def get_schedulers_from_db(self):
        sql = "select id,ip,cron,command,DATE_FORMAT(last_run,'%Y-%m-%d %H:%i:%s') as last_run,enabled,success,failed from yandi.crontab  where deleted=false order by ip,enabled desc"
        return self.exe_sql(sql)

    def get_scheduler_logs(self):
        job_id = self.request.form['job_id'].strip()
        sql = f"select success,output,DATE_FORMAT(start_time,'%Y-%m-%d %H:%i:%s') as start_time,DATE_FORMAT(stop_time,'%Y-%m-%d %H:%i:%s') as stop_time from yandi.crontab_result where job_id={job_id}  order by start_time desc limit 100"
        results = self.exe_sql(sql)
        return {
            'status':True,
            'msg':'成功获取日志',
            'data':results
        }

    def add_scheduler(self):
        ips = self.request.form['ip'].split(',')
        cron = self.request.form['cron'].strip()
        command = self.request.form['command'].strip()
        enabled = self.request.form['enabled'].strip()

        print(cron,command,enabled)

        #还要检测cron是不是合规的
        if not croniter.is_valid(cron) :
            return {
                'status':False,
                'msg':f'{cron}的时间格式不对'
            }
        elif command == '':
            return {
                'status':False,
                'msg':'command命令不能为空'
            }

        for ip in ips:
            sql = 'insert into yandi.crontab(ip,cron,command,enabled,last_run) values(%s,%s,%s,%s,now())'
            self.exe_sql_binary(sql,ip,cron,command,enabled)

        return {
            'status':True,
            'msg':'添加成功',
            'data':self.get_schedulers_from_db()
        }

    def edit_scheduler(self):
        #还要检测cron是不是合规的
        id = self.request.form['id'].strip()
        cron = self.request.form['cron'].strip()
        command = self.request.form['command'].strip()
        enabled = self.request.form['enabled'].strip()

        if not croniter.is_valid(cron) :
            return {
                'status':False,
                'msg':f'{cron}的时间格式不对'
            }
        elif command == '':
            return {
                'status':False,
                'msg':'command命令不能为空'
            }

        sql = 'update yandi.crontab set cron=%s,command=%s,enabled=%s where id=%s'
        self.exe_sql_binary(sql,cron,command,enabled,id)

        return {
            'status':True,
            'msg':'修改成功',
            'data':self.get_schedulers_from_db()
        }

    def delete_scheduler(self):
        id = self.request.form['id'].strip()
        sql = f'update yandi.crontab set deleted=true where id={id}'
        self.exe_sql(sql)
        return {
            'status':True,
            'msg':'成功删除',
            'data':self.get_schedulers_from_db()
        }