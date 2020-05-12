from flask import render_template
from flask import Flask, render_template, request, current_app, url_for
from flask import request, jsonify,make_response,Markup,send_file
from flask_cors import *
import json
import requests
from flask import make_response
from flask import Response
import os
server = Flask(__name__)
# server.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://123456:123456@localhost:3306/token1'  # 这里登陆的是root用户，要填上自己的密码，MySQL的默认端口是3306，填上之前创建的数据库名text1

#需要实现只对少数端口开放。
@server.route('/',methods=['get','post'])
def test():
    response = make_response(render_template('test.html'))
    return response

@server.route('/index',methods=['get','post'])
def index():
    response = make_response(render_template('index.html'))
    # response.mimetype = 'application/wasm'
    return response
# @server.route('/get_wasm',methods=['get','post'])
# def get_wasm():
#
#     response =''
#
#     response = make_response(server.send_static_file('encode.wasm'))
#     response.mimetype = 'application/wasm'
#     return response
# @server.route('/get_wasm1')
# def wasm_file():
#     return server.send_file('/static/encode.wasm', mimetype = 'application/wasm');
# @server.route('/get_wasm')
# def get_wasm(path):
#     base_dir = os.path.dirname(__file__)
#     resp = make_response(open(os.path.join(base_dir,path)).read())
#
#     resp.headers["Content-type"]='application/wasm'
#     return resp


@server.route('/index1',methods=['get','post'])
def index1():
    response = make_response(render_template('encode.html'))
    return response

@server.route('/get_msg',methods=['get','post'])
def get_msg():
    if request.method == 'POST':
        mm=request.form.get("mm")
        token=request.form.get("token")
    else:
        mm=request.args.get("mm")
        token = request.args.get("token")


    data = {
        'ip': ip,
        'user_id': user_id,
        'token': token
    }

    result = requests.post(url="http://127.0.0.1:5000/check_token", data=data)
    result = json.loads(result.text)
    if mm!='I am front':
        return 'not a true password!'
    else:
        return 'I am server!'
    return response

if __name__=='__main__':
    # init_ip()
    # result = requests.post("http://127.0.0.1:5000/test")
    server.run(debug='true' , port=8886, host='0.0.0.0')  # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问
