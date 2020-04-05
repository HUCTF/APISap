#coding:utf-8
from scapy.all import *
import sys
import os
from datetime import datetime
from threading import Timer
path=''
filename=''
filename_txt=''
filename_pcap=''
package_output='all' #'screen'/'document'/'all'/'pcap'
catch_method=0 #0连续抓包 1按数量抓包
Time_conversion=5 #使用连续抓包时的数据包保存时间间隔，仅在catch_method=0时有效
package_num=1000  #使用按数量抓包时的数据包抓取数量，仅在catch_method=1时有效
iface='Realtek 8821CE Wireless LAN 802.11ac PCI-E NIC'
pcap=[]
def create_dir_and_file():
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    fileisExists=os.path.exists(filename_txt)
    if not fileisExists:
        #os.mknod(filename_txt)
        #os.mknod(filename_pcap)
        fp = open(filename_txt,'w')
        fp.close()
        wrpcap(filename_pcap,'')

    pcap=rdpcap(filename_pcap)
def package_print(packet):
    if (package_output == 'screen') or (package_output == 'all'):
        print("\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n"))+'\n\n\n')
    if (package_output == 'document') or (package_output == 'all'):
        outputxt=open(filename_txt,'a')
        print(filename)
        outputxt.write("\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n"))+'\n\n\n')
    if (package_output == 'pcap'):
        pcap.extend(packet)
        wrpcap(filename_pcap,pcap)
        print(filename_pcap)
        #print("\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n"))+'\n\n\n')
    #return "\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n"))+'\n\n\n'
def time(): 
    global filename
    global filename_pcap
    global filename_txt
    filename=path+'//'+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(':','_'))
    filename_pcap=filename+'.pcap'
    filename_txt=filename+'.txt'
    wrpcap(filename_pcap,'')
    fp = open(filename_txt,'w')
    fp.close()
    #create_dir_and_file()
    #print(filename_pcap)
    Timer(Time_conversion, time).start()
path=sys.path[0]+'//'+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(':','_'))
filename=path+'//'+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(':','_'))
filename_pcap=filename+'.pcap'
filename_txt=filename+'.txt'
create_dir_and_file()

if catch_method==0:
    t = Timer(Time_conversion,time) 
    t.start()
    while(1):
        sniff(
        iface=iface,
        count=1,
        prn=package_print,
        lfilter=lambda p: ("GET" in str(p)) or ("POST" in str(p)),
        filter="tcp")
else:
    sniff(
    iface=iface,
    count=package_num,
    prn=package_print,
    lfilter=lambda p: ("GET" in str(p)) or ("POST" in str(p)),
    filter="tcp")

    #iface='XXX'  监听本地名为XXX的网卡