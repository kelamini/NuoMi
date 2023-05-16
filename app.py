from qtpy.QtCore import Qt
from qtpy.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout

from utils import AccessBlock


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(800, 600)
        # self.setMinimumSize(400, 300)  # 最小窗口尺寸
        # self.setMaximumSize(1080, 720) # 最大窗口尺寸

        self.video_canvas = QLabel("Videos")
        self.play_video_button = QPushButton("Click me")

        layout = QVBoxLayout()
        layout.addWidget(self.video_canvas)
        layout.addWidget(self.play_video_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.play_video_button.clicked.connect(self.play_video)


    def play_video(self):
        print("Playing Videos!!!")

