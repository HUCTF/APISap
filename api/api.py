#coding:utf-8
from api_class import token_check,op,msg_random_check,token_consume,msg_check_consume
from flask import Flask, render_template, request, current_app
from flask_cors import *
server = Flask(__name__)
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 设置这一项是每次请求结束后都会自动提交数据库中的变动
# server.config['SEND_FILE_MAX_AGE_DEFAULT']=timedelta(seconds=1)

CORS(server,supports_credentials=True)
token_api = token_check()
msg_check =msg_random_check()
token_consume=token_consume()
msg_consume=msg_check_consume()
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
        kid=request.form.get("kid")
    else:
        url=request.args.get("ip")
        kid = request.args.get("kid")

    if url:
        token_api.create_mid_server_key(kid,url)
        return json.dumps({'code': 200, 'result': "初始化成功"})
    else:
        resu = {'code': 10001, 'result': '参数不能为空！'}
        return json.dumps(resu)
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
    # data = request.get_data()
    # # data = data.decode('utf-8')
    # data = json.loads(data)
    # user_id = data['user_id']
    # url = data['ip']
    # print(url)
    # print(user_id)
    if request.method == 'POST':
        print('godo')
        url=request.form.get("ip")
        user_id=request.form.get("user_id")
    elif request.method == 'GET':
        # password=request.args.get("ip")
        url = request.args.get("ip")
        user_id=request.args.get("user_id")
    print(url)
    print(user_id)
    try:
        if user_id and url:
            #resu = {'code': 200, 'token': token,'msg':'申请token成功'}
            #resu={'code': 201, 'token': token,'msg':'数据库已有记录'}
            resu=token_api.server_get_token(user_id, url)
            return json.dumps(resu)
        else:
            resu = {'code': 10001, 'result': '参数不能为空！'}
            return json.dumps(resu)
        #return {'code': 201, 'token': token,'msg':'数据库已有记录'}
        #resu = {'code': 200, 'token': token,'msg':'申请token成功'}
        # resu = {'code': 10000, 'msg': '参数不能为空！'}
    except:
        resu = {'code': 10002, 'result': '出现未知错误！'}
        return json.dumps(resu)

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
        url=request.args.get("ip")
        user_id=request.args.get("user_id")
        server_token =request.args.get("token")
        print(url)
        print(user_id)
        print(server_token)
    try:

        if url and user_id and server_token:
            data = token_api.search_token_by_id(user_id, url)
            if data['code'] == 200:
                print('-------------------')
                sql_token = data['token']
                if server_token == sql_token:
                    resu = {'code': 200, 'msg': "token验证成功"}
                    return json.dumps(resu)
                else:
                    resu = {'code': 10000, 'msg': 'token验证失败'}
                    return json.dumps(resu)
            else:
                resu = {'code': 10001, 'msg': "token已更新，请重新登陆"}
                return json.dumps(resu)
        else:
            resu = {'code': 10002, 'result': '参数不能为空！'}
            return json.dumps(resu)
    except:
        resu = {'code': 10003, 'result': '出现未知错误！'}
        return json.dumps(resu)

def check_token2(url,user_id,server_token):
    try:
        if url and user_id and server_token:
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
    except:
        resu = {'code': 10002, 'result': '出现未知错误！'}
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
    try:
        if url:
            resu = msg_check.create_seq(url)
            # resu = {'code': 200, 'sq': sq, 'puk': self.public_key, 'msg': '数据创建成功。'}
            # resu = {'code': 200,'sq':sq,'puk':self.public_key, 'msg': '数据已创建。'}
            return json.dumps(resu)
        else:
            resu = {'code': 10000, 'result': '参数不能为空！'}
            return json.dumps(resu)
    except:
        resu = {'code': 10002, 'result': '出现未知错误！'}
        return json.dumps(resu)

