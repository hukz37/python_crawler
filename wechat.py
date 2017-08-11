#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/10 下午3:06
# @Author  : Aries
# @Site    : 
# @File    : wechat.py
# @Software: PyCharm


import itchat
from itchat.content import TEXT
import sys
import time

from datetime import datetime

#@ed155009cc6d91a697e7a25244a33850

reload(sys)
sys.setdefaultencoding('utf8')

#itchat.auto_login(True)
#itchat.run()


#
# @itchat.msg_register
# def text_reply(msg):
#     print msg
#     print '********************************'
#     return msg
#     #return msg['Text']



# @itchat.msg_register
# def simple_reply(msg):
#     print msg
#     if msg['Type'] == TEXT:
#         return 'I received: %s' % msg['Content']


dt = datetime.time

print time.strftime('%H',time.localtime(time.time()))

# user=itchat.search_friends(name='房小喵')  #输入她的备注
# username=user[0]['UserName']
# itchat.send('你好你好你好!',toUserName=username)
#
#
# mps = itchat.get_mps()
# print(mps)
# itchat.auto_login(True)
# itchat.run()


# #想给谁发信息，先查找到这个朋友,name后填微信备注即可
# users = itchat.search_friends(name='房小喵')
# #获取对方UserName,返回一个列表
# print(users)
#
#


