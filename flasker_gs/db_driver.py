import pymysql
import paramiko
from settings import *

script_dir=script_dir
host_yandi=DB_CONFIG['host']
port_yandi=DB_CONFIG['port']
user_yandi=DB_CONFIG['user']
password_yandi=DB_CONFIG['password']

class mysql_driver():

    def __init__(self,host,user,password,port,cursorclass,charset):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.cursorclass = cursorclass
        self.charset = charset
        print(host,user,password,port)
        # #执行sql语句
    def execute(self,sql_text):
        try:
            connection = pymysql.connect(host=host_yandi, user=user_yandi, passwd=password_yandi, db='yandi',port=port_yandi,autocommit = True,charset='utf8mb4')
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql_text)
            connection.commit()
            result = cursor.fetchall()
            return result
        finally:
            connection.close()
            
    def exe_sql_binary(self,sql,*args):

        con = pymysql.connect(host=host_yandi, user=user_yandi, passwd=password_yandi, db='yandi',port=port_yandi,autocommit = True,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

        try:

            cursor = con.cursor()
            cursor.execute(sql,args)
            results = cursor.fetchall()
            #print(results)
            con.commit()
            return results

        finally:
            con.close()
            
            
    def exe_sql(self,sql_text):
        try:
            # connection = pymysql.connect(host='10.10.10.10', user='yunwei', passwd='testpwd', db='yandi',port=35972,autocommit = True,charset='utf8mb4')
            connection = pymysql.connect(host=host_yandi, user=user_yandi, passwd=password_yandi, db='yandi',port=port_yandi,autocommit = True,charset='utf8mb4')
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql_text)
            connection.commit()
            result = cursor.fetchall()
            return result
        finally:
            connection.close()
            
                
    def exe_sql_one_col(self,sql):
            con = pymysql.connect(host=host_yandi, user=user_yandi, passwd=password_yandi, db='gsdb',port=port_yandi,autocommit = True,charset='utf8mb4')
 
            try:

                cursor = con.cursor()
                cursor.execute(sql)
                results = cursor.fetchall()
                #print(results)
                return list(map(lambda x: x[0], results))
            finally:
                con.close()

    def remote_excute(self,ip,port,user,pwd,db,sql_text):
        try:
            connection = pymysql.connect(host=ip, user=user, passwd=pwd, db=db,port=port,autocommit = True,charset='utf8mb4')
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql_text)
            connection.commit()
            result = cursor.fetchall()
            return result
        finally:
            # cursor.close()
            connection.close()
            # pass

    def exe_sql_no_col(self,sql):
            con = pymysql.connect(host=host_yandi, user=user_yandi, passwd=password_yandi, db='yandi',port=port_yandi,autocommit = True,charset='utf8mb4')

            try:

                cursor = con.cursor()
                cursor.execute(sql)
                results = cursor.fetchall()
                #print(results)
                con.commit()
                return results

            finally:
                con.close()
                
    def remote_ssh_noresult(self,cmd,ip,user,pwd):
      try:
        ssh = paramiko.SSHClient()# 创建ssh对象
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())# 允许连接不在know_host中的主机
        ssh.connect(hostname=ip, port=22, username=user, password=pwd)# 连接服务器
        ssh.exec_command(cmd)# 执行命令
        ssh.close()
      
      except Exception as e:
            print(e)
            
    def remote_ssh(self,cmd,ip,user,pwd):
      try:
        ssh = paramiko.SSHClient()# 创建ssh对象
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())# 允许连接不在know_host中的主机
        ssh.connect(hostname=ip, port=22, username=user, password=pwd)# 连接服务器
        stdin, stdout, stderr = ssh.exec_command(cmd)# 执行命令
        log_2=stderr.read().decode('utf-8')
        while True:
            line = stdout.readline()
            if not line:
                break
            return(line)
        ssh.close()
      except Exception as e:
        print(e)

            
    def remote_ssh_put(self,file_name,remote_dir,ip,user,pwd):
      try:
        # 首先连上服务器
        transport = paramiko.Transport((ip, 22))
        transport.connect(username=user, password=pwd)
        # 与主机交互
        sftp = paramiko.SFTPClient.from_transport(transport)
        # 将本地的文件上传到服务器/tmp/目录下
        sftp.put(file_name, remote_dir)
        # 将服务器端的文件下载到本地
        # sftp.get('/root/stderr.txt', 'fromlinux.txt')

        #关闭
        transport.close()
      except Exception as e:
            return 1

