import requests
from selenium import webdriver
from pyquery import PyQuery as pq
import time
import re

USERNAME = "17816787010"
PASSWORD ""

def toutiao_login():
    login_url = "https://sso.toutiao.com/"
    browser = webdriver.Chrome()
    browser.get(login_url)
    MobileLogin = browser.find_element_by_id("login-type-mobile")
    MobileLogin.click()
    username = browser.find_element_by_id("user-name")
    username.send_keys(USERNAME)
    passwd = browser.find_element_by_id("password")
    passwd.send_keys(PASSWORD)