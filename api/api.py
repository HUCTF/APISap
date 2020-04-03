#coding:utf-8
from api_class import token_check,op,msg_random_check
from flask import Flask, render_template, request, current_app
from flask_cors import *
server = Flask(__name__)
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 设置这一项是每次请求结束后都会自动提交数据库中的变动

CORS(server,supports_credentials=True)
token_api = token_check()
msg_check =msg_random_check
import json

#函数功能：后端初始配置（只需执行一次）
#路径：/init_ip
#输入：
#   ip = 开发者ip
#返回：
#   成功：初始化完成
#       初始化成功{'code': 200, 'msg': "初始化成功"}
#
#   失败：
#       参数为空{'code': 10001, 'result': '参数不能为空！'}
@server.route('/init_ip',methods=['get','post'])
def init_ip():
    #访问时需要带上参数：自己的ip
    #data = request.get_data()
    #data = data.decode('utf-8')
    #data = json.loads(data)
    # print(data)
    #url = data['ip']
    if request.method == 'POST':
        url=request.form.get("ip")
    else:
        url=request.args.get("ip")
    if url:
        token_api.create_mid_server_key(url)
        return {'code': 200, 'msg': "初始化成功"}
    else:
        resu = {'code': 10001, 'result': '参数不能为空！'}
        return resu
    # print(url)
    #这里面会创建两个表，包括msg_tb、token_tb


#函数功能：token生成器（每次用户登陆时使用一次）
#路径：/init_token
#输入：
#   ip = 开发者ip
#   user_id = 登陆用户的id（唯一标识符)
#返回：
#   成功：生成并返回token
#       resu = {'code': 200, 'token': token,'msg':'申请token成功'}
#       resu={'code': 201, 'token': token,'msg':'数据库已有记录'}
#
#   失败：
#       参数为空{'code': 10001, 'result': '参数不能为空！'}
@server.route('/init_token',methods=['get','post'])
def init_token():
    #访问时需要带上参数：user_id,ip
    #data = request.get_data()
    #data = data.decode('utf-8')
    #data = json.loads(data)
    # plain_text = data['plain_text']
    #user_id = data['user_id']
    #url = data['ip']
    if request.method == 'POST':
        url=request.form.get("ip")
        user_id=request.form.get("user_id")
    else:
        password=request.args.get("ip")
        user_id=request.args.get("user_id")
    if user_id and url:
        #resu = {'code': 200, 'token': token,'msg':'申请token成功'}
        #resu={'code': 201, 'token': token,'msg':'数据库已有记录'}
        return token_api.server_get_token(user_id, url)
    else:
        resu = {'code': 10001, 'result': '参数不能为空！'}
        return resu
    #return {'code': 201, 'token': token,'msg':'数据库已有记录'}
    #resu = {'code': 200, 'token': token,'msg':'申请token成功'}
    # resu = {'code': 10000, 'msg': '参数不能为空！'}

#函数功能：token校验器(每次校验前端发来的token)
#路径：/init_token
#输入：
#   ip = 开发者ip
#   user_id = 登陆用户的id（唯一标识符)
#   token = 待校验的token
#返回：
#   成功：生成并返回token
#       resu = {'code': 200, 'msg': "token验证成功"}
#
#   失败：
#       resu = {'code': 10000, 'msg': 'token验证失败'}
#       resu = {'code': 10001, 'msg': "token已更新，请重新登陆"}
#       resu = {'code': 10002, 'result': '参数不能为空！'}
@server.route('/check_token',methods=['get','post'])
def check_token():
    #访问时需要带上参数：user_id,ip,以及需要检测的token
    if request.method == 'POST':
        url=request.form.get("ip")
        user_id=request.form.get("user_id")
        server_token =request.form.get("token")
    else:
        password=request.args.get("ip")
        user_id=request.args.get("user_id")
        server_token =request.args.get("token")

    if url and user_id and url:
        data = token_api.search_token_by_id(user_id, url)
        if data['code'] == 200:
            sql_token = data['token']
            if server_token == sql_token:
                resu = {'code': 200, 'msg': "token验证成功"}
                return resu
            else:
                resu = {'code': 10000, 'msg': 'token验证失败'}
                return resu
        else:
            resu = {'code': 10001, 'msg': "token已更新，请重新登陆"}
            return resu
    else:
        resu = {'code': 10002, 'result': '参数不能为空！'}
        return resu


