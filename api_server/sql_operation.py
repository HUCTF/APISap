# from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from sqlalchemy.orm import mapper
from sqlalchemy import Table,MetaData
metadata = MetaData()
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://123456:123456@localhost:3306/token1'  # 这里登陆的是root用户，要填上自己的密码，MySQL的默认端口是3306，填上之前创建的数据库名text1
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 设置这一项是每次请求结束后都会自动提交数据库中的变动

db = SQLAlchemy(app)  # 实例化
tablename=''
import time


class token1(db.Model):
    __tablename__ = 'token_1'
    user_id = db.Column(db.String(255), unique=True,primary_key=True,nullable=False)
    time_code = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255), nullable=False)

    # @orm.reconstructor
    # def __init__(self):
    #     self.api_name = ["id", "nickname", "mobile", "email"]
    def init(self,url):
        # id = db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True
        # try:
        # items = db.session.execute("select table_nm from server WHERE url=%s "%(url))
        results = server.query.filter_by(url=url).all()
        # print(results)
        resData = []
        for x in results:
            resData.append({
                'table_nm': x.table_nm,
            })
        # print(resData)
        if resData!=[]:
            # print(items[0][0])
            __tablename__ = resData[0]['table_nm']
            tablename=self.__tablename__
            print(self.__tablename__)
            print('找表成功')
            return tablename
            # return {'code':200,'msg':'找表成功'}
        else:
            print('没找到表')
            return {'code':10000,'msg':'没有找到表'}
        # except:
        #     print('地址格式错误')
        #     return {'code': 10001, 'msg': '地址格式错误'}
        # self.__tablename__=
#server表
class server(db.Model):
    __tablename__ = 'server'
    # id = db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True)
    url = db.Column(db.String(255), unique=True,primary_key=True,nullable=False)
    pub_key = db.Column(db.String(255), nullable=False)
    private_key = db.Column(db.String(255), nullable=False)
    table_nm= db.Column(db.String(255), nullable=False)


token=token1()
#token表的操作
class db_operation:
    def __init__(self):
        self.token=''
    # 增
    # token = token1()
    # token.init('123')
    def __init__(self):
        self.url=''
    def init(self,url):
        # print(url)
        token1.init(token1,url)
        self.token=token1()
        print(self.token.__tablename__)
        print("--------------")
        # token=token1()
        # print(url)

    def insert(self,user_id,time_code,token):
        db.session.add(token(user_id=user_id,time_code=time_code,token=token))
        db.session.commit()
        print('单个数据添加成功')

    def createMany(self,list):
        # users=[Role(name="lisi"),Role(name="wangwu"),Role(name="zhaosi")]
        db.session.add_all(list)
        db.session.commit()
        print('多个数据添加成功')

    # 删
    def deleteis(self,user_id):
        results = self.token.query.filter_by(user_id=user_id).all()
        db.session.delete(results)
        db.session.commit()
        print('数据删除成功')

    #删除已经过时的密钥
    def delete_task(self):
        now=self.get_time()/1000000-86400
        items=db.session.execute("delete  from token  where (time_code+0)/1000000<'%d'"%(now))
        items=list(items)
        print(items)
        # db.session.execute("delete from user where id=1 ")


    # # 改
    def update(self,uer_id,time_code,token):
        results = token.query.filter_by(user_id=uer_id).all()
        # print(results[0].title)
        results[0].time_code = time_code
        results[0].token=token
        db.session.commit()
        print('修改成功')


    #
    # # 查
    def search_by_user_id(self,user_id):
        results = self.token.query.filter_by(user_id=user_id).all()
        # print(results)
        resData = []
        for x in results:
            resData.append({
                'user_id': x.user_id,
                'time_code': x.time_code,
                'token':x.token,
            })
        # print(resData)
        if resData!=[]:
            return resData[0]
        else:
            return resData

    def search_by_time_code(self,time_code):
        results = token.query.filter_by(time_code=time_code).all()
        # print(results)
        resData = []
        for x in results:
            resData.append({
                'user_id': x.user_id,
                'time_code': x.time_code,
                'token':x.token,
            })
        # print(resData)
        if resData!=[]:
            return resData[0]
        else:
            return resData


    def search_by_token(self,token):
        results = self.token.query.filter_by(token=token).all()
        # print(results)
        resData = []
        for x in results:
            resData.append({
                'user_id': x.user_id,
                'time_code': x.time_code,
                'token':x.token,
            })
        # print(resData)
        if resData!=[]:
            return resData[0]
        else:
            return resData

    #获取所有数据
    def search_all(self):
        dict = token.query.all()
        for each in dict:
            # print(each)
            print(each.user_id + '|' + each.time_code + '|' + each.token)
        return dict

    def checkhave(self,user_id):
        print(self.token.__tablename__)
        results = self.token.query.filter_by(user_id=user_id).all()
        print(results[0].token)
        print(12345)
        if results ==[]:
            print(0)
            return 0
        else:
            print(1)
            return 1

    def get_time(self):
        t = time.time()
        # print(t)  # 原始时间数据
        # print(int(t))  # 秒级时间戳
        # print(int(round(t * 1000)))  # 毫秒级时间戳
        print(int(round(t * 1000000)))  # 微秒级时间戳
        return int(round(t * 1000000))/1000000

