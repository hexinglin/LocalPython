
# 打开摄像头并灰度化显示
import cv2
import numpy as np
# 不需要建立连接
import socket
from HomeCamera.TransmitManage import TransmitManage

transmitManage = TransmitManage()

transmitManage.addCamera(0)
transmitManage.sendPic(None,0)

#：请：：q
# # 创建socket对象
# # SOCK_DGRAM    udp模式
#
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# capture = cv2.VideoCapture(0)
# encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
#
# while(True):
#     # 获取一帧
#
#     ret, frame = capture.read()
#     # frame = cv2.resize(frame, (int(frame.shape[1]/2), int(frame.shape[0]/2)), interpolation=cv2.INTER_CUBIC)
#     # 将这帧转换为灰度图
#     # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#     # 首先对图片进行编码，因为socket不支持直接发送图片
#     # '.jpg'表示把当前图片frame按照jpg格式编码
#     # result, img_encode = cv2.imencode('.jpg', frame)
#     img_encode = cv2.imencode('.jpg', frame, encode_param)[1]
#     data = np.array(img_encode)
#     stringData = data.tostring()
#     print(len(stringData))
#
#     # 发送数据 字节
#     s.sendto(stringData, ("127.0.0.1", 8000))
#     break
#     cv2.imshow('frame', frame)
#     cv2.waitKey(0)
#     if cv2.waitKey(1) == ord('q'):
#         break
#
#


