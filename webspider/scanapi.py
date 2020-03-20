import requests
from selenium import webdriver
from pyquery import PyQuery as pq
import time
import re

WebServer = "http://jkxxcj.zjhu.edu.cn/"

browser = webdriver.Chrome()
browser.get(WebServer)

s = requests.session()
# r = requests.get(browser.current_url)
r = s.get(browser.current_url)
params = re.compile('id="(.*?)"',re.S)
result = re.findall(params, r.text)

print(result)
# print(browser.page_source)
print(browser.current_url)
doc = pq(browser.page_source)
# items = doc('')

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
# print(browser.page_source)
print(browser.current_url)
# for i in browser.get_cookies():
    # cookies = i


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
# r = requests.get(browser.current_url, cookies=cookies)
r = s.get(browser.current_url, cookies=Cookies)
# params = re.compile('id="(.*?)"',re.S)
params = re.compile('href="(.*?).html"',re.S)
result = re.findall(params, r.text)
print(result)
MainServer = browser.current_url
time.sleep(1)
main_handle = browser.current_window_handle
Logout = ['logout', 'login', 'login.html']

for i in result:
    if i.lower() not in Logout:
        try:
            print(i)
            browser.get(MainServer)
            # button_a = browser.find_element_by_id(i)
            # button_a.click()
            # js = 'window.open("%s");' % browser.current_url
            js = 'window.open("%s");' % (WebServer + i + '.html')
            browser.execute_script(js)
            print(i, browser.current_url)
            time.sleep(1) 
            browser.back()
            time.sleep(1)
        except:
            print('next')
time.sleep(1)

handles = browser.window_handles # 获取当前窗口句柄集合（列表类型）
# for i in handles:
#     time.sleep(1)
#     print(i)
#     browser.switch_to.window(i)

browser.switch_to.window(handles[0])

# print(browser)