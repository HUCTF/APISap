#coding:utf-8
import sys
##resend the package in package.txt, and get the return from server.
fd=open(sys.path[0]+'//package.txt')
def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()
def Read_package():
    line=fd.readline()
    while ('GET' not in line) and ('POST' not in line):
        line=fd.readline()
        #print(line)
    if 'GET' in line:
        msd='GET'
        print(getmidstring(line,'GET ',' HTTP/'))

Read_package()
Read_package()
Read_package()