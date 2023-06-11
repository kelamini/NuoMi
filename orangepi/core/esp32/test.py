import urllib.request
import cv2
import numpy as np

url='http://192.168.4.10/cam.mjpeg'#// 改成自己的ip地址+/cam-hi.jpg

url2 = "http://www.baidu.com"
while True:
    imgResp=urllib.request.urlopen(url2)
    print(imgResp.read())
    
    # print(imgResp.read())
    # imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    
    # img=cv2.imdecode(imgNp,-1)

    # # all the opencv processing is done here
    # cv2.imshow('test',img)
    # #print("test")
    # if ord('q')==cv2.waitKey(10):
    #     exit(0)
