#coding:utf_8
import os
import json
import requests
import hashlib
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Cryptodome.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from binascii import b2a_hex, a2b_hex
from Cryptodome.Cipher import AES
from Cryptodome import Random
import base64
from threading import Timer
from sql_operation import db_operation,token,server_operation,msg_operation
import time
from flask import request

import rsa
op=db_operation()
server=server_operation()
msg=msg_operation()
# class content:
#     def __init__(self):
#         self.server_plaintext=''
#         self.server_cyphertext=''
#         # self.front_plaintext = ''
#         # self.front_cyphertext = ''
class token_check:
    """MD5 base64 AES RSA 四种加密方法"""
    def __init__(self):
        # self.server_url='123'
        # self.cypher_text = ''
        # self.curr_dir = os.path.dirname(os.path.realpath(__file__))
        # self.server_private_key_file = os.path.join(self.curr_dir, "server_private_rsa_key.bin")
        # self.server_public_key_file = os.path.join(self.curr_dir, "server_rsa_public.pem")
        self.server_private_key=''
        self.server_public_key=''

    # def updatekey(self):
    # def init_url(self,url):
    #     op.init
    # 时间戳生成器
    def get_time(self):
        t = time.time()
        # print(t)  # 原始时间数据
        # print(int(t))  # 秒级时间戳
        # print(int(round(t * 1000)))  # 毫秒级时间戳
        print(int(round(t * 1000000)))  # 微秒级时间戳
        return int(round(t * 1000000))

    # 生成随机数，用于rsa参数生成
    def rsa_random_num(self):
        return str(self.get_time())

    # 中间人为后端提供的解密接口
    # def server_decode(self,Decrypts):
    #     data = request.get_data()
    #     data = data.decode('utf-8')
    #     data = json.loads(data)
    #     cypher_text = data['cypher_text']
    #     source_text=data['source']
    #     plain_text=Decrypts.rsa_decode('huctf',cypher_text,self.server_private_key_file)

    #获得user_id对应的token
    def search_token_by_id(self,user_id,url):
        op.init(url)
        print('___________aaa')
        result = op.search_by_user_id(user_id)
        if result!=[]:
            token=result['token']
            resu = {'code': 200, 'token': token,'msg':'查询成功'}
            return resu
        else:
            resu = {'code': 10000, 'msg':"token已更新，请重新登陆" }
            return resu

    #y用于数据加密
    # def server_encode(self, Encrypts,user_id):
    #     result=self.get_token_by_id(user_id)
    #     if result['code']==10000:
    #         resu = {'code': 10000, 'result': "token已更新，请重新登陆"}
    #         return resu
    #     elif result['code']==200:
    #         test=1

    #根据user_id请求一个token
    def server_get_token(self,user_id,url):
        op.init(url)
        if op.checkhave(user_id)==1:
            dict=op.search_by_user_id(user_id)
            token=dict['token']
            print('数据库已有记录')
            return {'code': 201, 'token': token,'msg':'数据库已有记录'}

        else:
            random_num = self.rsa_random_num()
            # print(random_num)
            # token由时间戳+user_id+'huctf'的明文加密而成，加密算法可以是其他非对称算法
            plain_text = random_num + user_id + 'huctf'
            cypher_text = Encrypts.md5_encrypt( plain_text)
            token =cypher_text
            op.insert(user_id,random_num,token)

            print('申请token成功')
            resu = {'code': 200, 'token': token,'msg':'申请token成功'}
            return resu

        # except:
        #     resu = {'code': 10001, 'msg': '未知错误。'}
        #     return resu

    # # 中间人为后端提供公钥的接口
    # def mid_server_transport_Key(self):
    #     pub_data = {
    #         'private_key': open(self.server_private_key_file).read(),
    #         'public_key': open(self.server_publiv_key_file).read(),
    #     }
    #     resu = pub_data
    #     return resu

    # 创建一组中间人与后端的密钥
    def create_mid_server_key(self,url):
        # print('0')
        if server.checkhave(url) == 1:
            print('已有记录。')
            resu = {'code': 200, 'msg': '已有记录。'}
            return resu
        else:
            token_tb='token_'+url
            msg_tb='msg_check_'+url
            # print('0')
            server.insert(url,token_tb,msg_tb)
            server.create_new_table(token_tb,msg_tb)
            print('初始化成功。')
            resu = {'code': 200, 'msg': '初始化成功。'}
            return resu

    #定时任务
    def timedTask(self):
        #每天更新一次
        Timer(5, self.task, ()).start()


    # 定时任务,定时更新密钥
    def task(self):
        #用于删除一天以上的密钥
        # op.delete_task()
        server.delete_task()


