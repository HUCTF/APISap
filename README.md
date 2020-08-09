
[![](https://sourcerer.io/fame/Sierra007117/HUCTF/2020-Works-ApiSecurity/images/0)](https://sourcerer.io/fame/Sierra007117/HUCTF/2020-Works-ApiSecurity/links/0)[![](https://sourcerer.io/fame/Sierra007117/HUCTF/2020-Works-ApiSecurity/images/1)](https://sourcerer.io/fame/Sierra007117/HUCTF/2020-Works-ApiSecurity/links/1)[![](https://sourcerer.io/fame/Sierra007117/HUCTF/2020-Works-ApiSecurity/images/2)](https://sourcerer.io/fame/Sierra007117/HUCTF/2020-Works-ApiSecurity/links/2)[![](https://sourcerer.io/fame/Sierra007117/HUCTF/2020-Works-ApiSecurity/images/3)](https://sourcerer.io/fame/Sierra007117/HUCTF/2020-Works-ApiSecurity/links/3)[![](https://sourcerer.io/fame/Sierra007117/HUCTF/2020-Works-ApiSecurity/images/4)](https://sourcerer.io/fame/Sierra007117/HUCTF/2020-Works-ApiSecurity/links/4)[![](https://sourcerer.io/fame/Sierra007117/HUCTF/2020-Works-ApiSecurity/images/5)](https://sourcerer.io/fame/Sierra007117/HUCTF/2020-Works-ApiSecurity/links/5)[![](https://sourcerer.io/fame/Sierra007117/HUCTF/2020-Works-ApiSecurity/images/6)](https://sourcerer.io/fame/Sierra007117/HUCTF/2020-Works-ApiSecurity/links/6)[![](https://sourcerer.io/fame/Sierra007117/HUCTF/2020-Works-ApiSecurity/images/7)](https://sourcerer.io/fame/Sierra007117/HUCTF/2020-Works-ApiSecurity/links/7)

## 如何贡献/更新代码 [How to contribute]

1. fork一份到本地仓库 [Fork this repository and clone it to local from remote repository]
2. 添加你需要的内容，更新到自己的库中 [Make your desired changes and push updates on a new branch]
3. 先提交issue [Submit an issue before you create a pull request]
4. 再提交pr [Create a pull request]
5. 成员review考虑是否合并到库中 [A project maintainter will check and merge it to the main branch]

## API安全检测整合数据集 [API security detection integration data set]

**实验环境** [Development environmen]

python3+

### web爬虫 [Web crawler(Spider)]

1. selenium， requests爬虫获取页面内所有的url链接(js, css等) [Selenium, requests crawler to get all url links in the page (js, css, etc.)]



### 数据包分析 [Packet analysis]

1. scapy获取网卡数据包 [scapy gets the NIC packet]
2. 编写数据包过滤脚本，获得目标链接 [Write a packet filtering script to get the target link]



### 手机端API安全检测 [Mobile terminal API security detection]

1. mitmproxy，requests实现爬虫获取页面内所有外链(js, css等) [mitmproxy, requests to achieve crawlers to get all the external links in the page (js, css, etc.)]



**文件类型** [File System]

将url整合到txt文件中 [Integrate url into txt file]

## 文本分析 [Text Analysis]

1. 文本分析(敏感词：用户名，手机号，地址，身份证，年龄，学号等) [Text analysis (sensitive words: user name, mobile phone number, address, ID card, age, student number, etc.]
2. 安全验证及其评级(3个等级 高，低，中) [Safety verification and its rating (3 levels high, low, medium)]



## 提供API安全接口服务 [Provide API security interface service]

1. 编写加密算法(RSA) [Write encryption algorithm (RSA)]
2. 需要前端和后端提供控制台服务 [Requires front-end and back-end to provide console services]











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

