import socket
import json
import numpy as np


#创建socket对象
#SOCK_DGRAM    udp模式
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(("192.168.1.102",6000))  #绑定服务器的ip和端口
str = json.dumps({"mod": "homeCamera", "action": "regiter", "identity": "viviter", "NO": 0 })
bs = bytes(str, encoding="gbk")
print(s.sendto(bs, ('hecao.pw', 20001)))
stringData=s.recvfrom(65500)  #一次接收1024字节
recvData = json.loads(stringData[0])
print(recvData)

str = json.dumps({"mod": "test", "action": "feedback", "identity": "viviter", "NO": 0})
bs = bytes(str, encoding="gbk")
print(s.sendto(bs, (recvData['data']['ip'], recvData['data']['port'])))

str = json.dumps({"mod": "homeCamera", "action": "feedback", "identity": "viviter", "NO": 0 })
bs = bytes(str, encoding="gbk")
s.sendto(bs, ('hecao.pw', 20001))
import cv2
while True:
    # print('wait')
    stringData=s.recvfrom(65500)  #一次接收1024字节
    # print(stringData)
    data = np.frombuffer(stringData[0],dtype='uint8')

    decimg = cv2.imdecode(data,1)
    cv2.imshow('sssss',decimg)
    cv2.waitKey(1)
