#coding:utf-8
import json
import base64
import requests
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Cryptodome.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Cryptodome.PublicKey import RSA
from binascii import b2a_hex, a2b_hex
from Cryptodome.Cipher import AES
from Cryptodome import Random
#import RSA
#data={
#    'password':'123456',
#    'user_id':'123456'
#}
#print(requests.post(url="http://www.hutc.xyz:8884/login_check",data=data).text)
puk=''#当前公钥
operator='search_all'
prk='57687'
sq=''#当前公钥序列号
kid='1'
uid='adasd5xc89aaaa+9d8a+9d'
ip='1.1.1.1'
user_id='Luz'
token=''#当前token
text='1234'
cipher_text=''
public_key = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC2GdFVfnjmqWNfN3m2Hml4pMcm
o66ltA2NHiG0DWuEs2XWVaNL8dAc6/Z/qA2nBXfKg/W/nEzJr6bbSm3oxlGm+AOA
Ennra+YPnS1ocoMbXwM1JUwjH5GbO93xfSDBGvOUE7c30zVkRkasN0vzG0WnoSTR
ErSrz0laLtVq1a980wIDAQAB
-----END PUBLIC KEY-----
'''
cipher_decode=''
def menu():
    print('\n\n\n')
    print('*'*30)
    print('-'*10+'当前状态'+'-'*10)
    print('当前公钥：',puk)
    print('当前kid',kid)
    print('当前操作：',operator)
    print('当前公钥序列号：',sq)
    print('当前ip：',ip)
    print('当前用户：',user_id)
    print('当前token：',token)
    print('当前原始信息：',text)
    print('当前密文：',cipher_text)
    print('解密密文：',cipher_decode)
    print('-'*10+'操作选项'+'-'*10)
    print('0.init')
    print('1.修改ip')
    print('2.修改用户')
    print('3.获取公钥和序列号')
    print('4.获取token')
    print('5.验证token')
    print('6.修改原始信息')
    print('7.加密原始信息')
    print('8.解密密文')
    print('9.msg_check表的增删改查')
    print('10.token表的增删改查')
    print('11.更新token表kid的消费参数')
    print('12.查询token表kid消费数据信息')
    print('13.更新msg_check的消费数据')
    print('14.查询msg_check表kid的消费数据信息')
    print('15.输入新的数据库操作')
    print('*'*30)

    
def init_ip():
    data={
    'kid':kid,
    'ip':ip
    }
    print(requests.post(url="http://127.0.0.1:5000/init_ip",data=data).text)

def get_puk_sq():
    data={
    'ip':ip
    }
    result=requests.post(url="http://127.0.0.1:5000/get_puk_sq",data=data)
    print(result.text.replace('\'','\"'))
    #result.text.replace('\\n','')
    result=json.loads(result.text.replace('\'','\"'))
    puk=str(result['puk'])
    puk=puk.replace("\\n", "")[26:-24]
    start = '-----BEGIN RSA PRIVATE KEY-----\n'
    end = '-----END RSA PRIVATE KEY-----'
    length = len(puk)
    divide = 64  # 切片长度
    offset = 0  # 拼接长度
    result0=''
    while length - offset > 0:
        if length - offset > divide:
            result0 += puk[offset:offset + divide] + '\n'
        else:
            result0 += puk[offset:] + '\n'
        offset += divide
    result0 = start + result0 + end
    puk=result0
    sq=result['sq']
    print('puk:',puk,'\nsq:',sq)
    return puk,sq
    
def init_token():
    data={
    'ip':ip,
    'user_id':user_id
    }
    result=requests.post(url="http://127.0.0.1:5000/init_token",data=data)
    result=json.loads(result.text)
    token=result['token']
    return token

def check_token():
    data={
    'ip':ip,
    'user_id':user_id,
    'token':token
    }
    result=requests.post(url="http://127.0.0.1:5000/check_token",data=data)
    result=json.loads(result.text)
    print(result)

def rsa_encrypt():
    # 加密对象
    #print(text)
    rsakey=RSA.importKey(puk)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    # 分段加密
    # default_encrypt_length = 245
    # length = default_encrypt_length
    # msg_list = [msg[i:i + length] for i in list(range(0, len(msg), length))]
    # 加密后信息列表
    # encrypt_msg_list = []
    # for msg_str in msg_list:
    cipher_text = base64.b64encode(cipher.encrypt(text.encode('utf-8'))).decode('utf-8')
    return cipher_text
    # encrypt_msg_list.append(ciph

def decrypt():
    data={
    'ip':ip,
    'sq':sq,
    'cypher':cipher_text
    }
    result=requests.post(url="http://127.0.0.1:5000/server_decode",data=data)
    result=json.loads(result.text)
    print(result)

def msg_sql():
    data={
    'kid':kid,
    'operator':operator,
    'ip':ip,
    'sq':sq,
    'puk':puk,
    'prk':prk,
    'time_code':'157789422313221'
    }
    result=requests.post(url="http://127.0.0.1:5000/msg_sql",data=data)
    result=json.loads(result.text)
    print(result)

def token_sql():
    data={
    'kid':kid,
    'ip':ip,
    'operator': operator,
    'user_id':user_id,
    'time_code':'123456489',
    'token':token,
    }
    result=requests.post(url="http://127.0.0.1:5000/token_sql",data=data)
    result=json.loads(result.text)
    print(result)

def update_token_consume():
    data={
    'kid':kid,
    'num_or_type':100,
    'operator':'add_times',
    }
    result=requests.post(url="http://127.0.0.1:5000/update_token_consume",data=data)
    result=json.loads(result.text)
    print(result)

def token_consum_search():
    data={
    'kid':kid,
    }
    result=requests.post(url="http://127.0.0.1:5000/token_consum_search",data=data)
    result=json.loads(result.text)
    print(result)

def update_msg_check_consume():
    data={
    'kid':kid,
    'num_or_type':100,
    'operator':'add_times',
    }
    result=requests.post(url="http://127.0.0.1:5000/update_msg_check_consume",data=data)
    result=json.loads(result.text)
    print(result)

def msg_check_consum_search():
    data={
    'kid':kid,
    }
    result=requests.post(url="http://127.0.0.1:5000/msg_check_consum_search",data=data)
    result=json.loads(result.text)
    print(result)

while(1):
    # init_ip()
    menu()

    choose=input("请输入操作选项：")
    #print(choose)
    if choose=='0':
        init_ip()
    elif(choose=='1'):
        #print(1)
        ip=input("请输入新的ip：")
    elif(choose=='2'):
        user_id=input("请输入新的user_id：")
    elif(choose=='3'):
        puk,sq=get_puk_sq()
    elif(choose=='4'):
        token=init_token()
    elif(choose=='5'):
        check_token()
    elif(choose=='6'):
        text=input("请输入新的原始信息：")
    elif(choose=='7'):
        cipher_text=rsa_encrypt()
    elif(choose=='8'):
        decrypt()
    elif (choose == '9'):
        msg_sql()
    elif (choose == '10'):
        token_sql()
    elif (choose == '11'):
        update_token_consume()
    elif (choose == '12'):
        token_consum_search()
    elif (choose == '13'):
        update_msg_check_consume()
    elif (choose == '14'):
        msg_check_consum_search()
    elif (choose == '15'):
        operator = input("请输入新的数据库操作：")
#token=init_token()
#print(check_token(token,'1.1.1.1','Luz'))

