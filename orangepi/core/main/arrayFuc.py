import cv2
import numpy as np

# 从内存池读取图片
def readImgFromArray(lock, buf):
    lock.acquire()

    img = np.frombuffer(buf, dtype=np.uint8).reshape(480, 640, 3)

    lock.release()
    return img

# 从内存池写入图片
def writeImgFromArray(lock, buf, img):
    lock.acquire()

    img = cv2.resize(img, (640, 480))
    img = img.flatten(order='C')
    temp = np.frombuffer(buf, dtype=np.uint8)
    temp[:] = img
    
    lock.release()
    return True