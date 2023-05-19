import os
import os.path as osp
import cv2 as cv

from qtpy.QtCore import Qt, QTimer
from qtpy.QtGui import QPixmap, QImage
from qtpy.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout

from utils import AccessBlock


class MainWindow(QMainWindow):
    def __init__(self, videofile=None):
        super(MainWindow, self).__init__()
        self.resize(800, 600)

        self.play_video_button = QPushButton("Play")
        self.unplay_video_button = QPushButton("Unplay")
        
        # show images
        self.videos_label = QLabel("Display Videos")
        self.videos_label.setScaledContents(True)
        self.videos_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.play_video_button)
        hlayout.addWidget(self.unplay_video_button)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.videos_label)
        vlayout.addLayout(hlayout)
        
        widget = QWidget()
        widget.setLayout(vlayout)
        self.setCentralWidget(widget)
        self.video_path = videofile
        self.video_timer = QTimer()
        self.handle_buttons()
        self.open_video()

    def handle_buttons(self):
        self.play_video_button.clicked.connect(self.button_start)
        self.unplay_video_button.clicked.connect(self.button_stop)
        
    def button_start(self):
        self.video_timer.start(100)
        self.video_timer.timeout.connect(self.video_play)
        
    def button_stop(self):
        self.video_timer.stop()
    
    def open_video(self):
        if self.video_path == None:
            print("Video Path Error!!!")
        else:
            self.cap = cv.VideoCapture(self.video_path)
    
    def video_play(self):
        ret, image = self.cap.read()
        if ret:
            if len(image.shape) == 3:
                video_img = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
            elif len(image.shape) == 1:
                video_img = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_Indexed8)
            else:
                video_img = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
            self.videos_label.setPixmap(QPixmap(video_img))
        else:
            self.cap.release()
            self.video_timer.stop()
