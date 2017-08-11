#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/9 下午1:31
# @Author  : hukezhu
# @Site    : 
# @File    : 妹子图.py
# @Software: PyCharm


import requests
from lxml import etree
import time
import sys
import MySQLdb
import os
#import leancloud


reload(sys)
sys.setdefaultencoding("utf-8")

headers111 = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36',
'Accept':'text/html;q=0.9,*/*;q=0.8',
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding':'gzip',
'Connection':'close',
'Referer':None #注意如果依然不能抓取的话，这里可以设置抓取网站的host
}


headers1 = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36',
'Accept':'image/webp,image/apng,image/*,*/*;q=0.8',
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding':'gzip',
'Connection':'close',
'Referer':'http://www.mzitu.com/' , #注意如果依然不能抓取的话，这里可以设置抓取网站的host
'Host' : 'i.meizitu.net'
}



def get_url(url,a):
    html = requests.get(url,headers = headers111)
    selector = etree.HTML(html.text)
    infos = selector.xpath('//*[@id="pins"]/li/a/img')
    for info in infos:
        try:
            content = MySQLdb.escape_string(info.get('alt'))
            imgsource = MySQLdb.escape_string(info.get('data-original'))
            print content + '  ' + imgsource
            time.sleep(0)
            saveImg(imgsource,content)
            #leancloud.init("xlWVj5yFEf2YEWsKhR2iaNrI-gzGzoHsz", "v8z65COo5xHyYfquH0S3CDpw")
            #todo = Todo()
            #todo.set('title', content)
            #todo.set('img', imgsource)
            #todo.save()
        except IndexError:
            pass
    time.sleep(2)
    a = a + 1
    url = 'http://www.mzitu.com/page/%s' % a
    print '现在是第%s页' % a
    get_url(url, a)


def saveImg(img_url,name):
    #name = img_url[-9:-4]
    img = request_content(img_url)
    f = open("/Users/hukezhu/Desktop/meizi1/" + name + '.jpg', 'ab')
    f.write(img.content)
    f.close()

def request_content( url):  ##这个函数获取网页的response 然后返回
    #headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    content = requests.get(url, headers=headers1)
    return content

def mkdir( path):  ##这个函数创建文件夹
    path = path.strip()
    isExists = os.path.exists(os.path.join("/Users/hukezhu/Desktop", path))
    if not isExists:
        print(u'建了一个名字叫做', path, u'的文件夹！')
        os.makedirs(os.path.join("/Users/hukezhu/Desktop", path))
        os.chdir(os.path.join("/Users/hukezhu/Desktop", path))  ##切换到目录
        return True
    else:
        print(u'名字叫做', path, u'的文件夹已经存在了！')
        return False

if __name__ == '__main__':
    #leancloud.init("xlWVj5yFEf2YEWsKhR2iaNrI-gzGzoHsz", "vv8z65COo5xHyYfquH0S3CDpw")
    #Todo = leancloud.Object.extend('Todo')

    url = 'http://www.mzitu.com/'
    a = 1
    mkdir('meizi1')
    get_url(url,a)