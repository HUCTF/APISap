#coding:utf-8
from scapy.all import *
import sys
package_output='document' #'screen'/'document'/'all'
def package_print(packet):
    if (package_output == 'screen') or (package_output == 'all'):
        print("\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n"))+'\n\n\n')
    if (package_output == 'document') or (package_output == 'all'):
        outputxt=open(sys.path[0]+'//package.txt','a')
        print(sys.path[0]+'//package.txt')
        outputxt.write("\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n"))+'\n\n\n')
        
    #return "\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n"))+'\n\n\n'
sniff(
    iface='Realtek 8821CE Wireless LAN 802.11ac PCI-E NIC',
    prn=package_print,
    lfilter=lambda p: ("GET" in str(p)) or ("POST" in str(p)),
    filter="tcp")
    #iface='XXX'  监听本地名为XXX的网卡