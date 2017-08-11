#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/31 下午3:53
# @Author  : hukezhu
# @Site    : 
# @File    : 房产信息爬取.py
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
import pycurl
import random

reload(sys)
sys.setdefaultencoding("utf-8") #更改默认编码为utf-8

headers111 = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept':'text/html;q=0.9,*/*;q=0.8',
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding':'gzip',
'Connection':'close',
'Referer':None #注意如果依然不能抓取的话，这里可以设置抓取网站的host
}

#fp = open('/Users/hukezhu/Desktop/wenxiong1.csv','wt')
#writer = csv.writer(fp)
#writer.writerow(('content','creationTime','productColor','productSize','userClientShow','userLevelName'))

db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='123456',db='TAIAN',charset='utf8mb4')
cursor = db.cursor()



# cursor.execute("DROP TABLE IF EXISTS HOUSE11")
# sql = """CREATE TABLE HOUSE11 (
#         ID INT NOT NULL,
#         city11  CHAR(200),
#         name11  CHAR(200),
#         card11  CHAR(200),
#         company11 text,
#         time11 CHAR(200))"""
#
#
# cursor.execute(sql)




def get_id(url,a):
    print url
    #
    # py = pycurl.Curl()  # 创建一个pycurl对象的方法
    # py.setopt(py.URL, url)
    # py.setopt(py.MAXREDIRS, 5)  # 设置最大重定向次数
    # py.setopt(py.CONNECTTIMEOUT, 60)
    # py.setopt(py.TIMEOUT, 300)  # 连接超时设置
    # py.setopt(py.USERAGENT,
    #                      "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)")  # 模拟浏览器
    # print py.perform()  # 服务器端返回的信息


    options = webdriver.ChromeOptions()
    # options.add_argument(
    #     'Accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","Accept-Encoding"= "gzip, deflate",Accept-Language= "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",Cookie= "JSESSIONID=CF97DB9D486D913AD3E07468FAFC381A-n2; pubDistrict=370900; _gscu_548463855=99332093cli56710; _gscbrs_548463855=1",User-Agent= "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36",Host= "cucc.tazzfdc.com"')
    # UA = ["Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    #       "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"]
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Upgrade-Insecure-Requests": "1",
        "Cookie": "JSESSIONID=CF97DB9D486D913AD3E07468FAFC381A-n2; pubDistrict=370900; _gscu_548463855=99332093cli56710; _gscbrs_548463855=1",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36",
        "Host": "cucc.tazzfdc.com",

    }
    # 更换头部
    options.add_argument('user-agent="Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36"')
    options.add_argument('Accept="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"')
    options.add_argument('Upgrade-Insecure-Requests="1"')
    options.add_argument('Cookie="JSESSIONID=CFAC46F8E681265CAE8857B141E02D22-n1; pubDistrict=370900; _gscu_548463855=99332093cli56710; _gscs_548463855=016372841xxl7629|pv:1; _gscbrs_548463855=1"')
    options.add_argument('Connection="keep-alive"')
    options.add_argument('Host="cucc.tazzfdc.com"')
    options.add_argument('Accept-Encoding="gzip, deflate"')
    options.add_argument('Accept-Language="zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"')
    options.add_argument('Cache-Control="max-age=0"')

    html = requests.get(url, headers=headers)
    #print html.text
    #options.add_argument('--user-data-dir=/Users/hukezhu/Library/Application Support/Google/Chrome/Default')
    browser = webdriver.Chrome(executable_path='/Users/hukezhu/Downloads/chromedriver',chrome_options=options)

    browser.get('https://cucc.tazzfdc.com/reisPub/pub/')
    time.sleep(10)
    browser.get(url)

    a = 1
    b = 1
    while a == 1 :
        # print browser.page_source
        # data = browser.find_element_by_id("data_table_2")
        selector = etree.HTML(browser.page_source)
        infos = selector.xpath('//*[@id="data_table_2"]/tbody/tr')
        for info in infos:
            try:



                if info.xpath('td[1]/div')[0].text is None:
                    content1 = 'data null'
                else:
                    content1 = MySQLdb.escape_string(info.xpath('td[1]/div')[0].text)

                if info.xpath('td[2]/a')[0].text is None:
                    content2 = 'data null '
                else:
                    content2 = MySQLdb.escape_string(info.xpath('td[2]/a')[0].text)

                if info.xpath('td[3]')[0].text is None:
                    content3 = 'data null '
                else:
                    content3 = MySQLdb.escape_string(info.xpath('td[3]')[0].text)

                if info.xpath('td[4]')[0].text is None:
                    content4 = 'data null'
                else:
                    content4 = MySQLdb.escape_string(info.xpath('td[4]')[0].text)

                if info.xpath('td[5]')[0].text is None:
                    content5 = 'data null '
                else:
                    content5 = MySQLdb.escape_string(info.xpath('td[5]')[0].text)

                #print info.xpath('td[1]/div')[0].text
                print b
                b = b + 1
                #print info.xpath('td[3]')[0].text
                #print info.xpath('td[4]')[0].text
                #print info.xpath('td[5]')[0].text
                #content = MySQLdb.escape_string(info.text)
                # print info.get('href')
                # print '\n'
                # print info.xpath('text()')[0] + "  " + "http://www.bookingtee.com/"+info.xpath('@href')[0]
                # print "http://www.bookingtee.com/"+info.xpath('@href')[0]


                sql1 = "INSERT INTO HOUSE11(city11,name11, card11,company11,time11) \
                                   VALUES ('%s', '%s', '%s','%s','%s' )" % \
                       (content1, content2,content3,content4,content5)
                cursor.execute(sql1)
                db.commit()
                time.sleep(1)
                # get_comment_info("http://www.bookingtee.com/"+info.xpath('@href')[0])
            except IndexError:
                pass
        wss = browser.find_elements_by_xpath('//*[@id="center"]/a')
        for wd in wss:
            if wd.text == '下一页 »':
                print '点击了下一页 \n'
                wd.click()
        time.sleep(5)

    browser.close()
    # #browser.close()
    # url = 'https://cucc.tazzfdc.com/reisPub/pub/preSaleBuildingStatist'
    # a = 1
    # get_id(url, a)




def get_comment_info(url):
    html = requests.get(url, headers=headers)
    # print html.text
    selector = etree.HTML(html.text)
    courseinfo = selector.xpath('/html/body/div[13]/div/div[2]/ul/li')

    for course in courseinfo:
        try:
            content = course.xpath('a')[0].text
            content = MySQLdb.escape_string(content)
            print content + '   '
            print '\n\n\n\n'
            # sql1 = "INSERT INTO YUNGAO11(name,price, web) \
            #                    VALUES ('%s', '%s', '%s')" % \
            #        (content, course.xpath('span')[0].text, "http://www.bookingtee.com/"+ course.xpath('a')[0].get('href'))
            # # try:
            # # db.set_character_set('utf8')
            # cursor.execute(sql1)
            # print "保存成功"
            # db.commit()
            # except:
            #     db.rollback()
            #     print "保存失败"
        except IndexError:
            pass

        time.sleep(2)




if __name__ == '__main__':
    url = 'https://cucc.tazzfdc.com/reisPub/pub/preSaleBuildingStatist'
    a = 1
    #browser = webdriver.Chrome(executable_path='/Users/hukezhu/Downloads/chromedriver')
    #browser.get(url)
    get_id(url,a)