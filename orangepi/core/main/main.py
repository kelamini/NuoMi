from threading import Thread, current_thread
import numpy as np
import time, os
import cv2
import multiprocessing
import psutil
from human_track import human_track_thread
from face_detec import face_detec_thread

from sockets import Server

import ctypes

#from multiprocessing import shared_memory
# from video import videoProcess
#facCap = cv2.VideoCapture(0)

swich_key = 0

IP = "192.168.4.15"
PORT = 8000


HUM_CAP_NUM = 0
FAC_CAP_NUM = 2

server = Server()

# video process
# def videoProcess(lock, shareMemName, shape, dtype, event):
def videoProcess(img_lock, buf, img_deal_lock, dbuf):
    # video init 
    huaCap = cv2.VideoCapture(HUM_CAP_NUM)
    facCap = cv2.VideoCapture(FAC_CAP_NUM)

    if huaCap.isOpened():
        print("huaCap init is ok")
    else:
        print("huaCap init is fail")

    if facCap.isOpened():
        print("facCap init is ok")
    else:
        print("facCap init is fail")

    # img = cv2.imread("./image/bus.jpg")
    pid = os.getpid()
    print("video process pid is ",pid)
    
    # img = [[[1, 2, 3], [0, 2, 0], [2, 2, 0], [3, 2,3,4], [3, 2,3,4]], [1,2]]
    
    while True:
       
        # get lock
        img_lock.acquire()
        # buf = img

        # send image data to process
        ret, img = facCap.read()

        # print(img)
        if ret:
            # qImg.put(img)
            img = img.flatten(order='C')
            temp = np.frombuffer(buf, dtype=np.uint8)
            temp[:] = img
            # print(img)
            # print("video")
        # print(len(img))
        # buf = img
        
        # print(img)
        
        # print(buf)
        # print("video process")
        # if ret:
        #     # shared_mem = shared_memory.SharedMemory(name=shareMemName)
        #     # shared_array = np.ndarray(shape=shape, dtype=dtype, buffer= shared_mem.buf)
        #     # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #     # np.copyto(shared_array, img)
        #     # shared_mem.close()

        #     print(len(img))
        #     buf = img
            # print(np.shape(img))
        # print(len(img))
        # print(buf)
        # print(img)
    
        
        # print("sum is ", buf.size)
        # print("video buf is", buf)
        # release lock
        img_lock.release()
        time.sleep(0.03)
        

        # imgDeal = pLeft.recv()
        # print(len(imgDeal))
            # print("send image ", img)
            # print("send len", len(img))
            # cnt += 1
        # time.sleep(1)


        # ret, img = huaCap.read()
        # # send image data to queue
        # if ret:
        #     qImg.put(img)
        #     # print("send image")
        # else:
        #     print("video process humCap is fail")
        # time.sleep(1)

        # print("this is video process")
        # time.sleep(1)
        # # switch
        # if cmd == 0:
        #     # get image
        #     ret, img = huaCap.read()
        #     # send image data to queue
        #     if ret:
        #         qImg.put(img)
        #     else:
        #         print("video process humCap is fail")
        # elif cmd == 1:
        #     # get image
        #     ret, img = facCap.read()
        #     # send image data to queue
        #     if ret:
        #         qImg.put(img)
        #     else:
        #         print("video process facCap is fail")


