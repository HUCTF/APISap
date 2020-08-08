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

def write_env(current_user, env_list, flag):
    '''
    function: write env to user/.env
    params: env_list: env list msg
    type: env_list: list
    return: none
    '''
    print('====== current_user username ======')
    print(current_user.username)
   
    center_file = 'userfile_center'
    userfile = center_file + os.path.sep + '{}'.format(current_user.username.lower())
    env_path_file = userfile + os.path.sep + '{}_env'.format(current_user.username.lower()) + os.path.sep + '.env'
    
    if flag=='w':
        with open(env_path_file, 'w') as fn:
            for env in env_list:
                fn.write(env)
    elif flag=='a': 
        with open(env_path_file, 'a') as fn:
            for env in env_list:
                fn.write(env)


def initenv_userfile(current_user, website, runway):
    '''
    function: init .envrc
    params: current_user: 
    type: current_user: dict
    return: none
    '''
#    if runway == 'cookie':
#        env_msg = '''
#            RUNWAY=cookie
#            COOKIE1=
#            COOKIE2=
#            PASSWD=1234qwer
#            WEBSITE=
#        '''
#    elif runway == 'userid':
#        env_msg = '''
#            USERNAME=USER
#            USERNAME=99kies
#            PASSWD=1234qwer
#            WEBSITE=
#    '''
    
    envrc = '''USERNAME={}\nWEBSITE={}\nRUNWAY={}\n'''.format(current_user.username, website, runway)
    
    center_file = 'userfile_center'

    userfile = center_file + os.path.sep + '{}'.format(current_user.username.lower())
    if not os.path.exists(userfile):
        os.makedirs(userfile)
    env_path = userfile + os.path.sep + '{}_env'.format(current_user.username.lower())
    filename = env_path + os.path.sep +'.env'
    if not os.path.exists(env_path):
        os.makedirs(env_path)
        with open(filename, 'w', encoding='utf-8') as fn:
            fn.write(envrc)
    spiderpath = userfile + os.path.sep + '{}_spider'.format(current_user.username.lower())
    if not os.path.exists(spiderpath):
        os.mkdir(spiderpath)


def write_dp_yaml(current_user):

    dp = """apiVersion: apps/v1
kind: Deployment
metadata:
 name: {0}-deployment
spec:
 selector:
  matchLabels:
   app: {0}
 replicas: 3
 template:
  metadata:
   labels:
    app: {0}
  spec:
   containers:
   - name: {0}
     image: scanserver
     imagePullPolicy: IfNotPresent
     ports:
     - containerPort: 80
    """
    dp_user_yaml = db.format(current_user.username)
            
