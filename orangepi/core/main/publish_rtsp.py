import os
import os.path as osp
import cv2 as cv
from time import time, sleep
import subprocess
import numpy as np

class GstreeamerPublishRtsp:
    def __init__(self, urlrtsp="127.0.0.1", portrtsp=8554):
        self.url = urlrtsp
        self.port = portrtsp
        self.dir = "mystream"
        self.fps = 20
        self.width = 1080
        self.height = 720

    def init_gstreamer(self):
        self.videowriter = cv.VideoWriter('appsrc ! videoconvert' + \
    ' ! x264enc speed-preset=ultrafast bitrate=600 key-int-max=' + str(self.fps * 2) + \
    ' ! video/x-h264,profile=baseline' + \
    ' ! rtspclientsink location='+self.url+':'+str(self.port)+"/"+self.dir,
    cv.CAP_GSTREAMER, 0, self.fps, (self.width, self.height), True)
        if not self.videowriter.isOpened():
            raise Exception("Can't open video writer!!!")
    
    def init_videocapture(self):
        self.cap = cv.VideoCapture()
        if not self.cap.isOpened():
            raise Exception("Can't open video capture!!!")

    def publish(self):
        start = time()
        while True:
            ret, frame = self.cap.read()
            if not ret:
                raise Exception("Can't read frame!!!")
            self.videowriter(frame)
            now = time()
            diff = (1/self.fps) - now - start
            if diff > 0:
                sleep(diff)
            start = now

    def run(self):
        self.init_gstreamer()
        self.init_videocapture()
        self.publish()


class FfmpegPublishRtsp:
    def __init__(self, urlrtsp="192.168.4.15", portrtsp=8554):
        self.url = urlrtsp
        self.port = portrtsp
        self.stream = "streamrtsp"
    
    def init_videocapture(self):
        # self.cap = cv.VideoCapture(2)
        # if not self.cap.isOpened():
        #     raise Exception("Can't open video capture!!!")
        self.fps = 25#int(self.cap.get(cv.CAP_PROP_FPS))
        self.width = 640#int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.height = 480#int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    
    def init_ffmpeg(self):
        command = [
            'ffmpeg',
            '-y', '-an',
            '-re',
            '-f', 'rawvideo',
            # '-vcodec','v4l2',
            '-pix_fmt', 'bgr24', #像素格式
            '-s', "{}x{}".format(self.width, self.height),
            '-r', str(self.fps),
            '-i', '-',
            '-c:v', 'libx264',  # 视频编码方式
            # '-b:v', '400k'
            '-maxrate:v', '6M',
            '-minrate:v', '2M',
            '-bufsize:v', '4M',
            '-pix_fmt', 'yuv420p',
            '-preset', 'ultrafast',
            '-tune', 'zerolatency',
            '-f', 'rtsp', #  flv rtsp
            '-rtsp_transport', 'tcp',
            'rtsp://{}:{}/{}'.format(self.url, self.port, self.stream),
            ] # rtsp rtmp 
        self.pipe = subprocess.Popen(command, shell=False, stdin=subprocess.PIPE)

    def frame_process(self, frame):
        ...
        return frame
    
    def publish(self, frame):
        start = time()
        while True:
            # ret, frame = self.cap.read()

            if frame is  None:
                self.cap.release()
                self.pipe.terminate()
                raise Exception("Can't read frame!!!")
            
            # frame = self.frame_process(frame)
            self.pipe.stdin.write(frame.tostring())
            # self.pipe.stdin.write(frame.tobytes())
            
            now = time()
            diff = (1/self.fps) - now - start
            if diff > 0:
                sleep(diff)
            start = now
        

    def run(self, img):
        self.init_videocapture()
        self.init_ffmpeg()
        self.publish(img)



# val -> value
# bit -> quary bit
# return true or false
def myReadBit(val, bit):
    return (val >> bit)&1

# pulish thread
def pulish_thread(ip, img_ser, even):
    while True:
        
        # wait even is set
        even.wait()

        print("this is pulish thread")
        
        # # cam0_sts = myReadBit(val, 0)
        # # cam1_sts = myReadBit(val, 1)
        # # cam2_sts = myReadBit(val, 2)
        # val = server_data.value
        # cam0_sts = myReadBit(val, 0)
        # cam1_sts = myReadBit(val, 1)
        # cam2_sts = myReadBit(val, 2)
        # # cam0_sts = (val >> 0)&1
        
        # # cam1_sts = (val >> 1)&1
        # # cam2_sts = (val >> 2)&1

        # if cam0_sts:
        #     print("\r\ncam0\r\n")
        #     image_buf = cam0_deal
        # elif cam1_sts:
        #     print("\r\ncam1\r\n")
        #     image_buf = cam1_deal
        # elif cam2_sts:
        #     print("\r\ncam2\r\n")
        #     image_buf = cam2_deal

        image = img_ser.read()
        # server.conn.send("True".encode("utf-8"))
        publish_ffmpeg_frame = FfmpegPublishRtsp(ip, portrtsp=8554)
        publish_ffmpeg_frame.run(image)


# if __name__ == "__main__":
#     # publish_video = GstreeamerPublishRtsp()
#     # publish_video.run()
#     publish_ffmpeg_frame = FfmpegPublishRtsp()
#     publish_ffmpeg_frame.run()