if __name__ == '__main__':

    multiprocessing.set_start_method("fork")

    # ctx = multiprocessing.get_context()
    # event = ctx.Event()
    # # 进程锁
    imgLock = multiprocessing.Lock()
    imgDLock = multiprocessing.Lock()
    # y = np.ones((480,640,3))
    # 共享内存
    imgBuf = multiprocessing.Array(ctypes.c_uint8, 640*480*3, lock= False)
    imgDBuf = multiprocessing.Array(ctypes.c_uint8, 640*480*3, lock= False)
    # main_nparray = main_nparray.reshape(NUM_PROCESS, 10)

    # print("share")
    # dtype = np.uint8()
    # shape = (480, 640, 3)
    # shareMem = shared_memory.SharedMemory(create= True, size = int(np.prod(shape)*np.dtype(dtype).itemsize))
    # shareMemName = shareMem.name()
    # print("share end")
    # print(imgBuf[:])
    # imgDBuf = multiprocessing.Value(np.ones((480,640,3)))


    # # quenu
    # qImg = multiprocessing.Queue(0)
    # qCmd = multiprocessing.Queue()

    # pipe
    #(pipe_left, pipe_right) = multiprocessing.Pipe(True)

    print('开始主进程。。。')
    # start = time.time()

    # 使用线程池建立3个子进程
    # pool = multiprocessing.Pool(3)
    # print('开始3个子进程。。。')

    # videoThread = Thread(target = videoProcess)
    
    # videoThread.start()
    # videoThread.join()

    # videoThread = Thread(target=videoProcess, args = (qCmd, qImg))
    # videoThread.start()
    # videoThread.join()

    # img = cv2.imread("./image/bus.jpg")
    # imgDBuf = 1
    # videoProces = multiprocessing.Process(target=videoProcess, args = (lock, shareMemName,shape, dtype, event))
    videoProces = multiprocessing.Process(target=videoProcess, args = (imgLock, imgBuf, imgDLock, imgDBuf,))
    videoProces.start()

    time.sleep(0.1)

    # humProces = multiprocessing.Process(target=human_track_thread, args = (imgLock, imgBuf, imgDLock, imgDBuf))
    # humProces.start()

    facProces = multiprocessing.Process(target=face_detec_thread, args = (imgLock, imgBuf, imgDLock, imgDBuf,))
    facProces.start()

    # videoProces.terminate()

    print("videoProce", videoProces.is_alive())
    # print("humProce", humProces.is_alive())

    # pool.apply_async(human_track_thread(qImg))

    # pool.apply_async(face_detec_thread)
    
    # pool.apply_async(server_process, IP, PORT)
    # for i in range(3):
    #     pool.apply_async(apply_test, [i])
    # print('主进程结束，耗时 %s' % (time.time() - start))
    
    # 
    # img[] = 0
    time.sleep(2)
    while True:

        
        imgDLock.acquire()

        image = np.frombuffer(imgDBuf, dtype=np.uint8).reshape(480, 640, 3)
        


        # cv2.imwrite("img.jpg", image)
        
        # print("data is ",imgDBuf[2])
        imgDLock.release()
        server.run(image)
        # qImg.put(img)
        # data = pipe_right.recv()
        # lock.acquire()
        
        # image = imgBuf
        # image = np.frombuffer(imgBuf, dtype=np.uint8).reshape(480, 640, 3)
        # # cv2.imshow(image)
        # cv2.imwrite("img.jpg", image)
        # print(image)
        # print("len is ", len(imgBuf))
       # print(imgBuf)
        # shared_mem = shared_memory.SharedMemory(name=shareMemName)
        # shared_array = np.ndarray(shape=shape, dtype=dtype, buffer= shared_mem.buf)
        # img = cv2.cvtColor(shared_array, cv2.COLOR_RGB2BGR)
        # cv2.imshow(img)

        # shared_mem.close()

        # cv2.imshow(imgBuf)
        # server_process()
        # data = qImg.get()
        # print("receive is ", data)
        # print("receive len", len(data))
        # print(imgBuf)
        # cv2.imwrite("img.jpg", imgBuf)
        # print("len is ", len(data))
        # print(img.shape)
        # cv2.imshow("img", data)
        # print(img)
        
       
        # lock.release()
        time.sleep(0.01)
        print("this is main process")
    # 为了演示效果，这儿使用休眠方式
    # time.sleep(10)

# def case_fcn_1():
#     if (facCap.isOpened()):

#         ret, facImg = facCap.read()
#         # if swich_key == 1:

#         cv2.imshow("facWin", facImg)

#         # if cv2.waitKey(1) & 0xFF == ord('w'):
#         #     break

    
# def case_fcn_2():
#     if (humCap.isOpened()):

#         ret, humImg = humCap.read()
#         # if swich_key == 0:
#         cv2.imshow("humWin", humImg)
    
           

# if __name__ == "__main__":
    
#     cnt = 0
#     while True:
#         cnt += 1
#         if swich_key == 0:
#             case_fcn_1()
#         elif swich_key == 1:
#             case_fcn_2()
#         if cnt > 1000:

#             if swich_key == 0:
#                 swich_key = 1
#             elif swich_key == 1:
#                 swich_key = 0

#             cnt = 0
#             print("switch")
#         time.sleep(0.01)
  

# while True:

#     switc
#     time.sleep(1)

# print("now switch_key is", swich_key)
# time.sleep(5)
# swich_key = 1
# print("now switch_key is", swich_key)
