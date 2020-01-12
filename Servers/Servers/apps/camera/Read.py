import mmap
import os
import numpy as np
import cv2


class Camera():
    def __init__(self,no:int=0):
        # savePath = '/etc/home/camera/{}/'.format(no)

        savePath = '/Users/hxl/my/LocalPython/{}/'.format(no)
        #检查信息存储文件
        if not os.path.exists(savePath):
            os.makedirs(savePath)
        self.f = open(savePath+"pic.dat", "r+")
        self.f_infor = open(savePath+"infor.txt", "r+")

    def read(self):
        try:
            mm = mmap.mmap(self.f.fileno(), 0, access=mmap.ACCESS_COPY)
            image_array = np.frombuffer(mm.read(), dtype=np.uint8)
            mm = mmap.mmap(self.f_infor.fileno(), 0, access=mmap.ACCESS_COPY)
            frame = image_array.reshape(int(mm.readline()), int(mm.readline()), int(mm.readline()))
            return True,frame
        except:
            return False,None


if __name__ == '__main__':
    cap= Camera()
    while True:
        ret, frame = cap.read()
        cv2.imshow('ss',frame)
        cv2.waitKey(20)



