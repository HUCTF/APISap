import requests
from selenium import webdriver
from pyquery import PyQuery as pq
import time
import re

USERNAME = "17816787010"
PASSWORD = "thf1290017556"




# def csdn_login():
login_url = "https://passport.csdn.net/login?code=public"
options = webdriver.ChromeOptions()
options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"')
browser = webdriver.Chrome(chrome_options=options)
browser.get("https://passport.csdn.net/login?code=public")
MobileLogin = browser.find_element_by_css_selector("#app > div > div > div.main > div.main-login > div.main-select > ul > li:nth-child(2)")
MobileLogin.click()
username = browser.find_element_by_id("all")
username.send_keys(USERNAME)
passwd = browser.find_element_by_id("password-number")
passwd.send_keys(PASSWORD)
time.sleep(1)
button = browser.find_element_by_class_name("btn-primary")
try:
    time.sleep(1)
    button.click()
    time.sleep(5)
    print("Success Login!")
except:
    print("Login Fail!")
time.sleep(1)
browser.get("https://mp.csdn.net/console/article")
time.sleep(1)
    

# csdn_login()