# 不需要建立连接
import socket
import threading
import json
from HomeCamera.Visitor import Visitor


class Net(threading.Thread):
    transmitManage = None
    def __init__(self,transmitManage):
        super().__init__()
        self.transmitManage = transmitManage
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(("0.0.0.0", 8000))  # 绑定服务器的ip和端口
        self.start()



    def dealData(self,dataJson:'dict'):
        if dataJson.get('action') == None:
            return
        if "feedback" == dataJson['action']:
            try:
                self.transmitManage.addCameraVisitor(Visitor(jsonData=dataJson))
            except:
                pass



    def sendPic(self,ip,port,pic):
        # if "feedback" == dataJson
        pass

    def sendData(self,ip,port,data):
        str = json.dumps(data)
        bs = bytes(str, encoding="utf8")
        self.s.sendto(bs,(ip,port))
        pass

    def run(self):
        while True:
            try:
                stringData = self.s.recv(65500)
                recvData=json.loads(stringData)
                self.dealData(recvData)
            except :
                continue







