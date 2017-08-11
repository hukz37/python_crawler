#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/24 下午9:57
# @Author  : Aries
# @Site    : 
# @File    : send_weibo.py
# @Software: PyCharm

# ! /usr/bin/python

from initclient import initclient
import time
import qiubai
import sys
import datetime


APP_KEY = '4015256835'
APP_SECRET = 'cbc2fe77aba628a33f469ebf3db18ef9'
CALL_BACK = 'https://api.weibo.com/oauth2/default.html'

def run():
    # 调用initclietn模块创建授权的client对象
    client = initclient.get_client(APP_KEY, APP_SECRET, CALL_BACK)
    reload(sys)
    sys.setdefaultencoding('utf8')
    if not client:
        print  'client 不存在!!!!'
        return

        # 根据用户输入内容发微博
    while True:
        #print "Ready! Do you want to send a new weibo?(y/n)"
        #choice = raw_input()
        #time.sleep(600)
        choice = 'y'
        if choice == 'y' or choice == 'Y':
            #content = raw_input('input the your new weibo content : ')
            spider = qiubai.Spider_QSBK()
            temStr = spider.start()
            content = '[糗事百科]%s 现在北京时间是:%s  ---自动发送 [黑线]' % (
            temStr, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            if len(content) > 140:
                content = content[0:139]
            if content:
                client.statuses.update.post(status=content)#,pic= open('/Users/hukezhu/PycharmProjects/python/sendweibo/123.jpeg' ,'rb'))
                print "Send succesfully!"
                break
                #continue
            else:
                print "Error! Empty content!"
        if choice == 'n' or choice == 'N':
            break


if __name__ == "__main__":
    run()