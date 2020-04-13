## Get_Requests_From_Local_NIC
**环境要求**
Python3.5+

------------------
**NIC_package_get**
基于网卡的抓包服务，用于从网卡抓取数据包  
```bash
cd 2020-Works-ApiSecurity/Get_Requests_From_Local_NIC
pip install -r requirement.txt
python NIC_package_get.py
```
主要参数设置  
```python
    self.package_output='all' #数据包保存设置  'screen' 仅在屏幕上打印 /'document'保存到txt文件/'pcap' 保存到pcap文件 /'all' 全部选择
    self.catch_method=0 #0连续抓包 1按数量抓包
    self.Time_conversion=0 #使用连续抓包时的数据包保存时间间隔，仅在catch_method=0时有效
    self.package_num=NEEDPCAP  #使用按数量抓包时的数据包抓取数量，仅在catch_method=1时有效
```
**RepeterByRequests**
基于保存到txt数据包的重发器 ，用于重发数据包并获取返回值 
```bash
cd 2020-Works-ApiSecurity/Get_Requests_From_Local_NIC
pip install -r requirement.txt
python RepeterByRequests.py
```
