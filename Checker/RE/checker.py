import string
import re
def id_code(resp):
    pat="[1-9]\d{5}(?:19|20)\d\d(?:0[1-9]|1[012])(?:0[1-9]|[12]\d|3[01])\d{4}"
    res= re.findall(pat,resp)
    print(res)
def phone_number(resp):
    pat="(1(([35789]\d)|(47))\d{8})"
    res= re.findall(pat,resp)
    print(res)
#def home_address(resp):
def checker(resp):
    phone_number(resp)
    id_code(resp)
checker("330424199901011122233aaaaaa hyluz17816783987")