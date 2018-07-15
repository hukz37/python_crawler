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
            get_comment_info("https://so.gushiwen.org"+info.xpath('@href')[0])
        except IndexError:
            pass





def get_comment_info(url):
    #print url
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
                get_poem_detail(title,author,url)
        except IndexError:
            pass

        time.sleep(2)

def get_poem_detail(title,author,url):
    html = requests.get(url)
    selector = etree.HTML(html.text)
    source = selector.xpath('//p[@class="source"]/a[1]/text()')[0] #唐代
    poem = selector.xpath('//div[@class="contson"]')[0].xpath('string(.)') #//*[@id="contson45c396367f59"]/text()[2]  //*[@id="contson45c396367f59"]/text()[2]
    poem = MySQLdb.escape_string(poem)
    print poem

if __name__ == '__main__':
    url = 'https://so.gushiwen.org/gushi/tangshi.aspx'
    get_id(url)