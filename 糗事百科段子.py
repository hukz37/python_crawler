#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/28 下午2:37
# @Author  : hukezhu
# @Site    : 
# @File    : 糗事百科段子.py
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

#fp = open('/Users/hukezhu/Desktop/wenxiong1.csv','wt')
#writer = csv.writer(fp)
#writer.writerow(('content','creationTime','productColor','productSize','userClientShow','userLevelName'))

db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='123456',db='YUNGAO',charset='utf8mb4')
cursor = db.cursor()
#
# cursor.execute("DROP TABLE IF EXISTS QIUBAI")
#
#
# #sql = """CREATE TABLE YUNGAO11 {ID INT NOT NULL,name CHAR(200),price CHAR(200),web CHAR(200)}"""
# sql = """CREATE TABLE QIUBAI (
#         ID INT NOT NULL,
#         content  longtext )"""
#
#
# cursor.execute(sql)





def get_id(url,a):
    html = requests.get(url, headers=headers)
    # print html.text
    selector = etree.HTML(html.text)
    infos = selector.xpath('//div[@class="content"]/span')
    for info in infos:
        try:
            content1 = info.text.replace('\n',' ')
            content = MySQLdb.escape_string(content1)
            print content
            print '\n'
            #print info.xpath('text()')[0] + "  " + "http://www.bookingtee.com/"+info.xpath('@href')[0]
            #print "http://www.bookingtee.com/"+info.xpath('@href')[0]
            sql11 = "INSERT INTO QIUBAI(content) \
                                           VALUES ('%s')" % \
                   (content)
            # try:
            # db.set_character_set('utf8')
            cursor.execute(sql11)
            db.commit()
            time.sleep(2)
            #get_comment_info("http://www.bookingtee.com/"+info.xpath('@href')[0])
        except IndexError:
            print '出错了'
            pass
    time.sleep(5)
    a = int(a) + 1
    url1 = 'https://www.qiushibaike.com/8hr/page/%s/' % a
    print '**************'+url1
    get_id(url1,a)


if __name__ == '__main__':
    #url = 'https://www.qiushibaike.com/text/page/182/'
    url = 'https://www.qiushibaike.com/8hr/page/1/'
    a = 1;
    get_id(url,a)