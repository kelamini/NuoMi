import sys

from qtpy.QtCore import Qt
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel)

"""
知识点：
1. 
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("QLabel")
        
        # show texts
        text_label = QLabel("Hello")
        font = text_label.font()
        font.setPointSize(30)
        text_label.setFont(font)
        text_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        # show images
        images_label = QLabel("images")
        images_label.setPixmap(QPixmap("assets/images.jpeg"))
        images_label.setScaledContents(True)
        images_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout = QVBoxLayout()
        layout.addWidget(text_label)
        layout.addWidget(images_label)
        
        main_widget = QWidget()
        main_widget.setLayout(layout)
        
        self.setCentralWidget(main_widget)


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.raise_()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
