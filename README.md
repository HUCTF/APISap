## 如何贡献/更新代码

1. fork一份到本地仓库
2. 添加你需要的内容，更新到自己的库中
3. 先提交issue
4. 再提交pr
5. 成员review考虑是否合并到库中

## API安全检测整合数据集

**实验环境**

python3+

### web爬虫

1. selenium， requests爬虫获取页面内所有的url链接(js, css等)



### 数据包分析

1. scapy获取网卡数据包
2. 编写数据包过滤脚本，获得目标链接



### 手机端API安全检测

1. mitmproxy，requests实现爬虫获取页面内所有外链(js, css等)



**文件类型**

将url整合到txt文件中

## 文本分析

1. 文本分析(敏感词：用户名，手机号，地址，身份证，年龄，学号等)
2. 安全验证及其评级(3个等级 高，低，中)



## 提供API安全接口服务

1. 编写加密算法(RSA)
2. 需要前端和后端提供控制台服务











-----------------------
```bash
e.g.
url:https://www.baidu.com
method:GET/POST
data:Accept:*/*
	Cache-Control:no-cache
	Connection:keep-alive
	Content-Length:438
	Host:seeds-darwin.xycdn.com
	Pragma:no-cache
	{"url":"m701.music.126.net/20200316195545/035eed50001bed1d8ce2ecdbf5d161f9/jdyyaac/015a/510e/0f0b/600184ef5cfd9ca30f398a27dbbfefb2.m4a","surl":"https://m701.music.126.net/20200316195545/035eed50001bed1d8ce2ecdbf5d161f9/jdyyaac/015a/510e/0f0b/600184ef5cfd9ca30f398a27dbbfefb2.m4a?xyop=2","sid":"9eec9f81d374fceeb66826135a2af3b64e2e185e66cfaf2b6cee90b465e34395","fs":4245477,"ofs":424576,"nt":0,"type":"sdk","ver":"1.5.99","peer_status":[]}

===
```



