#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/10 下午3:06
# @Author  : hukezhu
# @Site    :
# @File    : wechat.py
# @Software: PyCharm


from numpy import *
import itchat
import urllib
import requests
import os
import sys

import PIL.Image as Image
from os import listdir
import math

itchat.auto_login(True)

reload(sys)
sys.setdefaultencoding('utf8')




friends = itchat.get_friends(update=True)[0:]

user = friends[0]["UserName"]

print(user)

os.mkdir(user)

num = 0

for i in friends:
    img = itchat.get_head_img(userName=i["UserName"])
    fileImage = open(user + "/" + str(num) + ".png",'wb')
    fileImage.write(img)
    fileImage.close()
    num += 1

pics = listdir(user)

numPic = len(pics)

print(numPic)

eachsize = int(math.sqrt(float(600 * 600) / numPic))

print(eachsize)

numline = int(600 / eachsize)

toImage = Image.new('RGBA', (600, 600))


print(numline)

x = 0
y = 0

for i in pics:
    try:
        #打开图片
        img = Image.open(user + "/" + i)
    except IOError:
        print("Error: 没有找到文件或读取文件失败")
    else:
        #缩小图片
        img = img.resize((eachsize, eachsize), Image.ANTIALIAS)
        #拼接图片
        toImage.paste(img, (x * eachsize, y * eachsize))
        x += 1
        if x == numline:
            x = 0
            y += 1


toImage.save(user + ".png")


userhh=itchat.search_friends(name="房小喵")  #输入她的备注
username=userhh[0]['UserName']
itchat.send_image(user + ".png", username)
