#coding:utf-8
from scapy.all import *
import sys
import os

package_output='pcap' #'screen'/'document'/'all'/'pcap'
# pcap=rdpcap(sys.path[0]+'\\package.pcap')
WORKPATH = os.path.realpath('.')

pcap=rdpcap(WORKPATH + '\\package.pcap')

def package_print(packet):
    if (package_output == 'screen') or (package_output == 'all'):
        print("\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n"))+'\n\n\n')
    if (package_output == 'document') or (package_output == 'all'):
        outputxt=open(WORKPATH + '//package.txt','a')
        print(WORKPATH + '//package.txt')
        outputxt.write("\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n"))+'\n\n\n')
    if (package_output == 'pcap'):
        pcap.extend(packet)
        wrpcap(WORKPATH + '//package.pcap',pcap)
        print("\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n"))+'\n\n\n')
    #return "\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n"))+'\n\n\n'
    
sniff(
    iface='Realtek PCIe GbE Family Controller',
    prn=package_print,
    lfilter=lambda p: ("GET" in str(p)) or ("POST" in str(p)),
    filter="tcp")
    #iface='XXX'  监听本地名为XXX的网卡