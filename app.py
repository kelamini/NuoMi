import os
import os.path as osp

from qtpy.QtCore import Qt
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout

from utils import AccessBlock


class MainWindow(QMainWindow):
    def __init__(self, imagedir):
        super(MainWindow, self).__init__()
        self.resize(800, 600)
        # self.setMinimumSize(400, 300)  # 最小窗口尺寸
        # self.setMaximumSize(1080, 720) # 最大窗口尺寸
        
        self.images_dir = imagedir

        self.play_video_button = QPushButton("Play")
        self.play_video_button.clicked.connect(self.play_video)
        self.unplay_video_button = QPushButton("Unplay")
        self.unplay_video_button.clicked.connect(self.unplay_video)
        
        # show images
        self.images_label = QLabel("Videos")
        self.images_label.setScaledContents(True)
        self.images_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.play_video_button)
        hlayout.addWidget(self.unplay_video_button)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.images_label)
        vlayout.addLayout(hlayout)
        
        widget = QWidget()
        widget.setLayout(vlayout)
        self.setCentralWidget(widget)

    def play_video(self):
        print("Playing Videos!!!")
        images_list = os.listdir(self.images_dir)
        for imagename in images_list:
            images_path = osp.join(self.images_dir, imagename)
            self.images_label.setPixmap(QPixmap(images_path))
    
    def unplay_video(self):
        print("Unplaying Videos!!!")
        self.images_label.setText("Videos")
