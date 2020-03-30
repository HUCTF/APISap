import string
import re
#def id_code(resp):
def phone_number(resp):
    pat=r"(1(([35789]\d)|(47))\d{8})"
    res= re.findall(pat,resp)
    print(res)
#def home_address(resp):
#def checker(resp):
phone_number("dfad14735354568fewdf13135354568klmdfa17816783987")