class msg_random_check:
    """MD5 base64 AES RSA 四种加密方法"""
    def __init__(self):
        self.private_key = ''
        self.public_key = ''
        self.sq=''

    # 时间戳生成器
    def get_time(self):
        t = time.time()
        # print(int(round(t * 1000000)))  # 微秒级时间戳
        return str(int(round(t * 1000000)))

    # 中间人为前端提供的加密接口
    def mid_front_encode(self,plain_text,sq,url):
        puk=self.mid_front_transport_pubKey(sq,url)
        if (puk['code'] == 200):
            puk = puk['puk']
            return {'code': 200, 'result': Encrypts.rsa_encode(puk,plain_text)}
        else:
            return {'code': 10000, 'msg': '未找到公钥'}

    #<script src="http://passport.cnblogs.com/scripts/jsencrypt.min.js"></script>
    #function encrypt(req_url,self_url,data){
    #       $.ajax({
    #            url:req_url,
    #            type:'post',


    #中间人为后端提供的解密接口
    def mid_sever_decode(self,cypher,sq,url):
        prk=self.mid_server_transport_priKey(self,sq,url)
        # print('---------------------------2')
        if(prk['code']==200):
            prk=prk['prk']
            return {'code': 200, 'result': Decrypts.rsa_decrypt(Decrypts, cypher, prk)}
        else:
            return {'code': 10000, 'msg': '解密失败'}

       # else:
         #   return {'code':10000,'msg':'未找到私钥'}

    def check_sq(self,url,sq):
        return msg.checkhave(sq)

    # 中间人为前端提供公钥的接口
    def mid_front_transport_pubKey(self,sq,url):
        msg.init(url)
        result=msg.search_by_sq(sq)
        # print(result)
        if result!=[]:
            return {'code': 200, 'puk': result['puk']}
        else:
            result={'code':10000,'msg':'没有这个序列号'}
            return result

    #中间人为后端提供私钥的接口
    def mid_server_transport_priKey(self,sq,url):
        # print(sq)
        msg.init(url)
        #if self.check_sq(self,sq,url) !=1:
        # print("hghhhhhhhhhhhhhhhghg")
        result=msg.search_by_sq(sq)
        # print(result)
        # print('----------------------------')
        # exit()
        if result!=[]:
            prk=result['prk']
            print(prk)
            msg.deleteis_by_sq(sq)
            return {'code':200,'prk':prk}
        else:
           result={'code':10000,'msg':'未找到私钥'}
           return result
    #else:
      #  result = {'code': 10001, 'msg': '没有这个序列号'}
       # return  result

    #中间人为自己提供私钥的接口
    def mid_server_transport_priKey2(self,sq,url):
        # print(sq)
        msg.init(url)
        #if self.check_sq(self,sq,url) !=1:
        result=msg.search_by_sq(sq)
        #print('\n\n\n\n\n\n',result)
        if result!=[]:
            prk=result['prk']
            return{'code':200,'prk':prk}
        else:
           result={'code':10000,'msg':'未找到私钥'}
           return result
    #else:
      #  result = {'code': 10001, 'msg': '没有这个序列号'}
       # return  result


    #用于生成序列号并且生成相应的rsa key，插入数据库中
    def create_seq(self,url):
        time_code=self.get_time(self)
        strr=time_code+'huctf'
        sq=Encrypts.md5_encrypt(strr)
        self.sq=sq
        return self.create_key(self,str(sq),url,time_code)

    # 创建一组密钥
    def create_key(self,sq,url,time_code):
        # print('0')
        msg.init(url)
        if server.checkhave(sq) == 1:
            print('已有记录。')
            resu = {'code': 200,'sq':sq,'puk':self.public_key, 'msg': '数据已创建。'}
            return resu
        else:
            # print('2')
            self.public_key,self.private_key=Encrypts.generate_rsa_keys(Encrypts)

            # print('0')
            msg.insert(sq,self.public_key,self.private_key,time_code)
            print('数据创建成功。')
            resu = {"code": 200,"sq":str(sq),"puk":str(self.public_key)[2:-1], "msg": "数据创建成功。"}
            return resu

    # 用于删除失效密钥
    def delete_key(self,url,sq):
        msg.init(url)
        msg.deleteis_by_sq(sq)


