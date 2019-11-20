
from HomeCamera.Net import Net
import threading
from HomeCamera.Visitor import Visitor

class TransmitManage(threading.Thread):

    clientList={}
    net = None
    def __init__(self):
        super().__init__()
        self.net = Net(self)

    def addCamera(self,NO):
        self.clientList[NO]=[]
        infor = {"mod":"homeCamera","action":"regiter","identity":"camera","NO":NO}
        self.net.sendData('hecao.pw',20001,infor)

    def addCameraVisitor(self,visitor:'Visitor'):
        clients:'list' = self.clientList[visitor.NO]
        clients.append(visitor)

    def removeCamera(self,NO):
        # self.clientList.
        pass

    def sendPic(self,pic,NO):
        self.net.sendPic2(pic)

        if self.clientList.get(NO) == None:
            return
        clients = self.clientList[NO]
        for visitor in clients:
            if visitor.COUNT >0:
                self.net.sendPic(visitor.IP,visitor.PORT,pic)
                visitor.COUNT = visitor.COUNT - 1
                print(visitor.IP,visitor.PORT,visitor.COUNT)
            else:
                self.clientList[NO].remove(visitor)

    def run(self):

        pass