#函数功能：服务端通过序列号对密文解密
#路径：/server_decode
#输入：
#   ip = 开发者ip
#   sq=序列号
#   cyhper=密文
#返回：
#   成功：生成并返回token
#       resu = {'code': 200, 'result': plaintext}(返回明文)
#
#   失败：
#       resu = {'code': 10001, 'result': '参数不能为空！'}
#       return {'code': 10000, 'msg': '未找到私钥'}
@server.route('/server_decode2',methods=['get','post'])
def server_decode2():
    if request.method == 'POST':
        url=request.form.get("ip")
        sq=request.form.get("sq")
        cypher =request.form.get("cypher")
        user_id = request.form.get("user_id")
        token = request.form.get("token")
    else:
        url=request.args.get("ip")
        sq=request.args.get("sq")
        cypher =request.args.get("cypher")
        user_id = request.args.get("user_id")
        token = request.args.get("token")

    # try:
    if url and sq and cypher and user_id and token:
        result=check_token2(url,user_id,token)
        if result['code']==200:
            result = msg_check.mid_sever_decode(cypher, sq,url)
            return result
            # return {'code': 200, 'result': Decrypts.rsa_decrypt(cypher, prk)}
            # return {'code': 10000, 'msg': '未找到私钥'}
        else:
            return result
    else:
        resu = {'code': 10001, 'result': '参数不能为空！'}
        return resu
    # except:
    #     resu = {'code': 10002, 'result': '出现未知错误！'}

@server.route('/server_decode', methods=['get', 'post'])
def server_decode():
    if request.method == 'POST':
        url = request.form.get("ip")
        sq = request.form.get("sq")
        cypher = request.form.get("cypher")
    else:
        url = request.args.get("ip")
        sq = request.args.get("sq")
        cypher = request.args.get("cypher")
    # url = data['ip']
    # sq = data['sq']
    # cypher = data['cypher']
    # try:
    if url and sq and cypher:
        result = msg_check.mid_sever_decode(cypher, sq, url)
        return result
        # return {'code': 200, 'result': Decrypts.rsa_decrypt(cypher, prk)}
        # return {'code': 10000, 'msg': '未找到私钥'}
    else:
        resu = {'code': 10001, 'result': '参数不能为空！'}
        return resu
    # except:
    #     resu = {'code': 10002, 'result': '出现未知错误！'}
    #     return resu

#函数功能：服务端通过序列号对密文解密
#路径：/msg_check表的增删改查
#输入：
#   kid = 执行操作的用户id
#   operator = 需要执行的操作[insert_msg,deleteis_by_sq,update_by_sq,search_by_sq,search_all]
#               insert_msg: 插入数据，参数[url,sq,puk,prk,time_code]
#               deleteis_by_sq:删除数据，参数[url,sq]
#               update_by_sq：更新数据，参数[url,sq,puk,prk,time_code]
#               search_by_sq：查找数据，参数[url,sq]
#               search_all:查询所有数据，参数[url]


#返回：
#   成功：生成并返回token
#       {'code':200,'result':'操作成功'}
#       {'code':200,'result':result}
#   失败：
#       {'code':10000,'msg':'没有找到用户的记录'}
#       {'code': 10001, 'result': '参数不能为空！'}
#       {'code': 10002, 'result': '出现未知错误！'}
@server.route('/msg_sql', methods=['get', 'post'])
def msg_sql():
    if request.method == 'POST':
        kid= request.form.get("kid")
        operator = request.form.get("operator")
        url = request.form.get("ip")
        sq = request.form.get("sq")
        puk = request.form.get("puk")
        prk = request.form.get("prk")
        time_code=request.form.get("time_code")
    else:
        kid = request.args.get("kid")
        operator = request.args.get("operator")
        url = request.args.get("ip")
        sq = request.args.get("sq")
        puk = request.args.get("puk")
        prk = request.args.get("prk")
        time_code = request.args.get("time_code")

    try:
        if operator and kid:
            # print('1111111111111')
            result = msg_check.check_have(kid)
            # print('22222222222222')
            print(result)
            if result['code']==10000:
                return result
            #     return {'code':10000,'msg':'没有找个用户的记录'}
            if (operator == 'insert_msg'):
                if url and sq and puk and prk and time_code:
                    return msg_check.insert_msg(url, sq, puk, prk,time_code)
                else:
                    return {'code': 10001, 'result': '参数不能为空！'}

            elif (operator == 'deleteis_by_sq'):
                if url and sq:
                    return msg_check.deleteis_by_sq(url, sq)
                else:
                    return {'code': 10001, 'result': '参数不能为空！'}

            elif (operator == 'update_by_sq'):
                if url and sq and puk and prk and time_code:
                    return msg_check.update_by_sq(url, sq, puk, prk,time_code)
                else:
                    return {'code': 10001, 'result': '参数不能为空！'}

            elif (operator == 'search_by_sq'):
                if url and sq:
                    return msg_check.search_by_sq(url, sq)
                else:
                    return {'code': 10001, 'result': '参数不能为空！'}
            elif (operator == 'search_all'):
                if url:
                    return msg_check.search_all(url)
                else:
                    return {'code': 10001, 'result': '参数不能为空！'}
        else:
            resu = {'code': 10001, 'result': '参数不能为空！'}
            return resu
    except:
        resu = {'code': 10002, 'result': '出现未知错误！'}


