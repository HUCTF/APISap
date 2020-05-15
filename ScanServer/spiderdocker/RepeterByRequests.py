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
# fd=open(sys.path[0]+'/packpost.txt', errors='ignore')
fd=open(sys.path[0]+'/package.txt', errors='ignore')
def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return str(html[start:end].strip())
def Read_package():
    line=fd.readline()
    if not line:
        return False
    while ('GET' not in line) and ('POST' not in line):
        line=fd.readline()
    if 'GET' in line:
        msd='GET'
        host = getmidstring(line, 'GET ', ' HTTP/')
        print("===========GET==========")
        print(host)
        # print("=========================")
        requests_get(line, host)
    else:
       msd='POST'
       host=getmidstring(line,'POST ',' HTTP/')
       print("===========post==========")
       print(host)
       # print("=========================")
       requests_post(line, host)
    return True

       #############################
       #####  ���Ż�������      #####
       #############################


def requests_get(line, host):
    line = line[1:]
    headers={}
    cookie = {}
    headers.clear()
    cookie.clear()
    while("'" not in line):
        line = fd.readline()
        head = line.split(": ")
        if "\n" not in head[0] and head[0] != '':
            headers[head[0]]=head[1][:-1]
    if 'Cookie' in headers.keys():
        cookie.setdefault('Cookie',headers['Cookie'])
        del headers['Cookie']
        print(cookie)
    print(headers)
    try:
        headers['Host']
    except:
        print("not Host!")
    else:
        host='http://'+str(headers['Host'])+str(host)
        try:
            resp=requests.get(url=host,headers=headers,cookies=cookie,timeout=3).text
        except:
            print("pass")
        else:
            print(resp)



def requests_post(line, host):
    line = line[1:]
    headers={}
    data={}
    cookie ={}
    headers.clear()
    data.clear()
    cookie.clear()
    # time.sleep(1)
    print(line)
    line = fd.readline()
    while("'" not in line and ":" in line):
        head = line.split(": ")
        if "\n" not in head[0] and head[0] != '' :
            headers[head[0]]=head[1][:-1]
        line = fd.readline()
    line = fd.readline()
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
        headers['Host']
    except:
        print("not Host!")
    else:
        host = 'http://' + str(headers['Host']) + str(host)
        try:
            resp=requests.post(url=host,headers=headers,data=data,timeout=3).text
        except:
            print("pass")
        else:
            print(resp)

if __name__ == "__main__":
    while(1):
        flag = Read_package()
        if not flag:
            break