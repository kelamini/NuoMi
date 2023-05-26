# import time
# import multiprocessing
# import cv2
 
# humCap = cv2.VideoCapture(0)
# facCap = cv2.VideoCapture(2)

# def humProcess():
#     while True:
#         if (humCap.isOpened()):

#             ret, humImg = humCap.read()

#             # if swich_key == 0:
#             if ret:
#                 #cv2.imshow("humWin", humImg)
#                 print("hum cap get")
#             else:
#                 print("hum cap fail")    
#             # if cv2.waitKey(1) & 0xFF == ord('q'):
#             #     break
#         print("this is human track \r\n")
#         time.sleep(1)  
#     cv2.destroyALLWindows()  


#     # while True:
#     #     time.sleep(1)
#     #     print("human process")

# def faceProcess():
#     while True:
#         if (facCap.isOpened()):

#             ret, facImg = facCap.read()
#             # if swich_key == 1:

#             if ret:
#                 print("face cap get")
#                 #cv2.imshow("facWin", facImg)
#             else:
#                 print("face cap fail")    
    
#             # if cv2.waitKey(1) & 0xFF == ord('w'):
#             #     break

#         print("this is face detec thread \r\n")
#         time.sleep(1)
#     cv2.destroyALLWindows()

 
# if __name__ == '__main__':
#     print('开始主进程。。。')
#     start = time.time()

#     # 使用线程池建立3个子进程
#     pool = multiprocessing.Pool(3)
#     print('开始3个子进程。。。')

#     pool.apply_async(humProcess)
#     pool.apply_async(faceProcess)

#     # for i in range(3):
#     #     pool.apply_async(apply_test, [i])
#     print('主进程结束，耗时 %s' % (time.time() - start))
    
#     # 为了演示效果，这儿使用休眠方式
#     time.sleep(10)





# import cv2
# import threading

# # 摄像头1的线程函数
# def camera1_thread():
#     cap1 = cv2.VideoCapture(0)
#     while True:
#         ret, frame = cap1.read()
#         if ret:
#             #cv2.imshow('Camera 1', frame)
#             print("cap1 get")
#         if cv2.waitKey(1) == ord('q'):
#             break
#     cap1.release()
#     cv2.destroyAllWindows()

# # 摄像头2的线程函数
# def camera2_thread():
#     cap2 = cv2.VideoCapture(2)
#     while True:
#         ret, frame = cap2.read()
#         if ret:
#             #cv2.imshow('Camera 2', frame)
#             print("cap2 get")
#         if cv2.waitKey(1) == ord('q'):
#             break
#     cap2.release()
#     cv2.destroyAllWindows()

# if __name__ == '__main__':
#     # 创建两个线程分别打开摄像头
#     t1 = threading.Thread(target=camera1_thread)
#     t2 = threading.Thread(target=camera2_thread)
#     # 启动线程
#     t1.start()
#     t2.start()
#     # 等待线程结束
#     t1.join()
#     t2.join()

