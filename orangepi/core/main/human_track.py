import cv2
import time
from rknnpool import rknnPoolExecutor
# 图像处理函数，实际应用过程中需要自行修改
from func import myFunc
from func import findPeple
from serve import Ser
from control import DeltaPID
import multiprocessing
import numpy as np
# Pitch limit
PIT_DUTY_DOWN = 90
PIT_DUTY_UP = 10
PIT_DUTY_NOR = 50
PIT_PWM_CHIPX = 0     # PWM chip    
PIT_PWM_CH = 0        # PWM ch      PWM0
PIT_PWM_HZ = 50

YAW_DUTY_LEFT = 100
YAW_DUTY_RIGHT= 0
YAW_DUTY_NOR = 55
YAW_PWM_CHIPX = 1     # PWM chip  PWM1
YAW_PWM_CH = 0        # PWM ch 
YAW_PWM_HZ = 50

CENTER_X = 320
CENTER_Y = 320+50

AXSI_FITER_PRE = 50

yawSer = Ser(YAW_PWM_CHIPX, YAW_PWM_CH, YAW_PWM_HZ, YAW_DUTY_NOR, YAW_DUTY_LEFT, YAW_DUTY_RIGHT)
pitSer = Ser(PIT_PWM_CHIPX, PIT_PWM_CH, PIT_PWM_HZ, PIT_DUTY_NOR, PIT_DUTY_DOWN, PIT_DUTY_UP)

yawPid = DeltaPID(YAW_DUTY_NOR, 0.15, 0.02, 0.01, 0.01)
pitPid = DeltaPID(PIT_DUTY_NOR, 0.15, 0.01, 0.01, 0.00)



def human_track_thread(img_lock, buf, img_deal_lock, dbuf):

    #cap = cv2.VideoCapture('./video/islandBenchmark.mp4')
    # cap = cv2.VideoCapture(num)
    

    print("this is human thread")
    modelPath = "./rknnModel/yolov5s.rknn"
    # 线程数, 增大可提高帧率
    TPEs = 4
    # 初始化rknn池
    pool = rknnPoolExecutor(
        rknnModel=modelPath,
        TPEs=TPEs,
        func=myFunc)
    print("human process rknn init is ok")
    # 初始化异步所需要的帧
   
    # for i in range(TPEs + 1):
    #     frame = np.frombuffer(buf, dtype=np.uint8).reshape(480, 640, 3)
    #     pool.put(frame)

    img_lock.acquire()
    for i in range(TPEs + 1):
        frame = np.frombuffer(buf, dtype=np.uint8).reshape(480, 640, 3)
    img_lock.release()
    #     pool.put(frame)
    # if (cap.isOpened()):
    #     for i in range(TPEs + 1):
    #         ret, frame = cap.read()
    #         if not ret:
    #             cap.release()
    #             del pool
    #             exit(-1)
    #         pool.put(frame)

    frames, loopTime, initTime = 0, time.time(), time.time()

    person_flag , personSum_x, personSum_y, person_x, person_y= 0, 0, 0, 0, 0



    print("human process init is ok")

    # lock.release()
    while True:

        img_lock.acquire()
    # while (cap.isOpened()):
        frame = np.frombuffer(buf, dtype=np.uint8).reshape(480, 640, 3)
        img_lock.release()
        # print(len(frame))
        # print(cv2.shape(frame))
        # frame = q.get()
        if frame is not None:
            # print("human thread get image")
            frames += 1
        # ret, frame = cap.read()
        # if ret:
            pool.put(frame)

            #从线程池取结果
            #frame, boxes, classes, scores, flag = pool.get()
            retData ,flag = pool.get()
            img = retData[0]

            if flag == False:
                break
        
            # 寻找人  
            n, imgCen_x, imgCen_y, score = findPeple(retData)
            
        

            if n > 0:

                #imgCen_x = int(imgCen_x/10*10)
                #imgCen_y = int(imgCen_y/10*10)

                #print("find ", n, "personal")
                person_flag += 1
                personSum_x += imgCen_x
                personSum_y += imgCen_y
                
                if person_flag > 3:

                    person_x = int(personSum_x/person_flag/AXSI_FITER_PRE*AXSI_FITER_PRE)
                    person_y = int(personSum_y/person_flag/AXSI_FITER_PRE*AXSI_FITER_PRE)

                    person_flag = 0
                    personSum_x = 0
                    personSum_y = 0

                    cv2.circle(img, (person_x, person_y), 1, (0, 0, 255), 2)

                    yawPid.calcalate(CENTER_X, imgCen_x)
                    pitPid.calcalate(imgCen_y, CENTER_Y)

                    yawSer.set(yawPid.cur_val)
                    pitSer.set(pitPid.cur_val)
            else:
                person_flag = 0
                personSum_x = 0
                personSum_y = 0
                
                
            if frames % 30 == 0:

                print("30帧平均帧率:\t", 30 / (time.time() - loopTime), "帧")
                print("score", score)
                
                # print("x_pwm:", yawPid.cur_val)
                # print("y_pwm:", pitPid.cur_val)
                
                # print("x error", yawPid._pre_error)
                # print("y error", pitPid._pre_error)
                #print("output", yawPid.delta_output)
                # print("img",retData[0])
                # print("boxes",retData[1])
                # print("classes",retData[2])
                # print("scores",retData[3])

                
            loopTime = time.time()

            # img_deal_lock.acquire()
            # # img = img.reshape(640, 640, 3)
            # # print(img.reshape)
            # img = img.flatten(order='C')
            # temp = np.frombuffer(dbuf, dtype=np.uint8)
            # temp[:] = img

            # img_deal_lock.release()

            # pip right send image
            # pRight.send(img)
            # cv2.circle(img, (CENTER_X, CENTER_Y), 1, (0, 255, 0), 2)
            # cv2.imshow('test', img)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
                # print("this human thead")
        else:
            print("human thread not image")
        # lock.release()

        # img_lock.release()
    print("总平均帧率\t", frames / (time.time() - initTime))
    # 释放cap和rknn线程池
    # cap.release()
    cv2.destroyAllWindows()
    pool.release()
