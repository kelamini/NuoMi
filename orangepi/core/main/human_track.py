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


YAW_DUTY_LEFT = 100
YAW_DUTY_RIGHT= 0
YAW_DUTY_NOR = 56
YAW_PWM_CHIPX = 1     # PWM chip  PWM1
YAW_PWM_CH = 0        # PWM ch 
YAW_PWM_HZ = 50


# Pitch limit
PIT_DUTY_DOWN = 25
PIT_DUTY_UP = 75
PIT_DUTY_NOR = 45
PIT_PWM_CHIPX = 0     # PWM chip    
PIT_PWM_CH = 0        # PWM ch      PWM0
PIT_PWM_HZ = 50

CENTER_X = 320
CENTER_Y = 320+50

AXSI_FITER_PRE = 90

yawSer = Ser(YAW_PWM_CHIPX, YAW_PWM_CH, YAW_PWM_HZ, YAW_DUTY_NOR, YAW_DUTY_LEFT, YAW_DUTY_RIGHT)
pitSer = Ser(PIT_PWM_CHIPX, PIT_PWM_CH, PIT_PWM_HZ, PIT_DUTY_NOR, PIT_DUTY_UP, PIT_DUTY_DOWN)

yawPid = DeltaPID(YAW_DUTY_NOR, 0.15, 0.020, 0.015, 0)
pitPid = DeltaPID(PIT_DUTY_NOR, 0.15, 0.020, 0.018, 0)



def human_track_thread(img_cam0, img_hum, event, ary):

    #cap = cv2.VideoCapture('./video/islandBenchmark.mp4')
    # cap = cv2.VideoCapture(num)
    
    event.wait()

    print("this is human thread")
    modelPath = "./rknnModel/yolov5s.rknn"
    # 线程数, 增大可提高帧率
    TPEs = 3
    # 初始化rknn池
    pool = rknnPoolExecutor(
        rknnModel=modelPath,
        TPEs=TPEs,
        func=myFunc)
    print("human process rknn init is ok")

    # 初始化异步所需要的帧
    for i in range(TPEs + 1):
        frame = img_cam0.read()
    
   

    frames, loopTime, initTime = 0, time.time(), time.time()

    person_flag , personSum_x, personSum_y, person_x, person_y= 0, 0, 0, 0, 0



    print("human process init is ok")

    # lock.release()
    while True:
        event.wait()

        img_cam0.read()
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

                    cv2.circle(img, (person_x, person_y), 4, (0, 0, 255), 2)
                    cv2.circle(img, (CENTER_X, CENTER_Y), 4, (0, 255, 0), 2)

                    if abs(CENTER_X-imgCen_x) > 10:
                        yawPid.calcalate(CENTER_X, imgCen_x)

                    if abs(CENTER_Y-imgCen_y) > 10:
                        pitPid.calcalate(CENTER_Y, imgCen_y)

                    yawSer.set(yawPid.cur_val)
                    pitSer.set(pitPid.cur_val)
                # 共享内存
                ary[5] = int(imgCen_x)&0xF0           # 高8位
                ary[6] = int(imgCen_x)&0x0F           # 低8位
                ary[7] = int(imgCen_y)&0xF0           # 高8位
                ary[8] = int(imgCen_y)&0x0F           # 低8位
            else:
                person_flag = 0
                personSum_x = 0
                personSum_y = 0

                 # 共享内存
                ary[5] = 0           # 高8位
                ary[6] = 0           # 低8位
                ary[7] = 0           # 高8位
                ary[8] = 0           # 低8位
                
                
            if frames % 30 == 0:
                print("this is gesture")
                # print("30帧平均帧率:\t", 30 / (time.time() - loopTime), "帧")
                # print("score", score)
                
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


            ############# write deal image ###############
            img_hum.write(img)
            event.clear()

           
        else:
            print("human thread not image")

       
    print("总平均帧率\t", frames / (time.time() - initTime))
    # 释放cap和rknn线程池
    # cap.release()
    cv2.destroyAllWindows()
    pool.release()
