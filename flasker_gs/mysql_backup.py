import pymysql
import logging
from db_driver import mysql_driver

class mysql_backup(mysql_driver):
    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request


    def bak_detail(self):
            vip=self.request.form['vip']
            # sql="""SELECT ip,file_name,file_size,backup_status,create_time,update_time FROM `backup_detail` WHERE create_time>DATE_ADD(NOW(), INTERVAL -7 DAY)  ORDER BY id DESC; """
            sql=f"""SELECT
  a.ip,
  a.file_name,
  (
    CASE
      WHEN SUBSTRING_INDEX(a.file_size, '.', 1) < 1000
      THEN CONCAT(
        SUBSTRING_INDEX(a.file_size, '.', 1),
        'M'
      )
      ELSE CONCAT(
        FORMAT(
          SUBSTRING_INDEX(a.file_size, '.', 1) / 1024,
          2
        ),
        'G'
      )
    END
  ) AS file_size,
 (CASE a.backup_status WHEN '1' THEN '完成备份' ELSE '未完成' END) AS backup_status,
  a.create_time,
  a.update_time
FROM
  `backup_detail` a,
  a_inventory b
WHERE a.`ip` = b.ip
  AND b.vip = '{vip}' AND b.deleted=0  AND a.`create_time`>DATE_ADD(NOW(), INTERVAL -b.bak_store DAY)
ORDER BY a.id DESC;
"""
            return {
            'status':True,
            'msg':'成功获取数据',
            'data':self.exe_sql(sql)
        }


    def bak_set(self):
            vip=self.request.form['vip']
            sql=f"""SELECT vip,bak,bak_store FROM a_inventory WHERE deleted=0 AND vip='{vip}' AND ms<>'master';"""
            return {
            'status':True,
            'msg':'成功获取数据',
            'data':self.exe_sql(sql)
        }
            
            
    def save_set(self):
            vip = self.request.form['vip']
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
            logging.warning('vip: {0}'.format(vip))
            logging.warning('bak: {0}'.format(bak))
            logging.warning('bak_store: {0}'.format(bak_store))
              
            sql_1=f"UPDATE yandi.`a_inventory` SET bak='{bak}',bak_store={bak_store} WHERE vip='{vip}' AND deleted=0;"
            self.exe_sql(sql_1)
            sql_2=f"""SELECT vip,bak,bak_store FROM a_inventory WHERE deleted=0 AND vip='{vip}' AND ms<>'master';"""
            return {
                'status':True,
                'msg':'成功获取数据',
                'data':self.exe_sql(sql_2)
            }
        

    def get_db_size(self):
        size_data = []
        date_range = []
        status=''
        msg=''
        host = self.request.form['host']
        start_date = self.request.form['start_date']  
        sql=f"SELECT create_time,ROUND(file_size/1024,2) as file_size FROM yandi.`backup_detail` WHERE file_name LIKE '%full%' AND ip='{host}' and create_time>='{start_date}' ORDER BY id asc"
        sql_1=f"SELECT create_time,ROUND(file_size/1024,2) as file_size FROM yandi.`backup_detail` WHERE file_name LIKE '%full%' AND ip='{host}' ORDER BY id asc"

        if host=='':
              status=1
              msg='警告:IP不为空'
        else:
              status=True
              msg='获取数据成功'
        if start_date=='':             
          results = self.exe_sql(sql_1)
        else:
          results = self.exe_sql(sql)
        for result in results:
            size_data.append(str(result['file_size']))
            date_range.append(str(result['create_time']))
        return {
            'status':status,
            'msg':msg,
            'data':{'size_data': size_data, 'date_range': date_range}
        }

        
    def get_dbname(self):
        sql = f"SELECT DISTINCT(ip) FROM yandi.backup_detail"    

        return {
            'status':True,
            'msg':'成功获取数据',
            'data':self.exe_sql(sql)
        }