## 运行ScanServer

**环境要求**

Windows

Python3.5+

------------------
**初始化**

新建apiserver数据库

**运行**

```bash
git clone https://github.com/HUCTF/2020-Works-ApiSecurity
cd 2020-Works-ApiSecurity/ApiSecurity
pip install -r requirement.txt

python3 manager.py reset_db	# 重置数据库
python3 manager.py init_db	# 数据库初始化
python3 manager.py set_user [username] [email] [password] # 添加新用户
python3 manager.py runserver	# 启动服务 0.0.0.0:5000
```
启动成功后访问 <http://localhost:5000>
