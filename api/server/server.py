from flask import render_template
from flask import Flask, render_template, request, current_app
from flask import request, jsonify,make_response,Markup
from flask_cors import *
import json
import requests
server = Flask(__name__)
CORS(server,supports_credentials=True)
# server.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://123456:123456@localhost:3306/token1'  # 这里登陆的是root用户，要填上自己的密码，MySQL的默认端口是3306，填上之前创建的数据库名text1

#需要实现只对少数端口开放。
@server.route('/',methods=['get','post'])
def index():
    response = make_response(render_template('test.html'))
    return response
@server.route('/login_check',methods=['get','post'])
def login_check():
    data = request.get_data()
    data = data.decode('utf-8')
    data = json.loads(data)
    password = data['password']
    user_id = data['user_id']
    res={}
    if password=='123456'and user_id=='123456':
        code=generate_token(user_id)
        if code==200:
            res = {'code': 200, 'msg': '登陆成功'}
        else:
            res = {'code': 1001, 'msg': 'token申请失败'}
    else:
        res={'code':10000,'msg':'账号或密码错误'}
    return res

@server.route('/msg_check',methods=['get','post'])
def msg_check():
    data = request.get_data()
    data = data.decode('utf-8')
    data = json.loads(data)
    token = data['token']
    user_id='123456'
    if trans_check(user_id,token)==200:
        return 'getmsg'
    else:
        return 'false'



ip='http://127.0.0.1/8886'
headers = {"Content-Type": "application/x-www-form-urlencoded"}
#需要执行一次的初始化操作
def init_ip():
    # print('1')
    data = {"ip": ip}
    data = "%s" % json.dumps(data)

    result = requests.post("http://127.0.0.1:5000/init_ip", data,headers = headers)
    print(result)
    return result['code']
    # print(result.json())

    # print(result['msg'])

def trans_check(user_id,token):
    data = {"user_id":user_id,"ip": ip,'token':token}
    result = requests.post("http://127.0.0.1:5000/check_token", data,headers = headers)
    code = result['code']
    print(result['msg'])
    return code


def generate_token(user_id):
    data={"user_id":user_id,'ip':ip}
    result=requests.post("http://127.0.0.1:5000/init_token",data,headers = headers)
    code=result['code']
    print(result['msg'])
    return code



if __name__=='__main__':
    # init_ip()
    # result = requests.post("http://127.0.0.1:5000/test")
    server.run(debug='true' , port=8886, host='0.0.0.0')  # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问
