# from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from sqlalchemy.orm import mapper
from sqlalchemy import Table,MetaData
import time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
app=Flask(__name__)
engine = create_engine('mysql://123456:123456@localhost:3306/token1?charset=utf8', echo=True)
Session = sessionmaker(bind=engine)

session = Session()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://123456:123456@localhost:3306/token1'  # 这里登陆的是root用户，要填上自己的密码，MySQL的默认端口是3306，填上之前创建的数据库名text1
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 设置这一项是每次请求结束后都会自动提交数据库中的变动
#
# db = SQLAlchemy(app)  # 实例化
tablename=''

#msg_check_count表，用于记录
class msg_check_count(Base):
    __tablename__ = 'msg_check_count'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    kid = Column(String(255), unique=True, primary_key=True, nullable=False)
    count = Column(int(10), nullable=False,default=0)
    times = Column(int(10), nullable=False,default=0)
    free = Column(int(10), nullable=False,default=1000)
    data=Column(int(15), nullable=False,default=0)
    type=Column(String(255), nullable=False)

#token_count表，用于记录
class token_count(Base):
    __tablename__ = 'token_count'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    kid = Column(String(255), unique=True, primary_key=True, nullable=False)
    count = Column(int(10), nullable=False,default=0)
    times = Column(int(10), nullable=False,default=0)
    free = Column(int(10), nullable=False,default=1000)
    data=Column(int(15), nullable=False,default=0)
    type=Column(String(255), nullable=False)

#token表
class token(Base):
    __tablename__ = 'token_1'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    user_id = Column(String(255), unique=True,primary_key=True,nullable=False)
    time_code = Column(String(255), nullable=False)
    token = Column(String(500), nullable=False)

    # @orm.reconstructor
    # def __init__(self):
    #     self.api_name = ["id", "nickname", "mobile", "email"]
    def init(self,url):
        # id = Column(Integer, primary_key=True,unique=True,autoincrement=True
        # try:
        # items = session.execute("select table_nm from server WHERE url=%s "%(url))
        results = session.query(server).filter_by(url=url).all()
        # print(results)
        resData = []
        for x in results:
            resData.append({
                'token_tb': x.token_tb,
            })
        # print(resData)
        if resData!=[]:
            # print(items[0][0])
            self.__table__.name = resData[0]['token_tb']
            # __init__(app)
            tablename=self.__table__.name
            # print(tablename)
            print('找表成功')
            # return tablename
            return {'code':200,'table_name':tablename,'msg':'找表成功'}
        else:
            print('没找到表')
            return {'code':10000,'msg':'没有找到表'}
        # except:
        #     print('地址格式错误')
        #     return {'code': 10001, 'msg': '地址格式错误'}
        # self.__tablename__=

#server表
class server(Base):
    __tablename__ = 'server'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    # id = Column(Integer, primary_key=True,unique=True,autoincrement=True)
    kid=Column(String(255), unique=True,primary_key=True,nullable=False)
    url = Column(String(255), unique=True,primary_key=True,nullable=False)
    token_tb= Column(String(255), nullable=False)
    msg_tb= Column(String(255), nullable=False)

#msg_check表
class msg(Base):
    __tablename__ = 'msg_check'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    # id = Column(Integer, primary_key=True,unique=True,autoincrement=True)
    sq = Column(String(255), unique=True,primary_key=True,nullable=False)
    puk = Column(String(1000), nullable=False)
    prk = Column(String(1000), nullable=False)
    time_code= Column(String(255), nullable=False)

    def init(self, url):
        # id = Column(Integer, primary_key=True,unique=True,autoincrement=True
        # try:
        # items = session.execute("select table_nm from server WHERE url=%s "%(url))
        results = session.query(server).filter_by(url=url).all()
        # print(results)
        resData = []
        for x in results:
            resData.append({
                'msg_tb': x.msg_tb,
            })
        # print(resData)
        if resData != []:
            # print(items[0][0])
            self.__table__.name = resData[0]['msg_tb']
            # __init__(app)
            tablename = self.__table__.name
            # print(tablename)
            print('找表成功')
            # return tablename
            return {'code': 200, 'table_name': tablename, 'msg': '找表成功'}
        else:
            print('没找到表')
            return {'code': 10000, 'msg': '没有找到表'}

