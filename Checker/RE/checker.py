import string
import re
def id_code(resp):
    pat="[1-9]\d{5}(?:19|20)\d\d(?:0[1-9]|1[012])(?:0[1-9]|[12]\d|3[01])\d{4}"
    res= re.findall(pat,resp)
    print('检测到身份证信息:'+str(res))
def phone_number(resp):
    pat="1((3[\d])|(4[5679])|(5[0-35-9])|(6[5-7])|(7[0-8])|(8[\d])|(9[189]))\d{8}"
    res= re.findall(pat,resp)
    print('检测到手机号信息:'+str(res))
def bank_id(resp):
    pat="([1-9]{1})(\d{15}|\d{18})"
    res= re.findall(pat,resp)
    print('检测到银行卡信息:'+str(res))
def email(resp):
    pat="\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*"
    res= re.findall(pat,resp)
    print('检测到邮箱信息:'+str(res))
def name(resp):
    pat="([\u4e00-\u9fa5·]{210})"
    res= re.findall(pat,resp)
    print('检测到中文姓名:'+str(res))



def checker(resp):
    phone_number(resp)
    id_code(resp)
    bank_id(resp)

testtext = 'address=132456123456&phone=17816783700'
checker(testtext)
