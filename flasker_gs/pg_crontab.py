import pymysql
import logging
import schedule
import time
import threading
from datetime import datetime
import paramiko
import json

from db_driver import mysql_driver

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class pg_crontab(mysql_driver):
    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request
        self.start_scheduler()

    def get_bak(self):
        try:
                sql_1='''SELECT * FROM `pg_inventory` WHERE deleted=0 AND bak='是' AND ms='master';'''
                datas=self.exe_sql(sql_1)
                for server in datas:
                    # print(server)
                    host = server["ip"]
                    port = server["port"]
                    bak_store = server["bak_store"]
                    logger.info(f"get_bak ip: {host}:{port}") 
                    # 获取备份信息
                    info_cmd = f"/app/postgresql/app/pg_extention/pgbackrest/src/pgbackrest --stanza=db1 --output=json info"
                    aa=self.remote_ssh(info_cmd,host,'postgres','zmzqruq6')
                    aa=str(aa)
                    my_dict = json.loads(aa) 
                    for info1 in my_dict:
                        for info2 in info1['backup']:
                            filename=info2['label']
                            start_time=info2['timestamp']['start']
                            stop_time=info2['timestamp']['stop']
                            stop_time = info2['timestamp'].get('stop', 0)  # 未完成备份则为0
                            backup_size = info2['info'].get('size', 0)  # 默认0
                            is_completed = 1 if stop_time > 0 else 0
                            # print(start_time)
                            # 转换为日期格式用于打印
                            start_time_str = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
                            stop_time_str = datetime.fromtimestamp(stop_time).strftime('%Y-%m-%d %H:%M:%S') if stop_time > 0 else "Not Completed"
                            sql_5=f'''select * from yandi.pg_backup where ip='{host}' and port='{port}' and file_name='{filename}';'''
                            # print(sql_5)
                            res5=self.exe_sql(sql_5)
                            # print(res5)
                            if res5==():
                                sql_2=f'''insert into yandi.pg_backup(ip,port,file_name,file_size,backup_status,create_time,update_time) 
                                values('{host}','{port}','{filename}','{backup_size}','{is_completed}','{start_time_str}','{stop_time_str}');'''
                                self.exe_sql(sql_2)
                            else:
                                pass     
        except Exception as e:
            logger.error(f"get_bak error: {e}") 

    def pg_bak(self):
        try:
                sql_1='''SELECT * FROM `pg_inventory` WHERE deleted=0 AND bak='是' AND ms='master';'''
                datas=self.exe_sql(sql_1)
                for server in datas:
                    host = server["ip"]
                    port = server["port"]
                    bak_store = server["bak_store"]
                    # 执行全量备份
                    backup_cmd = f"nohup /app/postgresql/app/pg_extention/pgbackrest/src/pgbackrest --stanza=db1 --type=full --repo1-retention-full={bak_store} backup >> /tmp/pgbackup.output 2>&1 &"
                    logger.info(f"pg_bak  ip: {host}; bak_cmd: {backup_cmd}") 
                    self.remote_ssh_noresult(backup_cmd,host,'postgres','zmzqruq6')
        except Exception as cc:
                logger.error(f"pg_bak error: {cc}") 
            

      # 定时任务调度
    def schedule_tasks(self):
        #每天凌晨
        schedule.every().day.at("02:00").do(self.pg_bak).tag("daily", "backup")
        schedule.every(1).hour.do(self.get_bak).tag("daily", "get_backup")
        while True:
            schedule.run_pending()
            time.sleep(1)

    # 启动定时任务（后台线程）
    def start_scheduler(self):
        scheduler_thread = threading.Thread(target=self.schedule_tasks, daemon=True)
        scheduler_thread.start()
        # print("Scheduler started in background")
        logger.info("Scheduler started in background")