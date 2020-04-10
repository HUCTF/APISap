#coding:utf-8
import sys
import requests
import time
import re
from scapy.utils import PcapReader
##resend the package in package.txt, and get the return from server.
host=''
fd=open(sys.path[0]+'/packpost.txt', errors='ignore')
def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return str(html[start:end].strip())
def Read_package():
    line=fd.readline()
    while ('GET' not in line) and ('POST' not in line):
        line=fd.readline()
    if 'GET' in line:
        msd='GET'
        host=getmidstring(line,'GET ',' HTTP/')
        requests_get(line, host)
    else:
       msd='POST'
       host=getmidstring(line,'POST ',' HTTP/')
       print("===========post==========")
       print(host)
       print("=========================")

       requests_post(line, host)

       
       #############################
       #####  ���Ż�������      #####
       #############################


def requests_get(line, host):
    line = line[1:]
    headers={}
    headers.clear()
    while("'" not in line):
        line = fd.readline()
        head = line.split(": ")
        if "\n" not in head[0] and head[0] != '':
            headers[head[0]]=head[1][:-1]
    host='http://'+str(headers['Host'])+str(host)
    print(host)
    print(headers)
    resp=requests.get(url=host,headers=headers).text
    # print(resp)



def requests_post(line, host):
    line = line[1:]
    headers={}
    data={}
    headers.clear()
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
    print(headers)
    print(data)
    host = 'http://' + str(headers['Host']) + str(host)
    # resp=requests.post(url=host,headers=headers,data=data).text
    # print(resp)

if __name__ == "__main__":
    while(1):
        Read_package()