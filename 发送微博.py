#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/22 下午2:23
# @Author  : hukezhu
# @Site    : 
# @File    : 发送微博.py
# @Software: PyCharm

import weibo
import webbrowser  # python内置的包
import time
from selenium import webdriver
import datetime
import qiubai
import sys

APP_KEY = '4015256835'
APP_SECRET = 'cbc2fe77aba628a33f469ebf3db18ef9'
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'


def get_selenium_js_html(url):
    print '进入了get_selenium_js_html'
    #这个是打开firefox的方式
    #browser = webdriver.Firefox(executable_path='/Users/hukezhu/Downloads/geckodriver')

    #这个是打开chrome的方式
    browser = webdriver.Chrome(executable_path='/Users/hukezhu/Downloads/chromedriver')
    browser.get(url)
    #time.sleep(3)
    a = 1
    code = ''
    while 1 == a:
        time.sleep(1)
        print browser.current_url
        if browser.current_url .find('code=') != -1 :
            code = browser.current_url.split('code=')[1]
            a = 0
    # 执行js得到整个页面内容
    #html = browser.execute_script("return document.documentElement.outerHTML")
    print code
    browser.quit()
    return code

def run():
    # weibo模块的APIClient是进行授权、API操作的类，先定义一个该类对象，传入参数为APP_KEY, APP_SECRET, CALL_BACK
    client = weibo.APIClient(APP_KEY, APP_SECRET, CALLBACK_URL)
    # 获取该应用（APP_KEY是唯一的）提供给用户进行授权的url
    auth_url = client.get_authorize_url()
    # 打印出用户进行授权的url，将该url拷贝到浏览器中，服务器将会返回一个url，该url中包含一个code字段（如图1所示）
    print "auth_url : " + auth_url
    # 输入该code值（如图2所示）

    #code = raw_input("input the retured code : ")
    code =  get_selenium_js_html(auth_url)
    print '呵呵哒 code已经出来了 %s ' % {code}
    # 通过该code获取access_token，r是返回的授权结果，具体参数参考官方文档：
    # http://open.weibo.com/wiki/Oauth2/access_token
    r = client.request_access_token(code)
    # 将access_token和expire_in设置到client对象
    client.set_access_token(r.access_token, r.expires_in)

    # 以上步骤就是授权的过程，现在的client就可以随意调用接口进行微博操作了，下面的代码就是用用户输入的内容发一条新微博

    reload(sys)
    sys.setdefaultencoding('utf8')

    while True:
        #print "Ready! Do you want to send a new weibo?(y/n)"
        #choice = raw_input()
        time.sleep(600);
        choice = 'y';
        if choice == 'y' or choice == 'Y':
            #content = raw_input('input the your new weibo content : ')
            spider = qiubai.Spider_QSBK()
            temStr = spider.start()
            content = '[糗事百科]%s 现在北京时间是:%s  ---自动发送 [黑线]' % (temStr,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            if len(content) > 140 :
                content = content[0:139]
            if content:
                # 调用接口发一条新微薄，status参数就是微博内容
                client.statuses.update.post(status=content)
                print "Send succesfully!"
                #break
                continue
            else:
                print "Error! Empty content!"
        if choice == 'n' or choice == 'N':
            break



if __name__ == "__main__":
    run()
