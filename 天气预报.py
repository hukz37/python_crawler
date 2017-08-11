#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/10 下午1:20
# @Author  : hukezhu
# @Site    : 
# @File    : 天气预报.py
# @Software: PyCharm


#import urllib.request
import json
import base64
import requests
from bs4 import BeautifulSoup
import datetime
import sys
import time


reload(sys)
sys.setdefaultencoding("utf-8")

url = 'http://www.weather.com.cn/weather1d/101010300.shtml'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

html = requests.get(url,headers).content
soup = BeautifulSoup(html,'lxml')
weather_day = soup.select('div.t > ul > li > p.wea')[0].text
weather_night = soup.select('div.t > ul > li > p.wea')[1].text
tmp_day = soup.select('div.t > ul > li > p.tem > span')[0].text
tmp_night = soup.select('div.t > ul > li > p.tem > span')[1].text
wind_day = soup.select('div.t > ul > li > p.win > span')[0].text
wind_night = soup.select('div.t > ul > li > p.win > span')[1].text
uv_index = soup.select('div.con.today.clearfix > div.left.fl > div.livezs > ul > li.li1.hot > span')[0].text #紫外线指数
ganmao_index = soup.select('div.con.today.clearfix > div.left.fl > div.livezs > ul > li.li2.hot > span')[0].text
gaomao_detail = soup.select('div.con.today.clearfix > div.left.fl > div.livezs > ul > li.li2.hot > p')[0].text
dress_index = soup.select('li#chuanyi > a > span')[0].text     #穿衣指数
dress_detail = soup.select('li#chuanyi > a > p')[0].text
carwash_index = soup.select('div.con.today.clearfix > div.left.fl > div.livezs > ul > li.li4.hot > span')[0].text    #洗车指数
carwash_detail = soup.select('div.con.today.clearfix > div.left.fl > div.livezs > ul > li.li4.hot > p')[0].text
play_index = soup.select('div.con.today.clearfix > div.left.fl > div.livezs > ul > li.li5.hot > span')[0].text       #运动指数
play_detail = soup.select('div.con.today.clearfix > div.left.fl > div.livezs > ul > li.li5.hot > p')[0].text
air_index = soup.select('div.con.today.clearfix > div.left.fl > div.livezs > ul > li.li6.hot > span')[0].text
air_detail = soup.select('div.con.today.clearfix > div.left.fl > div.livezs > ul > li.li6.hot > p')[0].text
now_date = datetime.datetime.now().strftime('%Y-%m-%d %A')
weather_txt = "今天是%s,白天%s,%s,最高温度%s摄氏度,夜间%s,%s,最低温度%s摄氏度((今日紫外线指数,%s,感冒指数,%s,%s"\
            "穿衣指数,%s,%s,运动指数,%s,%s空气污染扩散指数,%s,%s))[北京-朝阳]"%(now_date,weather_day,wind_day,tmp_day,\
            weather_night,wind_day,tmp_night,uv_index,ganmao_index,gaomao_detail,dress_index,dress_detail,\
            play_index,play_detail,air_index,air_detail)
print weather_txt