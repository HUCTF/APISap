import requests
import time
import re
import base64
import json
# 无头浏览器模块

def find_cookies(Url, username, password):
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


def RUN_COOKIE(url, cookie):
    '''
    :param url:扫描url
    :param type:1为cookie，2为用户名密码
    :return:
    '''
    #https://jkxxcj.zjhu.edu.cn/
    global base_url
    #base_url = input("基础url:")
    #login_url = input("登入接口url:")
    base_url= url
    login_url = url
    cof = cookie.split("=")
    cookie={
        cof[0]:cof[1]
    }
    # print(find_url(s_find(url, cookie)))
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
        print(x)
        if (url_repeat(str(x),OLD_URL)):
            # print('链接:' + str(x))
            UN_URL = UN_URL +find_url(s_find(str(x), cookie))
            OLD_URL.append(str(x))
        else:
            UN_URL.pop(0)
    print(OLD_URL)

