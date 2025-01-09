import pymysql
from db_driver import mysql_driver

class dbcreate(mysql_driver):

    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request
            
    def get_dbinfo(self):
        sql = '''SELECT vip,GROUP_CONCAT(DISTINCT(ip)) AS ip,PORT,GROUP_CONCAT(DISTINCT(dbname)) AS db FROM (
SELECT b.vip,b.ip,a.port,a.dbname FROM yandi.`db_name` a,yandi.`inventory` b WHERE a.ip=b.vip) aa GROUP BY vip,PORT'''  

        return {
            'status':True,
            'msg':'成功获取数据',
            'data':self.exe_sql(sql)
        }
        
   

    def save_db(self):
        vip = self.request.form['vip']
        port = self.request.form['port']
        dbname = self.request.form['dbname']
        port=int(port)
        
        if dbname =="" :
            msg='警告:请填写完整信息'
            sql = '''SELECT vip,GROUP_CONCAT(DISTINCT(ip)) AS ip,PORT,GROUP_CONCAT(DISTINCT(dbname)) AS db FROM (
    SELECT b.vip,b.ip,a.port,a.dbname FROM yandi.`db_name` a,yandi.`inventory` b WHERE a.ip=b.vip) aa GROUP BY vip,PORT'''  
            data=self.exe_sql(sql)
        else:
            sql_1=f"create database {dbname};"
            res_4=self.remote_excute(vip,port,'yunwei','testpwd','mysql',sql_1)
            sql_6=f"INSERT INTO yandi.db_name(dbname,ip,port) VALUES('{dbname}','{vip}','{port}')"
            vip=self.exe_sql(sql_6)
            msg='DB创建成功'
            
            sql = '''SELECT vip,GROUP_CONCAT(DISTINCT(ip)) AS ip,PORT,GROUP_CONCAT(DISTINCT(dbname)) AS db FROM (
    SELECT b.vip,b.ip,a.port,a.dbname FROM yandi.`db_name` a,yandi.`inventory` b WHERE a.ip=b.vip) aa GROUP BY vip,PORT'''   
            data=self.exe_sql(sql)
        
        return {
            'status': True,
            'msg': msg,
            'data': data
        }
