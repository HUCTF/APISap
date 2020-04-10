import requests
from selenium import webdriver
from pyquery import PyQuery as pq
import time
import re
import json
# 无头浏览器模块
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def find_cookies(WebServer):
    # WebServer = "http://jkxxcj.zjhu.edu.cn/"
    # 无头浏览器浏览
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(WebServer)

    s = requests.session()
    r = s.get(browser.current_url)
    params = re.compile('id="(.*?)"',re.S)
    result = re.findall(params, r.text)

    login_url = browser.current_url
    # return 登入接口用于post检验
    userid = browser.find_element_by_id('zgh')
    time.sleep(1)
    userid.send_keys("2018283120")
    
    passwd = browser.find_element_by_id('mm')
    time.sleep(1)
    passwd.send_keys("1234qwer")
    
    button = browser.find_element_by_id('loginBtn')
    try:
        button.click()
        print("Success Login")
    except:
        print("Login Fail! Please try again!")

    time.sleep(1)

    cookies_msg = {}
    Cookies = {}

    try:
        # msg = {}
        for j in browser.get_cookies():
            msg = j
        for i in msg:
            if i == 'name':
                cookies_msg[i]=msg[i]
            if i == 'value':
                cookies_msg[i]=msg[i]
            # print(i, msg[i])
        
        Cookies[cookies_msg['name']] = cookies_msg['value']
            
    except:
        print("get_cookies error")
    
    browser.close()
    return Cookies, login_url


def complete_url(url): #自动补全urls
    if(re.match('http',url)):
        return url
    else:
        base_url = 'http://jkxxcj.zjhu.edu.cn/'
        return base_url+url

def url_repeat(url,array): #url查重 如果不重复返回1
    flag = False
    for y in array:
        if (str(url)) == str(y):
            flag = True
        else:
            flag = False
    if (flag == False):
        return 1



def s_find(url, cookie):
    surl=url
    # cookie = {"JSESSIONID":'MWQxY2ExYmItYjMxYy00MjU1LWE2ODktYzRhNzU4ZGY4OTNh'}
    res = requests.get(url=surl,cookies=cookie)
    return res.text

def find_url(html):  #查找返回的a标签链接
    from bs4 import BeautifulSoup
    # 解析成文档对象
    soup = BeautifulSoup(html, 'html.parser')  # 文档对象
    # 非法URL 1
    invalidLink = ['#' ]
    # 集合
    result = []
    # 计数器
    mycount = 0
    # 查找文档中所有a标签
    for k in soup.find_all('a'):
        # 查找href标签
        link = k.get('href')
        # 过滤没找到的
        if (link is not None):
            # 过滤非法链接
            if link in invalidLink:
                pass
            elif re.match('javascript',link,re.IGNORECASE):
                pass
            else:
                mycount = mycount + 1
                if(url_repeat(complete_url(link),result)):
                    result.append(complete_url(link))
    # print("打印超链接个数:", mycount)
    return result


def post_login(url):
    s = requests.session()
    data = {
        'ZGH': 'Base64MjAxODI4MzEyMA==',
        'MM': '1234qwer'
    }
    
    r = s.post(url, data=data)
    # print(r.text)
    
    return r.text
    

def RQRUN():
    OLD_URL = []
    UN_URL = []
    url = 'http://jkxxcj.zjhu.edu.cn/serviceList.html'
    msg_cookies = find_cookies("http://jkxxcj.zjhu.edu.cn/login.html")
    cookie = msg_cookies[0]
    login_url = msg_cookies[1]
    base_url = 'http://jkxxcj.zjhu.edu.cn/'
    UN_URL = find_url(s_find(url, cookie))
    OLD_URL.append(url)
    OLD_URL.append(login_url)
    for x in UN_URL:
        if (url_repeat(str(x),OLD_URL)):
            # print('链接:' + str(x))
            UN_URL = UN_URL +find_url(s_find(str(x), cookie))
            OLD_URL.append(str(x))
        else:
            UN_URL.pop(0)
            # print(UN_URL)
    print(OLD_URL)
    print(login_url)
    print(post_login("http://jkxxcj.zjhu.edu.cn/yhb/login"))

# # s_find()
# if __name__ == "__main__":
#     OLD_URL = []
#     UN_URL = []
#     url = 'http://jkxxcj.zjhu.edu.cn/serviceList.html'
#     msg_cookies = find_cookies("http://jkxxcj.zjhu.edu.cn/login.html")
#     cookie = msg_cookies[0]
#     login_url = msg_cookies[1]
#     base_url = 'http://jkxxcj.zjhu.edu.cn/'
#     UN_URL = find_url(s_find(url, cookie))
#     OLD_URL.append(url)
#     OLD_URL.append(login_url)
#     for x in UN_URL:
#         if (url_repeat(str(x),OLD_URL)):
#             # print('链接:' + str(x))
#             UN_URL = UN_URL +find_url(s_find(str(x), cookie))
#             OLD_URL.append(str(x))
#         else:
#             UN_URL.pop(0)
#             # print(UN_URL)
#     print(OLD_URL)
#     print(login_url)
#     print(post_login("http://jkxxcj.zjhu.edu.cn/yhb/login"))