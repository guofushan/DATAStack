import pymysql
import base64
from Crypto.Cipher import AES
import hashlib
from db_driver import mysql_driver
import logging

    
class mysql_setmodify(mysql_driver):

    def __init__(self,db_config,request):
        super().__init__(**db_config)
        self.request = request
        
    def get_inventory(self):

        return {
            'status':True,
            'msg':'成功获取资产列表',
            'data':self.get_inventory_from_db()
        }

    def get_inventory_from_db(self):
        sql = '''SELECT id,mysql_name,mysql_password FROM mysql_user WHERE deleted ='false';'''
        return  self.exe_sql(sql)


    def save_inventory(self):
        id = self.request.form['id']
        mysql_name = self.request.form['mysql_name']
        mysql_password = self.request.form['mysql_password']
        logging.warning('{0},{1}'.format(mysql_name,mysql_password))

        encryptKey = "iEdSxIwA1vpMxAabsjxWzg=="
        key = base64.b64decode(encryptKey)
        BS = 16
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        cipher = AES.new(key, AES.MODE_ECB)
        encrData = cipher.encrypt(pad(mysql_password).encode('utf-8'))
        encrData = base64.b64encode(encrData)
    
        logging.warning('pwd: {0}'.format(encrData))
        
        if mysql_name=='' or mysql_password=='':
            msg='警告：请填写完整信息'
            # data=''
        else:
            msg='success'
            if id == '':
                sql = f'''insert into yandi.mysql_user(mysql_name,mysql_password) values('{mysql_name}','{mysql_password}');'''
                self.exe_sql(sql)
            else:
                sql = f'''update yandi.mysql_user set mysql_name='{mysql_name}',mysql_password='{mysql_password}' where id = {id} ;'''
                self.exe_sql(sql)

        sql = '''update yandi.mysql_user set  password = %s where mysql_name=%s '''
        self.exe_sql_binary(sql,encrData,mysql_name)

            
        return {
            'status': True,
            'msg': msg,
            'data': self.get_inventory_from_db()
        }


    def delete_inventory(self):
        id = self.request.form['id']
        sql = f'''UPDATE yandi.mysql_user SET deleted ='is_true' WHERE id={id};'''
        self.exe_sql(sql)
        return {
            'status': True,
            'msg': '删除成功',
            'data': self.get_inventory_from_db()
        }