# 函数功能：token表的增删改查
# 路径：/token_sql
# 输入：
#   kid = 执行操作的用户id
#   operator = 需要执行的操作[insert_token,dele_by_uid,update_by_uid,search_by_uid,search_all]
#               insert_token: 插入数据，参数[url,user_id,time_code,token]
#               dele_by_uid:删除数据，参数[url,user_id]
#               update_by_uid：更新数据，参数[url,user_id,time_code,token]
#               search_by_uid：查找数据，参数[url,user_id]
#               search_all:查询所有数据，参数[url]


# 返回：
#   成功：生成并返回token
#       {'code':200,'result':'操作成功'}
#       {'code':200,'result':result}
#   失败：
#       {'code':10000,'msg':'没有找到用户的记录'}
#       {'code': 10001, 'result': '参数不能为空！'}
#       {'code': 10002, 'result': '出现未知错误！'}
@server.route('/token_sql', methods=['get', 'post'])
def token_sql():
    if request.method == 'POST':
        kid =request.form.get("kid")
        operator=request.form.get("operator")
        url = request.form.get("ip")
        user_id = request.form.get("user_id")
        time_code = request.form.get("time_code")
        token =request.form.get("token")
    else:
        kid = request.args.get("kid")
        operator = request.args.get("operator")
        url = request.args.get("ip")
        user_id = request.args.get("user_id")
        time_code = request.args.get("time_code")
        token = request.args.get("token")

    print(operator)
    print(url)
    try:
        if operator and kid:
            result = token_api.check_have(kid)
            if result['code'] == 10000:
                return result
            if(operator=='insert_token'):
                if url and user_id and time_code and token:
                    return token_api.insert_token(url,user_id,time_code,token)
                else:
                    return  {'code': 10001, 'result': '参数不能为空！'}

            elif(operator=='dele_by_uid'):
                if url and user_id:
                    return token_api.dele_by_uid(url,user_id)
                else:
                    return {'code': 10001, 'result': '参数不能为空！'}

            elif (operator == 'update_by_uid'):
                if url and user_id and time_code and token:
                    return token_api.update_by_uid(url,user_id,time_code,token)
                else:
                    return  {'code': 10001, 'result': '参数不能为空！'}

            elif (operator == 'search_by_uid'):
                if url and user_id:
                    return token_api.search_by_uid(url,user_id)
                else:
                    return {'code': 10001, 'result': '参数不能为空！'}
            elif (operator == 'search_all'):

                if url :
                    return token_api.search_all(url)
                else:
                    return {'code': 10001, 'result': '参数不能为空！'}
        else:
            resu = {'code': 10001, 'result': '参数不能为空！'}
            return resu
    except:
        resu = {'code': 10002, 'result': '出现未知错误！'}


#函数功能：修改用户的消费参数，operator为[add_count,add_times,add_newdata，up_type]中的一个

#路径：/update_consume
#输入：
#   kid = 开发者kid
#   num_or_type = 你想要增加参数的值，或者修改type的字符串
#   operator = 你下要执行的操作，operator为[add_count,add_times,add_newdata，up_type]中的一个
#               其中 add_count:增加count的num_or_type的量
#                    add_times：增加times的num_or_type的量
#                    add_newdata：增加newdata的num_or_type的量，为当前时间+num_or_type
#                    up_type：通过num_or_type修改type的参数
#               其中count:开发者拥有的可用的ip数量
#                   free:开发者拥有的免费的调用次数，默认为1000
#                   times:开发者能够调用的次数（消费获取）
#                   newdata:当前能够使用的最晚期限（消费获取），时间戳表示
#                   type: #开发者目前消费的类型，为[free,times,newdata]中的一个
#                   通过num_or_type次数可以增加数量或者期限，也可以修改type
#
#返回：
#   成功：生成并返回token
#       resu = {'code': 200, 'result': '更新type成功！'}
#       return {'code': 200, 'result': '增加成功！'}
#
#   失败：
#       {'code':10000,'msg':'没有找个用户的记录'}
#       {'code': 10001, 'result': '参数不能为空！'}
#       {'code': 10002, 'result': '出现未知错误！'}
@server.route('/update_token_consume',methods=['get','post'])
def update_token_consume():
    if request.method == 'POST':
        kid=request.form.get("kid")
        num_or_type=request.form.get("num_or_type")
        operator =request.form.get("operator")
    else:
        kid=request.args.get("kid")
        num_or_type=request.args.get("num_or_type")
        operator =request.args.get("operator")
    try:
        if kid and num_or_type and operator:
            result=token_consume.check_have(kid)
            if result['code']==10000:
                return result
            #     return {'code':10000,'msg':'没有找个用户的记录'}
            #     return  {'code':200,'msg':'存在记录'}
            if operator=='up_type':
                token_consume.update_type(kid,num_or_type)
                return {'code': 200, 'result': '更新type成功！'}
            else:
                token_consume.update_num(kid,num_or_type,operator)
                return {'code': 200, 'result': '增加成功！'}
        else:
            resu = {'code': 10001, 'result': '参数不能为空！'}
            return resu
    except:
        resu = {'code': 10002, 'result': '出现未知错误！'}

