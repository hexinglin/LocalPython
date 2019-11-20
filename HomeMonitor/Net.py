# 不需要建立连接
import socket
import threading
import json
import cv2
import numpy as np
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]


class Net(threading.Thread):
    transmitManage = None
    def __init__(self,transmitManage):
        super().__init__()
        self.transmitManage = transmitManage
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(("0.0.0.0", 9000))  # 绑定服务器的ip和端口
        self.start()



    def dealData(self,dataJson:'dict'):
        if dataJson.get('action') == None:
            return
        print(dataJson)



    def sendPic(self,ip,port,pic):
        img_encode = cv2.imencode('.jpg', pic, encode_param)[1]
        data = np.array(img_encode)
        stringData = data.tobytes()
        # self.ss.send(stringData)
        # self.s.sendto(stringData,('118.199.210.122',6000))
        # self.s.sendto(stringData, ('192.168.3.2', 8000))

    def sendPic2(self,pic):
        img_encode = cv2.imencode('.jpg', pic, encode_param)[1]
        data = np.array(img_encode)
        stringData = data.tobytes()
        self.s.sendto(stringData, ('tokgo.cn', 20003))

    def sendData(self,ip,port,data):
        str = json.dumps(data)
        bs = bytes(str, encoding="gbk")
        self.s.sendto(bs,(ip,port))
        pass

    def run(self):
        while True:
            try:
                stringData = self.s.recvfrom(65500)
                print(stringData)
                recvData=json.loads(stringData[0])
                self.dealData(recvData)
            except :
                continue







