import requests
from selenium import webdriver
from pyquery import PyQuery as pq
import time
import re
WebServer = "http://jkxxcj.zjhu.edu.cn/"

def selenium_login(WebServer):
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
    return Cookies, browser ,s
OLDER_URL = []

def get_url(s, browser, Cookies):
    r = s.get(browser.current_url, cookies=Cookies)
    # params = re.compile('id="(.*?)"',re.S)
    params = re.compile('href="(.*?)"',re.S)
    result = re.findall(params, r.text)
    # print(result)
    MainServer = browser.current_url
    time.sleep(1)
    Logout = ['logout', 'login', 'login.html', 'javascript:void(0);','javascript:history.back(-1);','javascript:void(0)','#',browser.current_url.split("/")[-1]]
    OLDER_URL.append(browser.current_url.split("/")[-1])
    print(OLDER_URL)
    for i in result:
        if i.lower() not in Logout and i not in OLDER_URL:
            try:
                windows = browser.window_handles
                browser.switch_to.window(windows[0])
                browser.get(MainServer)
                # js = 'window.open("%s");' % (WebServer + i )
                # browser.execute_script(js)
                browser.get(WebServer + i)
                print(i, browser.current_url)
                get_url(s, browser, Cookies)
                time.sleep(1) 
                # browser.close()
                # time.sleep(1)
            except:
                print(i, 'error go next')

# time.sleep(1)

if __name__ == "__main__":
        
    login_msg = selenium_login(WebServer)
    Cookies = login_msg[0]
    browser = login_msg[1]
    s = login_msg[2]
    get_url(s, browser, Cookies)
    windows = browser.window_handles
    browser.switch_to.window(windows[0])



# def get_deep_url(browser):

