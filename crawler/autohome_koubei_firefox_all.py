#coding:utf-8
import time,random
import pymongo
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
#from config import *
from crawler.mongoutil import insertMongoKoubei
from bs4 import BeautifulSoup
from crawler.seleniumutil import getBrowserFirefox
from crawler.seleniumutil import getBrowserFirefoxWait



#适配爬取所有车型口碑数据

browser=getBrowserFirefox()

#保存至MongoDB
def save_to_mongo(result):
    try:
        if insertMongoKoubei(result):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')


def index_page(title,type,url,i):
    if i>1:
       url=url+'index_'+str(i)+'.html#dataList' 
    print('这次url是： ')
    print(url)
    get_content(title,type,url)
    
#分析网页内容，获取数据
def get_content(title,type,url):
    browser.get(url)
    html = browser.page_source
    
    soup=BeautifulSoup(html,'html.parser')
    divs=soup.find_all(class_='mouthcon-cont fn-clear')
    #print('获取网页中元素divs如下: ')
    
    for index,div in enumerate(divs):
        #print('------下一个div对象-----')
        item={}
        bbscontent=div.find(class_='text-con ').find('div').text  #评论内容(最满意，最不满意)
        username=div.find(class_='name-pic').find('img').get_attribute_list('title')[0]   #用户昵称
      
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
        #print(dds)
        purposestr=getBuyPurpose(dds)    
        
        #item['']=用户id
        item['title']=title
        item['type']=type
        item['url']=url
        
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
        
        bbscollection=getbbsTypeContent(bbscontent)
        print('bbscollection如下')
        print(bbscollection)
        item['manyi_msg']=bbscollection[0]
        item['bumanyi_msg']=bbscollection[1]
        item['kongjian_msg']=bbscollection[2]
        
        #item['html']=html   #整个页面所有文本字符
        save_to_mongo(item)    



#获取对车评价分组数据：最满意一点，最不满意一点，空间，动力.....
def getbbsTypeContent(bbs):
    restr='[split]'
    keylist=['【最满意的一点】','【最不满意的一点】','【空间】','【动力】','【操控】','【能耗】',
             '【舒适性】','【外观】','【内饰】','【性价比】','【为什么选择这款车】']
    bbs=bbs.replace(' ','').replace(keylist[0],'')
    for i in range(1,11):
        bbs=bbs.replace(keylist[i],restr)
        
    bbslist=bbs.split(restr)
    #bbscontent={'manyi_msg':'','bumanyi_msg':'','kongjian_msg':'','dongli_msg':'','caokong_msg':'','nenghao_msg':'','shushixing_msg':'','waiguan_msg':'','neishi_msg':'','xingjiabi_msg':'','whycar_msg':''}
    bbscontent=['','','','','','','','','','','']
    for index,i in enumerate(bbslist):
        bbscontent[index]=i
    return(bbscontent)
        
   
   

#组合购车目的字符串，中间逗号隔开
def getBuyPurpose(dds):
    purposestr=''
    for index,d in enumerate(dds):
            if index>0:
                purposestr=purposestr+','+d.text
            else:
                purposestr=purposestr+d.text    
    return purposestr        
    
    
    

def main(title,type,url):
    """
    遍历每一页
    """
    for i in range(1, 49):
        sleepsecs=random.random()*7+random.random()*9
        time.sleep(sleepsecs)
        print('这次sleep了时间为 '+str(sleepsecs)+'秒')
        print('---这次i是  '+str(i))
        #index_page(i)
        index_page(title,type,url,i)
    browser.close()

      

if __name__ == '__main__':
    list1=['荣威RX5新能源','1','https://k.autohome.com.cn/4240/']
    #list3=['荣威MarvelX','2','https://k.autohome.com.cn/4653/']    无口碑数据
    list3=['领克02','3','https://k.autohome.com.cn/4616/']
    list4=['广汽GE3','4','https://k.autohome.com.cn/4291/']
    list5=['宝马3系','5','https://k.autohome.com.cn/66/']
    list6=['蔚来ES8','6','https://k.autohome.com.cn/4427/']
    list7=['奔驰C级','7','https://k.autohome.com.cn/588/']
    
    #list8=['奔驰A200','8','https://car.autohome.com.cn/price/series-4764-0-2-0-0-0-0-1.html#']    #   无数据
    #list9=['威马ex5','9','https://k.autohome.com.cn/4652/#pvareaid=3454440']      #   无数据
    list8=['长安CS35PLUS','8','https://k.autohome.com.cn/4976/']
    
    main(list8[0],list8[1],list8[2])
    

