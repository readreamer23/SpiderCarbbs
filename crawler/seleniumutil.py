#coding:utf-8
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait



def getBrowserFirefox():
    browser=webdriver.Firefox()
    wait = WebDriverWait(browser, 10)
    return browser

def getBrowserFirefoxWait(seconds):
    browser=webdriver.Firefox()
    wait = WebDriverWait(browser, seconds)
    return browser

def closeBrowser(browser):
    browser.close()


if __name__=='__main__':
    browser=getBrowserFirefox()
    url='http://www.baidu.com'
    browser.get(url)
    content = browser.page_source
    print(content)
    closeBrowser(browser)

