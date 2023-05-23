import os
import os.path as osp
from typing import Any
import cv2 as cv


class ReadRtspFromFfmpeg:
    def __init__(self, urlrtsp="192.168.4.15", portrtsp=8554):
        self.url = urlrtsp
        self.port = portrtsp
        self.dir = "mystream"
    
    def init_videocapture(self):
        rtsp_url = f"rtsp://{self.url}:{self.port}/{self.dir}"
        self.cap = cv.VideoCapture(rtsp_url)
        if not self.cap.isOpened():
            raise Exception("Can't open video capture!!!")

    def read_frame(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                raise Exception("Can't read frame!!!")
            cv.imshow("img", frame)
            if cv.waitKey(0) == 27:
                cv.destroyAllWindows()
                self.cap.release()

    def run(self):
        self.init_videocapture()
        self.read_frame()


if __name__ == "__main__":
    read_rtsp = ReadRtspFromFfmpeg()
    read_rtsp.run()