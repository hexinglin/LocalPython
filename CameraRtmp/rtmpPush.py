#coding=utf8
import cv2
import subprocess as sp
import time
import numpy as np
from datetime import datetime

def get_cap(cap):
    try:
        cap.release()
    except:
        pass
    while True :
        for i in range(5):
            try:
                cap = cv2.VideoCapture(i)
                ret, frame = cap.read()
                if ret:
                    print(datetime.now(), "摄像头打开成功，id",i)
                    return cap
            except:
                pass
            time.sleep(1)
        print(datetime.now(),"尝试打开摄像头失败")
        time.sleep(5)
def init_info(rtmpUrl,cap):
    cap = get_cap(cap = cap)
    # Get video information
    fps = 10
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # ffmpeg command
    command = ['ffmpeg',
                    '-y',
                    '-f', 'rawvideo',
                    '-vcodec', 'rawvideo',
                    '-pix_fmt', 'bgr24',
                    '-s', "{}x{}".format(width, height),
                    '-r', str(fps),
                    '-i', '-',
                    '-c:v', 'libx264',
                    '-pix_fmt', 'yuv420p',
                    '-preset', 'ultrafast',
                    '-f', 'flv',
                    rtmpUrl]

    p = sp.Popen(command, stdin=sp.PIPE)

    return cap,p,fps
def add_time_flag(frame):
    time_str = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    h = frame.shape[0]
    w = frame.shape[1]

    #当背景色为黑色时，时间显示为白色
    color = (255, 255, 255)
    if np.mean(frame[int(h*0.97):h, int(w*0.01):int(w*0.2)]) > 128:
        color = (0, 0, 0)

    cv2.putText(frame, time_str, (int(w*0.01), int(h*0.97)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    return frame

if __name__ == '__main__':
    rtmpUrl = "rtmp://121.36.74.137:1935/stream/test"
    # rtmpUrl = "rtmp://192.168.0.135:1935/stream/test"
    cap,p,fps = init_info(rtmpUrl=rtmpUrl,cap= None)
    while True:
        try:
            #为了网络考虑不要那么多
            time.sleep(0.1)
            ret, frame = cap.read()
            if ret:
                try:
                    add_time_flag(frame)
                    p.stdin.write(frame.tostring())
                except Exception as e:
                    print(datetime.now(),e)
            else:
                raise Exception(datetime.now(),'read false')
        except Exception as e:
            cap, p, fps = init_info(rtmpUrl=rtmpUrl, cap=cap)
            print(datetime.now(),e)



