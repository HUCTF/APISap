import difflib
import Levenshtein#python-Levenshtein

str1 = '{"cleanCache":false,"id":"9ED676EFEA73E2FCE055000000000001","mm":"25110CAABBB4B66D42ED09665DC32C3A","zjhm":"330281200005128217","zgh":"2018283303","xm":"俞鸿权","lxdh":"17816783700","sfqy":"1","sfxgmm":"1","bjid":null,"xslbid":"1","bjmc":"20182831","xnqs":"17幢507","jtszd":"阳明街道鲤鱼山庄","sftxg":"1","xyid":"0020","yhlx":"student","sfid":"31/浙江","csid":"388/宁波","qyid":"3285/余姚市"}'
str2 = '{"cleanCache":false,"id":"9ED676EFEA5AE2FCE055000000000001","mm":"FA5CD106598C5B7477B0269638A187BA","zjhm":"340321200008015630","zgh":"2018283120","xm":"汤会枫","lxdh":"17816787010","sfqy":"1","sfxgmm":"1","bjid":null,"xslbid":"1","bjmc":"20182831","xnqs":"17—504","jtszd":"椒江区","sftxg":"1","xyid":"0020","yhlx":"student","sfid":"31/浙江","csid":"390/台州","qyid":"3296/椒江区"}'

def similarity(str1,str2):
    # 1. difflib
    seq = difflib.SequenceMatcher(None, str1, str2)
    ratio = seq.ratio()
    # print('difflib similarity1: ', ratio)
    #返回的结果超过0.6就算很相似。目前做近义词词典就是借助相似度自动化来实现。

    # 3. 编辑距离，描述由一个字串转化成另一个字串最少的操作次数，在其中的操作包括 插入、删除、替换
    sim1 = Levenshtein.distance(str1, str2)
    # print('Levenshtein similarity: ', sim1)

    # 4.计算莱文斯坦比
    sim2 = Levenshtein.ratio(str1, str2)
    # print('Levenshtein.ratio similarity: ', sim2)

    # 5.计算jaro距离
    sim3 = Levenshtein.jaro(str1, str2)
    # print('Levenshtein.jaro similarity: ', sim3)

    # 6. Jaro–Winkler距离
    sim4 = Levenshtein.jaro_winkler(str1, str2)
    # print('Levenshtein.jaro_winkler similarity: ', sim4)

    if ratio>0.6 or sim1 <50 or ((sim2+sim3+sim4)/3)>0.8:
        return True


print(similarity(str1,str2))
