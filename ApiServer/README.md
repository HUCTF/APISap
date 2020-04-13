## 运行ScanServer

**环境要求**

Windows

Python3.5+

------------------
**运行**
```bash
git clone https://github.com/HUCTF/2020-Works-ApiSecurity
cd 2020-Works-ApiSecurity/ApiSecurity
pip install -r requirement.txt

set FLASK_APP=ApiServer
flask initdb
flask run
```
启动成功后访问 <http://localhost:5000>
