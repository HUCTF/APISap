import requests
from selenium import webdriver
from pyquery import PyQuery as pq
import time
import re
import json

def find_cookies(WebServer):
    # WebServer = "http://jkxxcj.zjhu.edu.cn/"

    browser = webdriver.Chrome()
    browser.get(WebServer)

    s = requests.session()
    # r = requests.get(browser.current_url)
    r = s.get(browser.current_url)
    params = re.compile('id="(.*?)"',re.S)
    result = re.findall(params, r.text)

    doc = pq(browser.page_source)
    
    login_url = browser.current_url
    # return 登入接口用于post检验

    userid = browser.find_element_by_id('zgh')
    userid.send_keys("2018283120")
    time.sleep(1)
    passwd = browser.find_element_by_id('mm')
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



def s_find(url, cookie):
    surl=url
    # cookie = {"JSESSIONID":'MWQxY2ExYmItYjMxYy00MjU1LWE2ODktYzRhNzU4ZGY4OTNh'}
    res = requests.get(url=surl,cookies=cookie)
    return res.text

def find_url(html):
    from bs4 import BeautifulSoup
    # 解析成文档对象
    soup = BeautifulSoup(html, 'html.parser')  # 文档对象
    # 非法URL 1
    invalidLink1 = '#'
    # 非法URL 2
    invalidLink2 = 'javascript:void(0)'
    # 集合
    result = set()
    # 计数器
    mycount = 0
    # 查找文档中所有a标签
    for k in soup.find_all('a'):
        # 查找href标签
        link = k.get('href')
        # 过滤没找到的
        if (link is not None):
            # 过滤非法链接
            if link == invalidLink1:
                pass
            elif link == invalidLink2:
                pass
            elif re.match('javascript',link,re.IGNORECASE):
                pass
            else:
                mycount = mycount + 1
                result.add(link)
    print("打印超链接个数:", mycount)
    for a in result:
        print(a + "\n")
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
    


# s_find()
if __name__ == "__main__":
    url = 'http://jkxxcj.zjhu.edu.cn/serviceList.html'
    msg_cookies = find_cookies("http://jkxxcj.zjhu.edu.cn/")
    cookie = msg_cookies[0]
    login_url = msg_cookies[1]
    base_url = 'http://jkxxcj.zjhu.edu.cn/'
    for i in find_url(s_find(url, cookie)):
        # find_url(s_find(base_url+i, cookie))
        print(i)
    print(login_url)
    print(post_login("http://jkxxcj.zjhu.edu.cn/yhb/login"))