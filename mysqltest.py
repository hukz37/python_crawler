#!/usr/bin/env python
# -*- coding: utf-8 -*-


import MySQLdb

db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="123456",db="test")

cursor = db.cursor()

cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

sql = """CREATE TABLE EMPLOYEE (
         content1  TEXT(20000) NOT NULL,
         creationTime1  CHAR(200),
         productColor1  CHAR(200),
         productSize1   CHAR(200),
         userClientShow1   CHAR(100),
         userLevelName1   CHAR(100))"""

cursor.execute(sql)

sql1 = """INSERT INTO EMPLOYEE(content1,creationTime1, productCoslor1, productSize1, userClientShow1,userLevelName1); VALUES ('1','2', '2', '3','3','3') """
try:
    cursor.execute(sql1)
    db.commit()
    print "保存成功"
except:
    db.rollback()
    print "保存失败"


db.close()