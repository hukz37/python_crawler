#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/11 上午10:26
# @Author  : hukezhu
# @Site    : 
# @File    : 妹子图合成视频.py
# @Software: PyCharm

# import os
# #import cv2
# import numpy as np
#
# import cv2.cv as cv
#
# #help(cv2)
# path = '/Users/hukezhu/Desktop/meizi/'
# filelist = os.listdir(path)
# total_num = len(filelist)
#
# video=cv.CreateVideoWriter("/Users/hukezhu/Desktop/meizi.avi",cv.CV_FOURCC("M", "J", "P", "G ") , 2, (236,354))#cv2.cv.VideoWriter_fourcc('M', 'J', 'P', 'G')
# for item in filelist:
#     if item.endswith('.jpg'):
#         item='/home/pi/Desktop/meizi1/'+item
#         img1 = cv.imread(item)
#         print item
#
#         video.write(img1)
#         #cv2.imshow("Image", img1)
#         key=cv.waitKey(100)
#
# video.release()
# cv.destroyAllWindows()






import numpy as np
import cv2

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame,0)

        # write the flipped frame
        out.write(frame)

        #cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()