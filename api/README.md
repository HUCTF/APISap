## 运行ApiServer
**环境要求**
Python3.5+
Mysql

------------------
**设置数据库**
在sql_operation.py中完成数据库的设置
```python
engine = create_engine('mysql://123456:123456@localhost:3306/token1?charset=utf8', echo=True)
```

**api服务运行**
```bash
cd 2020-Works-ApiSecurity/api
pip install -r requirement.txt
python api.py
```
**api服务测试**  
在本地搭建的情况下可以直接运行test.py测试  
在远程服务器上搭建的情况下修改test.py中的127.0.0.1为服务器ip地址后进行测试
