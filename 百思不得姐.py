#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/28 上午10:57
# @Author  : hukezhu
# @Site    : 
# @File    : 百思不得姐.py
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
    'Cookie':'ipLoc-djd=1-72-2799-0; unpl=V2_ZzNtbRZXF0dwChEEfxtbV2IKFQ4RUBcSdg1PVSgZCVAyCkBVclRCFXMUR1NnGFkUZgoZXkpcQxNFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2VH4RWAVmBxVeS19AEHUJR1x6GFsBYQEibUVncyVyDkBQehFsBFcCIh8WC0QcdQ1GUTYZWQ1jAxNZRVRKHXYNRlV6EV0EYAcUX3JWcxY%3d; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_e1ec43fa536c486bb6e62480b1ddd8c9|1496536177759; mt_xid=V2_52007VwMXWllYU14YShBUBmIDE1NVWVNdG08bbFZiURQBWgxaRkhKEQgZYgNFV0FRVFtIVUlbV2FTRgJcWVNcSHkaXQVhHxNVQVlXSx5BEl0DbAMaYl9oUmofSB9eB2YGElBtWFdcGA%3D%3D; __jda=122270672.14951056289241009006573.1495105629.1496491774.1496535400.5; __jdb=122270672.26.14951056289241009006573|5.1496535400; __jdc=122270672; 3AB9D23F7A4B3C9B=EJMY3ATK7HCS7VQQNJETFIMV7BZ5NCCCCSWL3UZVSJBDWJP3REWXTFXZ7O2CDKMGP6JJK7E5G4XXBH7UA32GN7EVRY; __jdu=14951056289241009006573',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}

global a
a = 1
#fp = open('/Users/hukezhu/Desktop/wenxiong1.csv','wt')
#writer = csv.writer(fp)
#writer.writerow(('content','creationTime','productColor','productSize','userClientShow','userLevelName'))

# db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='123456',db='YUNGAO',charset='utf8')
# cursor = db.cursor()

# cursor.execute("DROP TABLE IF EXISTS YUNGAO11")
#
# #sql = """CREATE TABLE YUNGAO11 {ID INT NOT NULL,name CHAR(200),price CHAR(200),web CHAR(200)}"""
# sql = """CREATE TABLE YUNGAO11 (
#         ID INT NOT NULL,
#         city  CHAR(200),
#         name  CHAR(200),
#         price  CHAR(200),
#         web   CHAR(200))"""
#
#
# cursor.execute(sql)




def get_id(url,a):
    html = requests.get(url, headers=headers)
    # print html.text
    selector = etree.HTML(html.text)
    infos = selector.xpath('//div[@class="j-r-list-c-desc"]/a')
    for info in infos:
        try:
            print info.text
            print '\n'
            #print info.xpath('text()')[0] + "  " + "http://www.bookingtee.com/"+info.xpath('@href')[0]
            #print "http://www.bookingtee.com/"+info.xpath('@href')[0]
            # sql11 = "INSERT INTO YUNGAO11(city) \
            #                                VALUES ('%s')" % \
            #        (info.xpath('text()')[0])
            # try:
            # db.set_character_set('utf8')
            # cursor.execute(sql11)
            #get_comment_info("http://www.bookingtee.com/"+info.xpath('@href')[0])
        except IndexError:
            print '出错了'
            pass
    time.sleep(3)
    a = int(a) + 1
    url1 = 'http://www.budejie.com/text/%s' % a
    get_id(url1,a)




def get_comment_info(url):
    html = requests.get(url, headers=headers)
    # print html.text
    selector = etree.HTML(html.text)
    courseinfo = selector.xpath('/html/body/div[13]/div/div[2]/ul/li')

    for course in courseinfo:
        try:
            content = course.xpath('a')[0].text
            content = MySQLdb.escape_string(content)
            print content + '   ' + "http://www.bookingtee.com/"+ course.xpath('a')[0].get('href') + "    "  +course.xpath('span')[0].text
            print '\n\n\n\n'
            sql1 = "INSERT INTO YUNGAO11(name,price, web) \
                               VALUES ('%s', '%s', '%s')" % \
                   (content, course.xpath('span')[0].text, "http://www.bookingtee.com/"+ course.xpath('a')[0].get('href'))
            # try:
            # db.set_character_set('utf8')
            cursor.execute(sql1)
            print "保存成功"
            db.commit()
            # except:
            #     db.rollback()
            #     print "保存失败"
        except IndexError:
            pass

        time.sleep(2)

if __name__ == '__main__':
    url = 'http://www.budejie.com/text/1'
    a = 1;
    get_id(url,a)