from db_driver import mysql_driver
from user import User
import random
class mongo(mysql_driver):
    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request
        self.db_config = db_config
        # self.get_all_vips()



    def get_all_ips(self):
        return {
            'status':True,
            'data':self.get_all_ips_from_db()
        }

    def get_all_ips_from_db(self):
        sql = 'SELECT DISTINCT(ip) FROM yandi.mongo_slowlog;'
        return self.exe_sql_one_col(sql)

    def get_all_db_ips(self):
        return {
            'status':True,
            'data':self.get_all_ips_from_db()
        }

    def get_slow_log(self):

        start_time = self.request.form['start_time']
        stop_time = self.request.form['stop_time']
        hostip = self.request.form['hostip']
        sql = f"""
                SELECT
             *
                FROM
                    yandi.mongo_slowlog
                WHERE
                 ip = '{hostip}'
                 and ts >= '{start_time}' and ts <= '{stop_time}'
                """
        detail_slow_logs = self.exe_sql(sql=sql)

        return {
            'status':True,
            'msg':'成功获取慢日志数据',
            'data':{
                'detail':detail_slow_logs,
            }
        }


    def get_db_lists(self):
        vip_db_lists = []
        sql = "select schema_name from information_schema.SCHEMATA  where SCHEMA_NAME not in ('information_schema','mysql','performance_schema','sys')"
        for vip in self.vips:
            db_names = self.exe_sql_one_col(sql,host=vip)
            vip_db_lists.append({'vip':vip,'db_names':db_names})

        return {
            'status':True,
            'msg':'获取数据列成功',
            'data':vip_db_lists
        }
