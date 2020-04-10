from flask import jsonify
import psutil
import os
def get_net():
    '''
    获取当前机器所有的网卡名
    return [('网卡名', 'ip'), (), ...]
    '''
    netcard_info=[]
    info = psutil.net_if_addrs()
    for k, v in info.items():
        for item in v:
            if item[0] == 2 and not item[1][:3] != '192':
                netcard_info.append((k, item[1]))
    return netcard_info

def get_txt_file(filename):
    if '\\' in filename:
        dirpath = os.path.abspath('.')
        filename = os.path.join(dirpath, filename).replace('\\', '\\\\')
    with open(filename) as f:
         s=f.read()
         f.close()
    return str(s)

