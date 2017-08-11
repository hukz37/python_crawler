#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/19 下午5:54
# @Author  : Aries
# @Site    : 
# @File    : h5.py
# @Software: PyCharm


# !/usr/bin/python
# coding: utf-8

'''
总的来说就是通过搜狗搜索中的微信搜索入口来爬取
2017-04-12 by Jimy_fengqi
'''

# 这三行代码是防止在python2上面编码错误的，在python3上面不要要这样设置
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from urllib import quote
from pyquery import PyQuery as pq
from selenium import webdriver
from pyExcelerator import *  # 导入excel相关包

import requests
import time
import re
import json
import os


class weixin_spider:
    def __init__(self, keywords):
        ' 构造函数 '
        self.keywords = keywords
        # 搜狐微信搜索链接入口
        # self.sogou_search_url = 'http://weixin.sogou.com/weixin?type=1&query=%s&ie=utf8&_sug_=n&_sug_type_=' % quote(self.keywords)
        self.sogou_search_url = 'http://weixin.sogou.com/weixin?type=1&query=%s&ie=utf8&s_from=input&_sug_=n&_sug_type_=' % quote(
            self.keywords)

        print '呵呵'

        # 爬虫伪装头部设置
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}

        # 设置操作超时时长
        self.timeout = 5

        # 爬虫模拟在一个request.session中完成
        self.s = requests.Session()

        # excel 第一行数据
        self.excel_data = [u'编号', u'时间', u'文章标题', u'文章地址', u'文章简介']
        # 定义excel操作句柄
        self.excle_w = Workbook()

    # 搜索入口地址，以公众为关键字搜索该公众号
    def get_search_result_by_keywords(self):
        self.log('搜索地址为：%s' % self.sogou_search_url)
        return self.s.get(self.sogou_search_url, headers=self.headers, timeout=self.timeout).content

    # 获得公众号主页地址
    def get_wx_url_by_sougou_search_html(self, sougou_search_html):
        doc = pq(sougou_search_html)
        # print doc('p[class="tit"]')('a').attr('href')
        # print doc('div[class=img-box]')('a').attr('href')
        # 通过pyquery的方式处理网页内容，类似用beautifulsoup，但是pyquery和jQuery的方法类似，找到公众号主页地址
        return doc('div[class=txt-box]')('p[class=tit]')('a').attr('href')

    # 使用webdriver 加载公众号主页内容，主要是js渲染的部分
    def get_selenium_js_html(self, url):
        print '进入了get_selenium_js_html'
        browser = webdriver.Firefox(executable_path='/Users/hukezhu/Downloads/geckodriver')
        browser.get(url)
        time.sleep(3)
        # 执行js得到整个页面内容
        html = browser.execute_script("return document.documentElement.outerHTML")
        browser.quit()
        return html

    # 获取公众号文章内容
    def parse_wx_articles_by_html(self, selenium_html):
        doc = pq(selenium_html)
        print '开始查找内容msg'
        return doc('div[class="weui_media_box appmsg"]')

    # 有的公众号仅仅有10篇文章，有的可能多一点
    # return doc('div[class="weui_msg_card"]')#公众号只有10篇文章文章的


    # 将获取到的文章转换为字典
    def switch_arctiles_to_list(self, articles):
        # 定义存贮变量
        articles_list = []
        i = 1

        # 以当前时间为名字建表
        excel_sheet_name = time.strftime('%Y-%m-%d')
        excel_content = self.excle_w.add_sheet(excel_sheet_name)

        # 遍历找到的文章，解析里面的内容
        if articles:
            for article in articles.items():
                self.log(u'开始整合(%d/%d)' % (i, len(articles)))
                # 处理单个文章
                articles_list.append(self.parse_one_article(article, i, excel_content))
                i += 1
        return articles_list

    # 解析单篇文章
    def parse_one_article(self, article, i, excel_content):
        article_dict = {}

        # 获取标题
        title = article('h4[class="weui_media_title"]').text()
        self.log('标题是： %s' % title)
        # 获取标题对应的地址
        url = 'http://mp.weixin.qq.com' + article('h4[class="weui_media_title"]').attr('hrefs')
        self.log('地址为： %s' % url)
        # 获取概要内容
        summary = article('.weui_media_desc').text()
        self.log('文章简述： %s' % summary)
        # 获取文章发表时间
        date = article('.weui_media_extra_info').text()
        self.log('发表时间为： %s' % date)
        # 获取封面图片
        pic = self.parse_cover_pic(article)
        # 获取文章内容
        content = self.parse_content_by_url(url).html()
        # 存储文章到本地
        contentfiletitle = self.keywords + '/' + title + '_' + date + '.html'
        self.save_content_file(contentfiletitle, content)

        # 将这些简单的信息保存成excel数据
        cols = 0
        tempContent = [i, date, title, url, summary]
        for data in self.excel_data:
            excel_content.write(0, cols, data)
            excel_content.write(i, cols, tempContent[cols])

            cols += 1
        self.excle_w.save(self.keywords + '/' + self.keywords + '.xls')

        # 返回字典数据
        return {
            'title': title,
            'url': url,
            'summary': summary,
            'date': date,
            'pic': pic,
            'content': content
        }

    # 查找封面图片，获取封面图片地址
    def parse_cover_pic(self, article):
        pic = article('.weui_media_hd').attr('style')

        p = re.compile(r'background-image:url\((.*?)\)')
        rs = p.findall(pic)
        self.log('封面图片是：%s ' % rs[0] if len(rs) > 0 else '')

        return rs[0] if len(rs) > 0 else ''

    # 获取文章页面详情
    def parse_content_by_url(self, url):
        page_html = self.get_selenium_js_html(url)
        return pq(page_html)('#js_content')

    # 存储文章到本地
    def save_content_file(self, title, content):
        with open(title, 'w') as f:
            f.write(content)

    # 存贮json数据到本地
    def save_file(self, content):
        ' 数据写入文件 '
        with open(self.keywords + '/' + self.keywords + '.txt', 'w') as f:
            f.write(content)

    # 自定义log函数，主要是加上时间
    def log(self, msg):
        print u'%s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg)

    # 验证函数
    def need_verify(self, selenium_html):
        ' 有时候对方会封锁ip，这里做一下判断，检测html中是否包含id=verify_change的标签，有的话，代表被重定向了，提醒过一阵子重试 '
        return pq(selenium_html)('#verify_change').text() != ''

    # 创建公众号命名的文件夹
    def create_dir(self):
        if not os.path.exists(self.keywords):
            os.makedirs(self.keywords)

            # 爬虫主函数

    def run(self):


        ' 爬虫入口函数 '
        # Step 0 ：  创建公众号命名的文件夹
        print '进入run函数'

        self.create_dir()

        # Step 1：GET请求到搜狗微信引擎，以微信公众号英文名称作为查询关键字
        self.log(u'开始获取，微信公众号英文名为：%s' % self.keywords)
        self.log(u'开始调用sougou搜索引擎')
        sougou_search_html = self.get_search_result_by_keywords()

        # Step 2：从搜索结果页中解析出公众号主页链接
        self.log(u'获取sougou_search_html成功，开始抓取公众号对应的主页wx_url')
        wx_url = self.get_wx_url_by_sougou_search_html(sougou_search_html)
        self.log(u'获取wx_url成功，%s' % wx_url)

        # Step 3：Selenium+PhantomJs获取js异步加载渲染后的html
        self.log(u'开始调用selenium渲染html')
        selenium_html = self.get_selenium_js_html(wx_url)

        # Step 4: 检测目标网站是否进行了封锁
        if self.need_verify(selenium_html):
            self.log(u'爬虫被目标网站封锁，请稍后再试')
        else:
            # Step 5: 使用PyQuery，从Step 3获取的html中解析出公众号文章列表的数据
            self.log(u'调用selenium渲染html完成，开始解析公众号文章')
            articles = self.parse_wx_articles_by_html(selenium_html)
            self.log(u'抓取到微信文章%d篇' % len(articles))

            # Step 6: 把微信文章数据封装成字典的list
            self.log(u'开始整合微信文章数据为字典')
            articles_list = self.switch_arctiles_to_list(articles)

            # Step 7: 把Step 5的字典list转换为Json
            self.log(u'整合完成，开始转换为json')
            data_json = json.dumps(articles_list)

            # Step 8: 写文件
            self.log(u'转换为json完成，开始保存json数据到文件')
            self.save_file(data_json)

            self.log(u'保存完成，程序结束')


# main
# 几个可供参考的公众号
# DataBureau
# python6359
# ArchNotes
if __name__ == '__main__':
    print '''
			*****************************************
			**    Welcome to Spider of 公众号       **
			**      Created on 2017-04-12          **
			**                                     **
			*****************************************
	'''
    gongzhonghao = raw_input(u'')
    if not gongzhonghao:
        gongzhonghao = '树莓派'
    weixin_spider(gongzhonghao).run()
