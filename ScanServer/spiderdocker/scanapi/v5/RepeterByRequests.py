#coding:utf-8
import sys
import requests
import time
import re
from .diffstr import similarity
from scapy.utils import PcapReader
from .sqltest import insert_db
import collections
##resend the package in package.txt, and get the return from server.
# host=''
# cookienum = 2
# cookie1 = {'Cookie':'456789test'}
# cookie2 = {'Cookie':'159786test'}

def cut_text(text,lenth):
    textArr = re.findall('.{'+str(lenth)+'}', text)
    textArr.append(text[(len(textArr)*lenth):])
    return textArr


def regenerate(rtext):
    from .Checker.RE.checker import checker_idcode, checker_address, checker_bank_id, checker_emall
    from .Checker.NLP.address import address
    texts = " ".join(str(i) for i in checker_address(rtext))
    if len(texts) >= 280:
        texts = cut_text(texts, 280)
        addresslist = []
        province_codelist = []
        phonelist = []
        personlist = []
        for i in range(len(texts)):
            res = address(texts[i - 1])
            strs = res.get('province', '') + res.get('city', '') + res.get('county', '')
            if strs:
                addresslist.append(strs)
            strs = res.get('province_code', '')
            if strs:
                province_codelist.append(strs)
            strs = res.get('phonenum', '')
            if strs:
                phonelist.append(strs)
            strs = res.get('person', '')
            if strs:
                personlist.append(strs)
        res1 = {
            "address": addresslist,
            "province_code": province_codelist,
            "phone": phonelist,
            "person": personlist,
            "idcode": "".join(checker_idcode(rtext)),
            "bankid": "".join(checker_bank_id(rtext)),
            "emall": "".join(checker_emall(rtext))
        }
        return res1
    else:
        res = address(texts)
        res1 = {
            "address": str(res.get('province', '') + res.get('city', '') + res.get('county', '')),
            "province_code": res.get('province_code', ''),
            "phone": res.get('phonenum', ''),
            "person": res.get('person', ''),
            "idcode": "".join(checker_idcode(rtext)),
            "bankid": "".join(checker_bank_id(rtext)),
            "emall": "".join(checker_emall(rtext))
        }
        return res1

class RepeterByRequests:

    def __init__(self, username,cookie1,cookie2):
        self.username = username
        self.cookie1 = cookie1
        self.cookie2 = cookie2
        self.filename = '/opt/spider/{0}/{0}.txt'.format(self.username)
        # self.filename = 'admin.txt'.format(self.username)
        self.fd=open(self.filename, errors='ignore')
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
                try:
                    headers[head[0]]=head[1][:-1]
                except:
                    headers[head[0]]=''
        hosts='http://'+str(headers['Host'])+str(host)
        if "Cookie" in headers:
            del headers['Cookie']
        if "'" in headers:
            del headers["'"]
        r = requests.get(hosts, cookies=self.cookie1, headers=headers, timeout=5)#2 cookie
        retext=r.text.encode('utf8').decode('unicode_escape')
        d = collections.OrderedDict(r.request.headers)
        requests_text='GET '+str(host)+' HTTP/1.1\nHost: '+str(headers['Host']+"\n")
        for k, v in d.items():
            requests_text+=(k+": "+v+"\n")
        Url=hosts
        Request=requests_text
        Response=retext
        info = str(regenerate(retext))
        resflag=False
        if r.status_code == 200:
            s=requests.get(hosts, cookies=self.cookie2, headers=headers, timeout=5)
            retexts=r.text.encode('utf8').decode('unicode_escape')
            info_cookie2 = str(regenerate(retexts))
            if similarity(info,info_cookie2)==True and len(info)>130:
                 resflag=True
        insert_db(Url,Request,Response,info,resflag)
        r.encoding = r.apparent_encoding
        print('---------')



    def requests_post(self, line, host):
        line = line[1:]
        headers={}
        data={}
        cookie ={}
        headers.clear()
        data.clear()
        cookie.clear()
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
            datas= line.split("&")
            for l in datas:
                list = l.split('=')
                data[list[0]]=list[1]
        hosts='http://'+str(headers['Host'])+str(host)
        if "Cookie" in headers:
            del headers['Cookie']
        r = requests.post(hosts, cookies=self.cookie1, headers=headers, data=data,timeout=5)  # 2 cookie
        retext=r.text.encode('utf8').decode('unicode_escape')
        d = collections.OrderedDict(r.request.headers)
        requests_text = 'POST ' + str(host) + ' HTTP/1.1\nHost: ' + str(headers['Host']+"\n")
        for k, v in d.items():
            requests_text += (k + ": " + v + "\n")
        postdata = collections.OrderedDict(data)
        for k, v in postdata.items():
            requests_text += ("\n"+k + "=" + v + "&")
        Url = hosts
        Request = requests_text[:-1]
        Response = retext
        info = str(regenerate(retext))
        resflag = False
        if r.status_code == 200:
            s = requests.post(hosts, cookies=self.cookie2, data=data,headers=headers, timeout=5)
            retexts=r.text.encode('utf8').decode('unicode_escape')
            info_cookie2 = str(regenerate(retexts))
            if similarity(info, info_cookie2) == True and len(info) > 130:
                resflag = True
        insert_db(Url, Request, Response, info, resflag)
        r.encoding = r.apparent_encoding
        print('---------')


def RUNRepeter(username,cookie1,cookie2):
    # while(1):
    flag = RepeterByRequests(username,cookie1,cookie2)


