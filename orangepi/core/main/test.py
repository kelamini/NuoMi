import threading 
import numpy as np
import time, os
import cv2
import multiprocessing
import psutil
import ctypes,sys

CAP_NUM_0 = 0
CAP_NUM_1 = 2
CAP_NUM_2 = 0


# val -> value
# bit -> quary bit
# return true or false
def myReadBit(val, bit):
    return (val >> bit)&1


class multiProSusRes():
    def __init__(self, hum_pid, fac_pid, ges_pid, fir_pid):
        self.hum = psutil.Process(hum_pid)
        self.fac = psutil.Process(fac_pid)
        self.ges = psutil.Process(ges_pid)
        self.fir = psutil.Process(fir_pid)
    def susPro(self, str):
        if str == "hum":
            self.hum.suspend()
        elif str == "ges":
            self.ges.suspend()
        elif str == "fac":
            self.fac.suspend()
        elif str == "fir":
            self.fir.suspend()

    def resPro(self, str):
        if str == "hum":
            self.hum.resume()
        elif str == "ges":
            self.ges.resume()
        elif str == "fac":
            self.fac.resume()
        elif str == "fir":
            self.fir.resume()

# video process class
class VideoProcess:

    # init
    def __init__(self, cap_num_0, cap_num_1, cap_num_2, serve_buf, serve_val):

        # init video
        self.cap0 = cv2.VideoCapture(cap_num_0)
        self.cap1 = cv2.VideoCapture(cap_num_1)
        self.cap2 = cv2.VideoCapture(cap_num_2)
        self.serBuf = serve_buf
        self.serVal = serve_val
       
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

        if self.cap2.isOpened():
            print("Cap2 init is ok")
            
        else:
            print("Cap2 init is fail")
            sys.exit()
        
    # process run
    def runCam0(self,
                multi_process,
                img_cam0,
                img_hum,
                img_ges,
                eHum,
                eGes):
        
        while(True):

            ret0, imgCam0 = self.cap0.read() 
            # ret0, img0 = self.cap1.read() 
            
            if ret0:
                # write image0
                img_cam0.write(imgCam0)
            
            camSts = myReadBit(self.serVal.value, 0)
            huaSts = myReadBit(self.serVal.value, 8)
            gesSts = myReadBit(self.serVal.value, 10)
            # print("val:", bin(self.serVal))
            # print("camSts", camSts)
            # print("huaSts", huaSts)
            # print("gesSts", gesSts)

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

                imgDeal_g = img_ges.read()

                self.data2server(camSts, imgDeal_g)
                
            # only human 
            elif huaSts:
                multi_process.resPro("hum")
                multi_process.susPro("ges")
                eHum.set()   
                
                imgDeal = img_hum.read()                  
                self.data2server(camSts, imgDeal)
                # print("only human")
            # only gesture
            elif gesSts: 
                multi_process.susPro("hum")
                multi_process.resPro("ges")
                eGes.set() 

                imgDeal = img_ges.read()
                self.data2server(camSts, imgDeal)
                # print("only gesture")
            #none
            else:
                multi_process.susPro("hum")
                multi_process.susPro("ges")
                self.data2server(camSts, imgCam0) 
                   
    # cam1 process
    def runCam1(self,
            multi_process,
            img_cam1,
            img_fac,
            eFac,
            ):
        while(True):
                               
            ret, imgCam = self.cap1.read() 
            
            if ret:
                # write image0
                img_cam1.write(imgCam)


            camSts = myReadBit(self.serVal.value, 1)
            facSts = myReadBit(self.serVal.value, 9)
         
            # both human and gesture
            if facSts:
                
                multi_process.resPro("fac")
                eFac.set()   
                img_deal = img_fac.read()

                self.data2server(camSts, img_deal)          
            else:
                
                multi_process.susPro("fac")
                self.data2server(camSts, imgCam)
    # cam2 process
    def runCam2(self,
            multi_process,
            img_cam2,
            img_fir,
            eFir,
            ):
        while(True):
                               
            ret, imgCam = self.cap2.read() 
            
            if ret:
                # write image0
                img_cam2.write(imgCam)


            camSts = myReadBit(self.serVal.value, 2)
            firSts = myReadBit(self.serVal.value, 11)
            # print("camsts", camSts)
            # both human and gesture
            if firSts:
                
                multi_process.resPro("fir")
                eFir.set()   
                img_deal = img_fir.read()

                self.data2server(camSts, img_deal)          
            else:
                # print("cam2 is ok")
                # print("camsts", )
                multi_process.susPro("fir")
                self.data2server(camSts, imgCam)
                                    
    def data2server(self, camSts, img):
        if camSts:
            self.serBuf.write(img)


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


serVal = multiprocessing.Manager().Value(ctypes.c_int, 0x01)
imgSer = ArrayLockClass()

#------------------------------  Process  ----------------------------#
video = VideoProcess(CAP_NUM_0, CAP_NUM_1, CAP_NUM_2, imgSer, serVal)


# cam0Proces = multiprocessing.Process(target=video.runCam0, args = (multiPro,
#                                                                     imgCam0, 
#                                                                     imgHum, 
#                                                                     imgGes,
#                                                                     eHum, 
#                                                                     eGes))
# cam0Proces.start()

# cam1Proces = multiprocessing.Process(target=video.runCam1, args = ( multiPro,
#                                                                     imgCam1, 
#                                                                     imgFac,  
#                                                                     eFace, 
#                                                                     ))
# # cam1Proces.start()

# cam2Proces = multiprocessing.Process(target=video.runCam2, args = ( multiPro,
#                                                                     imgCam2, 
#                                                                     imgFir,  
#                                                                     eFir, 
#                                                                     ))
# cam2Proces.start()

while True:
        time.sleep(1)
        print("this is main process")       