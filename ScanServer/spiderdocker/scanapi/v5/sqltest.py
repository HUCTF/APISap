import pymysql
import datetime
# 连接database
db= pymysql.connect(
    host="47.115.30.24",
    user="root",password="root",
    database="scanserver",charset="utf8")
# 使用cursor()方法获取操作游标
cursor = db.cursor()
def insert_db(Url,Request,Response,Info,flag):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = "Insert into scanresult(URL,Request,Response,SensitiveInfo,CreatTime,Result) values({}, {},{},{},{},{});".format(db.escape(Url),db.escape(Request),db.escape(Response),db.escape(Info),db.escape(now_time),flag)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    # 关闭数据库连接
    db.close()