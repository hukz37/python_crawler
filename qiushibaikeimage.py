#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/26 下午1:14
# @Author  : Aries
# @Site    : 
# @File    : qiushibaikeimage.py
# @Software: PyCharm

import requests
from lxml import etree
import time
import json
import re
import csv
import sys
import MySQLdb
import os
import urllib
import uuid
import urllib2
# from html.parser import HTMLParser
import HTMLParser

reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
    'Cookie': 'ipLoc-djd=1-72-2799-0; unpl=V2_ZzNtbRZXF0dwChEEfxtbV2IKFQ4RUBcSdg1PVSgZCVAyCkBVclRCFXMUR1NnGFkUZgoZXkpcQxNFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2VH4RWAVmBxVeS19AEHUJR1x6GFsBYQEibUVncyVyDkBQehFsBFcCIh8WC0QcdQ1GUTYZWQ1jAxNZRVRKHXYNRlV6EV0EYAcUX3JWcxY%3d; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_e1ec43fa536c486bb6e62480b1ddd8c9|1496536177759; mt_xid=V2_52007VwMXWllYU14YShBUBmIDE1NVWVNdG08bbFZiURQBWgxaRkhKEQgZYgNFV0FRVFtIVUlbV2FTRgJcWVNcSHkaXQVhHxNVQVlXSx5BEl0DbAMaYl9oUmofSB9eB2YGElBtWFdcGA%3D%3D; __jda=122270672.14951056289241009006573.1495105629.1496491774.1496535400.5; __jdb=122270672.26.14951056289241009006573|5.1496535400; __jdc=122270672; 3AB9D23F7A4B3C9B=EJMY3ATK7HCS7VQQNJETFIMV7BZ5NCCCCSWL3UZVSJBDWJP3REWXTFXZ7O2CDKMGP6JJK7E5G4XXBH7UA32GN7EVRY; __jdu=14951056289241009006573',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}


class MyHTMLParser():
    '''
    网页解析生成一个HTMLParser的类，然后利用这个类，
    把给定的一个网址中所需要的地址解析并保存在该类中，
    然后利用该类的的地址，下载图片。
    '''

    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
        pass

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:",tag)
        if tag == "img":
            s = []
            for (variable, value) in attrs:
                s.append(value)
            # print("ss:",s)
            self.links.append(s)
            s = []
        pass

    def handle_endtag(self, tag):
        # print("Encountered a end tag:",tag)
        pass

    def handle_data(self, data):
        # print("Encountered some data:",data)
        pass


# 生成一个文件名字符串
def generateFileName():
    return str(uuid.uuid4())


# 根据文件名创建文件
def createFileWithFileName(localPathParam, fileName):
    totalPath = localPathParam + '' + fileName
    if not os.path.exists(totalPath):
        file = open(totalPath, 'wb+')
        file.close()
        return totalPath

def save_img(img_url, file_name, file_path='/Users/hukezhu/Desktop/img/'):
    # 保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的 book\img文件夹
    try:
        # if not os.path.exists(file_path):
        #     print '文件夹', file_path, '不存在，重新建立'
        #     #os.mkdir(file_path)
        #     os.makedirs(file_path)

        # # 获得图片后缀
        # file_suffix = os.path.splitext(img_url)[1]
        # # 拼接图片名（包含路径）
        # filename = '{}{}{}{}'.format(file_path, os.sep, file_name, file_suffix)
        # # 下载图片，并保存到文件夹中
        # path = r'/Users/hukezhu/Desktop/img/' + file_name
        # urllib.urlretrieve(img_url, path)e
        fileName = generateFileName() + '.jpg'
        urllib.urlretrieve(img_url, createFileWithFileName("/Users/hukezhu/Desktop/img/", fileName))
        time.sleep(5)
    except IOError as e:
        #print '文件操作失败', e
        pass
    except Exception as e:
        print '错误 ：', e


def down_image(url,file_name):
    global headers
    req = urllib2.Request(url = url, headers = headers)
    binary_data = urllib2.urlopen(req).read()
    temp_file = open(file_name, 'wb')
    temp_file.write(binary_data)
    temp_file.close()


def geturl(url):
    '''
    打开给定的网页，并返回网页的内容,
    python3中来来是以字节码形式返回的，
    可以根据网页编码判定编码为gb2312,是gbk的子集，
    以字符串形式返回。
    '''
    req = urllib.urlopen(url)
    req = req.read()
    return req.decode("gbk")


def continsrc(src):
    '''
    根据网页的内容，找到我们所需要的内容，
    这里主要是有两个需要关注的内容，一个是picture标签，另一个是boxinfo标签。
    '''
    inta = src.find("<div id=\"picture\">")
    # print(inta) 所找的第一个位置点
    intb = src.find("<div class=\"boxinfo\">")
    # print(intb) 所找的第二个位置点
    content = src[inta:intb]
    return content

def pageinurl(url):
    '''
    这个是把上面的许多功能放在一个函数库里，方便操作。
    作用是给定一个url，自动去解析地址，并自动下载保存图片。
    '''
    src = geturl(url)
    content = continsrc(src)
    parser = MyHTMLParser()
    parser.feed(content)
    parser.close()
    alinks = parser.links
    for i in range(len(alinks)):
        print("filename:",alinks[i][0],"fileurl:",alinks[i][1])
        urllib.request.urlretrieve(alinks[i][1],alinks[i][0]+".jpg")
    print("ok!!")

def get_id(url, a):
    html = requests.get(url, headers=headers)
    # print html.text
    selector = etree.HTML(html.text)
    infos = selector.xpath('//div[@class="thumb"]/a/img')
    for info in infos:
        try:
            urlstr = "http" + info.get('src')
            print urlstr
            # print info.xpath('text()')[0] + "  " + "http://www.bookingtee.com/"+info.xpath('@href')[0]
            # print "http://www.bookingtee.com/"+info.xpath('@href')[0]
            #save_img(urlstr, 'qiubai')
            time.sleep(5)
            # get_comment_info("http://www.bookingtee.com/"+info.xpath('@href')[0])
            #downloadCatoon(urlstr,'/Users/hukezhu/Desktop/img',uuid.uuid4())
            pageinurl(urlstr)
        except IndexError:
            print '出错了'
            pass
    time.sleep(5)
    print "当前保存了%s页" % a
    a = a + 1
    url = 'https://www.qiushibaike.com/imgrank/page/%s/?s=5003486' % a
    get_id(url, a)


def get_comment_info(url):
    html = requests.get(url, headers=headers)
    # print html.text
    selector = etree.HTML(html.text)
    courseinfo = selector.xpath('/html/body/div[13]/div/div[2]/ul/li')

    for course in courseinfo:
        try:
            content = course.xpath('a')[0].text
            content = MySQLdb.escape_string(content)

            print '\n\n\n\n'
        except IndexError:
            pass

        time.sleep(2)


if __name__ == '__main__':
    a = 1
    url = 'https://www.qiushibaike.com/imgrank/page/1/?s=5003486'
    get_id(url, a)