#token表的操作
class db_operation:
    def __init__(self):
        token=''
    def init(self,url):
        token.init(token,url)

        # print(self.token.__tablename__)
        # print("--------------")
        # token=token1()
        # print(url)
    def insert(self,user_id1,time_code1,token1):
        # print(user_id1)
        # print(time_code1)
        # print(token1)
        session.add(token(user_id=user_id1,time_code=time_code1,token=token1))
        session.commit()
        print('单个数据添加成功')

    def createMany(self,list):
        # users=[Role(name="lisi"),Role(name="wangwu"),Role(name="zhaosi")]
        session.add_all(list)
        session.commit()
        print('多个数据添加成功')

    # 删
    def deleteis(self,user_id):
        results = session.query(token).filter_by(user_id=user_id).all()
        session.delete(results[0])
        session.commit()
        print('数据删除成功')

    #删除已经过时的密钥
    def delete_task(self):
        now=self.get_time()/1000000-86400
        items=session.execute("delete  from %s  where (time_code+0)/1000000<'%d'"%(token.__tablename__,now))
        items=list(items)
        print(items)
        # session.execute("delete from user where id=1 ")


    # # 改
    def update(self,uer_id,time_code,token):
        results = session.query(token).filter_by(user_id=uer_id).all()
        # print(results[0].title)
        results[0].time_code = time_code
        results[0].token=token
        session.commit()
        print('修改成功')


    #
    # # 查
    def search_by_user_id(self,user_id):
        results = session.query(token).filter_by(user_id=user_id).all()
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
        results = session.query(token).filter_by(time_code=time_code).all()
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
        results = session.query(token).filter_by(token=token).all()
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
        dict = session.query(token).all()
        for each in dict:
            # print(each)
            print(each.user_id + '|' + each.time_code + '|' + each.token)
        return dict

    def checkhave(self,user_id):
        print(token.__tablename__)
        results = session.query(token).filter_by(user_id=user_id).all()
        # print(results)
        # print(results[0].token)
        # print(12345)
        if results ==[]:
            # print(0)
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
    def insert(self,kid, url,token_tb,msg_tb):

        session.add(server(kid=kid,url=url,token_tb=token_tb,msg_tb=msg_tb))
        session.commit()
        print('单个数据添加成功')

    def createMany(self, list):
        # users=[Role(name="lisi"),Role(name="wangwu"),Role(name="zhaosi")]
        session.add_all(list)
        session.commit()
        print('多个数据添加成功')

    # 删
    def deleteis(self, kid):
        results = session.query(server).filter_by(kid=kid).all()
        session.delete(results[0])
        session.commit()
        print('数据删除成功')

    # 删除已经过时的密钥
    # def delete_task(self):
    #     now = self.get_time() / 1000000 - 86400
    #     items = session.execute("delete  from server  where (time_code+0)/1000000<'%d'" % (now))
    #     items = list(items)
    #     print(items)
        # session.execute("delete from user where id=1 ")

    # # 改
    def update(self,  kid,url,token_tb,msg_tb):
        results = session.query(server).filter_by(kid=kid).all()
        # print(results[0].title)
        results[0].token_tb=token_tb
        results[0].msg_tb=msg_tb
        session.commit()
        print('修改成功')

    #
    # # 查
    def search_by_kid(self,  kid):
        results = session.query(server).filter_by(kid=kid).all()
        # print(results)
        resData = []
        for x in results:
            resData.append({
                'kid':x.kid,
                'url': x.url,
                'token_tb':x.token_tb,
                'msg_tb':x.msg_tb,
            })
        # print(resData)
        if resData != []:
            return resData[0]
        else:
            return resData

    def search_by_url(self,  url):
        results = session.query(server).filter_by(url=url).all()
        # print(results)
        resData = []
        for x in results:
            resData.append({
                'kid': x.kid,
                'url': x.url,
                'token_tb':x.token_tb,
                'msg_tb':x.msg_tb,
            })
        # print(resData)
        if resData != []:
            return resData[0]
        else:
            return resData

    def search_by_token_tb(self, token_tb):
        results = session.query(server).filter_by(token_tb=token_tb).all()
        # print(results)
        resData = []
        for x in results:
            resData.append({
                'kid': x.kid,
                'url': x.url,
                'token_tb': x.token_tb,
                'msg_tb': x.msg_tb,
            })
        # print(resData)
        if resData != []:
            return resData[0]
        else:
            return resData

    # 获取所有数据
    def search_all(self):
        dict = session.query(server).all()
        # print('good')
        for each in dict:
            # print(each)
            print(each.url +'|'+each.token_tb+'|'+each.msg_tb)
        return dict

    def checkhave(self, url,kid):
        # print('goddddddd' + url)
        # url='123'
        results = session.query(server).filter_by(url=url,kid=kid).all()
        # print('adas')
        if results == []:
            return 0
        else:
            return 1
            # 删除已经过时的密钥
    def get_time(self):
        t = time.time()
        # print(t)  # 原始时间数据
        # print(int(t))  # 秒级时间戳
        # print(int(round(t * 1000)))  # 毫秒级时间戳
        # print(int(round(t * 1000000)))  # 微秒级时间戳
        return int(round(t * 1000000))

    def delete_task(self):
        print('good')
        now = str(self.get_time()-60*60*24*1000000)
        # now='0'
        print(now)
        dict = session.query(server).all()
        for each in dict:
            # each.token_tb  + each.msg_tb
            session.execute("delete from `%s` where time_code+0<=%s"% (each.msg_tb, now))
            session.execute("delete  from `%s`  where `time_code`+0<= %s" % (each.token_tb, now))

            session.commit()
        print('good')

    def create_new_table(self,token_tb,msg_check):
        str1="CREATE TABLE `"+token_tb+"` "+\
            "(`user_id` varchar(255) CHARACTER SET utf8 NOT NULL,"+\
            "`time_code` varchar(255) CHARACTER SET utf8 NOT NULL,"+\
            "`token` varchar(500) CHARACTER SET utf8 NOT NULL,"+\
            "PRIMARY KEY (`user_id`) USING BTREE)"+\
            " ENGINE=InnoDB DEFAULT CHARSET=utf8;"
        session.execute(str1)
        str2=" CREATE TABLE `"+msg_check+"`"+\
             " (`sq` varchar(255) DEFAULT NULL,"+\
             "`puk` varchar(1000) DEFAULT NULL,"+\
             "`prk` varchar(1000) DEFAULT NULL,"+\
             "`time_code` varchar(255) DEFAULT NULL)"+\
             " ENGINE=InnoDB DEFAULT CHARSET=utf8"
        session.execute(str2)
        print('建表成功')