class Encrypts:
    """MD5 base64 AES RSA 四种加密方法"""
    def __init__(self):
        self.aes_mode = AES.MODE_ECB  # AES加密模式
        self.aes_key_size = 256  # AES秘钥，随机数值
        self.rsa_count = 1024  # RSA秘钥对，随机数值

    def md5_encrypt(plaintext):
        """ MD5加密
        :param plaintext: 需要加密的内容
        :return: encrypt_str密文
        """
        h1 = hashlib.md5()  # 创建md5对象
        h1.update(plaintext.encode(encoding='utf-8'))  # 必须声明encode
        # 加密
        encrypt_str = h1.hexdigest()
        return encrypt_str

    def base64_encry(plaintext):
        """base64加密"""
        base64_encry = base64.b64encode(plaintext.encode('utf-8'))
        return base64_encry

    def generate_aes_key(self):
        """AES秘钥生成"""
        # length for urandom
        key_size = self.aes_key_size
        u_len = int(key_size / 8 / 4 * 3)
        aes_key = base64.b64encode(os.urandom(u_len))  # os.urandom()生成随机字符串
        return aes_key

    def aes_encrypt(self, message, aes_key):
        """use AES to encrypt message,
        :param message: 需要加密的内容
        :param aes_key: 密钥
        :return: encrypted_message密文
        """
        mode = self.aes_mode  # 加密模式
        if type(message) == str:
            message = bytes(message, 'utf-8')
        if type(aes_key) == str:
            aes_key = bytes(aes_key, 'utf-8')
        # aes_key, message必须为16的倍数
        while len(aes_key) % 16 != 0:
            aes_key += b' '

        while len(message) % 16 != 0:
            message += b' '
        # 加密对象aes
        aes = AES.new(key=aes_key, mode=mode)
        encrypt_message = aes.encrypt(plaintext=message)
        return b2a_hex(encrypt_message)

    def generate_rsa_keys(self):
        """RSA秘钥对生成"""
        rsa_count = 1024
        # 随机数生成器
        random_generator = Random.new().read
        # rsa算法生成实例
        rsa = RSA.generate(rsa_count, random_generator)
        # master的秘钥对的生成
        rsa_public_key = rsa.publickey().exportKey()
        rsa_private_key = rsa.exportKey()
        # with open(private_key, "wb") as f:
        #     f.write(rsa_public_key)
        # with open(public_key, "wb") as f:
        #     f.write(rsa_private_key)
        return rsa_public_key, rsa_private_key

    def rsa_encrypt(self,message, rsa_public_key):
        """use RSA to encrypt message,
        :param message: 需要加密的内容
        :param rsa_public_key: 公钥(字节类型）
        :return: encrypt_msg_list密文列表
        """
        pub_key = RSA.importKey(rsa_public_key)
        # 加密对象
        cipher = Cipher_pkcs1_v1_5.new(pub_key)
        msg = message.encode('utf-8')
        # 分段加密
        # default_encrypt_length = 245
        # length = default_encrypt_length
        # msg_list = [msg[i:i + length] for i in list(range(0, len(msg), length))]
        # 加密后信息列表
        # encrypt_msg_list = []
        # for msg_str in msg_list:
        cipher_text = base64.b64encode(cipher.encrypt(message=msg))
            # encrypt_msg_list.append(cipher_text)
        return cipher_text

    def create_rsa_key(self, private_key='server_private_rsa_key.bin', public_key='server_rsa_public.pem'):
        key = RSA.generate(1024)
        encrypted_key = key.exportKey(passphrase='179', pkcs=8, protection="scryptAndAES128-CBC")
        # print(public_key)
        with open(private_key, "wb") as f:
            f.write(encrypted_key)
        with open(public_key, "wb") as f:
            f.write(key.publickey().exportKey())

    def rsa_encode(self,public_key_file,plaintext):
        # 加载公钥
        plaintext=plaintext.encode(encoding='utf-8')
        recipient_key = RSA.import_key(
            open(public_key_file).read()
        )
        cipher_rsa = PKCS1_v1_5.new(recipient_key)

        en_data = cipher_rsa.encrypt(plaintext)
        # print(len(en_data), en_data)
        return en_data

