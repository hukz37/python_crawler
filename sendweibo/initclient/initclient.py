#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/24 下午9:54
# @Author  : Aries
# @Site    : 
# @File    : initclient.py.py
# @Software: PyCharm


# ! /usr/bin/python

import weibo
import urllib
import time
import os
from selenium import webdriver


class myAPIClient(weibo.APIClient):
    """
    myAPIClient类继承自weibo包中的APIClient类，对其进行了扩展。SDK中的APIClient类没有根据已授权的access_token获取授权详细信息的接口。另外，SDK中
    的APIClient不能保存当前授权用户的uid，该继承类实现了这两个功能，使得用起来更加方便。

    """

    def __init__(self, app_key, app_secret, redirect_uri=None, response_type='code', domain='api.weibo.com',
                 version='2'):
        weibo.APIClient.__init__(self, app_key, app_secret, redirect_uri=None, response_type='code',
                                 domain='api.weibo.com',
                                 version='2')
        # 保存当前授权用户的uid
        self.uid = ""

    def request_access_token_info(self, at):
        """
        该接口传入参数at为已经授权的access_token，函数将返回该access_token的详细信息，返回Json对象，与APIClient类的request_access_token类似。
        """
        print '进入到了request_access_token_info函数'
        r = weibo._http_post('%s%s' % (self.auth_url, 'get_token_info'), access_token=at)
        current = int(time.time())
        expires = r.expire_in + current
        remind_in = r.get('remind_in', None)
        print  '哈哈哈哈哈 %s' % (remind_in)
        if remind_in:
            rtime = int(remind_in) + current
            if rtime < expires:
                expires = rtime
        return weibo.JsonDict(expires=expires, expires_in=expires, uid=r.get('uid', None))

    def set_uid(self, uid):
        self.uid = uid











TOKEN_FILE = 'token-record.log'


def load_tokens(filename=TOKEN_FILE):
    acc_tk_list = []
    try:
        filepath = os.path.join(os.path.dirname(__file__), filename)
        print 'load_tokens: %s' % (filepath)
        f = open(filepath)
        acc_tk_list.append(f.readline().strip())
        print "===> Get the access_token from file token-record.log : ", acc_tk_list[0]
    except IOError:
        print "===> File token-record.log does not exist."
    f.close()
    return acc_tk_list


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
    #browser.quit()
    return code


def dump_tokens(tk, filename=TOKEN_FILE):
    try:
        filepath = os.path.join(os.path.dirname(__file__), filename)
        f = open(filename, 'a')
        f.write(tk)
        f.write('\n')
        print 'dump_tokens: %s' % (filepath)
    except IOError:
        print "===> File token-record.log does not exist."
    f.close()
    print "===> The new access_token has been written to file token-record.log."


def get_client(appkey, appsecret, callback):
    client = myAPIClient(appkey, appsecret, callback)
    at_list = load_tokens()
    print at_list
    if at_list and at_list != ['']:
        print '1111111111111111'
        access_token = at_list[-1]
        print access_token
        r = client.request_access_token_info(access_token)
        print '呵呵哒'
        expires_in = r.expires_in
        print "===> The access_token's expires_in : %f" % expires_in
        # 授权access_token过期
        if r.expires_in <= 0:
            return None
        client.set_access_token(access_token, expires_in)
        client.set_uid(r.uid)
    else:
        print '2222222222222222'
        auth_url = client.get_authorize_url(redirect_uri=callback)
        print "===> auth_url : " + auth_url
        print """===> Note! The access_token is not available, you should be authorized again. Please open the url above in your browser,
then you will get a returned url with the code field. Input the code in the follow step."""
        #code = raw_input("===> input the retured code : ")
        code = get_selenium_js_html(auth_url)
        print '呵呵哒 code已经出来了 %s ' % {code}
        r = client.request_access_token(code,redirect_uri=callback)
        access_token = r.access_token
        expires_in = r.expires_in
        print "===> the new access_token is : ", access_token
        dump_tokens(access_token)
        client.set_access_token(access_token, expires_in)
        client.set_uid(r.uid)
    return client