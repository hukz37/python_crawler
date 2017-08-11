#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/2 上午10:44
# @Author  : Aries
# @Site    : 
# @File    : qiushibaike22.py
# @Software: PyCharm

import re
import urllib,urllib2
import thread
from bs4 import BeautifulSoup

# class Baike:
#     def __init__(self):
#         self.pageIndex = 1
#         self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
#         self.headers = {'User-Agent':self.user_agent}
#         self.stories = []
#         self.enable = False
#
#     def getPageCode(self,pageIndex):
#         URL = 'http://www.qiushibaike.com/8hr/page/%d/?s=4987892' % (pageIndex)
#
#         try:
#             req = urllib2.Request(URL,headers=self.headers)
#             Response = urllib2.urlopen(req)
#             text = Response.read()
#             pageCode = text.decode('UTF-8')
#             return pageCode
#         except urllib2.URLError, e:
#             if hasattr(e,"code"):
#                 print e.code
#
#     def getPageContent(self,pageIndex):
#         pageCode = self.getPageCode(pageIndex)
#
#         if not pageCode:
#             print "页面加载失败......"
#             return None
#
#         soup = BeautifulSoup(pageCode,'html.parser')
#
#         pageListItems, aa ,bb = [], [], []
#
#         for m,n in zip(soup('h2'),soup.select('div .content-text')):
#             ans1 = ''.join(m.string).strip()
#             aa.append(ans1)
#             bb.append(n.string)
#
#         for i,j in zip(aa,bb):
#             if str(type(j)) != '<type \'NoneType\'>':
#                 pageListItems.append([i+'\n',j.strip()])
#             else:
#                 pageListItems.append([i,j])
#
#         return pageListItems
#
#     def loadPageListItems(self):
#         if self.enable == True:
#             if len(self.stories) < 2:
#                 list = self.getPageContent(self.pageIndex)
#                 if list:
#                     self.stories.append(list)
#                     self.pageIndex += 1
#
#
#     def getOneStory(self,pageListItems,page):
#         for one in pageListItems:
#             input = raw_input()
#             self.loadPageListItems()
#             if input == 'quit':
#                 self.enable = False
#                 return
#             print u"第%d页\t发布人: %s 内容: %s" % (page,one[0],one[1])
#
#
#     def start(self):
#         print u"正在读取糗事百科段子,请输入quit退出"
#         self.enable = True
#
#         thread.start_new_thread(self.loadPageListItems, ())
#
#         nowPage = 1
#         while self.enable:
#             if len(self.stories) > 0:
#                 pageStories = self.stories[0]
#                 del self.stories[0]
#                 self.getOneStory(pageStories,nowPage)
#                 nowPage += 1
#
#
# spider = Baike()
#
# spider.start()

import requests
from bs4 import BeautifulSoup as bs


# 获取单个页面的源代码网页
def gethtml(pagenum):
    url = 'http://www.qiushibaike.com/8hr/page/%d/?s=4987892' % (pagenum)
    req = requests.get(url, headers=Headers)
    html = req.text
    #print(html)
    return html


# 获取单个页面的所有段子
def getitems(pagenum):
    html = gethtml(pagenum)
    soup = bs(html, "html.parser")
    f = soup.find_all('div', 'content')
    items = []
    for x in f:
        #print(x.get_text())
        items.append(x.get_text())
    #print(items)
    return items


# 分别打印单个页面的所有段子
def getduanzi(pagenum):
    print("呵呵********进入了getduanzi")
    n = 0
    for x in getitems(pagenum):
        n += 1
        print('第%d条段子：\n%s' % (n, x))


# 分别打印所有页面的段子
def getall(bginpage, endpage):
    try:
        for pagenum in range(int(bginpage), int(endpage) + 1):
            print(('----------华丽丽的分割线【第%d页】----------' % pagenum).center(66))
            getduanzi(pagenum)
    except:
        print('页码输入错误，只接收正整数输入。')


if __name__ == '__main__':
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    bginpage = str(input('输入起始页：')).strip()
    endpage = str(input('输入终止页：')).strip()
    print bginpage,endpage
    getall(bginpage, endpage)