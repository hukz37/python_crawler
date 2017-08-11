#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/24 下午3:24
# @Author  : Aries
# @Site    : 
# @File    : jdpy.py
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

fp = open('/Users/hukezhu/Desktop/wenxiong1.csv','wt')
writer = csv.writer(fp)
writer.writerow(('content','creationTime','productColor','productSize','userClientShow','userLevelName'))

db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="123456",db="test",charset="utf8")

cursor = db.cursor()
#
# cursor.execute("DROP TABLE IF  EXISTS EMPLOYEE")
#
# sql = """CREATE TABLE EMPLOYEE (
#         ID INT NOT NULL,
#         content1  longtext NOT NULL,
#         creationTime1  CHAR(200),
#         productColor1  CHAR(200),
#         productSize1   CHAR(200),
#         userClientShow1   CHAR(100),
#         userLevelName1   CHAR(100))"""
#
# cursor.execute(sql)


def get_id(url):
    html = requests.get(url, headers=headers)
    print html
    selector = etree.HTML(html.text)
    infos = selector.xpath('//ul[@class="gl-warp clearfix"]/li')
    for info in infos:
        try:
            id = info.xpath('@data-sku')[0]
            comment_url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv6&productId={}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'.format(id)
            get_comment_info(comment_url,id)
        except IndexError:
            pass

def get_comment_info(url,id):
    html = requests.get(url,headers=headers)
    t = re.findall('fetchJSON_comment98vv6\((.*)\);', html.text)
    json_data = json.loads(t[0])
    page = json_data['maxPage']
    urls = ['https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv6&productId=%s&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1'.format(str(i)) for i in range(0,int(page))]
    for path in urls:
        html1 = requests.get(path%id, headers=headers)
        t1 = re.findall('fetchJSON_comment98vv6\((.*)\);', html1.text)
        json_data = json.loads(t1[0])
        for comment in json_data['comments']:
            content = comment['content']
            creationTime = comment['creationTime']
            productColor = comment['productColor']
            productSize = comment['productSize']
            userClientShow = comment['userClientShow']
            userLevelName = comment['userLevelName']
            content = MySQLdb.escape_string(content)
            # print(content,creationTime,productColor,productSize,userClientShow,userLevelName)
            #writer.writerow((content,creationTime,productColor,productSize,userClientShow,userLevelName))
            #sql1 = "INSERT INTO EMPLOYEE(content1) VALUES ('%s')" % (content)
            sql1 = "INSERT INTO EMPLOYEE(content1,creationTime1, productColor1, productSize1, userClientShow1,userLevelName1) \
                   VALUES ('%s', '%s', '%s', '%s', '%s' ,'%s' )" % \
                  (content, creationTime, productColor, productSize, userClientShow,userLevelName)
            # try:
            #db.set_character_set('utf8')
            cursor.execute(sql1)
            print "保存成功"
            db.commit()
            # except:
            #     db.rollback()
            #     print "保存失败"
        time.sleep(2)

if __name__ == '__main__':
    url = 'https://search.jd.com/Search?keyword=%e5%8d%8e%e4%b8%ba%e6%89%8b%e6%9c%ba&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.his.0.0&page=1&s=1&click=0'
    get_id(url)