#函数功能：客户端请求获得公钥与序列号
#路径：/get_puk_sq
#输入：
#   ip = 开发者ip
#返回：
#   成功：生成并返回token
#       resu = {'code': 200, 'sq': sq, 'puk': self.public_key, 'msg': '数据创建成功。'}
#       resu = {'code': 200,'sq':sq,'puk':self.public_key, 'msg': '数据已创建。'}
#
#   失败：
#       resu = {'code': 10000, 'result': '参数不能为空！'}
@server.route('/get_puk_sq',methods=['get','post'])
def front_get_puk_sq():
    if request.method == 'POST':
        url=request.form.get("ip")
    else:
        url=request.args.get("ip")
    if url:
        result = msg_check.create_seq(msg_check,url)
        # resu = {'code': 200, 'sq': sq, 'puk': self.public_key, 'msg': '数据创建成功。'}
        # resu = {'code': 200,'sq':sq,'puk':self.public_key, 'msg': '数据已创建。'}
        return result
    else:
        resu = {'code': 10000, 'result': '参数不能为空！'}
        return resu


#函数功能：服务端通过序列号对密文解密
#路径：/server_decode
#输入：
#   ip = 开发者ip
#返回：
#   成功：生成并返回token
#       resu = {'code': 200, 'result': plaintext}(返回明文)
#
#   失败：
#       resu = {'code': 10000, 'result': '参数不能为空！'}
#       return {'code': 10000, 'msg': '未找到私钥'}
@server.route('/server_decode',methods=['get','post'])
def server_decode():
    if request.method == 'POST':
        url=request.form.get("ip")
        sq=request.form.get("sq")
        cypher =request.form.get("cypher")
    else:
        url=request.args.get("ip")
        sq=request.args.get("sq")
        cypher =request.args.get("cypher")
    #url = data['ip']
    #sq = data['sq']
    #cypher = data['cypher']
    if url and sq and cypher:
        result = msg_check.mid_sever_decode(msg_check ,cypher, sq,url)
        return result
        # return {'code': 200, 'result': Decrypts.rsa_decrypt(cypher, prk)}
        # return {'code': 10000, 'msg': '未找到私钥'}
    else:
        resu = {'code': 10001, 'result': '参数不能为空！'}
        return resu




@server.route('/test',methods=['get','post'])
def test():
    return 'good'
if __name__ == '__main__':
    # cypher="UM2/fqjmvx5nouTZXZ5opcKGWLvBUxp2tVmp180ob1pZl0D30zLiW2XQ88oQ0C+vIJl6+sehRXwj2FT6PKtwHK7V/cpwvHfblt4L8ZMdB+eiili29iBdSmTBTpVeoqbm8WlPa7EG5yasa93qNvlAGS5mHLRIL4eBDD0wwNisA7s="
    # sq="87edcd8db7d42f2265a2cedaafecdee9"
    # url='1.1.1.1'
    # print(msg_check.mid_sever_decode(msg_check, cypher, sq, url))
    #用于定时清理
    token_api.timedTask()
    # test=1
    # print(token_api.search_token_by_id('2019', '127.0.0.1:8886'))
    # token_api.server_get_token('2019','127.0.0.1:8886')
    # print(test['token'])

    #token_api.create_mid_server_key('127.0.0.1:8886')
    #token_api.server_get_token('21111', '127.0.0.1:8886')

    #print(msg_check.create_seq(msg_check,'127.0.0.1:8886'))
    # server.run(debug='true' , port=5000, host='0.0.0.0')  # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问
