#coding:utf-8
import time,random
from crawler.autohome_content_selenium import  getTitleBBSContent
from crawler.autohome_gettopiclist_selenium import  getpagecount 
from crawler.autohome_gettopiclist_selenium import  getBBSTitleUrlList 

def getTotalBBSContent(url,title):
    #循环遍历荣威论坛页所有文章链接，分页循环获取
    count=getpagecount(url)
    print(title+'一共多少页='+str(count))
    for i in range(count):
        sleepsecs=random.random()*5+random.random()*9
        print('爬取下个页面前sleep'+str(sleepsecs)+'秒')
        time.sleep(sleepsecs)
        titleItemList=getBBSTitleUrlList(url,i)
        if titleItemList is None:
            print('第'+str(i)+'页titleItemList是none,没有获取到标题文章url数据')
            continue
            
        for index,i in enumerate(titleItemList):
            titleitem=titleItemList[index]
            print('第'+str(index)+'个标题文章url如下')
            titleurl=titleitem['titleurl']  
            print(titleurl)
            #循环访问每篇文章链接中的评论消息，分页循环获取
            getTitleBBSContent(titleurl)
            
    
    
if __name__=='__main__':
    #title1='荣威MARVEL X论坛'
    #url1='https://club.autohome.com.cn/bbs/forum-c-4653-1.html'
    title='荣威RX5论坛页'
    url='https://club.autohome.com.cn/bbs/forum-c-4080-1.html'   
    getTotalBBSContent(url,title)
    