# msg表的操作
class msg_operation:
    def init(self,url):
        msg.init(msg,url)

        # print(self.token.__tablename__)
        # print("--------------")
        # token=token1()
        # print(url)

    def insert(self,sq,puk,prk,time_code):
        # print(user_id1)
        # print(time_code1)
        # print(token1)
        session.add(msg(sq=sq,puk=puk,prk=prk,time_code=time_code))
        session.commit()
        print('单个数据添加成功')

    def createMany(self,list):
        # users=[Role(name="lisi"),Role(name="wangwu"),Role(name="zhaosi")]
        session.add_all(list)
        session.commit()
        print('多个数据添加成功')

    # 删
    def deleteis_by_sq(self,sq):
        results = session.query(msg).filter_by(sq=sq).all()
        print(results[0].puk)
        session.delete(results[0])
        session.commit()
        print('数据删除成功')

    #删除已经过时的密钥
    # def delete_task(self):
    #     now=self.get_time()/1000000-86400
    #     items=session.execute("delete  from msg  where (time_code+0)/1000000<'%d'"%(now))
    #     items=list(items)
    #     print(items)
        # session.execute("delete from user where id=1 ")


    # # 改
    def update(self,sq,puk,prk,time_code):
        results = session.query(msg).filter_by(sq=sq).all()
        # print(results[0].title)
        results[0].time_code = time_code
        results[0].puk = puk
        results[0].prk = prk
        session.commit()
        print('修改成功')


    #
    # # 查
    def search_by_sq(self,sq):
        results = session.query(msg).filter_by(sq=sq).all()
        # print(results)
        resData = []
        for x in results:
            resData.append({
                'sq': x.sq,
                'puk': x.puk,
                'prk':x.prk,
                'time_code':x.time_code,
            })
        # print(resData)
        if resData!=[]:
            return resData[0]
        else:
            return resData

    def search_by_time_code(self,time_code):
        results = session.query(msg).filter_by(time_code=time_code).all()
        # print(results)
        resData = []
        for x in results:
            resData.append({
                'sq': x.sq,
                'puk': x.puk,
                'prk':x.prk,
                'time_code':x.time_code,
            })
        # print(resData)
        if resData!=[]:
            return resData[0]
        else:
            return resData


    def search_by_puk(self,puk):
        results = session.query(msg).filter_by(puk=puk).all()
        # print(results)
        resData = []
        for x in results:
            resData.append({
                'sq': x.sq,
                'puk': x.puk,
                'prk':x.prk,
                'time_code':x.time_code,
            })
        # print(resData)
        if resData!=[]:
            return resData[0]
        else:
            return resData

    #获取所有数据
    def search_all(self):
        dict = session.query(msg).all()
        for each in dict:
            # print(each)
            print(each.sq + '|' + each.puk + '|' + each.prk + '|' + each.time_code)
        return dict

    def checkhave(self,sq):
        print(msg.__tablename__)
        results = session.query(msg).filter_by(sq=sq).all()
        # print(results)
        # print(results[0].token)
        # print(12345)
        if results ==[]:
            # print(0)
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

