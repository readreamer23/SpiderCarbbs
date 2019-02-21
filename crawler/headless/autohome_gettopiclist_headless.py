#coding:utf-8
from bs4 import BeautifulSoup
import sys
import time,random
from crawler.mongoutil import insertMongo2
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options


options = Options() 
options.add_argument('-headless') 
browser = webdriver.Firefox( firefox_options=options) 
print(browser.page_source) 
wait = WebDriverWait(browser, 8)


#爬取所有分页评论相关内容
def getBBSTitleUrlList(url,i):
    #拼接url： pvareaid是动态id,后期需研究汽车之家的id获取规则
    if i>1:
        url=url.replace('1.html', str(i)+'.html'+'?qaType=-1#pvareaid='+'101061')
    
    print(url)
    #res=configutil.getResponseRetry(url)
    #res=configutil.getResponse(url)
    #content=res.text
    
    browser.get(url)
    content = browser.page_source
    soup=BeautifulSoup(content,'html.parser')
    print('----------------------------------')
    print('--获取网页对象res如下:')
    divs = soup.find("div", attrs={"id":"subcontent"}) 
    if divs is None:
        print(url+'  获取divs是None,爬取页面没有返回数据')
        return
    
    topics=divs.find_all(class_="a_topic")
    print('获取a_topic列表是----------------------------------')
    linkitems={}
    for index,t in enumerate(topics):
        item={}
        item['totaltitleurl']=url  #论坛大类url
        item['title']=t.text.replace(' ','').replace('\r\n','').replace('\n','')
        item['titleurl']='https://club.autohome.com.cn'+t['href']
        linkitems[index]=item
        insertMongo2(item)
        print(item) 
           
    return linkitems  
     
     
     
#获取评论分页个数
def getpagecount(url):
    #res=configutil.getResponse4Proxy(url)
    #res=configutil.getResponse(url)
    #content=res.text
    browser.get(url)
    content = browser.page_source
    soup=BeautifulSoup(content,'html.parser')
    fenyecount='1'
    gopage=soup.find(class_='pagearea')
    if gopage is None:
        return 1
    
    objgopage=gopage.find(class_='fr')
    if not objgopage is None:
        pagecountext=objgopage.text.replace(' ','').replace('/','')
        yeindex=pagecountext.find('页')
        fenyecount=pagecountext[1:yeindex]
        print(fenyecount)
    return int(fenyecount)


def getTotalBBSTopicList(url):
    count=getpagecount(url)
    print('一共多少页='+str(count))
    for i in range(count):
        sleepsecs=random.random()*5+random.random()*4
        print('爬取下个页面前sleep'+str(sleepsecs)+'秒')
        time.sleep(sleepsecs)
        getBBSTitleUrlList(url,i)   



if __name__=='__main__':
    #第二页   https://club.autohome.com.cn/bbs/forum-c-4080-2.html?qaType=-1#pvareaid=101061
    #第三页   https://club.autohome.com.cn/bbs/forum-c-4080-3.html?qaType=-1#pvareaid=101061
    #URL特点是后缀id加1
    #此页面为汽车之家论坛-->荣威RX5/RX5新能源论坛  的首页
    url='https://club.autohome.com.cn/bbs/forum-c-4080-1.html'
    getTotalBBSTopicList(url)
    


