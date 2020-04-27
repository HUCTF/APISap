import string
import re
def id_code(resp):
    pat="\d{18}|\d{17}X"
    res= re.findall(pat,resp)
    if res:
        print('检测到疑似身份证信息:'+str(res))
def phone_number(resp):
    pat="1((3[\d])|(4[5679])|(5[0-35-9])|(6[5-7])|(7[0-8])|(8[\d])|(9[189]))\d{8}"
    res= re.findall(pat,resp)
    if res:
        print('检测到疑似手机号信息:'+str(res))
def bank_id(resp):
    pat="([1-9]{1})(\d{15}|\d{18})"
    res= re.findall(pat,resp)
    if res:
        print('检测到疑似银行卡信息:'+str(res))
def email(resp):
    pat="\w+@[a-z0-9]+\.[a-z]+"
    res= re.findall(pat,resp)
    if res:
        print('检测到疑似邮箱信息:'+str(res))
def name(resp):
    pat="([\u4e00-\u9fa5·]{210})"
    res= re.findall(pat,resp)
    if res:
        print('检测到疑似中文姓名:'+str(res))
def address(resp):
    pat="[\u4e00-\u9fa5]{0,}(省|市|自治区|自治州|县|区)"
    res= re.findall(pat,resp)
    if res:
        print('检测到疑似地址:'+str(res))




def checker(resp):
    phone_number(resp)
    id_code(resp)
    bank_id(resp)
    email(resp)
    name(resp)
    address(resp)

testtext = '{"cleanCache":false,"id":"9ED676EFEA73E2FCE055000000000001",1732500265@qq.com"mm":"25110CAABBB4B66D42ED09665DC32C3A","zjhm":"33028120000512821X","zgh":"2018283303","xm":"俞鸿权","lxdh":"17816783700","sfqy":"1","sfxgmm":"1","bjid":null,"xslbid":"1","bjmc":"20182831","xnqs":"17幢507","jtszd":"阳明街道鲤鱼山庄","sftxg":"1","xyid":"0020","sfid":"31/浙江","csid":"388/宁波","qyid":"3285/余姚市","yhlx":"student"}'
checker(testtext)