#token_count表的操作
class token_count_operation:
    def __init__(self):
        token=''

    def insert(self,kid,count,times,free,data,type):
        # print(user_id1)
        # print(time_code1)
        # print(token1)
        session.add(token(kid=kid,count=count,times=times,free=free,data=data,type=type))
        session.commit()
        print('单个数据添加成功')

    def createMany(self,list):
        # users=[Role(name="lisi"),Role(name="wangwu"),Role(name="zhaosi")]
        session.add_all(list)
        session.commit()
        print('多个数据添加成功')

    # 删
    def deleteis(self,kid):
        results = session.query(token).filter_by(kid=kid).all()
        session.delete(results[0])
        session.commit()
        print('数据删除成功')


    # 改
    def update_count(self,kid,count):
        results = session.query(token).filter_by(kid=kid).all()
        # print(results[0].title)
        results[0].count = count
        session.commit()
        print('修改成功')

    def update_times(self,kid,times):
        results = session.query(token).filter_by(kid=kid).all()
        # print(results[0].title)
        results[0].times = times
        session.commit()
        print('修改成功')

    def update_free(self,kid,free):
        results = session.query(token).filter_by(kid=kid).all()
        # print(results[0].title)
        results[0].free = free
        session.commit()
        print('修改成功')

    def update_data(self,kid,data):
        results = session.query(token).filter_by(kid=kid).all()
        # print(results[0].title)
        results[0].data = data
        session.commit()
        print('修改成功')

    def set_type(self,kid,type):
        results = session.query(token).filter_by(kid=kid).all()
        # print(results[0].title)
        results[0].type = type
        session.commit()
        print('修改成功')

    def add_count(self,kid,num):
        result=self.search_by_kid(kid)
        count=result['count']
        count=count+num
        self.update_count(count)

    def add_times(self,kid,num):
        result = self.search_by_kid(kid)
        times = result['times']
        times = times + num
        self.update_count(times)

    def add_newdata(self,kid,num):
        now=self.get_time()
        newdata=now+num
        self.update_times(kid,newdata)
    #
    # # 查
    def search_by_kid(self,kid):
        results = session.query(token).filter_by(kid=kid).all()
        # print(results)
        resData = []
        for x in results:
            resData.append({
                'kid': x.kid,
                'count': x.count,
                'times':x.times,
                'free':x.free,
                'data':x.data,
                'type':x.type,
            })
        # print(resData)
        if resData!=[]:
            return resData[0]
        else:
            return resData


    #获取所有数据
    def search_all(self):
        dict = session.query(token_count).all()
        for each in dict:
            # print(each)
            print(each.user_id + '|' + each.time_code + '|' + each.token)
        return dict

    def checkhave(self,kid):
        print(token.__tablename__)
        results = session.query(token_count).filter_by(kid=kid).all()
        # print(results)
        # print(results[0].token)
        # print(12345)
        if results ==[]:
            # print(0)
            return 0
        else:
            print(1)
            return 1

    def check_num(self,kid,op):
        result=self.search_by_kid(kid)
        num=result[op]
        if num<=0:
            return {'code':10000,'msg':'次数不足'}
        return {'code':200,'msg':'次数充足'}

    def get_time(self):
        t = time.time()
        # print(t)  # 原始时间数据
        # print(int(t))  # 秒级时间戳
        # print(int(round(t * 1000)))  # 毫秒级时间戳
        print(int(round(t * 1000000)))  # 微秒级时间戳
        return int(round(t * 1000000))/1000000

