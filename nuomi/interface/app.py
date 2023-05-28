import os
import sys
import os.path as osp
from typing import Optional
import PySide6.QtCore
import cv2 as cv
from time import time, sleep

from utils import Client

from qtpy import QtCore
from qtpy.QtCore import Qt, QTimer, QEventLoop
from qtpy.QtGui import QPixmap, QImage, QTextCursor
from qtpy.QtWidgets import (QMainWindow, QWidget, QPushButton, QLabel, QHBoxLayout, 
                            QVBoxLayout,QSpacerItem, QSizePolicy, QCheckBox, QLineEdit, 
                            QComboBox, QTextBrowser)


class EmittingStr(QtCore.QObject):
    textWritten = QtCore.Signal(str)
    def write(self, text):
    #   text = f"({os.getcwd()})=> {text}\n"
      self.textWritten.emit(text)
      loop = QEventLoop()
      QTimer.singleShot(10, loop.quit)
      loop.exec_()

    def flush(self):
        pass


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1176, 720)
        self.setStyleSheet("""
                            background-color: #BBFFEE;
                            color: #000000;
                            font-family: Titillium;
                            font-size: 14px;
                            """)

        # spacer
        self.spacerItem = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        # textbrowser
        self.textBrowser = QTextBrowser()
        # 输出重定向到 textbrowser
        sys.stdout = EmittingStr()
        sys.stdout.textWritten.connect(self.outputWritten)
        sys.stderr = EmittingStr()
        sys.stderr.textWritten.connect(self.outputWritten)

        # button
        self.play_video_button = QPushButton("Play")
        # self.unplay_video_button = QPushButton("Unplay")
        self.control_top_button = QPushButton("Top")
        self.control_down_button = QPushButton("Down")
        self.control_lift_button = QPushButton("Lift")
        self.control_right_button = QPushButton("Right")
        
        # playing video's label
        self.display_videos_label = QLabel("Display Videos")
        self.display_videos_label.setScaledContents(True)
        self.display_videos_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display_videos_label.setStyleSheet("""
                                                background-color: #888888;
                                                color: #FFFFFF;
                                                font-family: Titillium;
                                                font-size: 26px;
                                                """)
        # explanatory label
        self.functions_label = QLabel("Functions")

        # debug label
        self.debug_label = QLabel("Debug for engine")

        # checkbox
        self.person_detect_checkbox = QCheckBox("Person Detection and Track")
        self.person_detect_checkbox.setCheckState(Qt.CheckState.Unchecked)
        self.gesture_recognition_checkbox = QCheckBox("Gesture Recognition")
        self.gesture_recognition_checkbox.setCheckState(Qt.CheckState.Unchecked)
        self.face_detection_checkbox = QCheckBox("Face Detection")
        self.face_detection_checkbox.setCheckState(Qt.CheckState.Unchecked)
        self.fire_smoke_checkbox = QCheckBox("Fire and Smoke Detection")
        self.fire_smoke_checkbox.setCheckState(Qt.CheckState.Unchecked)
        self.garbage_express_checkbox = QCheckBox("Garbage and Express Detection")
        self.garbage_express_checkbox.setCheckState(Qt.CheckState.Unchecked)

        # lineedit
        self.rtsp_url_lineedit = QLineEdit("RTSP URL: ")
        # self.rtsp_url_lineedit.setMaxLength(20)
        # self.rtsp_url_lineedit.setPlaceholderText("Enter rtsp url")
        self.rtsp_url_lineedit.setInputMask('rtsp://000.000.000.000:00000')
        # combobox
        self.stream_combobox = QComboBox()
        combobox_value_list = ["Living Room", "Kitchen", "Out Door"]
        self.stream_combobox.addItems(combobox_value_list)

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
        ai_checkbox_layout.addWidget(self.face_detection_checkbox)
        ai_checkbox_layout.addWidget(self.fire_smoke_checkbox)
        ai_checkbox_layout.addWidget(self.garbage_express_checkbox)

        # video stream combobox
        stream_combobox_layout = QHBoxLayout()
        stream_combobox_layout.addWidget(self.rtsp_url_lineedit, 3)
        stream_combobox_layout.addWidget(self.stream_combobox, 2)
        stream_combobox_layout.addWidget(self.play_video_button, 1)

        # button box
        button_layout = QVBoxLayout()
        button_layout.addLayout(stream_combobox_layout, 1)
        # button_layout.addWidget(self.functions_label)
        button_layout.addLayout(ai_checkbox_layout, 1)
        # button_layout.addWidget(self.debug_label)
        button_layout.addLayout(control_button_layout, 1)
        # button_layout.addItem(self.spacerItem)
        button_layout.addWidget(self.textBrowser)

        # global box
        global_layout = QHBoxLayout()
        global_layout.addWidget(self.display_videos_label, 5)
        global_layout.addLayout(button_layout, 1)
        
        # mainwindow widget
        widget = QWidget()
        widget.setLayout(global_layout)
        self.setCentralWidget(widget)
        
        # --------------------------------------------------------
        self.message = Message()
        self.client = None
        self.rtsp_url = None
        self.rtsp_stream = None
        self.video_timer = QTimer()
        self.handle_buttons()
        self.handle_checkbox()
        self.handle_lineedit()
        self.handle_combobox()

    def outputWritten(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def handle_buttons(self):
        self.play_video_button.clicked.connect(self.video_start)
        # self.unplay_video_button.clicked.connect(self.video_stop)
        self.control_top_button.clicked.connect(self.control_top)
        self.control_down_button.clicked.connect(self.control_down)
        self.control_lift_button.clicked.connect(self.control_lift)
        self.control_right_button.clicked.connect(self.control_right)

    def handle_checkbox(self):
        self.person_detect_checkbox.stateChanged.connect(self.person_detect_state_changed)
        self.gesture_recognition_checkbox.stateChanged.connect(self.gesture_recognition_state_changed)
        self.face_detection_checkbox.stateChanged.connect(self.face_detection_state_changed)
        self.fire_smoke_checkbox.stateChanged.connect(self.fire_smoke_state_changed)
        self.garbage_express_checkbox.stateChanged.connect(self.garbage_express_state_changed)

    def handle_lineedit(self):
        self.rtsp_url_lineedit.returnPressed.connect(self.url_pressed)
        self.rtsp_url_lineedit.textEdited.connect(self.url_edited)

    def handle_combobox(self):
        self.stream_combobox.currentIndexChanged.connect(self.stream_changed)

    def person_detect_state_changed(self, state):
        if self.client == None:
            print("You don't input rtsp url!")
            return

        if state == 0:  # False
            # print("person_detect_state_changed: ", state)
            self.client.open_client()
            send_message = "_".join([self.message.state[0], self.message.obt_message("functions", 0)])
            print("==> Send messages: ", send_message)
            self.client.send_message(send_message)
            rece_message = self.client.receive_message()
            print("==> Receive messages: ", rece_message)
            self.client.close_client()
            if rece_message.lower() == "true":
                print("Turn off functions to execute person detection.")
            else:
                print("Can't close functions to execute person detection.")
        if state == 2:  # True
            # print("person_detect_state_changed: ", state)
            self.client.open_client()
            send_message = "_".join([self.message.state[1], self.message.obt_message("functions", 0)])
            print("==> Send messages: ", send_message)
            self.client.send_message(send_message)
            rece_message = self.client.receive_message()
            print("==> Receive messages: ", rece_message)
            self.client.close_client()
            if rece_message.lower() == "true":
                print("Turn on functions to execute person detection.")
            else:
                print("Can't open functions to execute person detection.")

    def gesture_recognition_state_changed(self, state):
        if self.client == None:
            print("You don't input rtsp url!")
            return

        if state == 0:  # False
            # print("person_detect_state_changed: ", state)
            self.client.open_client()
            send_message = "_".join([self.message.state[0], self.message.obt_message("functions", 2)])
            print("==> Send messages: ", send_message)
            self.client.send_message(send_message)
            rece_message = self.client.receive_message()
            print("==> Receive messages: ", rece_message)
            self.client.close_client()
            if rece_message.lower() == "true":
                print("Turn off functions to execute gesture recognition.")
            else:
                print("Can't close functions to execute gesture recognition.")
        if state == 2:  # True
            # print("person_detect_state_changed: ", state)
            self.client.open_client()
            send_message = "_".join([self.message.state[1], self.message.obt_message("functions", 2)])
            print("==> Send messages: ", send_message)
            self.client.send_message(send_message)
            rece_message = self.client.receive_message()
            print("==> Receive messages: ", rece_message)
            self.client.close_client()
            if rece_message.lower() == "true":
                print("Turn on functions to execute gesture recognition.")
            else:
                print("Can't open functions to execute gesture recognition.")

    def face_detection_state_changed(self, state):
        if self.client == None:
            print("You don't input rtsp url!")
            return

        if state == 0:  # False
            # print("person_detect_state_changed: ", state)
            self.client.open_client()
            send_message = "_".join([self.message.state[0], self.message.obt_message("functions", 1)])
            print("==> Send messages: ", send_message)
            self.client.send_message(send_message)
            rece_message = self.client.receive_message()
            print("==> Receive messages: ", rece_message)
            self.client.close_client()
            if rece_message.lower() == "true":
                print("Turn off functions to execute face detection.")
            else:
                print("Can't close functions to execute face detection.")
        if state == 2:  # True
            # print("person_detect_state_changed: ", state)
            self.client.open_client()
            send_message = "_".join([self.message.state[1], self.message.obt_message("functions", 1)])
            print("==> Send messages: ", send_message)
            self.client.send_message(send_message)
            rece_message = self.client.receive_message()
            print("==> Receive messages: ", rece_message)
            self.client.close_client()
            if rece_message.lower() == "true":
                print("Turn on functions to execute face detection.")
            else:
                print("Can't open functions to execute face detection.")

    def fire_smoke_state_changed(self, state):
        if self.client == None:
            print("You don't input rtsp url!")
            return

        if state == 0:  # False
            # print("person_detect_state_changed: ", state)
            self.client.open_client()
            send_message = "_".join([self.message.state[0], self.message.obt_message("functions", 3)])
            print("==> Send messages: ", send_message)
            self.client.send_message(send_message)
            rece_message = self.client.receive_message()
            print("==> Receive messages: ", rece_message)
            self.client.close_client()
            if rece_message.lower() == "true":
                print("Turn off functions to execute fire-smoke detection.")
            else:
                print("Can't close functions to execute fire-smoke detection.")
        if state == 2:  # True
            # print("person_detect_state_changed: ", state)
            self.client.open_client()
            send_message = "_".join([self.message.state[1], self.message.obt_message("functions", 3)])
            print("==> Send messages: ", send_message)
            self.client.send_message(send_message)
            rece_message = self.client.receive_message()
            print("==> Receive messages: ", rece_message)
            self.client.close_client()
            if rece_message.lower() == "true":
                print("Turn on functions to execute fire-smoke detection.")
            else:
                print("Can't open functions to execute fire-smoke detection.")

    def garbage_express_state_changed(self, state):
        if self.client == None:
            print("You don't input rtsp url!")
            return

        if state == 0:  # False
            # print("person_detect_state_changed: ", state)
            self.client.open_client()
            send_message = "_".join([self.message.state[0], self.message.obt_message("functions", 4)])
            print("==> Send messages: ", send_message)
            self.client.send_message(send_message)
            rece_message = self.client.receive_message()
            print("==> Receive messages: ", rece_message)
            self.client.close_client()
            if rece_message.lower() == "true":
                print("Turn off functions to execute garbage-express recognition.")
            else:
                print("Can't close functions to execute garbage-express recognition.")
        if state == 2:  # True
            # print("person_detect_state_changed: ", state)
            self.client.open_client()
            send_message = "_".join([self.message.state[1], self.message.obt_message("functions", 4)])
            print("==> Send messages: ", send_message)
            self.client.send_message(send_message)
            rece_message = self.client.receive_message()
            print("==> Receive messages: ", rece_message)
            self.client.close_client()
            if rece_message.lower() == "true":
                print("Turn on functions to execute garbage_express recognition.")
            else:
                print("Can't open functions to execute garbage_express recognition.")

    def video_start(self):
        self.video_timer.start(10)
        self.video_timer.timeout.connect(self.video_play)
        
    # def video_stop(self):
    #     self.video_timer.stop()
    
    def open_video(self):
        rtsp_addr = self.rtsp_url + "/" + self.rtsp_stream
        print("Will connect this rtsp stream: ", rtsp_addr)
        sleep(2)
        self.cap = cv.VideoCapture(rtsp_addr)
        if not self.cap.isOpened():
            print("Can't open rtsp stream!!!")
        # while True:
        #     self.cap = cv.VideoCapture(rtsp_addr)
        #     if not self.cap.isOpened():
        #         print("Can't open rtsp stream!!!")
        #     else:
        #         print("Can open rtsp stream!")
        #         break

    def video_play(self):
        ret, image = self.cap.read()
        if ret:
            if len(image.shape) == 3:
                video_img = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_BGR888)
            elif len(image.shape) == 1:
                video_img = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_Indexed8)
            else:
                video_img = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_BGR888)
            self.display_videos_label.setPixmap(QPixmap(video_img))
        else:
            self.cap.release()
            self.video_timer.stop()

    def control_top(self):
        print("control top clicked.")

    def control_down(self):
        print("control down clicked.")

    def control_lift(self):
        print("control lift clicked.")

    def control_right(self):
        print("control right clicked.")

    def url_pressed(self):
        self.rtsp_url_lineedit.setText(self.rtsp_url)
        self.client = Client(ip=self.rtsp_url.split("//")[-1].split(":")[0], point=8000)
        self.client.open_client()
        self.client.send_message("Tell me your push rtsp stream address.")
        message = self.client.receive_message()
        print("===> RTSP Address: ", message)
        self.rtsp_stream = message
        self.client.close_client()
        if message.lower():
            self.open_video()
        else:
            print("Can't open rtsp stream!!!")

    def url_edited(self, text):
        self.rtsp_url = text

    def stream_changed(self, index):
        if index == 0:
            if not self.rtsp_url == None:
                self.client.open_client()
                self.client.send_message(self.message.obt_message("stream", index))
                message = self.client.receive_message()
                self.client.close_client()
                if message.lower() == "true":
                    self.open_video()
                else:
                    print("Can't open rtsp stream!!!")
            else:
                print("You don't input rtsp url!")

        elif index == 1:
            if not self.rtsp_url == None:
                self.client.open_client()
                self.client.send_message(self.message.obt_message("stream", index))
                message = self.client.receive_message()
                self.client.close_client()
                if message.lower() == "true":
                    self.open_video()
                else:
                    print("Can't open rtsp stream!!!")
            else:
                print("You don't input rtsp url!")

        elif index == 2:
            if not self.rtsp_url == None:
                self.client.open_client()
                self.client.send_message(self.message.obt_message("stream", index))
                message = self.client.receive_message()
                self.client.close_client()
                if message.lower() == "true":
                    self.open_video()
                else:
                    print("Can't open rtsp stream!!!")
            else:
                print("You don't input rtsp url!")
        else:
            pass

class Message:
    def __init__(self):
        self.messages = {
            "stream": ["mystream_0", "mystream_1", "mystream_2",],
            "functions": [
                "person_track", "face_detection", "gesture_recognition", 
                "fire_smoke", "garbage_express",
            ],
        }
        self.state = ["OFF", "ON"]

    def append_message(self, message):
        self.messages.append(message)

    def delete_message(self):
        self.messages.pop()

    def obt_message(self, type, index):
        return self.messages[type][index]
