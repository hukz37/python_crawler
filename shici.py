#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/14 下午4:37
# @Author  : Aries
# @Site    : 
# @File    : shici.py
# @Software: PyCharm

import requests
from lxml import etree
import time
import json
import re
import csv
import sys
import MySQLdb

reload(sys)
sys.setdefaultencoding("utf-8") #更改默认编码为utf-8
headers = {
    'Cookie':'Hm_lvt_04660099568f561a75456483228a9516=1531556767',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'referer':'https://so.gushiwen.org/gushi/tangshi.aspx'
}
db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='123456',db='POEM',charset='utf8')
cursor = db.cursor()

# cursor.execute("DROP TABLE IF EXISTS POEM")
#
# #sql = """CREATE TABLE YUNGAO11 {ID INT NOT NULL,name CHAR(200),price CHAR(200),web CHAR(200)}"""
# sql = """CREATE TABLE POEM (
#         ID INT NOT NULL,
#         category_name  text,
#         category_url  text,
#         categoryName text,
#         title text,
#         author text,
#         poemurl text,
#         poem text,
#         yiwen text)"""
#
# cursor.execute(sql)

def get_id(url):
    #print url
    #html = requests.get(url, headers=headers)
    html = requests.get(url)
    #print html.text
    selector = etree.HTML(html.text)
    infos = selector.xpath('//div[@class="cont"]/a')
    for info in infos:
        try:
            #print info.xpath('text()')[0] + "  " + "http://www.bookingtee.com/"+info.xpath('@href')[0]
            #print "http://www.bookingtee.com/"+info.xpath('@href')[0]
            print info.text + '   ' + 'https://so.gushiwen.org' + info.get('href')
            # try:
            # db.set_character_set('utf8')
            get_comment_info(info.text,"https://so.gushiwen.org"+info.xpath('@href')[0])
        except IndexError:
            pass





def get_comment_info(name,url):
    #print url
    category_name = name
    category_url = url
    html = requests.get(url)
    #print html.text
    selector = etree.HTML(html.text)
    courseinfo = selector.xpath('//div[@class="sons"]/div')#//span/a[@target="_blank"]'
    for course in courseinfo:
        try:
            categoryName = course.xpath('div/strong')[0].text
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
            print categoryName
            titleinfos = course.xpath('span') #/html/body/div[3]/div[1]/div[2]/div[1]/span[1]/text()
            for titleinfo in titleinfos:
                title = titleinfo.xpath('a')[0].text
                author = titleinfo.xpath('text()')[0]
                url = "https://so.gushiwen.org%s" % titleinfo.xpath('a')[0].get('href')
                print "%s  %s  %s" % (title,author,url)
                get_poem_detail(category_name,category_url,categoryName,title,author,url)
        except IndexError:
            pass

        time.sleep(2)

def get_poem_detail(category_name,category_url,categoryName,title,author,poemurl):
    html = requests.get(poemurl)
    selector = etree.HTML(html.text)
    source = selector.xpath('//p[@class="source"]/a[1]/text()')[0] #唐代
    poem = selector.xpath('//div[@class="contson"]')[0].xpath('string(.)') #//*[@id="contson45c396367f59"]/text()[2]  //*[@id="contson45c396367f59"]/text()[2]
    poem = MySQLdb.escape_string(poem)

    list = selector.xpath('//div[@class="contyishang"]')
    for node in list:
        print node.xpath('string(.)')
        yiwen = node.xpath('string(.)')
        yiwen = MySQLdb.escape_string(yiwen)
        sql1 = "INSERT INTO POEM(category_name,category_url, categoryName,title,author,poemurl,poem,yiwen) \
                                          VALUES ('%s', '%s', '%s','%s','%s','%s' ,'%s','%s')" % \
               (category_name, category_url, categoryName, title, author,poemurl,poem,yiwen)
        cursor.execute(sql1)
    db.commit()




if __name__ == '__main__':
    url = 'https://so.gushiwen.org/gushi/tangshi.aspx'
    get_id(url)