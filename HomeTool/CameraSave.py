#coding=utf-8
import json
import mmap
import os
import cv2
import numpy as np
import socket
import threading
import time
from datetime import datetime

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]


class Net(threading.Thread):
    client_list = []


    def __init__(self):
        super().__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(("0.0.0.0", 9000))  # 绑定服务器的ip和端口
        self.start()


    def sendPic(self,pic):
        img_encode = cv2.imencode('.jpg', pic, encode_param)[1]
        data = np.array(img_encode)
        imgData = data.tobytes()
        for client in self.client_list:
            try:
                self.s.sendto(imgData, client['adrr'])
                client['count'] = client['count'] - 1
                print(client['count'])
                if client['count'] < 0:
                    self.client_list.remove(client)
            except:
                pass


    def sendData(self,ip,port,data):
        str = json.dumps(data)
        bs = bytes(str, encoding="gbk")
        self.s.sendto(bs,(ip,port))
        pass


    def regClient(self,adrr):
        for client in self.client_list:
            if client['adrr'] == adrr:
                client['count'] = 10000
                return
        self.client_list.append({'adrr':adrr,'count':10000})

    def run(self):
        while True:
            try:
                stringData,adrr = self.s.recvfrom(65500)
                self.regClient(adrr)
            except :
                continue



class PicSave():
    def __init__(self,no:int=0):
        savePath = '/etc/home/camera/{}/'.format(no)
        #检查信息存储文件
        if not os.path.exists(savePath):
            os.makedirs(savePath)

        #图片
        try:
            picPath =savePath+"pic.dat"
            self.f = open(picPath,"r+")
        except:
            with open(picPath, "w") as f:
                f.truncate(100)
            self.f = open(picPath, "r+")
        #保存图片信息
        try:
            picPath =savePath+"infor.txt"
            self.f_infor = open(picPath,"r+")
        except:
            with open(picPath, "w") as f:
                f.truncate(100)
            self.f_infor = open(picPath, "r+")


    def save(self,frame):
        data = frame.tobytes()
        dt = datetime.now()
        infor_str = dt.strftime('{}\n{}\n{}\nsave time:%y-%m-%d_%H:%M:%S'.format(frame.shape[0],frame.shape[1],frame.shape[2]))
        infor_byte=bytes(infor_str,encoding='utf8')
        self.f_infor.truncate(len(infor_byte))
        VDATA = mmap.mmap(self.f_infor.fileno(),0,access=mmap.ACCESS_WRITE)
        VDATA.write(infor_byte)
        VDATA.flush()

        self.f.truncate(len(data))
        VDATA = mmap.mmap(self.f.fileno(),0,access=mmap.ACCESS_WRITE)
        VDATA.write(data)
        VDATA.flush()



class CameraSave():

    def __init__(self,no:int=0):
        self.cap = cv2.VideoCapture(no)

    def read(self):
        ret, frame = self.cap.read()
        if ret:
            self.add_time_flag(frame)
        return ret,frame

    def add_time_flag(self,frame):
        time_str = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        h = frame.shape[0]
        w = frame.shape[1]

        #当背景色为黑色时，时间显示为白色
        color = (255, 255, 255)
        if np.mean(frame[int(h*0.97):h, int(w*0.01):int(w*0.2)]) > 128:
            color = (0, 0, 0)

        cv2.putText(frame, time_str, (int(w*0.01), int(h*0.97)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        return frame

    def re_load_camera(self):
        try:
            self.cap.release()
        except:
            pass
        for i in range(5):
            time.sleep(1)
            try:
                cap = cv2.VideoCapture(i)
                ret, frame = cap.read()
                if ret:
                    self.cap=cap
                    break
            except:
                pass

if __name__ == '__main__':
    CS = CameraSave(0)
    save= PicSave()
    net = Net()
    while True:
        time.sleep(0.01)
        try:
            ret,frame = CS.read()
            if ret:
                try:
                    save.save(frame)
                    net.sendPic(frame)
                    time.sleep(0.01)
                except Exception as e:
                    print(e)
            else:
                raise Exception('read false')
        except Exception as e:
            CS.re_load_camera()
            print(e)













