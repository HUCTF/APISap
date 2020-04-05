import requests
from selenium import webdriver
from pyquery import PyQuery as pq
import time
import re
WebServer = "https://hacking.kaiyuanshe.cn"
USERNAME = "XXXXXXXXX"
PASSWORD = "XXXXXXXXX"

def selenium_login(WebServer):
    Login_url = WebServer + '/login?return_url=%2F'
    browser = webdriver.Chrome()
    browser.get(Login_url)

    s = requests.session()
    # r = requests.get(browser.current_url)
    r = s.get(browser.current_url)
    params = re.compile('id="(.*?)"',re.S)
    result = re.findall(params, r.text)

    button = browser.find_element_by_class_name('btn-github')
    try:
        button.click()
        print("Success Login")
    except:
        print("Login Fail! Please try again!")

    userid = browser.find_element_by_id('login_field')
    userid.send_keys(USERNAME)
    passwd = browser.find_element_by_id('password')
    passwd.send_keys(PASSWORD)
    button_github = browser.find_element_by_class_name('btn-primary')
    try:
        button_github.click()
        print('GitHub Success Login!')
    except:
        print("Login Fail! Please try again!")
        
    button_index = browser.find_element_by_class_name('btn-activity')
    try:
        button_index.click()
        # print('')
    except:
        pass
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
result = []

def get_url(s, browser, Cookies):
    r = s.get(browser.current_url, cookies=Cookies)
    # params = re.compile('id="(.*?)"',re.S)
    params = re.compile('href="(.*?)"',re.S)
    res = re.findall(params, r.text)
    STATIC = ['jpg', 'css', 'js', 'png']
    print("===========result===========")
    for i in res:
        if i.split('.')[-1:][0] not in STATIC:
            print(i, i.split('.')[-1:][0])
            result.append(i)

    print(result)
    MainServer = browser.current_url
    # MainServer = 'https://hacking.kaiyuanshe.cn/index'
    print("===========current_url==========\n",browser.current_url)
    time.sleep(1)
    Logout = ['logout', '/landing', 'login', 'login.html', 'javascript:void(0);','javascript:history.back(-1);','javascript:void(0)','#',browser.current_url.split("/")[-1]]
    
    # OLDER_URL.append(browser.current_url.split("/")[-1])
    if '/'+'/'.join(browser.current_url.split('/')[3:]) not in OLDER_URL:
        # print('/'+'/'.join(browser.current_url.split('/')[3:]))
        OLDER_URL.append('/'+'/'.join(browser.current_url.split('/')[3:]))
    print("============OLDER===============", OLDER_URL)
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

