#coding:utf-8
import sys
import requests
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
        #print(line)
    if 'GET' in line:
        msd='GET'
        host=getmidstring(line,'GET ',' HTTP/')
    #else:
    #    msd='POST'
    #    host=getmidstring(line,'POST ',' HTTP/')
    head=''
    line=fd.readline()+'\n'
    while('Host:' not in line):
        line=fd.readline()+'\n'
        head=head+line
    host='http://'+str(getmidstring(line,'Host:','\n'))+str(host)
    print(host)
    resp=requests.get(url=host,data=head).text
    print(resp)

while(1):
    Read_package()