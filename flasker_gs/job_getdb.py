import pymysql
from settings import *


host=DB_CONFIG['host']
port=DB_CONFIG['port']
user=DB_CONFIG['user']
password=DB_CONFIG['password']

def exe_sql(sql_text):
    try:
        connection = pymysql.connect(host=host, user=user, passwd=password, db='yandi',port=port,autocommit = True,charset='utf8mb4')
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql_text)
        connection.commit()
        result = cursor.fetchall()
        return result
    finally:
        connection.close()
        

def remote_excute(ip,port,user,pwd,db,sql_text):
        try:
            connection = pymysql.connect(host=ip, user=user, passwd=pwd, db=db,port=port,autocommit = True,charset='utf8mb4')
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql_text)
            connection.commit()
            result = cursor.fetchall()
            return result
        finally:
            connection.close()
 
def get_alldbname():
    try:
        sql = f"SELECT DISTINCT(schema_name) as schema_name FROM information_schema.schemata WHERE schema_name NOT IN ('information_schema','mysql','sys','performance_schema');"    
        
        msg='获取DB成功'
        sql_1=f"SELECT DISTINCT(vip) AS vip,port FROM yandi.`inventory` WHERE deleted=0;"
        ips=exe_sql(sql_1)
        
        for i in ips:
            print(i)
            vip=i['vip']
            port=i['port']
            port=int(port)
            data=remote_excute(vip,port,'yunwei','testpwd','mysql',sql)
            for datas in data:
                schema_name=datas['schema_name']
                sql_3=f"select count(*) as v_1 from yandi.db_name where dbname='{schema_name}' and ip='{vip}' and port='{port}'; "
                v_2=exe_sql(sql_3)
                v_3=v_2[0]['v_1']
                if v_3==0: 
                    sql_2=f"insert into yandi.db_name(ip,port,dbname) values('{vip}','{port}','{schema_name}')"
                    exe_sql(sql_2)
                else:
                    pass
    except Exception as exec_error:
        print(exec_error)
   
get_alldbname()