import pymysql

from db_driver import mysql_driver


class inventory(mysql_driver):

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
        sql = 'select id,category,ip,description,vip,port from yandi.inventory where deleted = 0 ORDER BY vip;'
        return  self.exe_sql(sql)


    def save_inventory(self):
        id = self.request.form['id']
        category = self.request.form['category']
        ip = self.request.form['ip']
        description = self.request.form['description']
        vip = self.request.form['vip']
        port = self.request.form['port']
        if id == '':
            sql = f"insert into yandi.inventory(category,ip,description,vip,port) values('{category}','{ip}','{description}','{vip}','{port}')"
        else:
            sql = f"update yandi.inventory set category ='{category}',ip='{ip}',description='{description}',vip='{vip}',port='{port}' where id = {id} "
        self.exe_sql(sql)
            
        return {
            'status': True,
            'msg': '更新成功',
            'data': self.get_inventory_from_db()
        }


    def delete_inventory(self):
        id = self.request.form['id']
        sql = f'update yandi.inventory set deleted=true where id={id}'
        self.exe_sql(sql)
        return {
            'status': True,
            'msg': '删除成功',
            'data': self.get_inventory_from_db()
        }


