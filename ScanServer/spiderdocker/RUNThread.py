from .NIC_package_get import NICRUN
from threading import Thread
from .scanapi import RQRUN
import os



class spider():
    def __init__(self):
        self.WEBSITE=os.environ.get('WEBSITE')
        self.RUNWAY=os.environ.get('RUNWAY')
        self.USERNAME=os.environ.get('USERNAME')

        if RUNWAY == 'cookie':
            self.COOKIE1 = os.environ.get('COOKIE1')
            self.COOKIE2 = os.environ.get('COOKIE2')
        elif RUNWAY == 'userid':
            self.USERID1 = os.environ.get('USERID1')
            self.PASSWD1 = os.environ.get('PASSWD1')
            self.USERID2 = os.environ.get('USERID2')
            self.PASSWD2 = os.environ.get('PASSWD2')

    def RUNThread(self):
        needpcap = 1000
        thread = Thread(target=NICRUN, args=['eth0', needpcap, self.USERNAME])
        # 使用多线程
        thread.start()

        thread = Thread(target=RQRUN)
        # 使用多线程
        thread.start()
    

