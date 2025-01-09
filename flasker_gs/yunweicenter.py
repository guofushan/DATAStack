import pymysql

from db_driver import mysql_driver


class yunweicenter(mysql_driver):

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
        sql = 'SELECT id,url,user,pwd,description FROM yandi.`yunwei_center` WHERE deleted<>1;'
        return  self.exe_sql(sql)


    def save_inventory(self):
        id = self.request.form['id']
        url = self.request.form['url']
        user = self.request.form['user']
        pwd = self.request.form['pwd']
        description = self.request.form['description']
        if id == '':
            sql = f"insert into yandi.yunwei_center(url,user,pwd,description) values('{url}','{user}','{pwd}','{description}')"
        else:
            sql = f"update yandi.yunwei_center set url ='{url}',user='{user}',pwd='{pwd}',description='{description}' where id = {id} ;"
        self.exe_sql(sql)
            
        return {
            'status': True,
            'msg': '更新成功',
            'data': self.get_inventory_from_db()
        }


    def delete_inventory(self):
        id = self.request.form['id']
        sql = f'update yandi.yunwei_center set deleted=1 where id={id};'
        self.exe_sql(sql)
        return {
            'status': True,
            'msg': '删除成功',
            'data': self.get_inventory_from_db()
        }