#msg_check_count表的操作
class msg_check_count_operation:
    def __init__(self):
        token=''

    def insert(self,kid,count,times,free,data,type):
        # print(user_id1)
        # print(time_code1)
        # print(token1)
        session.add(token(kid=kid,count=count,times=times,free=free,data=data,type=type))
        session.commit()
        print('单个数据添加成功')

    def createMany(self,list):
        # users=[Role(name="lisi"),Role(name="wangwu"),Role(name="zhaosi")]
        session.add_all(list)
        session.commit()
        print('多个数据添加成功')

    # 删
    def deleteis(self,kid):
        results = session.query(token).filter_by(kid=kid).all()
        session.delete(results[0])
        session.commit()
        print('数据删除成功')


    # 改
    def update_count(self,kid,count):
        results = session.query(token).filter_by(kid=kid).all()
        # print(results[0].title)
        results[0].count = count
        session.commit()
        print('修改成功')

    def update_times(self,kid,times):
        results = session.query(token).filter_by(kid=kid).all()
        # print(results[0].title)
        results[0].times = times
        session.commit()
        print('修改成功')

    def update_free(self,kid,free):
        results = session.query(token).filter_by(kid=kid).all()
        # print(results[0].title)
        results[0].free = free
        session.commit()
        print('修改成功')

    def update_data(self,kid,data):
        results = session.query(token).filter_by(kid=kid).all()
        # print(results[0].title)
        results[0].data = data
        session.commit()
        print('修改成功')

    def set_type(self,kid,type):
        results = session.query(token).filter_by(kid=kid).all()
        # print(results[0].title)
        results[0].type = type
        session.commit()
        print('修改成功')

    def add_count(self,kid,num):
        result=self.search_by_kid(kid)
        count=result['count']
        count=count+num
        self.update_count(count)

    def add_times(self,kid,num):
        result = self.search_by_kid(kid)
        times = result['times']
        times = times + num
        self.update_count(times)

    def add_newdata(self,kid,num):
        now=self.get_time()
        newdata=now+num
        self.update_times(kid,newdata)
    #
    # # 查
    def search_by_kid(self,kid):
        results = session.query(token).filter_by(kid=kid).all()
        # print(results)
        resData = []
        for x in results:
            resData.append({
                'kid': x.kid,
                'count': x.count,
                'times':x.times,
                'free':x.free,
                'data':x.data,
                'type':x.type,
            })
        # print(resData)
        if resData!=[]:
            return resData[0]
        else:
            return resData


    #获取所有数据
    def search_all(self):
        dict = session.query(token_count).all()
        for each in dict:
            # print(each)
            print(each.user_id + '|' + each.time_code + '|' + each.token)
        return dict

    def checkhave(self,kid):
        print(token.__tablename__)
        results = session.query(msg_check_count).filter_by(kid=kid).all()
        # print(results)
        # print(results[0].token)
        # print(12345)
        if results ==[]:
            # print(0)
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

if __name__ == "__main__":

    # print(resData)
    op = db_operation()
    op.init('127.0.0.1:8886')
    # op = db_operation()
    op.checkhave('2019')
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

