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
from sql_operation import db_operation,token,server_operation
import time
from flask import request

op=db_operation()
server=server_operation()
# class content:
#     def __init__(self):
#         self.server_plaintext=''
#         self.server_cyphertext=''
#         # self.front_plaintext = ''
#         # self.front_cyphertext = ''
class mid_server:
    """MD5 base64 AES RSA 四种加密方法"""
    def __init__(self):
        self.server_url='123'
        # self.cypher_text = ''
        self.curr_dir = os.path.dirname(os.path.realpath(__file__))
        self.server_private_key_file = os.path.join(self.curr_dir, "server_private_rsa_key.bin")
        self.server_public_key_file = os.path.join(self.curr_dir, "server_rsa_public.pem")
        op.init(self.server_url)
    # def updatekey(self):

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
    def server_decode(self,Decrypts):
        data = request.get_data()
        data = data.decode('utf-8')
        data = json.loads(data)
        cypher_text = data['cypher_text']
        source_text=data['source']
        plain_text=Decrypts.rsa_decode('huctf',cypher_text,self.server_private_key_file)

    #获得user_id对应的token
    def search_token_by_id(self,user_id,url):
        op.init(url)
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
        print('good')
        try:
            if op.checkhave(user_id)==1:
                dict=op.search_by_user_id(user_id)
                token=dict['token']
                print('数据库已有记录')
                return {'code': 201, 'token': token,'msg':'数据库已有记录'}
            if  user_id!='':
                print(url)
                random_num=self.rsa_random_num()
                #token由时间戳+user_id+'huctf'的明文加密而成，加密算法可以是其他非对称算法
                plain_text = random_num + user_id + 'huctf'
                cypher_text = Encrypts.rsa_encode(self.public_key_file, plain_text)
                token=cypher_text
                if op.checkhave(user_id)==0:
                    op.insert(user_id,random_num,token)
                else:
                    op.update(user_id,random_num,token)
                print('申请token成功')
                resu = {'code': 200, 'token': token,'msg':'申请token成功'}
                return resu
            else:
                print('参数不能为空！')
                resu = {'code': 10000, 'msg': '参数不能为空！'}
                return resu
        except:
            resu = {'code': 10001, 'msg': '未知错误。'}
            return resu

    # 中间人为后端提供公钥的接口
    def mid_server_transport_Key(self):
        pub_data = {
            'private_key': open(self.server_private_key_file).read(),
            'public_key': open(self.server_publiv_key_file).read(),
        }
        resu = pub_data
        return resu

    # 创建一组中间人与后端的密钥
    def create_mid_server_key(self,url):
        # print('0')
        if server.checkhave(url) == 1:
            print('已有记录。')
            resu = {'code': 200, 'msg': '已有记录。'}
            return resu
        else:
            # print('2')
            print(self.server_public_key_file)
            Encrypts.create_rsa_key(self.server_private_key_file ,self.server_public_key_file)
            pub_key = ''
            pri_key = ''
            # print('1')
            with open(self.server_private_key_file) as file_obj:
                pub_key = file_obj.read()
            with open(self.server_public_key_file) as file_obj:
                pri_key = file_obj.read()
            table_nm='token_'+url
            # print('0')
            server.insert(url,pub_key,pri_key,table_nm)
            server.create_new_token_table(table_nm)
            print('初始化成功。')
            resu = {'code': 200, 'msg': '初始化成功。'}
            return resu




    #定时任务
    def timedTask(self):
        #每天更新一次
        Timer(86400, self.create_mid_server_key, ()).start()

    # 定时任务,定时更新密钥
    def task(self,Encrypts):
        #用于删除一天以上的密钥
        op.delete_task()

    def transport_msg(self):
        r = requests.post(self.server_url, self.cypher_text)


# class mid_front:
#     """MD5 base64 AES RSA 四种加密方法"""
#     def __init__(self):
#         # self.front_url=''
#         self.curr_dir = os.path.dirname(os.path.realpath(__file__))
#         self.front_private_key_file = os.path.join(self.curr_dir, "front_private_rsa_key.bin")
#         self.front_public_key_file = os.path.join(self.curr_dir, "front_rsa_public.pem")
#
#     # 中间人为前端提供的加密接口
#     def front_encode(self,plain_text,Encrypts):
#         return Encrypts.rsa_encode(self,self.public_key_file,plain_text)
#
#     # 中间人为前端提供公钥的接口
#     def mid_front_transport_pubKey(self):
#         return open(self.front_public_key_file).read()
#
#     # 创建一组中间人与前端的密钥
#     def create_mid_server_key(self,Encrypts):
#         Encrypts.create_rsa_key("huctf", self.front_private_key_file, self.front_public_key_file)


class Encrypts:
    """MD5 base64 AES RSA 四种加密方法"""
    def __init__(self):
        self.aes_mode = AES.MODE_ECB  # AES加密模式
        self.aes_key_size = 256  # AES秘钥，随机数值
        self.rsa_count = 2048  # RSA秘钥对，随机数值

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
        rsa_count = self.rsa_count
        # 随机数生成器
        random_generator = Random.new().read
        # rsa算法生成实例
        rsa = RSA.generate(rsa_count, random_generator)
        # master的秘钥对的生成
        rsa_public_key = rsa.publickey().exportKey()
        rsa_private_key = rsa.exportKey()
        return rsa_public_key, rsa_private_key

    def rsa_encrypt(message, rsa_public_key):
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
        default_encrypt_length = 245
        length = default_encrypt_length
        msg_list = [msg[i:i + length] for i in list(range(0, len(msg), length))]
        # 加密后信息列表
        encrypt_msg_list = []
        for msg_str in msg_list:
            cipher_text = base64.b64encode(cipher.encrypt(message=msg_str))
            encrypt_msg_list.append(cipher_text)
        return encrypt_msg_list

    def create_rsa_key(self, private_key='server_private_rsa_key.bin', public_key='server_rsa_public.pem'):
        key = RSA.generate(2048)
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
        print(len(en_data), en_data)
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

    def rsa_decrypt(encrypt_msg_list, rsa_private_key):
        """ RSA解密
        :param encrypt_msg_list: 密文列表
        :param rsa_private_key: 私钥(字节类型)
        :return  解密后内容
        """
        random_generator = Random.new().read
        pri_key = RSA.importKey(rsa_private_key)
        cipher = Cipher_pkcs1_v1_5.new(pri_key)
        # 解密后信息列表
        msg_list = []
        for msg_str in encrypt_msg_list:
            msg_str = base64.decodebytes(msg_str)
            de_str = cipher.decrypt(msg_str, random_generator)
            msg_list.append(de_str.decode('utf-8'))
        return ''.join(msg_list)

    def rsa_decode(self,password='huctf',en_data=b'',private_key_file=''):
        # 读取密钥
        private_key = RSA.import_key(
            open(private_key_file).read(),
            passphrase=password
        )
        cipher_rsa = PKCS1_v1_5.new(private_key)
        data = cipher_rsa.decrypt(en_data, None)

        print(data)
        return data
if __name__=='__main__':
    sv = server_operation()
    sv.search_all()
