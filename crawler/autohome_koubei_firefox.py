#coding:utf-8
import time,random
import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
#from config import *
from bs4 import BeautifulSoup



#url = 'https://k.autohome.com.cn/4240/'
client = pymongo.MongoClient('localhost')
db = client['qichezhijia']
collection='koubei'
cartitle='荣威RX5新能源'

browser=webdriver.Firefox()
wait = WebDriverWait(browser, 10)

#保存至MongoDB
def save_to_mongo(result):
    try:
        if db[collection].insert(result):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')


def index_page(i):
    url='https://k.autohome.com.cn/4240/'
    if i>1:
       url=url+'index_'+str(i)+'.html#dataList' 
    
    print('这次url是： ')
    print(url)
    get_content(url)
    

def get_content(url):
    browser.get(url)
    html = browser.page_source
    
    soup=BeautifulSoup(html,'html.parser')
    divs=soup.find_all(class_='mouthcon-cont fn-clear')
    print('获取网页中元素divs如下: ')
    
    for index,div in enumerate(divs):
        print('------下一个div对象-----')
        item={}
        
        bbscontent=div.find(class_='text-con ').find('div').text  #评论内容
        print('---bbscontent是： ')
        #print(bbscontent)
        username=div.find(class_='name-pic').find('img').get_attribute_list('title')[0]   #用户昵称
        print(username)
      
        leftdiv=div.find(class_='choose-con mt-10')
        dllist=leftdiv.find_all(class_='choose-dl')
        cartype=dllist[0].find('span').text
        caraddress=dllist[1].find('dd').text.replace(' ','').replace('\n','').replace('&nbsp;','').replace('    ','')
        #carcompany=dllist[2].find('a').text.replace(' ','').replace('\n','')
        buydate=dllist[3].find('dd').text.replace(' ','').replace('\n','')   #购买时间
        buyprice=dllist[4].find('dd').text.replace(' ','').replace('\n','')[0:5]    
        kongjian=dllist[6].find_all('span')[1].text.replace(' ','').replace('\n','') 
        dongli=dllist[7].find_all('span')[1].text.replace(' ','').replace('\n','')   
        caokong=dllist[8].find_all('span')[1].text.replace(' ','').replace('\n','') 
        nenghao=dllist[9].find_all('span')[1].text.replace(' ','').replace('\n','') 
        shushixing=dllist[10].find_all('span')[1].text.replace(' ','').replace('\n','')
        waiguan=dllist[11].find_all('span')[1].text.replace(' ','').replace('\n','')
        neishi=dllist[12].find_all('span')[1].text.replace(' ','').replace('\n','')
        #xingjiabi=dllist[13].find_all('span')[1].text.replace(' ','').replace('\n','') 
        
        dds=div.find_all(class_='obje')   #购车目的
        if dds is None:
            continue
        print(dds)
        purposestr=getBuyPurpose(dds)    
        
        #item['']=用户id
        item['username']=username
        item['cartype']=cartype    #购买车型
        item['caraddress']=caraddress   #购买地点
        #item['carcompany']=carcompany   #购车经销商
        item['buydate']=buydate 
        item['buyprice']=buyprice    #裸车购买价
        #item['']=油耗
        #item['']=目前行驶
        item['kongjian']=kongjian  #空间
        item['dongli']=dongli   #动力
        item['caokong']=caokong  #操控
        item['nenghao']=nenghao   #能耗
        item['shushixing']=shushixing   #舒适性
        item['waiguan']=waiguan   #外观
        item['neishi']=neishi   #内饰
        #item['xingjiabi']=xingjiabi  #性价比
        item['buypurpose']=purposestr    #购车目的
        item['bbscontent']=bbscontent    #评论所有文本字符
        item['html']=html   #整个页面所有文本字符
        
        save_to_mongo(item)    


def getBuyPurpose(dds):
    purposestr=''
    for index,d in enumerate(dds):
            print(d.text)
            if index>0:
                purposestr=purposestr+','+d.text
            else:
                purposestr=purposestr+d.text    
    print(purposestr)
    return purposestr        
    
    

def main():
    """
    遍历每一页
    """
    for i in range(1, 12):
        sleepsecs=random.random()*12+random.random()*9
        time.sleep(sleepsecs)
        print('这次sleep了时间为 '+str(sleepsecs)+'秒')
        print('---这次i是  '+str(i))
        index_page(i)
    



if __name__ == '__main__':
    main()
    browser.close()



