#coding:utf-8
from scapy.all import *
import sys
import os
from datetime import datetime
from threading import Timer

class NICPackage:

    def __init__(self, IFACE=None, NEEDPCAP=None):
        # self.path=''
        # self.filename=''
        # self.filename_txt=''
        # self.filename_pcap=''

        WIN = sys.platform.startswith('win')
        if WIN:
            self.prefix = '\\'
        else:
            self.prefix = '/'
        self.package_output='all' #'screen'/'document'/'all'/'pcap'
        self.catch_method=0 #0连续抓包 1按数量抓包
        self.Time_conversion=0 #使用连续抓包时的数据包保存时间间隔，仅在catch_method=0时有效
        self.package_num=NEEDPCAP  #使用按数量抓包时的数据包抓取数量，仅在catch_method=1时有效
        self.iface=IFACE
        self.pcap=[]
        self.path = sys.path[0] + self.prefix + str(datetime.now().strftime("%Y-%m-%d_%H"))
        self.filename = self.path + self.prefix + str(datetime.now().strftime("%Y-%m-%d_%H"))
        self.filename_pcap = self.filename + '.pcap'
        self.filename_txt = self.filename + '.txt'
        
    def create_dir_and_file(self):
        isExists=os.path.exists(self.path)
        if not isExists:
            os.makedirs(self.path)
        fileisExists=os.path.exists(self.filename_txt)
        if not fileisExists:
            #os.mknod(filename_txt)
            #os.mknod(filename_pcap)
            fp = open(self.filename_txt,'w')
            fp.close()
            wrpcap(self.filename_pcap,'')

        self.pcap = rdpcap(self.filename_pcap)
    
    def package_print(self, packet):
        if (self.package_output == 'screen') or (self.package_output == 'all'):
            print("\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n"))+'\n\n\n')
        if (self.package_output == 'document') or (self.package_output == 'all'):
            with open(self.filename_txt,'a') as outputxt:
                outputxt.write("\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n"))+'\n\n\n')
                # outputxt.close()
        if (self.package_output == 'pcap') or (self.package_output == 'all'):
            self.pcap.extend(packet)
            wrpcap(self.filename_pcap,self.pcap)
            print(self.filename_pcap)
            #print("\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n"))+'\n\n\n')
        #return "\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n"))+'\n\n\n'
    def time(self):
        
        self.filename = self.path + self.prefix + str(datetime.now().strftime("%Y-%m-%d_%H"))
        self.filename_pcap = self.filename + '.pcap'
        self.filename_txt = self.filename + '.txt'
        wrpcap(self.filename_pcap,'')
        fp = open(self.filename_txt,'w')
        fp.close()
        #create_dir_and_file()
        #print(filename_pcap)
        Timer(self.Time_conversion, self.time).start()
    
    def mainrun(self):
        self.create_dir_and_file()
        if self.catch_method==0:
            #t = Timer(self.Time_conversion, self.time) 
            #t.start()
            while(1):
                sniff(
                iface=self.iface,
                count=1,
                prn=self.package_print,
                lfilter=lambda p: ("GET" in str(p)) or ("POST" in str(p)),
                filter="tcp")
        else:
            sniff(
            iface=self.iface,
            count=self.package_num,
            prn=self.package_print,
            lfilter=lambda p: ("GET" in str(p)) or ("POST" in str(p)),
            filter="tcp")

            #iface='XXX'  监听本地名为XXX的网卡


def NICRUN(netname=None, needpcap=10):
    # a = NICPackage('Realtek PCIe GbE Family Controller')
    # netname = "Realtek PCIe GbE Family Controller"

    if netname:
        print("Start get NIC package...")
        a = NICPackage(IFACE=netname, NEEDPCAP=needpcap)
        a.mainrun()
    else:
        print("=======================================================")
        print('请设置网卡名！！！')
        print("=======================================================")
# NICRUN(netname='Realtek PCIe GbE Family Controller',needpcap=1000)