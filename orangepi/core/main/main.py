from threading import Thread, current_thread
import time, os
import cv2
import multiprocessing
import psutil
from human_track import human_track_thread
from face_detec import face_detec_thread

from sockets import Server, server_process
# from video import videoProcess
#facCap = cv2.VideoCapture(0)

swich_key = 0

IP = "192.168.4.15"
PORT = 8000

# server = Server(IP, PORT)

#cv2.namedWindow("facWin", cv2.WINDOW_AUTOSIZE)

# def human_track_thread():

#     # cv2.namedWindow("humWin", cv2.WINDOW_AUTOSIZE)

#     while True:
#         if (humCap.isOpened()):

#             ret, humImg = humCap.read()

#             # if swich_key == 0:
#             if ret:
#                 # cv2.imshow("humWin", humImg)
#                 print("hum cat get")
    
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#         #print("this is human track \r\n")
#         time.sleep(1)  
#         # cv2.destroyALLWindows()  

#     humCap.release()
#     cv2.destroyALLWindows()
        
   

# def face_detec_thread():

    
#     # cv2.namedWindow("facWin", cv2.WINDOW_AUTOSIZE)
#     while True:
#         if (facCap.isOpened()):

#             ret, facImg = facCap.read()
#             # if swich_key == 1:

#             if ret:
#                 cv2.imshow("facWin", facImg)
#                 print("fac cat get")
    
#             if cv2.waitKey(1) & 0xFF == ord('w'):
#                 break

#         #print("this is face detec thread \r\n")
#         time.sleep(1)
        

#     facCap.release()
#     cv2.destroyALLWindows()
#     # print("face thread end")

# huaTraThread = Thread(target = human_track_thread)
# facDetThread = Thread(target = face_detec_thread)

# huaTraThread.start()
# facDetThread.start()

# huaTraThread.join()
# facDetThread.join()




# class VideoSwitch():
#     def __init__(self) -> None:

#         pass




    # cmd = qCmd.get()
        
HUM_CAP_NUM = 0
FAC_CAP_NUM = 2

# video process
def videoProcess(qCmd, qImg):

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
    cnt = 0
    # img = [1,2,3,4,5]
    while True:
       
        # send image data to queue
        ret, img = huaCap.read()
        if ret:
            qImg.put(img)
            # print("send image ", img)
            # print("send len", len(img))
            # cnt += 1
        # time.sleep(1)


        # ret, img = huaCap.read()
        # # send image data to queue
        # if ret:
        #     qImg.put(img)
        #     print("send image")
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

    # quenu
    qImg = multiprocessing.Queue(0)
    qCmd = multiprocessing.Queue()

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

    videoProces = multiprocessing.Process(target=videoProcess, args = (qCmd, qImg))
    videoProces.start()


    humProces = multiprocessing.Process(target=human_track_thread, args = (qImg,))
    humProces.start()

    # videoProces.terminate()

    print("videoProce", videoProces.is_alive())
    # print("humProce", humProces.is_alive())

    # pool.apply_async(human_track_thread(qImg))

    # pool.apply_async(face_detec_thread)
    
    # pool.apply_async(server_process, IP, PORT)
    # for i in range(3):
    #     pool.apply_async(apply_test, [i])
    # print('主进程结束，耗时 %s' % (time.time() - start))
    

    while True:
        # qImg.put(img)
        print("this is main process")
        # server_process()
        # data = qImg.get()
        # print("receive is ", data)
        # print("receive len", len(data))
        # cv2.imwrite("img.jpg", data)
        # print("len is ", len(data))
        # print(img.shape)
        # cv2.imshow("img", data)
        # print(img)
        time.sleep(2)

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
