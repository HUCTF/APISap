#coding:utf-8
import sys
import requests
import time
from scapy.utils import PcapReader
##resend the package in package.txt, and get the return from server.
host=''
fd=open(sys.path[0]+'//packpost.txt')
def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return str(html[start:end].strip())
def Read_package():
    line=fd.readline()
    while ('GET ' not in line) and ('POST ' not in line):
        print('111111')
        line=fd.readline()
    if 'GET' in line:
        print('2222222')
        msd='GET'
        host=getmidstring(line,'GET ',' HTTP/')
        requests_get(line, host)
    else:
        print('2222222')
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
    # print(resp.encode("gbk", errors="replace").decode('gb18030', 'ignore'))
    # print(resp.encode("gbk", errors="replace"))


def requests_post(line, host):
    headers={}
    headers.clear()
    # time.sleep(1)
    line = fd.readline()
    line = fd.readline()
    while('Host:' not in line):
        line = fd.readline()
        head = line.split(": ")
        # print(head)
        if "\n" not in head[0] and head[0] != '':
            if head[0] == 'Host':
                continue
            headers[head[0]]=head[1][:-1]
            # print(headers)

    host='http://'+str(getmidstring(line,'Host:','\n'))+str(host)
    print("=====host=====",host)
    print("=======header======", headers)
    try:
        resp=requests.post(url=host,headers=headers, timeout=3).text
        print(resp)
    except:
        print("Error! Continue Go Next!")
        Read_package()


if __name__ == "__main__":
    while(1):
        Read_package()