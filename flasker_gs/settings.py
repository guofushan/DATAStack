import pymysql
import configparser

cfg = configparser.ConfigParser()
cfg.read('/app/datastack.cfg')

mysqlip= cfg.get('section','mysqlip')
mysqluser= cfg.get('section','mysqluser')
mysqlport= cfg.get('section','mysqlport')
mysqlpwd= cfg.get('section','mysqlpwd')
mysqlport1=int(mysqlport)

root_user= cfg.get('section','root_user')
root_pwd= cfg.get('section','root_pwd')
datastack_ip= cfg.get('section','datastack_ip')

#定义datastack后端数据库信息
DB_CONFIG = {
    'host':mysqlip,
    'user':mysqluser,
    'password':mysqlpwd,
    'port':mysqlport1,
    'charset':'utf8mb4',
    'cursorclass':pymysql.cursors.DictCursor
}

JWT_KEY = 'super-secret'
#定义os用户密码
script_dir='/app/yandi/flasker_gs'
root_user=root_user
root_pwd=root_pwd
report_email='1031010310@qq.com'
#定义datastack部署ip
datastack_ip=datastack_ip
