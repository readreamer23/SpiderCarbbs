from bs4 import BeautifulSoup
from datetime import date
import time,random
from crawler.mongoutil import insertMongo1
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options

options = Options() 
options.add_argument('-headless') 
browser = webdriver.Firefox( firefox_options=options) 
print(browser.page_source) 
wait = WebDriverWait(browser, 7)


#一个程序文件爬取所有分页评论相关内容
def getBBSContent(url,i):
    print('----------------------------------')
    url=url.replace('1.html', str(i)+'.html')
    print(url)
    browser.get(url)
    content = browser.page_source
    soup=BeautifulSoup(content,'html.parser')
    divs=soup.find_all(class_='clearfix contstxt outer-section')
    messageList={}
    for index,div in enumerate(divs):
        messageitem={}
        date=''
        comment=''
        province='省'
        city='市'
        messagediv=div.find(class_="w740")
        address=div.find_all(class_='c01439a')[5].text
        datediv=div.find(class_='plr26 rtopconnext')
        
        if not datediv is None:
            date=datediv.find_all('span')[1].text
       
        if not messagediv is None:
            comment=messagediv.text.replace('\r\n','').replace(' ','')
        
        if not address is None:
            address=address.replace(' ',',')
            addressobj=address.split(',')
            province=addressobj[0]
            #city=city=addressobj[0] if addressobj[1] is None or addressobj[1]=='' else addressobj[1]
            
        messageitem['url']=url     
        messageitem['address']=address.replace(' ',',')
        messageitem['date']=date
        messageitem['comment']=comment
        messageitem['user']='user'
        messageitem['province']=province
        #messageitem['city']=city
        
        messageList[index]=messageitem
        insertMongo1(messageitem)
        print(index)
        print(messageitem) 
        


#获取评论分页个数
def getpagecount(url):
    browser.get(url)
    content = browser.page_source
    soup=BeautifulSoup(content,'html.parser')
    gopage=soup.find(class_='gopage')
    if gopage is None:
        print('获取分页对象gopage是None')
        return 1
        
    objgopage=gopage.find(class_='fs')
    if not objgopage is None:
        pagecount=objgopage.text.replace(' ','').replace('/','')
    
    fenyecount=pagecount[0:1]
    return int(fenyecount)



def getTitleBBSContent(url):
    count=getpagecount(url)+1
    print('一共几页='+str(count-1))
    for i in range(1,count):
        sleepsecs=random.random()*10+random.random()*3
        print('爬取到标题下第'+str(i)+'篇文章最终页面')
        print('爬取下个页面前sleep'+str(sleepsecs)+'秒')
        time.sleep(sleepsecs)
        getBBSContent(url,i)
        



#爬取所有分页评论相关内容
def getBBSTitleUrlList(url,i):
    #拼接url： pvareaid是动态id,后期需研究汽车之家的id获取规则
    if i>1:
        url=url.replace('1.html', str(i)+'.html'+'?qaType=-1#pvareaid='+'101061')
    
    print(url)
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
        #insertMongo2(item)
        print(item) 
           
    return linkitems  
     
     
     
#获取车型所有文章分页个数
def getTitlePageCount(url):
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



#循环遍历荣威论坛页所有文章链接，分页循环获取:第一层循环所有标题文章，第二层循环每篇文章评论
def getTotalBBSContent(url,title):
    count=getTitlePageCount(url)
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
    title='荣威RX5论坛页'
    url='https://club.autohome.com.cn/bbs/forum-c-4080-1.html'  
    #url='https://club.autohome.com.cn/bbs/forum-c-4080-6.html?qaType=-1#pvareaid=101061'
    getTotalBBSContent(url,title)
    browser.close()
    
    
    