class Decrypts:
    """base64 AES RSA 三种解密方法"""

    def __init__(self):
        # AES解密模式(须与加密模式一致）
        self.aes_mode = AES.MODE_ECB

    def base64_decry(ciphertext):
        """base64解密"""
        base64_decry = (base64.b64decode(ciphertext)).decode('utf-8')
        return base64_decry

    def aes_decrypt(self, encrypt_message, aes_key):
        """ AES解密
        :param encrypt_message: 密文
        :param aes_key: 秘钥
        :return: decrypt_text解密后内容
        """
        aes_mode = self.aes_mode
        aes = AES.new(key=aes_key, mode=aes_mode)
        decrypted_text = aes.decrypt(a2b_hex(encrypt_message))
        decrypted_text = decrypted_text.rstrip()  # 去空格
        return decrypted_text.decode()

    def rsa_decrypt1(self,cypher, rsa_private_key):  # 用私钥解密
        # with open('private.pem', 'rb') as privatefile:
        #     p = privatefile.read()
        privkey = rsa.PrivateKey.load_pkcs1(rsa_private_key)
        lase_text = rsa.decrypt(cypher, privkey).decode()  # 注意，这里如果结果是bytes类型，就需要进行decode()转化为str
        # print(lase_text)
        exit()

    def rsa_decrypt(self,cypher, rsa_private_key):
        """ RSA解密
        :param encrypt_msg_list: 密文列表
        :param rsa_private_key: 私钥(字节类型)
        :return  解密后内容
        """
        random_generator = Random.new().read
        pri_key = RSA.importKey(rsa_private_key)
        cipher = Cipher_pkcs1_v1_5.new(pri_key)
        # 解密后信息列表
        cypher=cypher.encode('gbk')
        msg_str = base64.decodebytes(cypher)
        de_str = cipher.decrypt(msg_str, random_generator)
        return  de_str.decode('utf-8')
        # msg_list = []
        # for msg_str in encrypt_msg_list:
        #     msg_str = base64.decodebytes(msg_str)
        #     de_str = cipher.decrypt(msg_str, random_generator)
        #     msg_list.append(de_str.decode('utf-8'))
        # return ''.join(msg_list)

    def rsa_decode(self,password='huctf',en_data=b'',private_key_file=''):
        # 读取密钥
        # en_data=en_data.decode("ISO-8859-1", 'ignore')
        private_key = RSA.import_key(
            open(private_key_file).read(),
            passphrase=password
        )
        cipher_rsa = PKCS1_v1_5.new(private_key)
        data = cipher_rsa.decrypt(en_data, None)

        print(data)
        return data
if __name__=='__main__':
    # print(op.init('127.0.0.1:8886'))
    sev=token_check()
    sev.create_mid_server_key('127.0.0.1:8886')
    sev.server_get_token('2019','127.0.0.1:8886')
    # sv = server_operation()
    # sv.search_all()
