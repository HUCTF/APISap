#coding:utf-8
import sys
import requests
import time
from scapy.utils import PcapReader
##resend the package in package.txt, and get the return from server.
host=''
fd=open(sys.path[0]+'//package.txt')
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
    #else:
    #    msd='POST'
    #    host=getmidstring(line,'POST ',' HTTP/')


def requests_get(line, host):
    headers={}
    headers.clear()
    # time.sleep(1)
    while('Host:' not in line):
        line = fd.readline()
        head = line.split(": ")
        if "\n" not in head[0] and head[0] != '':
            headers[head[0]]=head[1][:-1]
    # print(headers)
    host='http://'+str(getmidstring(line,'Host:','\n'))+str(host)
    print(host)
    resp=requests.get(url=host,headers=headers).text
    print(resp)


def requests_post(line, host):
    headers={}
    headers.clear()
    # time.sleep(1)
    while('Host:' not in line):
        line = fd.readline()
        head = line.split(": ")
        if "\n" not in head[0] and head[0] != '':
            headers[head[0]]=head[1][:-1]

    host='http://'+str(getmidstring(line,'Host:','\n'))+str(host)
    print(host)
    resp=requests.post(url=host,headers=headers).text
    print(resp)

while(1):
    Read_package()