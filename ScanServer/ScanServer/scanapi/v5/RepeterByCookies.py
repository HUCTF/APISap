#coding:utf-8
import sys
import requests
import time
import re
from scapy.utils import PcapReader
##resend the package in package.txt, and get the return from server.
# host=''
cookienum = 2
cookieB = {'Cookie':'456789test'}
cookieC = {'Cookie':'159786test'}

class RepeterByRequests:

    def __init__(self, username, cookieb=None):
        self.username = username
        self.filename = '/opt/2020-Works-ApiSecurity/ScanServer/userfile_center/{0}/{0}_spider/{0}.txt'.format(self.username)
        self.fd=open(self.filename, errors='ignore')
        self.cookieb=cookieb
        while(1):
            flag = self.Read_package()
            if not flag:
                break

    def getmidstring(self, html, start_str, end):
        start = html.find(start_str)
        if start >= 0:
            start += len(start_str)
            end = html.find(end, start)
            if end >= 0:
                return str(html[start:end].strip())

    def Read_package(self):
        line=self.fd.readline()
        if not line:
            return False
        while ('GET' not in line) and ('POST' not in line):
            line=self.fd.readline()
        if 'GET' in line:
            msd='GET'
            host = self.getmidstring(line, 'GET ', ' HTTP/')
            print("===========GET==========")
            print(host)
            self.requests_get(line, host)
        else:
           msd='POST'
           host=self.getmidstring(line,'POST ',' HTTP/')
           print("===========post==========")
           print(host)
           self.requests_post(line, host)
        return True


    def requests_get(self, line, host):
        line = line[1:]
        headers={}
        cookie = {}
        headers.clear()
        cookie.clear()
        while("'" not in line):
            line = self.fd.readline()
            head = line.split(": ")
            if "\n" not in head[0] and head[0] != '':
                headers[head[0]]=head[1][:-1]
        host='https://'+str(headers['Host'])+str(host)
        if 'Cookie' in headers.keys():
            cookie.setdefault('Cookie',headers['Cookie'])
            del headers['Cookie']
            print(cookie)
        print(headers)

#        try:
           # from Checker.NLP.address import address
            #import re
        from Checker.RE.checker import checker
        from Checker.NLP.address import address

        r = requests.get(host, cookies=self.cookieb, headers=headers, timeout=2)
        print(r.status_code)
        r.encoding = r.apparent_encoding
       #  print(r.text)
  #     jjj = re.sub(r'<.*?>', '', r.text)
        print(r.text)
        checker(r.text)
        print('---------')
        address(r.text)
      #  except:
       #     print('error')


    def requests_post(self, line, host):
        line = line[1:]
        headers={}
        data={}
        cookie ={}
        headers.clear()
        data.clear()
        cookie.clear()
    # time.sleep(1)
        print(line)
        line = self.fd.readline()
        while("'" not in line and ":" in line):
            head = line.split(": ")
            if "\n" not in head[0] and head[0] != '' :
                headers[head[0]]=head[1][:-1]
            line = self.fd.readline()
        line = self.fd.readline()
        if re.match(".+'", line):
            line = line[:-2]
            datas= line.split("&&")
            for l in datas:
                l.split('=')
                data[l[0]]=l[2]
        if 'Cookie' in headers.keys():
            cookie.setdefault('Cookie',headers['Cookie'])
            del headers['Cookie']
            print(cookie)
        print(headers)
        print(data)
        try: 
            from Checker.NLP.address import address
            import re
            r = requests.post(host, cookies=self.cookieb, data=data, headers=headers, timeout=2)
            print(r.status_code)
            r.encoding = r.apparent_encoding
            print(r.text)
            jjj = re.sub(r'<.*?>', '', r.text)
            print(jjj)
            address(jjj)
        except:
            print('error')


def RUNRepeter(filename, cookieb):
    while(1):
        flag = RepeterByRequests(filename, cookieb)


