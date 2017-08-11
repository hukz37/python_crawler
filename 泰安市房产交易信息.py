#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/3 下午2:04
# @Author  : hukezhu
# @Site    : 
# @File    : 泰安市房产交易信息.py
# @Software: PyCharm


import requests
from lxml import etree
import time
import json
import re
import csv
import sys
import MySQLdb
from selenium import webdriver


reload(sys)
sys.setdefaultencoding("utf-8") #更改默认编码为utf-8
headers = {
    'Cookie':'ipLoc-djd=1-72-2799-0; unpl=V2_ZzNtbRZXF0dwChEEfxtbV2IKFQ4RUBcSdg1PVSgZCVAyCkBVclRCFXMUR1NnGFkUZgoZXkpcQxNFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2VH4RWAVmBxVeS19AEHUJR1x6GFsBYQEibUVncyVyDkBQehFsBFcCIh8WC0QcdQ1GUTYZWQ1jAxNZRVRKHXYNRlV6EV0EYAcUX3JWcxY%3d; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_e1ec43fa536c486bb6e62480b1ddd8c9|1496536177759; mt_xid=V2_52007VwMXWllYU14YShBUBmIDE1NVWVNdG08bbFZiURQBWgxaRkhKEQgZYgNFV0FRVFtIVUlbV2FTRgJcWVNcSHkaXQVhHxNVQVlXSx5BEl0DbAMaYl9oUmofSB9eB2YGElBtWFdcGA%3D%3D; __jda=122270672.14951056289241009006573.1495105629.1496491774.1496535400.5; __jdb=122270672.26.14951056289241009006573|5.1496535400; __jdc=122270672; 3AB9D23F7A4B3C9B=EJMY3ATK7HCS7VQQNJETFIMV7BZ5NCCCCSWL3UZVSJBDWJP3REWXTFXZ7O2CDKMGP6JJK7E5G4XXBH7UA32GN7EVRY; __jdu=14951056289241009006573',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}

#fp = open('/Users/hukezhu/Desktop/wenxiong1.csv','wt')
#writer = csv.writer(fp)
#writer.writerow(('content','creationTime','productColor','productSize','userClientShow','userLevelName'))

db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='123456',db='TAIAN',charset='utf8mb4')
cursor = db.cursor()
#
# cursor.execute("DROP TABLE IF EXISTS JIAOYI")
#
# #sql = """CREATE TABLE YUNGAO11 {ID INT NOT NULL,name CHAR(200),price CHAR(200),web CHAR(200)}"""
# sql = """CREATE TABLE JIAOYI (ID INT NOT NULL,content  CHAR(200),href11 CHAR(200) )"""
# cursor.execute(sql)




def get_id(url,a):
    html = requests.get(url, headers=headers)
    #print html.text
    selector = etree.HTML(html.text)
    infos = selector.xpath('//*[@id="area2_body"]/div[1]/div/h3/a')
    for info in infos:
        try:
            content = MySQLdb.escape_string(info.text)
            href11 = MySQLdb.escape_string(info.get('href'))
            print content + '  ' +href11
            #print info.xpath('text()')[0] + "  " + "http://www.bookingtee.com/"+info.xpath('@href')[0]
            #print "http://www.bookingtee.com/"+info.xpath('@href')[0]

            sql11 = "INSERT INTO JIAOYI(content,href11) \
                                           VALUES ('%s','%s')" % \
                   (content,href11)
            cursor.execute(sql11)
            db.commit()
            time.sleep(1)
            # get_comment_info("http://www.bookingtee.com/"+info.xpath('@href')[0])
        except IndexError:
            pass
    time.sleep(2)
    #browser.find_element_by_class_name("loading-more").click()
    a = int(a) + 1
    url1 = 'http://www.home0538.com/index.php?caid=810&page=%s' % a
    get_id(url1,a)
    print '**********************************************' + a


if __name__ == '__main__':
    url = 'http://www.home0538.com/index.php?caid=810&page=1'
    a = 1
    #browser = webdriver.Chrome(executable_path='/Users/hukezhu/Downloads/chromedriver')
    #browser.get(url)
    get_id(url,a)

