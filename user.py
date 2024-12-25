from db_driver import mysql_driver
import base64
from Crypto.Cipher import AES
import hashlib
import logging

class AEScoder():
    def __init__(self):
        self.__encryptKey = "iEdSxIwA1vpMxAabsjxWzg=="
        self.__key = base64.b64decode(self.__encryptKey)
    # AES加密
    def encrypt(self,data):
        BS = 16
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        cipher = AES.new(self.__key, AES.MODE_ECB)
        encrData = cipher.encrypt(pad(data).encode('utf-8'))
        encrData = base64.b64encode(encrData)
        return encrData
    # AES解密
    def decrypt(self,encrData):
        encrData = base64.b64decode(encrData)
        #unpad = lambda s: s[0:-s[len(s)-1]]
        unpad = lambda s: s[0:-s[-1]]
        cipher = AES.new(self.__key, AES.MODE_ECB)
        decrData = unpad(cipher.decrypt(encrData))
        return decrData.decode('utf-8')

class User(mysql_driver):

  def __init__(self,db_config,request=None):

      super().__init__(**db_config)
      #print(host,user,password,port)
      self.request = request

  def set_password(self,user,password):
      encrypt_password =  AEScoder().encrypt(password)
      sql = '''update yandi.mysql_user set  password = %s where mysql_name=%s '''
      self.exe_sql_binary(sql,encrypt_password,user)

  def set_user_info(self,role,name,mysql_name):
      sql = f'''update yandi.mysql_user set role = '{role}',name='{name}' where mysql_name='{mysql_name}' '''
      self.exe_sql(sql)


  def get_password(self,user):

      sql = '''select password from yandi.mysql_user where  mysql_name= '{0}' and deleted=false '''.format(user)
      encrypted_pwd = self.exe_sql(sql)[0]['password']

      # 解密存储在数据库当中的密码，并且再次用md5加密和传过来的密码比较，如果一样就通过，如果不一样就返回登陆失败
      # 数据库当中mysql_user存储的password是先aes加密过的，然后在base64加密的最后结果
      return AEScoder().decrypt(encrypted_pwd)


  def get_user_info(self,user):
      sql = '''select * from yandi.mysql_user where  mysql_name='{0}'  and deleted=false '''.format(user)
      user_info = self.exe_sql(sql)[0]
      user_info['password'] = self.get_password(user)
      return user_info


  def get_user_list(self):
      sql = '''select id,name,mysql_name,role from yandi.mysql_user where deleted=false'''


      return self.exe_sql(sql)


  #登陆验证
  def check_password(self):

    username = self.request.form['username'].strip()
    password = self.request.form['password'].strip()

    if (not username or not password):
        logging.error('账号或者密码为空')
        return False
    else:
        #获取数据库当中的管理用户加密过的密码，然后解密，并且对比传过来的密码（密码直接用md5加密传过来）
        pwd = self.get_password(username)
        print(pwd,username)
        m = hashlib.md5()
        m.update(pwd.encode())

        #比对传过来的密码
        if password != m.hexdigest():
            return False
        else:
            return True
  
  def get_inventory(self):

    return {
        'status':True,
        'msg':'成功获取资产列表',
        'data':self.get_inventory_from_db()
    }

  def get_inventory_from_db(self):
    sql = '''SELECT id,mysql_name,mysql_password FROM mysql_user WHERE deleted ='false';'''
    return  self.exe_sql(sql)


