import mmap
import cv2
import os
from datetime import datetime


class CameraSave():
    def __init__(self,no:int=0):
        savePath = '/etc/home/camera/{}/'.format(no)

        # savePath = '/Users/hxl/my/LocalPython/{}/'.format(no)
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



if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    save= CameraSave()
    while True:
        ret, frame = cap.read()
        save.save(frame)






