# coding=utf-8
import ch
ch.set_ch()
#对pyplot添加中文支持
import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



#------------------------数据提取-----------------------------
url='https://bj.lianjia.com/ershoufang/pg/'

headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2;.NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; InfoPath.3; .NET4.0C; .NET4.0E)',
         'Accept':'image/webp,image/*,*/*;q=0.8',
         'Referer':'http://bj.lianjia.com/ershoufang/pg9/',
         'Accept-Encoding':'gzip, deflate',
         'Connection':'keep-alive'   }

#抓取网页存入变量html
for i in range(1,10):
    if i == 1:
        i=str(i)
        html=requests.get(url=url+i+'/',headers=headers).content
    else:
        i=str(i)
        html2=requests.get(url=url+i+'/',headers=headers).content
        html=html+html2
    time.sleep(0.5)


#还原成浏览器按f12看到的源代码
lj=BeautifulSoup(html,'html.parser')

#提取房源总价
price=lj.find_all('div',attrs={'class':'priceInfo'})
tp=[]
for a in price:
    totalPrice=a.span.string
    tp.append(totalPrice)
    
#提取房源信息
houseInfo=lj.find_all('div',attrs={'class':'houseInfo'})
hi=[]
for b in houseInfo:
    house=b.get_text()
    hi.append(house)

#提取房源关注度
followInfo=lj.find_all('div',attrs={'class':'followInfo'})
fi=[]
for c in followInfo:
    follow=c.get_text()
    fi.append(follow)



#------------------------数据规范-----------------------------
house=pd.DataFrame({'totalprice':tp,'houseinfo':hi,'followinfo':fi})
#house.head()



houseinfo_split=pd.DataFrame((x.split('|') for x in house.houseinfo),\
                             index=house.index,\
                             columns=['小区','户型','mianji','朝向','装修','电梯'])
#houseinfo_split.head()

house=pd.merge(house,houseinfo_split,right_index=True,left_index=True)

followinfo_split=pd.DataFrame((x.split('/') for x in house.followinfo),\
                             index=house.index,\
                             columns=['guanzhu','热度','日期'])
house=pd.merge(house,followinfo_split,right_index=True,left_index=True)




#----------------------房源户型分布情况数据分析-------------------------

'''
#按房源户型类别进行汇总
huxing=house.groupby('户型')['户型'].agg(len)
#或者huxing=house.groupby('户型').size()

print huxing

#绘制房源户型分布条形图
#plt.rc('ront',family='STXihei',size=11)


#绘制房源户型分布图

a=np.array([1,2,3,4,5,6,7,8,9,10,11,12,13])
plt.barh([1,2,3,4,5,6,7,8,9,10,11,12,13],huxing,color='#052B6C',
        alpha=0.8,align='center',edgecolor='white');
plt.ylabel(u'户型')
plt.xlabel(u'数量')
plt.xlim(0,90)
plt.ylim(0,13)
plt.title(u'北京市二手房户型分布情况')
plt.legend([u'数量'],loc='upper right')
plt.grid(color="#95a5a6",linestyle='--',linewidth=1,axis='y',alpha=0.4)

plt.yticks(a,(u'1室0厅',u'1室1厅',u'2室1厅',u'2室2厅',
           u'3室1厅',u'3室2厅',u'3室4厅',u'4室1厅',u'4室2厅',u'5室2厅',
           u'5室3厅',u'7室2厅',u'联排别墅' ))
plt.show()
'''




#----------------------房源面积分布情况数据分析-------------------------

#对房源面积进行二次分列
mianji_num_split = pd.DataFrame((x.split(u'平') for x in house.mianji),\
                                index=house.index,\
                                columns=['mianji_num','mi'])
#将分列后的房源面积拼接回原数据表
house=pd.merge(house,mianji_num_split,right_index=True,left_index=True)

#去除两端的空格,更改字段格式为float

for h in range(len(house['mianji_num'])):
    house['mianji_num'][h]=house['mianji_num'][h].encode('utf-8')
    house['mianji_num'][h]=house['mianji_num'][h].strip(' ')


#之所以用try是因为在测试的时候有两个值竟然是"3室2厅"。。将就了
    try:
        house['mianji_num'][h]=float(house['mianji_num'][h])
    except:
        house['mianji_num'][h]=house['mianji_num'][h-1]

#house['mianji_num'].min(),house['mianji_num'].max()
'''
bins=[0,50,100,150,200,250,300,350]
group_mianji=[u'小于50','50-100','100-150','150-200','200-250','250-300','300-350'];
house['mianji_num']=pd.cut(house['mianji_num'],bins,labels=group_mianji)

group_mianji=house.groupby('mianji_num')['mianji_num'].agg(len)
a=np.array([1,2,3,4,5,6,7])
plt.barh([1,2,3,4,5,6,7],group_mianji,color='#052B6C',
        alpha=0.8,align='center',edgecolor='white');

plt.ylabel(u"面积分布")
plt.xlabel(u'数量')
plt.title(u'北京市二手房户型面积分布')
plt.legend([u'数量'],loc='upper right')
plt.grid(color="#95a5a6",linestyle='--',linewidth=1,axis='y',alpha=0.4)
plt.yticks(a,(u'小于50','50-100','100-150','150-200','200-250','250-300','300-350' ))
plt.show()
'''

#----------------------房源关注度分布情况数据分析-------------------------

house['guanzhu']



for i in range(len(house['guanzhu'])):
    house['guanzhu'][i]=float(filter(str.isalnum,house['guanzhu'][i].encode('utf-8')))

'''
bins=[0,100, 200, 300, 400, 500, 600, 700,800]
group_mianji=[u'小于100','100-200','200-300','300-400','400-500','500-600','600-700','700-800'];
house['guanzhu']=pd.cut(house['guanzhu'],bins,labels=group_mianji)

group_mianji=house.groupby('guanzhu')['guanzhu'].agg(len)
a=np.array([1,2,3,4,5,6,7,8])
plt.barh([1,2,3,4,5,6,7,8],group_mianji,color='#052B6C',
        alpha=0.8,align='center',edgecolor='white');
plt.xlim(0.300)
plt.ylabel(u"关注人数")
plt.xlabel(u'数量')
plt.title(u'房源关注度分布')
plt.legend([u'数量'],loc='upper right')
plt.grid(color="#95a5a6",linestyle='--',linewidth=1,axis='y',alpha=0.4)
plt.yticks(a,(u'小于100','100-200','200-300','300-400','400-500','500-600','600-700','700-800'))
plt.show()
'''




#----------------------对房源关注度、总价、面积进行聚类分析-------------------------

from sklearn.cluster import KMeans
house_type=np.array(house[['totalprice','mianji_num','guanzhu']])
#设置质心数为3
clf=KMeans(n_clusters=3)
#计算聚类结果
clf=clf.fit(house_type)
#显示质心坐标
clf.cluster_centers_
#在原时间表中标注所属类别
house['label']=clf.labels_












