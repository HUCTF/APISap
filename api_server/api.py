from api_class import mid_server,Encrypts,Decrypts
from flask import Flask, render_template, request, current_app
from flask_cors import *
server = Flask(__name__)
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 设置这一项是每次请求结束后都会自动提交数据库中的变动

CORS(server,supports_credentials=True)
token_api = mid_server()
import json
@server.route('/init_ip',methods=['get','post'])
def create_key():
    #访问时需要带上参数：自己的ip
    data = request.get_data()
    # print(data)
    data = data.decode('utf-8')
    # print(data)
    data = json.loads(data)
    print(data)
    # return '1'
    # plain_text = data['plain_text']
    url = data['ip']
    print(url)
    print(token_api.create_mid_server_key(url))

@server.route('/init_token',methods=['get','post'])
def init_token():
    #访问时需要带上参数：user_id,ip
    data = request.get_data()
    data = data.decode('utf-8')
    data = json.loads(data)
    # plain_text = data['plain_text']
    user_id = data['user_id']
    url = data['ip']
    return  token_api.server_get_token(user_id,url)

@server.route('/check_token',methods=['get','post'])
def search_token():
    #访问时需要带上参数：user_id,ip,以及需要检测的token
    data = request.get_data()
    data = data.decode('utf-8')
    data = json.loads(data)
    # plain_text = data['plain_text']
    user_id = data['user_id']
    url = data['ip']
    server_token = data['token']
    data=token_api.search_token_by_id(user_id,url)
    if data['code']==200:
        sql_token=data['token']
        if server_token==sql_token:
            resu = {'code': 200, 'msg': "token验证成功"}
            return resu
        else:
            resu = {'code':10000,'msg':'token验证失败'}
    else:
        resu = {'code': 10001, 'msg': "token已更新，请重新登陆"}
        return resu

@server.route('/test',methods=['get','post'])
def test():
    return 'good'
if __name__ == '__main__':
    #用于定时清理
    test=1
    test=token_api.server_get_token('2019','127.0.0.1:8886')
    # print(test['token'])
    # token_api.timedTask()
    # token_api.create_mid_server_key('127.0.0.1:8886')
    # server.run(debug='true' , port=5000, host='0.0.0.0')  # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问
