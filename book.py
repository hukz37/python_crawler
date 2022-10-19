import requests
import os
import json
import random
import time
global isCount
isCount = 0


def getBookCount():
    global isCount
    data = {
        'period': '2022-10-22（星期六） 09:00-12:30'
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Cookie': 'JSESSIONID=E74E188E50D7DC5F52C30E3C31F6C435',
        'Host': '51zjmx.cn',
        'Origin': 'http://51zjmx.cn',
        'Referer': 'http://51zjmx.cn/sygh/',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
    }

    response = requests.post('http://51zjmx.cn/sygh/appoint/getRestQuota.do', params=data, headers=headers)
    print('接口返回数据为:%s \n' % response.text)
    # print(response.text)
    if response.status_code == 200:
        # isCount = isCount + 1
        res = json.loads(response.text).get('restQuota')
        # print(res)
        if int(res) > 0:
            while 1:
                os.system('say "释放名额了,抓紧去抢吧"')


def mymain(name):
    global isCount
    while isCount == 0:
        rand = random.randint(2, 100)
        # rand = random.randint(1, 50)
        print('本次随机时间为:%s \n' % rand)
        time.sleep(rand)
        getBookCount()


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    mymain('PyCharm')
