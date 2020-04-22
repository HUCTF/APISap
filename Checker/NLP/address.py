from . import client

def address():
    text = '''
        {
            'id':'0001',
            'text':'address',
            'name':'张三',
            'address':'浙江省湖州市吴兴区龙泉街道学士路21号'
        }
    '''


    t = client.address(text)
    print(t)
