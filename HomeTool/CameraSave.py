import mmap
import cv2
import os
import numpy as np
from datetime import datetime



class PicSave():
    def __init__(self,no:int=0):
        # savePath = '/etc/home/camera/{}/'.format(no)

        savePath = '/Users/hxl/my/LocalPython/{}/'.format(no)
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
        if np.mean(frame[int(h*0.97):h, int(w*0.05):w]) > 128:
            color = (0, 0, 0)

        cv2.putText(frame, time_str, (int(w*0.05), int(h*0.97)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        return frame


if __name__ == '__main__':
    CS = CameraSave()
    save= PicSave()
    while True:
        ret,frame = CS.read()
        if ret:
            save.save(frame)












