import cv2
import time
from rknnpool import rknnPoolExecutor
# 图像处理函数，实际应用过程中需要自行修改
from func import gesFunc, getGesture
import numpy as np

from arrayFuc import readImgFromArray, writeImgFromArray 



def gesThread(img_cam, img_ges, event, ary):

    # 等待事件
    event.wait()

    modelPath = "./rknnModel/yolov5_gesture.rknn"

    # 线程数, 增大可提高帧率
    TPEs = 2

    # 初始化rknn池
    pool = rknnPoolExecutor(
        rknnModel=modelPath,
        TPEs=TPEs,
        func=gesFunc)

    print("gesture rknn is ok")

    # 初始化异步所需要的帧
    
    for i in range(TPEs + 1):
        frame = img_cam.read()
   

    frames, loopTime, initTime = 0, time.time(), time.time()
    print("\r\ngesture is ok\r\n")

    while True:

        event.wait()
        # read image
        img_cam.read()

        frames += 1
        # print("this is gesture")
        if frame is not None:
            
            # 将图片放入线程池
            pool.put(frame)

            # 从线程池取结果
            retData ,flag = pool.get()

            # 结果图片
            img = retData[0]

            # class
           
            # print("get gesture is ",  getGesture(retData))
            ary[9] = getGesture(retData)

            # print("")
            
            if frames % 30 == 0:
                print("this is gesture")
                # print(ary[9])
                # print("gesture: 30帧平均帧率:\t", 30 / (time.time() - loopTime), "帧")

                # print("img",retData[0])
                # print("gesture")
                # print("boxes",retData[1])
                print("classes",retData[2])
                print("scores",retData[3])
                
                loopTime = time.time()
            
            # write deal image 
            img_ges.write(img)
            event.clear()
            

    print("总平均帧率\t", frames / (time.time() - initTime))
    # 释放cap和rknn线程池
    cap.release()
    cv2.destroyAllWindows()
    pool.release()
