import pymysql
# from settings import *
import datetime
import configparser


# host_yandi=DB_CONFIG['host']
# port_yandi=DB_CONFIG['port']
# user_yandi=DB_CONFIG['user']
# password_yandi=DB_CONFIG['password']

cfg = configparser.ConfigParser()
cfg.read('/app/datastack.cfg')
host_yandi= cfg.get('section','mysqlip')
user_yandi= cfg.get('section','mysqluser')
port_yandi= cfg.get('section','mysqlport')
password_yandi= cfg.get('section','mysqlpwd')
port_yandi=int(port_yandi)

def exe_sql(sql_text):
    try:
        connection = pymysql.connect(host=host_yandi, user=user_yandi, passwd=password_yandi, db='yandi',port=port_yandi,autocommit = True,charset='utf8mb4')
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
            
def get_all_table():
      try:
        get_tables_sql = """SELECT TABLE_CATALOG,TABLE_SCHEMA,TABLE_NAME,TABLE_TYPE,ENGINE,VERSION,ROW_FORMAT,TABLE_ROWS,AVG_ROW_LENGTH,DATA_LENGTH,MAX_DATA_LENGTH,INDEX_LENGTH,DATA_FREE,AUTO_INCREMENT,CREATE_TIME,UPDATE_TIME,CHECK_TIME,TABLE_COLLATION,CHECKSUM,CREATE_OPTIONS FROM information_schema.TABLES WHERE table_schema NOT IN('information_schema','performance_schema','sys','mysql')"""
        get_events_statements_summary_by_digest="""SELECT SCHEMA_NAME,DIGEST,DIGEST_TEXT,COUNT_STAR,SUM_TIMER_WAIT,MIN_TIMER_WAIT,AVG_TIMER_WAIT,MAX_TIMER_WAIT,SUM_LOCK_TIME,SUM_ERRORS,SUM_WARNINGS,
SUM_ROWS_AFFECTED,SUM_ROWS_SENT,SUM_ROWS_EXAMINED,SUM_CREATED_TMP_DISK_TABLES,SUM_CREATED_TMP_TABLES,SUM_SELECT_FULL_JOIN,
SUM_SELECT_FULL_RANGE_JOIN,SUM_SELECT_RANGE,SUM_SELECT_RANGE_CHECK,SUM_SELECT_SCAN,SUM_SORT_MERGE_PASSES,SUM_SORT_RANGE,SUM_SORT_ROWS,
SUM_SORT_SCAN,SUM_NO_INDEX_USED,FIRST_SEEN,LAST_SEEN FROM performance_schema.events_statements_summary_by_digest;"""

        # sql = f"SELECT ip as vip,port  FROM yandi.inventory WHERE deleted=0 ;"
        sql='''SELECT DISTINCT(vip) AS vip,`port`  FROM yandi.a_inventory WHERE deleted=0 ;'''
        ips=exe_sql(sql)
        for i in ips:
              ip=i['vip']
              port=i['port']
              port=int(port)
              print(ip)
              get_tables_results=remote_excute(ip,port,'yunwei','testpwd','mysql',get_tables_sql)
              get_essyd=remote_excute(ip,port,'yunwei','testpwd','mysql',get_events_statements_summary_by_digest)
              for result_1 in get_tables_results:
                  result_1['hostip'] = ip
              
              for result_2 in get_essyd:
                  result_2['hostip'] = ip
              
              insert_sql = """insert into yandi.tables(TABLE_CATALOG,TABLE_SCHEMA,TABLE_NAME,TABLE_TYPE,ENGINE,VERSION,ROW_FORMAT,TABLE_ROWS,AVG_ROW_LENGTH,DATA_LENGTH,MAX_DATA_LENGTH,INDEX_LENGTH,DATA_FREE,AUTO_INCREMENT,CREATE_TIME,UPDATE_TIME,CHECK_TIME,TABLE_COLLATION,CHECKSUM,CREATE_OPTIONS,hostip) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
              insert_sql_2="""insert into yandi.events_statements_summary_by_digest(SCHEMA_NAME,DIGEST,DIGEST_TEXT,COUNT_STAR,SUM_TIMER_WAIT,MIN_TIMER_WAIT,AVG_TIMER_WAIT,MAX_TIMER_WAIT,SUM_LOCK_TIME,SUM_ERRORS,SUM_WARNINGS,
SUM_ROWS_AFFECTED,SUM_ROWS_SENT,SUM_ROWS_EXAMINED,SUM_CREATED_TMP_DISK_TABLES,SUM_CREATED_TMP_TABLES,SUM_SELECT_FULL_JOIN,
SUM_SELECT_FULL_RANGE_JOIN,SUM_SELECT_RANGE,SUM_SELECT_RANGE_CHECK,SUM_SELECT_SCAN,SUM_SORT_MERGE_PASSES,SUM_SORT_RANGE,SUM_SORT_ROWS,
SUM_SORT_SCAN,SUM_NO_INDEX_USED,FIRST_SEEN,LAST_SEEN,hostip) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

              chuli_results = []
              chuli_results_2 = []
              for key in get_tables_results:
                  chuli_results.append(tuple(key.values()))
              for key_2 in get_essyd:
                  chuli_results_2.append(tuple(key_2.values()))

              connection = pymysql.connect(host=host_yandi,
                                          user=user_yandi,
                                          password=password_yandi,
                                          charset='utf8mb4',
                                          port=port_yandi,
                                          cursorclass=pymysql.cursors.DictCursor)

              try:
                  with connection.cursor() as cursor:
                      cursor.executemany(insert_sql,chuli_results)
                      cursor.executemany(insert_sql_2,chuli_results_2)
              finally:
                  connection.commit()
                  connection.close()
      except Exception as e:
          print(e)
          
get_all_table()