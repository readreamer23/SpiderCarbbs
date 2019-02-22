#coding:utf-8
from bs4 import BeautifulSoup
from datetime import date
import time,random
import pymongo
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
browser=webdriver.PhantomJS(service_args=SERVICE_ARGS)
browser.set_window_size(1400,900)

wait = WebDriverWait(browser, 10)


#爬取所有分页评论相关内容
def getBBSContent(url,i):
    print('----------------------------------')
    url=url.replace('1.html', str(i)+'.html')
    print(url)
    browser.get(url)
    content = browser.page_source
    #print(content)
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
        #address=div.find(class_='c01439a').text
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
        insertMongoBBS(messageitem)  
        print(index)
        print(messageitem) 
        

def insertMongoBBS(content):
    client=pymongo.MongoClient('127.0.0.1',27017)
    dbname='qichezhijia'
    autohome_bbs_content='autohome_bbs_content'
    db=client[dbname]
    collection=db[autohome_bbs_content]
    collection.insert(content)
    client.close()  



def getTotalBBSContent(url):
    count=3
    print('一共几页='+str(count-1))
    for i in range(1,count):
        sleepsecs=random.random()*10+random.random()*3
        print('爬取到标题下第'+str(i)+'篇文章最终页面')
        print('爬取下个页面前sleep'+str(sleepsecs)+'秒')
        time.sleep(sleepsecs)
        getBBSContent(url,i)

    
if __name__=='__main__':
    #url='https://club.autohome.com.cn/bbs/thread/05c6690871d9201b/59501783-1.html'
    url='https://club.autohome.com.cn/bbs/thread/151088f07afd9feb/75749718-1.html'
    getTotalBBSContent(url)
    browser.close()
    
    
    


