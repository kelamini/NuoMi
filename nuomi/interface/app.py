import os
import os.path as osp
import cv2 as cv

from qtpy.QtCore import Qt, QTimer
from qtpy.QtGui import QPixmap, QImage
from qtpy.QtWidgets import (QMainWindow, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout,
                            QSpacerItem, QSizePolicy, QCheckBox, QLineEdit)

from utils import AccessBlock


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1296, 720)
        
        # spacer
        self.spacerItem = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        # button
        self.play_video_button = QPushButton("Play")
        self.unplay_video_button = QPushButton("Unplay")
        self.control_top_button = QPushButton("Top")
        self.control_down_button = QPushButton("Down")
        self.control_lift_button = QPushButton("Lift")
        self.control_right_button = QPushButton("Right")
        
        # playing video's label
        self.videos_label = QLabel("Display Videos")
        self.videos_label.setScaledContents(True)
        self.videos_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # checkbox
        self.person_detect_checkbox = QCheckBox("person detection")
        self.person_detect_checkbox.setCheckState(Qt.CheckState.Unchecked)
        self.gesture_recognition_checkbox = QCheckBox("gesture recognition")
        self.gesture_recognition_checkbox.setCheckState(Qt.CheckState.Unchecked)

        # lineedit
        self.rtsp_url_lineedit = QLineEdit("RTSP URL: ")
        # self.rtsp_url_lineedit.setMaxLength(20)
        # self.rtsp_url_lineedit.setPlaceholderText("Enter rtsp url")
        self.rtsp_url_lineedit.setInputMask('rtsp://000.000.000.000:xxxxxxxxxxxxxxxxxxxxxx')
        
        # video button
        video_button_layout = QHBoxLayout()
        video_button_layout.addWidget(self.play_video_button)
        video_button_layout.addWidget(self.unplay_video_button)
        # control button
        control_button_layout = QHBoxLayout()
        control_button_layout.addWidget(self.control_top_button)
        control_button_layout.addWidget(self.control_lift_button)
        control_button_layout.addWidget(self.control_right_button)
        control_button_layout.addWidget(self.control_down_button)
        # ai checkbox
        ai_checkbox_layout = QVBoxLayout()
        ai_checkbox_layout.addWidget(self.person_detect_checkbox)
        ai_checkbox_layout.addWidget(self.gesture_recognition_checkbox)

        # button box
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.rtsp_url_lineedit)
        button_layout.addLayout(video_button_layout)
        button_layout.addLayout(control_button_layout)
        button_layout.addLayout(ai_checkbox_layout)
        button_layout.addItem(self.spacerItem)

        # global box
        global_layout = QHBoxLayout()
        global_layout.addWidget(self.videos_label, 5)
        global_layout.addLayout(button_layout, 1)
        
        # mainwindow widget
        widget = QWidget()
        widget.setLayout(global_layout)
        self.setCentralWidget(widget)
        
        # --------------------------------------------------------
        self.rtsp_url = None
        self.video_timer = QTimer()
        self.handle_buttons()
        self.handle_checkbox()
        self.handle_lineedit()


    def handle_buttons(self):
        self.play_video_button.clicked.connect(self.video_start)
        self.unplay_video_button.clicked.connect(self.video_stop)
        self.control_top_button.clicked.connect(self.control_top)
        self.control_down_button.clicked.connect(self.control_down)
        self.control_lift_button.clicked.connect(self.control_lift)
        self.control_right_button.clicked.connect(self.control_right)

    def handle_checkbox(self):
        self.person_detect_checkbox.stateChanged.connect(self.person_detect_state_changed)
        self.gesture_recognition_checkbox.stateChanged.connect(self.gesture_recognition_state_changed)

    def handle_lineedit(self):
        self.rtsp_url_lineedit.returnPressed.connect(self.return_pressed)
        self.rtsp_url_lineedit.textEdited.connect(self.text_edited)

    def person_detect_state_changed(self, state):
        if state == 0:  # False
            print("person_detect_state_changed: ", state)
        if state == 2:  # True
            print("person_detect_state_changed: ", state)

    def gesture_recognition_state_changed(self, state):
        if state == 0:  # False
            print("gesture_recognition_state_changed: ", state)
        if state == 2:  # True
            print("gesture_recognition_state_changed: ", state)

    def video_start(self):
        self.video_timer.start(10)
        self.video_timer.timeout.connect(self.video_play)
        
    def video_stop(self):
        self.video_timer.stop()
    
    def control_top(self):
        print("control top clicked.")

    def control_down(self):
        print("control down clicked.")

    def control_lift(self):
        print("control lift clicked.")

    def control_right(self):
        print("control right clicked.")

    def return_pressed(self):
        print("Return pressed!")
        self.rtsp_url_lineedit.setText(self.rtsp_url)
        print(self.rtsp_url)
        self.open_video()

    def text_edited(self, text):
        self.rtsp_url = text

    def open_video(self):
        self.cap = cv.VideoCapture(self.rtsp_url)
        if not self.cap.isOpened():
            print("Video Path Error!!!")

    def video_play(self):
        ret, image = self.cap.read()
        if ret:
            if len(image.shape) == 3:
                video_img = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_BGR888)
            elif len(image.shape) == 1:
                video_img = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_Indexed8)
            else:
                video_img = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_BGR888)
            self.videos_label.setPixmap(QPixmap(video_img))
        else:
            self.cap.release()
            self.video_timer.stop()
