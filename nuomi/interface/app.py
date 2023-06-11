import os
import sys
import os.path as osp
from typing import Optional
import cv2 as cv
import sqlite3
from time import time, sleep

from utils import Client
from dataManage import DataManageUI
from dataRecord import DataRecordUI

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTimer, QEventLoop
from PyQt5.QtGui import QPixmap, QImage, QTextCursor
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QLabel, QHBoxLayout, 
                            QVBoxLayout,QSpacerItem, QSizePolicy, QCheckBox, QLineEdit, 
                            QComboBox, QTextBrowser, QGroupBox)


class EmittingStr(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)
    def write(self, text):
    #   text = f"({os.getcwd()})=> {text}\n"
      self.textWritten.emit(text)
      loop = QEventLoop()
      QTimer.singleShot(10, loop.quit)
      loop.exec_()

    def flush(self):
        pass


# 找不到已训练的人脸数据文件
class TrainingDataNotFoundError(FileNotFoundError):
    pass


# 找不到数据库文件
class DatabaseNotFoundError(FileNotFoundError):
    pass


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1296, 720)
        self.setStyleSheet("""
                            background-color: #CCEEFF;
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
        self.add_face_button = QPushButton("Add Face")
        self.manage_face_button = QPushButton("Manage Face")
        self.database_button = QPushButton("Init Face Data")
        self.control_top_button = QPushButton("Top")
        self.control_down_button = QPushButton("Down")
        self.control_lift_button = QPushButton("Lift")
        self.control_right_button = QPushButton("Right")
        
        # playing video's label
        self.display_videos_label = QLabel("智慧家居安防系统\nAIOT")
        self.display_videos_label.setScaledContents(True)
        self.display_videos_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display_videos_label.setStyleSheet("""
                                                background-color: #666666;
                                                color: #CC0000;
                                                font-family: Titillium;
                                                font-size: 64px;
                                                """)

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
        self.rtsp_url_lineedit = QLineEdit()
        # self.rtsp_url_lineedit.setMaxLength(20)
        # self.rtsp_url_lineedit.setPlaceholderText("Enter rtsp url")
        self.rtsp_url_lineedit.setInputMask('rtsp://000.000.000.000:00000')
        # combobox
        self.stream_combobox = QComboBox()
        combobox_value_list = ["Living Room", "Out Door", "Kitchen"]
        self.stream_combobox.addItems(combobox_value_list)

        # control button
        control_button_layout = QHBoxLayout()
        control_button_layout.addWidget(self.control_top_button)
        control_button_layout.addWidget(self.control_lift_button)
        control_button_layout.addWidget(self.control_right_button)
        control_button_layout.addWidget(self.control_down_button)
        debug_groupbox = QGroupBox("Debug for Engine")
        debug_groupbox.setLayout(control_button_layout)

        # ai checkbox
        ai_checkbox_layout = QVBoxLayout()
        ai_checkbox_layout.addWidget(self.person_detect_checkbox)
        ai_checkbox_layout.addWidget(self.gesture_recognition_checkbox)
        ai_checkbox_layout.addWidget(self.face_detection_checkbox)
        ai_checkbox_layout.addWidget(self.fire_smoke_checkbox)
        ai_checkbox_layout.addWidget(self.garbage_express_checkbox)
        functions_groupbox = QGroupBox("Functions")
        functions_groupbox.setLayout(ai_checkbox_layout)

        # video stream combobox
        stream_combobox_layout = QHBoxLayout()
        stream_combobox_layout.addWidget(self.rtsp_url_lineedit, 4)
        stream_combobox_layout.addWidget(self.stream_combobox, 2)
        stream_combobox_layout.addWidget(self.play_video_button, 1)
        stream_groupbox = QGroupBox("RTSP")
        stream_groupbox.setLayout(stream_combobox_layout)

        # Init database groupbox
        database_layout = QHBoxLayout()
        database_layout.addWidget(self.add_face_button)
        database_layout.addWidget(self.manage_face_button)
        database_layout.addWidget(self.database_button)
        database_groupbox = QGroupBox("Face Data Base")
        database_groupbox.setLayout(database_layout)

        # button box
        button_layout = QVBoxLayout()
        button_layout.addWidget(stream_groupbox, 1)
        button_layout.addWidget(database_groupbox, 1)
        button_layout.addWidget(functions_groupbox, 1)
        button_layout.addWidget(debug_groupbox, 1)
        # button_layout.addItem(self.spacerItem)
        button_layout.addWidget(self.textBrowser, 5)

        # global box
        global_layout = QHBoxLayout()
        global_layout.addWidget(self.display_videos_label, 5)
        global_layout.addLayout(button_layout, 1)
        
        # mainwindow widget
        widget = QWidget()
        widget.setLayout(global_layout)
        self.setCentralWidget(widget)
        
        # --------------------------------------------------------
        self.database = './FaceBase.db'
        self.trainingData = './recognizer/trainingData.yml'
        self.message = Message()
        self.client = None
        self.rtsp_url = None
        self.rtsp_stream = None
        self.cap = None
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
        self.add_face_button.clicked.connect(self.add_face)
        self.manage_face_button.clicked.connect(self.manage_face)
        self.database_button.clicked.connect(self.init_face_database)
        self.control_top_button.clicked.connect(self.control_top)
        self.control_down_button.clicked.connect(self.control_down)
        self.control_lift_button.clicked.connect(self.control_lift)
        self.control_right_button.clicked.connect(self.control_right)

    def handle_checkbox(self):
        self.person_detect_checkbox.stateChanged.connect(self.person_detect_state_changed)
        self.face_detection_checkbox.stateChanged.connect(self.face_detection_state_changed)
        self.gesture_recognition_checkbox.stateChanged.connect(self.gesture_recognition_state_changed)
        self.fire_smoke_checkbox.stateChanged.connect(self.fire_smoke_state_changed)
        self.garbage_express_checkbox.stateChanged.connect(self.garbage_express_state_changed)

    def handle_lineedit(self):
        self.rtsp_url_lineedit.returnPressed.connect(self.url_pressed)
        self.rtsp_url_lineedit.textEdited.connect(self.url_edited)

    def handle_combobox(self):
        self.stream_combobox.currentIndexChanged.connect(self.stream_changed)

    def state_changed(self, state, message):
        if state == 0:  # False
            try:
                self.client.open_client()
                send_message = "_".join(['OFF', message])
                print("==> Send messages: ", send_message)
                self.client.send_message(send_message)
                rece_message = self.client.receive_message()
                print("==> Receive messages: ", rece_message)
                self.client.close_client()
                if rece_message.lower() == "true":
                    print(f"Turn off functions to execute {message.replace('_', ' ')}.")
                else:
                    print(f"Can't close functions to execute {message.replace('_', ' ')}.")
            except:
                print("Ensure you allready connected a server.")
        if state == 2:  # True
            try:
                self.client.open_client()
                send_message = "_".join(['ON', message])
                print("==> Send messages: ", send_message)
                self.client.send_message(send_message)
                rece_message = self.client.receive_message()
                print("==> Receive messages: ", rece_message)
                self.client.close_client()
                if rece_message.lower() == "true":
                    print(f"Turn on functions to execute {message.replace('_', ' ')}.")
                else:
                    print(f"Can't open functions to execute {message.replace('_', ' ')}.")
            except:
                print("Ensure you allready connected a server.")
    
    def person_detect_state_changed(self, state):
        self.state_changed(state, self.message.obt_message("functions", 0))

    def face_detection_state_changed(self, state):
        self.state_changed(state, self.message.obt_message("functions", 1))

    def gesture_recognition_state_changed(self, state):
        self.state_changed(state, self.message.obt_message("functions", 2))

    def fire_smoke_state_changed(self, state):
        self.state_changed(state, self.message.obt_message("functions", 3))

    def garbage_express_state_changed(self, state):
        self.state_changed(state, self.message.obt_message("functions", 4))

    def video_start(self):
        self.video_timer.start(10)
        self.video_timer.timeout.connect(self.video_play)
        
    # def video_stop(self):
    #     self.video_timer.stop()
    
    def open_video(self):
        rtsp_addr = self.rtsp_url + "/" + self.rtsp_stream
        print("Will connect this rtsp stream: ", rtsp_addr)
        sleep(1)
        self.cap = cv.VideoCapture(rtsp_addr)
        if not self.cap.isOpened():
            print("Can't open rtsp stream!!!")
        else:
            print("Can open rtsp stream.")

        # while True:
        #     self.cap = cv.VideoCapture(rtsp_addr)
        #     if not self.cap.isOpened():
        #         print("Can't open rtsp stream!!!")
        #     else:
        #         print("Can open rtsp stream!")
        #         break

    def video_play(self):
        try:
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

        except:
            print("Can't open rtsp stream!!!")
            self.video_timer.stop()

    def add_face(self):
        win = DataRecordUI()
        win.show()

    def manage_face(self):
        print("manage_face")
        win = DataManageUI()
        win.show()


    def init_face_database(self):
        try:
            if not os.path.isfile(self.database):
                raise DatabaseNotFoundError
            if not os.path.isfile(self.trainingData):
                raise TrainingDataNotFoundError

            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            cursor.execute('SELECT Count(*) FROM users')
            result = cursor.fetchone()
            dbUserCount = result[0]
        except DatabaseNotFoundError:
            print('系统找不到数据库文件{}'.format(self.database))
            print('Error：未发现数据库文件，你可能未进行人脸采集')
        except TrainingDataNotFoundError:
            print('系统找不到已训练的人脸数据{}'.format(self.trainingData))
            print('Error：未发现已训练的人脸数据文件，请完成训练后继续')
        except Exception as e:
            print('读取数据库异常，无法完成数据库初始化')
            print('Error：读取数据库异常，初始化数据库失败')
        else:
            cursor.close()
            conn.close()
            if not dbUserCount > 0:
                print('数据库为空，人脸识别功能不可用')
            else:
                print('Success：数据库状态正常，发现用户数：{}'.format(dbUserCount))
                self.database_button.setEnabled(False)
                self.face_detection_checkbox.setToolTip('须先开启人脸跟踪')
                self.face_detection_checkbox.setEnabled(True)

    def control_top(self):
        print("control top clicked.")

    def control_down(self):
        print("control down clicked.")

    def control_lift(self):
        print("control lift clicked.")

    def control_right(self):
        print("control right clicked.")

    def url_pressed(self):
        try:
            self.open_video()
            print("First open rtsp stream: OK.")
            return
        except:
            print("First open rtsp stream: Failed.")
        try:
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
        except:
            print("Can't connect the server: ", self.rtsp_url)

    def url_edited(self, text):
        self.rtsp_url = text

    def stream_changed(self, index):
        if index == 0:
            try:
                self.client.open_client()
                self.client.send_message(self.message.obt_message("stream", index))
                message = self.client.receive_message()
                self.client.close_client()
                if message.lower() == "true":
                    self.open_video()
                else:
                    print("Can't open rtsp stream!!!")
            except:
                print("Ensure you allready connected a server.")

        elif index == 1:
            try:
                self.client.open_client()
                self.client.send_message(self.message.obt_message("stream", index))
                message = self.client.receive_message()
                self.client.close_client()
                if message.lower() == "true":
                    self.open_video()
                else:
                    print("Can't open rtsp stream!!!")
            except:
                print("Ensure you allready connected a server.")

        elif index == 2:
            try:
                self.client.open_client()
                self.client.send_message(self.message.obt_message("stream", index))
                message = self.client.receive_message()
                self.client.close_client()
                if message.lower() == "true":
                    self.open_video()
                else:
                    print("Can't open rtsp stream!!!")
            except:
                print("Ensure you allready connected a server.")
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

    def append_message(self, message):
        self.messages.append(message)

    def pop_message(self):
        self.messages.pop()

    def obt_message(self, type, index):
        return self.messages[type][index]
