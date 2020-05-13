from NIC_package_get import NICRUN
from threading import Thread
#from scanapi-coomie import RUN_COOKIE
import os
import requests


class spider():
    def __init__(self):
        self.WEBSITE=os.environ.get('WEBSITE')
        self.RUNWAY=os.environ.get('RUNWAY')
        self.USERNAME=os.environ.get('USERNAME')

        if self.RUNWAY == 'cookie':
            self.COOKIE1 = os.environ.get('COOKIE1')
            self.COOKIE2 = os.environ.get('COOKIE2')
        elif self.RUNWAY == 'userid':
            self.USERID1 = os.environ.get('USERID1')
            self.PASSWD1 = os.environ.get('PASSWD1')
            self.USERID2 = os.environ.get('USERID2')
            self.PASSWD2 = os.environ.get('PASSWD2')

    def RUNThread_Cookie(self):
        needpcap = 1000
        thread = Thread(target=NICRUN, args=['eth0', needpcap, self.USERNAME])
        # 使用多线程
        thread.start()

#        thread = Thread(target=RQRUN)
        # 使用多线程
#        thread.start()
        RUN_COOKIE(self.WEBSITE, self.COOKIE1)
        
        print(self.COOKIE1, self.COOKIE2)

        
    def RUNThread_Userid(self):
        needpcap = 1000
        thread = Thread(target=NICRUN, args=['eth0', needpcap, self.USERNAME])
        thread.start()
 

        print('userid')
        print('userid')
        print('userid')
        print('userid')
        print(self.USERID1, self.PASSWD1, self.USERID2, self.PASSWD2)
    

a = spider()
if a.RUNWAY=='cookie':
    a.RUNThread_Cookie()
else:
    a.RUNThread_Userid()

