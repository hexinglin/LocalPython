
# 打开摄像头并灰度化显示
import cv2
import time
import numpy as np
# 不需要建立连接
import socket
from HomeCamera.TransmitManage import TransmitManage

transmitManage = TransmitManage()
transmitManage.addCamera(0)


capture = cv2.VideoCapture(0)

import time
while(True):
    # 获取一帧

    ret, frame = capture.read()
    # frame = cv2.resize(frame, (int(frame.shape[1]/2), int(frame.shape[0]/2)), interpolation=cv2.INTER_CUBIC)
    # 将这帧转换为灰度图
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 首先对图片进行编码，因为socket不支持直接发送图片
    # '.jpg'表示把当前图片frame按照jpg格式编码
    # result, img_encode = cv2.imencode('.jpg', frame)

    transmitManage.sendPic(frame,0)
    cv2.imshow('frame', frame)
    # cv2.waitKey(0)
    if cv2.waitKey(500) == ord('q'):
        break




