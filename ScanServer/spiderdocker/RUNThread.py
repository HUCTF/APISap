from NIC_package_get import NICRUN
from threading import Thread
from ScanapiCookie import RUN_COOKIE
import os
import requests
from flask import Flask, jsonify
from scanapi.v5.RepeterByRequests import RUNRepeter
import time

class spider():
    def __init__(self):
        self.WEBSITE=os.environ.get('WEBSITE')
        self.RUNWAY=os.environ.get('RUNWAY')
        self.USERNAME=os.environ.get('USERNAME')

        if self.RUNWAY == 'cookie':
            self.COOKIE1 = os.environ.get('USERCOOKIE1')
            self.COOKIE2 = os.environ.get('USERCOOKIE2')
        elif self.RUNWAY == 'userid':
            self.USERID1 = os.environ.get('USERID1')
            self.PASSWD1 = os.environ.get('PASSWD1')
            self.USERID2 = os.environ.get('USERID2')
            self.PASSWD2 = os.environ.get('PASSWD2')

    def RUNThread_Cookie(self):
        needpcap = 1000
        thread1 = Thread(target=NICRUN, args=['eth0', needpcap, self.USERNAME])
        # 使用多线程
        thread1.start()
#        thread1.join()

#        print("NICRUN('eth0', {0}, {1})".format(needpcap, self.USERNAME))

#        NICRUN('eth0', needpcap, self.USERNAME)

        thread2 = Thread(target=RUN_COOKIE, args=[self.WEBSITE, self.COOKIE1])
        thread2.start()
#        thread2.join()
#        RUN_COOKIE(self.WEBSITE, self.COOKIE1)

#        RUN_COOKIE(self.WEBSITE, self.COOKIE1)
#        RUN_COOKIE('https://jkxxcj.zjhu.edu.cn/serviceList.html','health-data-Id=MGQ0MTM0YmQtMWQ2NC00MGViLTkzMGMtODNkZDM4ODU3YjJi')
        time.sleep(3) 
        flag = 0
        while os.path.getsize('/opt/spider/{0}/{0}.txt'.format(self.USERNAME)) != 0 and flag == 0:
            if flag == 0:
                flag=1
                thread = Thread(target=RUNRepeter, args=[self.USERNAME])
                thread.start()
                break

 
    def RUNThread_Userid(self):
        needpcap = 1000
        thread = Thread(target=NICRUN, args=['eth0', needpcap, self.USERNAME])
        thread.start()
 

        print('userid')
        print(self.USERID1, self.PASSWD1, self.USERID2, self.PASSWD2)

def get_txt_file(filename):
    if '\\' in filename:
        dirpath = os.path.abspath('.')
        filename = os.path.join(dirpath, filename).replace('\\', '\\\\')
    with open(filename) as f:
         s=f.read()
         f.close()
    return str(s)

def nlp_file(username,COOKIE1,COOKIE2):
    flag = 0
    while os.path.getsize('/opt/spider/{0}/{0}.txt'.format(username)) != 0 and flag == 0:
        if flag == 0:
            flag=1
            RUNRepeter(username,COOKIE1,COOKIE2)
#            thread = Thread(target=RUNRepeter, args=[username])
#            thread.start()
            break
                                                                                                 

app = Flask(__name__)
    
@app.route("/")
def index():
    filename = "/opt/spider/{0}/{0}.txt".format(os.environ.get('USERNAME'))
    result = get_txt_file(filename)
    if result:
        nlp_file(os.environ.get('USERNAME'),os.environ.get('COOKIE1'),os.environ.get('COOKIE2'))
        return jsonify({
            "result": result,
            "code": "200"
        })
    else:
        return jsonify({
            "result": "wating pcap",
            "code": "404"
        })

 
def app_run(host, port):                                 
    app.run(host=host, port=int(port))                                         
                                                         
if __name__ == '__main__':                               
#    thread = Thread(target=app_run, args=['0.0.0.0', 81])
#    thread.start()                   
#    app.run(host='0.0.0.0', port=81)                                     
    a = spider()            
    if a.RUNWAY=='cookie':                      
        a.RUNThread_Cookie()
    else:                                                                     
        a.RUNThread_Userid()

