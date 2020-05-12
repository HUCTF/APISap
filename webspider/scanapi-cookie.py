import requests
from selenium import webdriver
from pyquery import PyQuery as pq
import time
import re
import base64
import json
# 无头浏览器模块
from selenium.webdriver.chrome.options import Options

def find_cookies(Url, username, password):
    # WebServer = "http://jkxxcj.zjhu.edu.cn/"
    # 无头浏览器浏览
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # browser = webdriver.Chrome(chrome_options=chrome_options)
    # browser = webdriver.Chrome()
    # browser.get(WebServer)

    # s = requests.session()
    # r = s.get(browser.current_url)
    # params = re.compile('id="(.*?)"',re.S)
    # result = re.findall(params, r.text)

    # login_url = browser.current_url
    # # return 登入接口用于post检验
    # userid = browser.find_element_by_id('zgh')
    # time.sleep(1)
    # userid.send_keys("2018283120")
    
    # passwd = browser.find_element_by_id('mm')
    # time.sleep(1)
    # passwd.send_keys("1234qwer")
    
    # button = browser.find_element_by_id('loginBtn')
    # try:
    #     button.click()
    #     print("Success Login")
    # except:
    #     print("Login Fail! Please try again!")

    # time.sleep(30)
    #
    # cookies_msg = {}
    # Cookies = {}
    #
    # try:
    #     msg = {}
        # for j in browser.get_cookies():
        #     msg = j
        # for i in msg:
        #     if i == 'name':
        #         cookies_msg[i]=msg[i]
        #     if i == 'value':
        #         cookies_msg[i]=msg[i]
            # print(i, msg[i])
        
        # Cookies[cookies_msg['name']] = cookies_msg['value']
            
    # except:
    #     print("get_cookies error")
    #
    # browser.close()
    header={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            }
    data= {'ZGH':'Base64'+str(base64.b64encode(username.encode("utf-8")))[2:-1],
           'MM':password
           }
    try:
        res = requests.post(Url + '/yhb/login', data=data, headers=header)
        cookies = res.cookies.items()

        cookie = ''
        for name, value in cookies:
            cookie += '{0}={1}'.format(name, value)
        return cookie
    except Exception as err:
        print('获取cookie失败：\n{0}'.format(err))

def complete_url(url): #自动补全urls
    if(re.match('http',url)):
        return url
    else:
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
    # cookie = {"JSESSIONID":'MWQxY2ExYmItYjMxYy00MjU1LWE2ODktYzRhNzU4ZGY4OTNh'}
    res = requests.get(url=url,cookies=cookie)
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

    


# s_find()
# if __name__ == "__main__":
#     OLD_URL = []
#     UN_URL = []
#     # url = 'https://jkxxcj.zjhu.edu.cn/serviceList.html'
#     url = input("主页url:")
#     base_url = input('base_url:')
#     login_url = input("登入接口url:")
#     msg_cookies = find_cookies(login_url)
#     cookie = msg_cookies[0]
#     login_url = msg_cookies[1]
#     # base_url = 'https://jkxxcj.zjhu.edu.cn/'
#     UN_URL = find_url(s_find(url, cookie))
#     OLD_URL.append(url)
#     OLD_URL.append(login_url)
#     for x in UN_URL:
#         if (url_repeat(str(x),OLD_URL)):
#             UN_URL = UN_URL +find_url(s_find(str(x), cookie))
#             OLD_URL.append(str(x))
#         else:
#             UN_URL.pop(0)


def RUN_COOKIE(url, type, cookie, useranme, password):
    '''
    :param url:扫描url
    :param type:1为cookie，2为用户名密码
    :return:
    '''https://jkxxcj.zjhu.edu.cn/
    url = url
    global base_url
    base_url = input("基础url:")
    login_url = input("登入接口url:")
    if type == 1:
        cof = cookie.split("=")
        Cookie={
            cof[0]:cof[1]
        }
        cookie = Cookie
    else:
        cof = find_cookies(base_url,useranme,password).split("=")
        Cookie = {
            cof[0]: cof[1]
        }
        cookie = Cookie
    print(find_url(s_find(url, cookie)))
    OLD_URL = []
    UN_URL = []
    # url = 'https://jkxxcj.zjhu.edu.cn/serviceList.html'
    # url = input("主页url:")
    # msg_cookies = find_cookies(url)
    # cookie = msg_cookies[0]
    # login_url = msg_cookies[1]
    # base_url = 'https://jkxxcj.zjhu.edu.cn/'
    UN_URL = find_url(s_find(url, cookie))
    OLD_URL.append(url)
    OLD_URL.append(url)
    for x in UN_URL:
        if (url_repeat(str(x),OLD_URL)):
            # print('链接:' + str(x))
            UN_URL = UN_URL +find_url(s_find(str(x), cookie))
            OLD_URL.append(str(x))
        else:
            UN_URL.pop(0)

RUN_COOKIE('https://jkxxcj.zjhu.edu.cn/serviceList.html',2,None,'2018283303','yhq20000512')

RUN_COOKIE('https://jkxxcj.zjhu.edu.cn/serviceList.html',1,'health-data-Id=MGQ0MTM0YmQtMWQ2NC00MGViLTkzMGMtODNkZDM4ODU3YjJi',None,None)