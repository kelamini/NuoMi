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


CAP_NUM_0 = 0
CAP_NUM_1 = 2

# init server
server = Server(IP, PORT)

# val -> value
# bit -> quary bit
# return true or false
def myReadBit(val, bit):
    return (val >> bit)&1


class multiProSusRes():
    def __init__(self, hum_pid, fac_pid, ges_pid):
        self.hum = psutil.Process(hum_pid)
        # self.fac = psutil.Process(fac_pid)
        self.ges = psutil.Process(ges_pid)
    def susPro(self, str):
        if str == "hum":
            self.hum.suspend()
        # elif str == "fac":
        #     self.fac.suspend()
        elif str == "ges":
            self.ges.suspend()
    def resPro(self, str):
        if str == "hum":
            self.hum.resume()
        # elif str == "fac":
        #     self.fac.resume()
        elif str == "ges":
            self.ges.resume()

# video process class
class VideoProcess:

    # init
    def __init__(self, cap_num_0, cap_num_1):

        # init video
        self.cap0 = cv2.VideoCapture(cap_num_0)
        self.cap1 = cv2.VideoCapture(cap_num_1)

        # check 
        if self.cap0.isOpened():
            print("Cap0 init is ok")
        else: 
            print("Cap0 init is fail")
            sys.exit()
            
        if self.cap1.isOpened():
            print("Cap1 init is ok")
            
        else:
            print("Cap1 init is fail")
            sys.exit()
        
        # get pid
        self.pid = os.getpid()
        print("video process pid is ", self.pid)
  
    
    # process run
    def run(self,
            multi_process,
            img_cam0,
            img_hum,
            img_fac,
            img_ges,
            img_ser,
            server_data, 
            eHum,
            eFace,
            eGes):
        
        while(True):

            val = server_data.value

            # cam 0
            #   model  |   cam
            # 0000 0000| 0000 0001
            #
            # bit 0
            # bit 1
            # bit 2

            # bit 8  human
            # bit 9  face
            # bit 10 ges

            # get image 
           
            ret0, imgCam0 = self.cap0.read() 
            # ret0, img0 = self.cap1.read() 
            
            if ret0:
                # write image0
                img_cam0.write(imgCam0)


            cam0Sts = myReadBit(val, 0)

            huaSts = myReadBit(val, 8)
            facSts = myReadBit(val, 9)
            gesSts = myReadBit(val, 10)
        
            # # human
            # if huaSts:
            #     # open ehum event
            #     eHum.set()      

            # if facSts:
            #     # open eface event
            #     eFace.set() 

            # if gesSts:
            #     # open eges event
            #     eGes.set()

            # CAM0
            if cam0Sts:
               
                # both human and gesture
                if huaSts and gesSts:
                    multi_process.resPro("hum")
                    multi_process.resPro("ges")
                    eHum.set()   
                    # eGes.set()

                    while True:
                        # human deal end
                        if not eHum.is_set():
                            break
                    img_deal = img_hum.read()
                    img_cam0.write(img_deal)
                    eGes.set()


                    # while True:
                    #     # human deal end
                    #     if  not eGes.is_set():
                    #         break
                       
                    # imgDeal_h = img_hum.read()
                    # imgDeal_g = img_ges.read()

                    # gray_imgCam0 = cv2.cvtColor(imgCam0, cv2.COLOR_BGR2GRAY)
                    # gray_imgDeal_h = cv2.cvtColor(imgDeal_h, cv2.COLOR_BGR2GRAY)
                    # gray_imgDeal_g = cv2.cvtColor(imgDeal_g, cv2.COLOR_BGR2GRAY)

                    # diffImg_h = cv2.absdiff(imgDeal_h, imgCam0)

                
                    # imgAdd = cv2.bitwise_and(imgDeal_g, diffImg_h, dst=None, mask=None)
                    # imgAdd = cv2.addWeighted(imgDeal_g, 0.4,imgDeal_h, 0.6)
                    # imgAdd = cv2.cvtColor(imgAdd, cv2.COLOR_GRAY2BGR)
                    imgDeal_g = img_ges.read()
                    img_ser.write(imgDeal_g)
                    # print("both human ges")
                # only human 
                elif huaSts:
                    multi_process.resPro("hum")
                    multi_process.susPro("ges")
                    eHum.set()   
                   
                    imgDeal = img_hum.read()                  
                    img_ser.write(imgDeal)
                    # print("only human")
                # only gesture
                elif gesSts: 
                    multi_process.susPro("hum")
                    multi_process.resPro("ges")
                    eGes.set() 

                    imgDeal = img_ges.read()
                    img_ser.write(imgDeal)
                    # print("only gesture")
                #none
                else:
                    multi_process.susPro("hum")
                    multi_process.susPro("ges")
                    img_ser.write(imgCam0)   
                    

            # if val == 1: 
                
            #     eHum.clear()
            #     eFace.clear()
            #     eGes.clear()
                
            #     # send image data to process
            #     ret, img = self.cap0.read()

            #     # image is ok
            #     if ret:
            #         img_ser.write(img)              

            # elif val == 2:

            #     eHum.set()
            #     eFace.clear()
            #     eGes.clear()

            #     # send image data to process
            #     ret, img = self.cap0.read()
            #     if ret:
            #         img_cam0.write(img)

            #     img_hum_deal = img_hum.read()

            #     # write image to server rtsp
            #     img_ser.write(img_hum_deal)
            # elif val == 3 :

            #     eHum.clear()
            #     eFace.set()
            #     eGes.clear()

            #     # send image data to process
            #     ret, img = self.facCap.read()
            #     if ret:
            #         img_lock.acquire()
            #         # img = cv2.resize(img, (640, 480))
            #         img = img.flatten(order='C')
            #         temp = np.frombuffer(buf, dtype=np.uint8)
            #         temp[:] = img
            #         img_lock.release()

            # elif val == 4:

            #     eHum.clear()
            #     eFace.clear()
            #     eGes.set()

            #     # send image data to process
            #     ret, img = self.facCap.read()
            #     if ret:
            #         img_lock.acquire()
            #         # img = cv2.resize(img, (640, 480))
            #         img = img.flatten(order='C')
            #         temp = np.frombuffer(buf, dtype=np.uint8)
            #         temp[:] = img
            #         img_lock.release()
                

            # time.sleep(0.01)


