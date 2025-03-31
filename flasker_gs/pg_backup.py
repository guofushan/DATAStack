import pymysql
import logging
from db_driver import mysql_driver

class pg_backup(mysql_driver):
    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request


    def bak_detail(self):
            vip=self.request.form['vip']
            port=self.request.form['port']
            
            sql=f"""SELECT * FROM yandi.pg_backup WHERE ip='{vip}' AND PORT='{port}' ORDER BY id DESC LIMIT 30;"""
            return {
            'status':True,
            'msg':'成功获取数据',
            'data':self.exe_sql(sql)
        }


    def bak_set(self):
            vip=self.request.form['vip']
            port=self.request.form['port']
            sql=f"""SELECT vip,bak,bak_store FROM pg_inventory WHERE deleted=0 AND vip='{vip}' AND PORT='{port}' AND ms='master';"""
            
            return {
            'status':True,
            'msg':'成功获取数据',
            'data':self.exe_sql(sql)
        }
            
            
    def save_set(self):
            vip = self.request.form['vip']
            port = self.request.form['port']
            bak = self.request.form['bak']
            bak_store = self.request.form['bak_store'] 
         
            if bak=='否':
                bak='否'
            else:
                bak='是'
            
            if bak_store=='':
                bak_store=5
            else:    
                bak_store=int(bak_store)
            logging.warning('vip: {0},port:{1}'.format(vip,port))
            logging.warning('bak: {0}'.format(bak))
            logging.warning('bak_store: {0}'.format(bak_store))
              
            sql_1=f"UPDATE yandi.pg_inventory SET bak='{bak}',bak_store={bak_store} WHERE vip='{vip}' and port='{port}' AND deleted=0;"
            self.exe_sql(sql_1)
            sql_2=f"""SELECT vip,bak,bak_store FROM pg_inventory WHERE deleted=0 AND vip='{vip}' AND PORT='{port}' AND ms='master';"""
            return {
                'status':True,
                'msg':'success',
                'data':self.exe_sql(sql_2)
            }
        