# server表的操作
class server_operation:
    # 增

    def __init__(self):
        self.url = ''
    def insert(self, url, pub_key, private_key,table_nm):
        # print(url)
        db.session.add(server(url=url,pub_key=pub_key, private_key=private_key,table_nm=table_nm))
        db.session.commit()
        print('单个数据添加成功')

    def createMany(self, list):
        # users=[Role(name="lisi"),Role(name="wangwu"),Role(name="zhaosi")]
        db.session.add_all(list)
        db.session.commit()
        print('多个数据添加成功')

    # 删
    def deleteis(self, url):
        results = server.query.filter_by(url=url).all()
        db.session.delete(results)
        db.session.commit()
        print('数据删除成功')

    # 删除已经过时的密钥
    # def delete_task(self):
    #     now = self.get_time() / 1000000 - 86400
    #     items = db.session.execute("delete  from server  where (time_code+0)/1000000<'%d'" % (now))
    #     items = list(items)
    #     print(items)
        # db.session.execute("delete from user where id=1 ")

    # # 改
    def update(self,  url, pub_key, private_key,table_nm):
        results = server.query.filter_by(url=url).all()
        # print(results[0].title)
        results[0].pub_key = pub_key
        results[0].private_key = private_key
        results[0].table_nm=table_nm
        db.session.commit()
        print('修改成功')

    #
    # # 查
    def search_by_url(self,  url):
        results = server.query.filter_by(url=url).all()
        # print(results)
        resData = []
        for x in results:
            resData.append({
                'url': x.url,
                'pub_key': x.pub_key,
                'private_key': x.private_key,
                'table_nm':x.table_nm,
            })
        # print(resData)
        if resData != []:
            return resData[0]
        else:
            return resData

    def search_by_table_nm(self, table_nm):
        results = server.query.filter_by(table_nm=table_nm).all()
        # print(results)
        resData = []
        for x in results:
            resData.append({
                'url': x.url,
                'pub_key': x.pub_key,
                'private_key': x.private_key,
                'table_nm': x.table_nm,
            })
        # print(resData)
        if resData != []:
            return resData[0]
        else:
            return resData

    # 获取所有数据
    def search_all(self):
        dict = server.query.all()
        # print('good')
        for each in dict:
            # print(each)
            print(each.url + '|' + each.pub_key + '|' + each.private_key+'|'+each.table_nm)
        return dict

    def checkhave(self, url):
        # print('goddddddd' + url)
        # url='123'
        results = server.query.filter_by(url=url).all()
        # print('adas')
        if results == []:
            return 0
        else:
            return 1

    def create_new_token_table(self,table_nm):
        str="CREATE TABLE `"+table_nm+"` "+\
            "(`user_id` varchar(255) CHARACTER SET utf8 NOT NULL,"+\
            "`time_code` varchar(255) CHARACTER SET utf8 NOT NULL,"+\
            "`token` varchar(255) CHARACTER SET utf8 NOT NULL,"+\
            "PRIMARY KEY (`user_id`) USING BTREE)"+\
            " ENGINE=InnoDB DEFAULT CHARSET=latin1;"
        db.session.execute(str)
        print('建表成功')

if __name__ == "__main__":

    # print(resData)
    op = db_operation()
    op.init('127.0.0.1:8886')

    # op.search_all()
    # sv = server_operation()
    # sv.search_by_url('127.0.0.1:8886')
    # sv.insert('123456','sadada','asdasdasd','token_2')
    # sv.search_all()
    # se=server_operation()
    # se.create_new_token_table('table_2')
    # op.update_task()
    # a=token()
    # a.init('123')
    # print(op.search_by_user_id('2019'))
    # print(op.get_time())
    # op.search_all()
    # print(op.checkhave(123))
    # dict = token.query.all()
    # for each in dict:
    #     # print(each)
    #     print(each.user_id + '|' + each.time_code + '|' + each.token)
    # op = db_operation()
    # op.search_all()
    # dict=token.query.all()
    # for each in dict :
    #     # print(each)
    #     print(each.source_text+'|'+each.time_code+'|'+each.token)

