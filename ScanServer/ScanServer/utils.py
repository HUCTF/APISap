# -*- coding: utf-8 -*-
try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for, current_app, jsonify
from werkzeug.http import HTTP_STATUS_CODES
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

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='user.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

def api_abort(code, message=None, **kwargs):
    if message is None:
        message = HTTP_STATUS_CODES.get(code, '')

    response = jsonify(message=message, **kwargs)
    return response,code

def write_env(username, env_listi, flag):
    '''
    write env to user/.env
        params: env_list: list
        mean: env_list: env list msg
        return: none
    '''
    if flag=='w':
        with open('.env', 'w') as fn:
            for env in env_list:
                fn.write(env)
    elif flag=='a': 
        with open('.env', 'a') as fn:
            for env in env_list:
                fn.write(env)
