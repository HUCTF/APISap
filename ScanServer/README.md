## 运行ScanServer

**环境要求**

Windows

Python3.5+

------------------
**运行**
请新建一个``scanserver``数据库

```bash
cd /opt
git clone https://github.com/HUCTF/2020-Works-ApiSecurity
cd 2020-Works-ApiSecurity
pip install -r requirement.txt

set FLASK_APP=ScanServer
flask initdb
flask run
```
启动成功后访问 <http://localhost:5000>
