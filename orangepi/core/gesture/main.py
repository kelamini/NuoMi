import cv2
import time
from rknnpool import rknnPoolExecutor
# 图像处理函数，实际应用过程中需要自行修改
from func import myFunc
from func import findPeple


cap = cv2.VideoCapture(4)
modelPath = "./yolov5_gesture.rknn"

# 线程数, 增大可提高帧率
TPEs = 1
# 初始化rknn池
pool = rknnPoolExecutor(
    rknnModel=modelPath,
    TPEs=TPEs,
    func=myFunc)

# 初始化异步所需要的帧
if (cap.isOpened()):
    for i in range(TPEs + 1):
        ret, frame = cap.read()
        if not ret:
            cap.release()
            del pool
            exit(-1)
        pool.put(frame)

frames, loopTime, initTime = 0, time.time(), time.time()

person_flag , personSum_x, personSum_y, person_x, person_y= 0, 0, 0, 0, 0

while (cap.isOpened()):
    frames += 1
    ret, frame = cap.read()
    if not ret:
        break
    pool.put(frame)

    #从线程池取结果
    # frame, boxes, classes, scores, flag = pool.get()
    retData ,flag = pool.get()
    img = retData[0]

    if flag == False:
        break   
        
    if frames % 30 == 0:
    
        print("30帧平均帧率:\t", 30 / (time.time() - loopTime), "帧")

        # print("img",retData[0])
        print("boxes",retData[1])
        print("classes",retData[2])
        print("scores",retData[3])
        
        loopTime = time.time()

   
    cv2.imshow('test', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
print("总平均帧率\t", frames / (time.time() - initTime))
# 释放cap和rknn线程池
cap.release()
cv2.destroyAllWindows()
pool.release()
