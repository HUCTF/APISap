#coding:utf-8
import sys
from scapy.all import *
from scapy.utils import PcapReader
pcap=rdpcap(sys.path[0]+'//package.pcap')
#try:
while(1):
    i=0
    while(1):
        p=sr1(pcap[i],timeout=1)
        #print(p.show())
        print(p)
        #print(pcap[i])
        i=i+1
#except:
    print('finish\n')