#函数功能：查询消费数据信息
#路径：/token_consum_search
#输入：
#   kid= 开发者kid
#返回：
#   成功：生成并返回token
#
#       result:[{'kid':test,'count':0,'times':0,'free':100,'data':1515151515,'type':'free'}]
#   失败：
#       resu = {'code': 10001, 'result': '参数不能为空！'}
@server.route('/token_consum_search',methods=['get','post'])
def search_by_kid():
    if request.method == 'POST':
        kid=request.form.get("kid")
    else:
        kid=request.args.get("kid")

    if kid:
        result=token_consume.check_have(kid)
        if result['code']==10000:
            return result
        #     return {'code':10000,'msg':'没有找个用户的记录'}
        return {'code': 200, 'result': token_consume.search_kid_msg(kid)}
        #  result:[{'kid':test,'count':0,'times':0,'free':100,'data':1515151515,'type':'free'}]
    else:
        resu = {'code': 10001, 'result': '参数不能为空！'}
        return resu


@server.route('/update_msg_check_consume',methods=['get','post'])
def update_msg_check_consume():
    if request.method == 'POST':
        kid=request.form.get("kid")
        num_or_type=request.form.get("num_or_type")
        operator =request.form.get("operator")
    else:
        kid=request.args.get("kid")
        num_or_type=request.args.get("num_or_type")
        operator =request.args.get("operator")
    try:
        if kid and num_or_type and operator:
            # print('11111111111111111111')
            result=msg_consume.check_have(kid)
            # print('222222222222222222222222')
            if result['code']==10000:
                return result
            #     return {'code':10000,'msg':'没有找个用户的记录'}
            #     return  {'code':200,'msg':'存在记录'}
            if operator=='up_type':
                msg_consume.update_type(kid,num_or_type)
                return {'code': 200, 'result': '更新type成功！'}
            else:
                msg_consume.update_num(kid,num_or_type,operator)
                return {'code': 200, 'result': '增加成功！'}
        else:
            resu = {'code': 10001, 'result': '参数不能为空！'}
            return resu
    except:
        resu = {'code': 10002, 'result': '出现未知错误！'}

@server.route('/msg_check_consum_search',methods=['get','post'])
def msg_check_consum_search():
    if request.method == 'POST':
        kid=request.form.get("kid")
    else:
        kid=request.args.get("kid")

    if kid:
        result=msg_consume.check_have(kid)
        if result['code']==10000:
            return result
        #     return {'code':10000,'msg':'没有找个用户的记录'}
        return {'code': 200, 'result': msg_consume.search_kid_msg(kid)}
        #  result:[{'kid':test,'count':0,'times':0,'free':100,'data':1515151515,'type':'free'}]
    else:
        resu = {'code': 10001, 'result': '参数不能为空！'}
        return resu


@server.route('/test',methods=['get','post'])
def test():
    return 'good'

if __name__ == '__main__':
    #用于定时清理
    # token_api.timedTask()
    # test=1
    # print(token_api.search_token_by_id('2019', '127.0.0.1:8886'))
    # token_api.server_get_token('2019','127.0.0.1:8886')
    # print(test['token'])

    #token_api.create_mid_server_key('127.0.0.1:8886')
    #token_api.server_get_token('21111', '127.0.0.1:8886')

    #print(msg_check.create_seq(msg_check,'127.0.0.1:8886'))
    server.run(debug='true' , port=5000, host='0.0.0.0')  # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问
