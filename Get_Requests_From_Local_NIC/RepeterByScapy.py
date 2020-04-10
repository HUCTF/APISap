#!/usr/bin/env python
#encoding=utf-8
import scapy.all as scapy

packets = scapy.rdpcap('./package.pcap')
for p in  packets:
    for f in p.payload.payload.payload.fields_desc:
            fvalue = p.payload.payload.getfieldval(f.name)
            reprval = f.i2repr(p.payload.payload, fvalue)# 转换成十进制字符串
            if 'HTTP' in reprval:
                if 'GET' or 'POST' in reprval:
                    lst = str(reprval).split(r'\r\n')
                    for l in lst:
                        print (l)