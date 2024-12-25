from flask import Flask
from flask import g
from flask import request
from flask import jsonify
from flask.json import JSONEncoder
import logging
import datetime
from user import User
import jwt
import traceback
from datetime import timedelta,datetime
import decimal
import settings
import inventory
import add_instance
import add_monitor
import dbcreate
import db_driver
import mysql_adduser
import mysql_backup
import mysql_binlog2sql
import mysql_crontab
import mysql_dbcreate
import mysql_detail
import mysql_log
import mysql
import mysql_setmodify
import mysql_topsql
import scheduler
import table_size
import tools
import user
import yunweicenter
import redis_detail
import add_redis
import redis_adduser

app = Flask(__name__)

class JSON_Encoder(JSONEncoder):

    def default(self,o):

        if isinstance(o, datetime):
            return o.__str__()
        elif isinstance(o, decimal.Decimal):
            return float(o)
        elif isinstance(o, timedelta):
            return round(o.total_seconds(), 3)
        elif isinstance(o, bytes):
            return str(o, encoding='utf-8')

        return JSONEncoder.default(self, o)

#加载配置
# app.config.from_pyfile('settings.py')
app.config.from_object(settings)

app.json_encoder = JSON_Encoder
print(app.config)

#设置日志
handler = logging.FileHandler('/tmp/flask.log', encoding='UTF-8')

handler.setLevel(logging.DEBUG)

logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

handler.setFormatter(logging_format)

app.logger.addHandler(handler)


#判断是否已经登陆，或者登陆是否已经过期
@app.before_request
def is_login():
    if request.path == "/api/login":
        return
    else:
        try:
            auth_header = request.headers.get('Authorization')
            print(auth_header)
            payload = jwt.decode(auth_header.strip('"'), app.config['JWT_KEY'], options={'verify_exp': True})
            operator = payload['data']['operator']
            #在这里获取操作者密码，然后构建连接字符串，放到g里面
            password = User(app.config['DB_CONFIG']).get_password(operator)
            g.db_config = {
                'host': app.config['DB_CONFIG']['host'],
                'user': operator,
                'password': password,
                'port': app.config['DB_CONFIG']['port'],
                'charset': app.config['DB_CONFIG']['charset'],
                'cursorclass': app.config['DB_CONFIG']['cursorclass']
            }
            return
        except jwt.ExpiredSignatureError :
            return jsonify({
                'status':'timeout',
                'msg':'登陆过期'
            })
        except Exception :
            logging.error(traceback.format_exc())
            return jsonify(
                {
                    'status':False,
                    'msg':traceback.format_exc()
                }
            )

@app.route('/api/login',methods=['POST'])
def login():
    try:

        user = User(app.config['DB_CONFIG'],request)
        #如果密码验证通过的话，就可以进行操作了
        if user.check_password():
                payload = {
                    'exp': datetime.utcnow() + timedelta(days=1),
                    'iat': datetime.utcnow(),
                    'iss': 'ken',
                    'data': {
                        'operator': request.form['username'].strip()
                    }
                }

                token = jwt.encode(
                    payload,
                    app.config['JWT_KEY'],
                    algorithm='HS256'
                )

                return jsonify({
                    "status": True,
                    "data": {'token': token.decode()},
                    "msg": 'success'
                })
        else:
            return jsonify({
                "status": False,
                "msg": '账号密码错误'
            })

    except Exception:
        logging.error(traceback.format_exc())

        return jsonify({
            "status":False,
            "msg":'账号或者密码错误，请重新输入'
        })


@app.route('/api/<class_name>/<method_name>/',methods=['POST','GET'])
def process_request(class_name,method_name):

    model_module = __import__(class_name)
    # 根据子类名称从m.py中获取该类
    obj_class_name = getattr(model_module, class_name)
    # 实例化对象
    obj = obj_class_name(g.db_config,request)
    # 调用print_name方法
    try:
        results = getattr(obj, method_name)()
    except Exception as e:
        #traceback.print_exc()
        results = {
            'status':False,
            'msg':str(e)
        }
    finally:
        print('helloworld')
        if method_name == 'download':
            return results
        else:
            return jsonify(results)

if __name__ == '__main__':
    # datastack
    app.run(host='0.0.0.0', port=5006,debug=True)
    # app.run(host='0.0.0.0', port=5001,debug=True)

