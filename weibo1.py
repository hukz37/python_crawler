#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/9 上午11:17
# @Author  : hukezhu
# @Site    : 
# @File    : weibo1.py
# @Software: PyCharm



#! /usr/bin/python

"""
引入Python SDK的包
"""
import sinaweibo


"""
授权需要的三个信息，APP_KEY、APP_SECRET为创建应用时分配的，CALL_BACK在应用的设置网页中
设置的。【注意】这里授权时使用的CALL_BACK地址与应用中设置的CALL_BACK必须一致，否则会出
现redirect_uri_mismatch的错误。
"""
APP_KEY = '2482130002'
APP_SECRET = '8c0ff22c537f4c182dc0f35706e57294'
CALL_BACK = 'https://api.weibo.com/oauth2/default.html'


def run():
        #weibo模块的APIClient是进行授权、API操作的类，先定义一个该类对象，传入参数为APP_KEY, APP_SECRET, CALL_BACK
	client = weibo.APIClient(APP_KEY, APP_SECRET, CALL_BACK)
        #获取该应用（APP_KEY是唯一的）提供给用户进行授权的url
	auth_url = client.get_authorize_url()
	#打印出用户进行授权的url，将该url拷贝到浏览器中，服务器将会返回一个url，该url中包含一个code字段（如图1所示）
	print "auth_url : " + auth_url
	#输入该code值（如图2所示）
	code = raw_input("input the retured code : ")
	#通过该code获取access_token，r是返回的授权结果，具体参数参考官方文档：
	# http://open.weibo.com/wiki/Oauth2/access_token
	r = client.request_access_token(code)
        #将access_token和expire_in设置到client对象
	client.set_access_token(r.access_token, r.expires_in)

	#以上步骤就是授权的过程，现在的client就可以随意调用接口进行微博操作了，下面的代码就是用用户输入的内容发一条新微博

	while True:
		print "Ready! Do you want to send a new weibo?(y/n)"
		choice = raw_input()
		if choice == 'y' or choice == 'Y':
			content = raw_input('input the your new weibo content : ')
			if content:
                                #调用接口发一条新微薄，status参数就是微博内容
				client.statuses.update.post(status=content)
				print "Send succesfully!"
				break;
			else:
				print "Error! Empty content!"
		if choice == 'n' or choice == 'N':
			break
		if choice == 'q':
			break


if __name__ == "__main__":
	run()
