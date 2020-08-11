from . import client

def address(text):
#    text = '''
#        {
#            'id':'0001',
#            'text':'address',
#            'name':'张三',
#            'address':'浙江省湖州市吴兴区龙泉街道学士路21号'
#        }
#    '''


    t = client.address(text)

    # print("===============")
    try:
        del t['log_id']
        del t['text']
        del t['town']
        del t['detail']
        del t['town_code']
        del t['county_code']
        del t['city_code']
    except:
        print('',end='')
    print(t)
    return t