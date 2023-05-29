import numpy as np
import time, os
import cv2
import multiprocessing
import psutil
import ctypes,sys


import threading 
from human_track import human_track_thread
from face_detec import face_detec_thread
from sockets import Server
from publish_rtsp import FfmpegPublishRtsp
from sockets import server_thread
from publish_rtsp import pulish_thread
from gesture import gesThread

#from multiprocessing import shared_memory
# from video import videoProcess
#facCap = cv2.VideoCapture(0)

swich_key = 0

IP = "192.168.4.15"
PORT = 8000


HUM_CAP_NUM = 0
FAC_CAP_NUM = 2

# init server
server = Server(IP, PORT)



# video process class
class VideoProcess:

    # init
    def __init__(self, hua_cap_num, fac_cap_num):

        # init video
        self.humCap = cv2.VideoCapture(hua_cap_num)
        self.facCap = cv2.VideoCapture(fac_cap_num)

        # check 
        if self.humCap.isOpened():
            print("huaCap init is ok")
        else: 
            print("huaCap init is fail")
            sys.exit()
            
        if self.facCap.isOpened():
            print("facCap init is ok")
            
        else:
            print("facCap init is fail")
            sys.exit()
        
        # get pid
        self.pid = os.getpid()
        print("video process pid is ", self.pid)
  
    
    # process run
    def run(self,
            img_lock,
            buf, 
            img_deal_lock, 
            dbuf, 
            server_data, 
            eHum,
            eFace,
            eGes):
        
        while(True):

            val = server_data.value
            if val == 1: 

                # eHum.clear()
                # eFace.clear()
                # eGes.clear()

                # # send image data to process
                # ret, img = self.humCap.read()

                # # image is ok
                # if ret:
                #     img_deal_lock.acquire()
                #     # img = cv2.resize(img, (640, 480))
                #     img = img.flatten(order='C')
                #     temp = np.frombuffer(dbuf, dtype=np.uint8)
                #     temp[:] = img
                #     img_deal_lock.release()

            
                # send image data to process
                ret, img = self.facCap.read()
                if ret:
                    img_lock.acquire()
                    # img = cv2.resize(img, (640, 480))
                    img = img.flatten(order='C')
                    temp = np.frombuffer(buf, dtype=np.uint8)
                    temp[:] = img
                    img_lock.release()

                eHum.clear()
                eFace.clear()
                eGes.set()

            elif val == 2:

                eHum.set()
                eFace.clear()
                eGes.clear()

                # send image data to process
                ret, img = self.humCap.read()
                if ret:
                    img_lock.acquire()
                    # img = cv2.resize(img, (640, 480))
                    img = img.flatten(order='C')
                    temp = np.frombuffer(buf, dtype=np.uint8)
                    temp[:] = img
                    img_lock.release()
            elif val == 3 :

                eHum.clear()
                eFace.set()
                eGes.clear()

                # send image data to process
                ret, img = self.facCap.read()
                if ret:
                    img_lock.acquire()
                    # img = cv2.resize(img, (640, 480))
                    img = img.flatten(order='C')
                    temp = np.frombuffer(buf, dtype=np.uint8)
                    temp[:] = img
                    img_lock.release()

            elif val == 4:

                eHum.clear()
                eFace.clear()
                eGes.set()

                # send image data to process
                ret, img = self.facCap.read()
                if ret:
                    img_lock.acquire()
                    # img = cv2.resize(img, (640, 480))
                    img = img.flatten(order='C')
                    temp = np.frombuffer(buf, dtype=np.uint8)
                    temp[:] = img
                    img_lock.release()
                

            time.sleep(0.01)


def processFuc(num):
    while True:
        print("this is Process ", num)
        time.sleep(0.01)

if __name__ == '__main__':

    multiprocessing.set_start_method("fork")


    # 进程锁
    imgLock = multiprocessing.Lock()
    imgDLock = multiprocessing.Lock()

    # 进程事件
    eHum = multiprocessing.Event()
    eFace = multiprocessing.Event()
    eGes = multiprocessing.Event()
    serEvent = multiprocessing.Event()

    eHum.clear()
    eFace.clear()
    serEvent.clear()

    # 共享内存
    imgBuf = multiprocessing.Array(ctypes.c_uint8, 640*480*3, lock= False)
    imgDBuf = multiprocessing.Array(ctypes.c_uint8, 640*480*3, lock= False)
    serData = multiprocessing.Manager().Value(ctypes.c_int, 1)


    #------------------------------  Process  ----------------------------#
    video = VideoProcess(HUM_CAP_NUM, FAC_CAP_NUM)
    

    videoProces = multiprocessing.Process(target=video.run, args = (imgLock, imgBuf, imgDLock, imgDBuf, serData, eHum, eFace, eGes))
    videoProces.start()

    time.sleep(0.1)

    humProces = multiprocessing.Process(target=human_track_thread, args = (imgLock, imgBuf, imgDLock, imgDBuf, eHum,))
    humProces.start()

    facProces = multiprocessing.Process(target=face_detec_thread, args = (imgLock, imgBuf, imgDLock, imgDBuf,eFace,))
    facProces.start()

    gesProces = multiprocessing.Process(target=gesThread, args = (imgLock, imgBuf, imgDLock, imgDBuf,eGes,))
    gesProces.start()


    pulThread =  multiprocessing.Process(target=pulish_thread, args= (IP, imgDLock, imgDBuf, serEvent))
    pulThread.start()
    

    serThread = multiprocessing.Process(target=server_thread, args= (server, serEvent, serData))
    serThread.start()

    # process1 = multiprocessing.Process(target=processFuc, args= (1,))
    # process1.start()

    # process2 = multiprocessing.Process(target=processFuc, args= (2,))
    # process2.start()

    # process3 = multiprocessing.Process(target=processFuc, args= (3,))
    # process3.start()

    # process4 = multiprocessing.Process(target=processFuc, args= (4,))
    # process4.start()

    # process5 = multiprocessing.Process(target=processFuc, args= (5,))
    # process5.start()

    # process6 = multiprocessing.Process(target=processFuc, args= (6,))
    # process6.start()

    # process7 = multiprocessing.Process(target=processFuc, args= (7,))
    # process7.start()

    # process8 = multiprocessing.Process(target=processFuc, args= (8,))
    # process8.start()

   

    # print("videoProce", videoProces.is_alive())
    # print("humProce", humProces.is_alive())

    while True:
        time.sleep(1)
        print("this is main process")
        print("server value", serData.value)

