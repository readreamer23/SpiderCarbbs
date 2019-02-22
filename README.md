# SpiderCarbbs
python版本: 3.5

1. 项目概述
  爬取汽车之家文章评论相关数据


2.安装依赖库

```shell
pip install -r  requirements.txt
```

3. autohome_bbs_whole  一个脚本实现从车型大类论坛总入口到每篇文章所有数据的抓取,selenium客户端打开浏览器形式(windows)

4.爬取汽车之家论坛评论数据--分多个文件抽离方法
   autohome_bbs_total_selenium     执行爬取入口文件
   autohome_gettopiclist_selenium  爬取每页每篇文章标题，Url
   autohome_content_selenium       爬取每篇文章所有分页评论数据

5.爬取汽车之家口碑数据      autohome_koubei_firefox_all
	   
	
6. headless目录：Linux环境运行无客户端selenium唤起浏览器爬虫脚本
	
	
7.mongodb下载地址	
	https://www.mongodb.com
	
8.作者联系方式
  QQ :  1140093856
     邮箱:  lihui1919@sina.com	
     
     