def processFuc(num):
    while True:
        print("this is Process ", num)
        time.sleep(0.01)


# 共享内存 类
class ArrayLockClass:
    def __init__(self):
        self.lock = multiprocessing.Lock()
        self.array =  multiprocessing.Array(ctypes.c_uint8, 640*480*3, lock= False)
    def write(self, img):
        self.lock.acquire()
        img = cv2.resize(img, (640, 480))
        img = img.flatten(order='C')
        temp = np.frombuffer(self.array, dtype=np.uint8)
        temp[:] = img
        self.lock.release()
    def read(self):
        self.lock.acquire()
        img = np.frombuffer(self.array, dtype=np.uint8).reshape(480, 640, 3)
        self.lock.release()
        return img

if __name__ == '__main__':

    multiprocessing.set_start_method("fork")



    # 共享内存
    imgCam0 = ArrayLockClass()
    imgHum = ArrayLockClass()
    imgFac = ArrayLockClass()
    imgGes = ArrayLockClass()
    imgSer = ArrayLockClass()

    # # 进程锁
    # imgLock_rawCam0 = multiprocessing.Lock()
    # imgLock_ser = multiprocessing.Lock()
    # imgLock_hum = multiprocessing.Lock()
    # imgLock_fac = multiprocessing.Lock()

    # 进程事件
    eHum = multiprocessing.Event()
    eFace = multiprocessing.Event()
    eGes = multiprocessing.Event()
    serEvent = multiprocessing.Event()


    
    eHum.clear()
    eFace.clear()
    serEvent.clear()

    # eHum.set()
    # eHum.wait()
    # print(eHum.is_set())
    # sys.exit()
    # # 共享内存
    # imgBuf_raw = multiprocessing.Array(ctypes.c_uint8, 640*480*3, lock= False)
    # imgBuf_ser = multiprocessing.Array(ctypes.c_uint8, 640*480*3, lock= False)
    # imgBuf_hum = multiprocessing.Array(ctypes.c_uint8, 640*480*3, lock= False)
    # imgBuf_fac = multiprocessing.Array(ctypes.c_uint8, 640*480*3, lock= False)
    
    serData = multiprocessing.Manager().Value(ctypes.c_int, 1)


   

    humProces = multiprocessing.Process(target=human_track_thread, args = (imgCam0, imgHum, eHum,))
    # facProces = multiprocessing.Process(target=face_detec_thread, args = (imgLock_raw, imgBuf, imgDLock, imgDBuf,eFace,))
    gesProces = multiprocessing.Process(target=gesThread, args = (imgCam0, imgGes, eGes,))

   
    humProces.start()
    gesProces.start()
    # facProces.start()
    


    multiPro = multiProSusRes(humProces.pid, 
                   0,
                   gesProces.pid)

     #------------------------------  Process  ----------------------------#
    video = VideoProcess(CAP_NUM_0, CAP_NUM_1)
    

    videoProces = multiprocessing.Process(target=video.run, args = (multiPro,
                                                                    imgCam0, 
                                                                    imgHum, 
                                                                    imgFac,
                                                                    imgGes,
                                                                    imgSer, 
                                                                    serData, 
                                                                    eHum, 
                                                                    eFace, 
                                                                    eGes))
    videoProces.start()

    time.sleep(0.1)



    pulThread =  multiprocessing.Process(target=pulish_thread, args= (IP, imgSer, serEvent))
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
        value = serData.value

        cam0Sts = myReadBit(value, 0)

        huaSts = myReadBit(value, 8)
        facSts = myReadBit(value, 9)
        gesSts = myReadBit(value, 10)

        print("cam0 sts", cam0Sts)
        print("human sts", huaSts)
        print("face sts", facSts)
        print("ges sts", gesSts)

        # data = 0xff
        # print(bin(data))
        # a = ~(1 << 3)
        # print(bin(a))
        # # print(bin(~a))
        # data_deal = data & a
       
        # print(bin(data_deal))
       
