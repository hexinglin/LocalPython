
# 打开摄像头并灰度化显示
import cv2
import time
import numpy as np
# 不需要建立连接
import socket
from TransmitManage import TransmitManage
from Camera import Camera

transmitManage = TransmitManage()
transmitManage.addCamera(0)
capture = Camera(0)

while(True):
    try:
        # 获取一帧
        ret, frame = capture.read()
        # frame = cv2.resize(frame, (int(frame.shape[1]/2), int(frame.shape[0]/2)), interpolation=cv2.INTER_CUBIC)
        transmitManage.sendPic(frame,0)
        #暂停0.5s
        time.sleep(0.5)
    except :
        print(time.time(),'read error')
        time.sleep(1)
        capture = cv2.VideoCapture(0)




