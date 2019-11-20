
from Net import Net
import threading

class TransmitManage(threading.Thread):

    clientList={}
    net = None
    def __init__(self):
        super().__init__()
        self.net = Net(self)

    def addCamera(self,NO):
        self.clientList[NO]=[]
        # infor = {"mod":"homeCamera","action":"regiter","identity":"camera","NO":NO}
        # self.net.sendData('hecao.pw',20001,infor)

    def removeCamera(self,NO):
        # self.clientList.
        pass

    def sendPic(self,pic,NO):
        self.net.sendPic2(pic)

    def run(self):

        pass









