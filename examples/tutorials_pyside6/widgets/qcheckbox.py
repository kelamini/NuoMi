import sys

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QCheckBox)

"""
知识点：
1. 
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("QLabel")

        # checkbox
        checkbox = QCheckBox()
        # ---------- 设置 checkbox 的初始状态（五选一） --------------
        # checkbox.setChecked(True)
        # checkbox.setChecked(False)
        checkbox.setCheckState(Qt.CheckState.Unchecked)           # status code: 0
        # checkbox.setCheckState(Qt.CheckState.PartiallyChecked)    # status code: 1
        # checkbox.setCheckState(Qt.CheckState.Checked)             # status code: 2
        # --------------------------------------------------------
        checkbox.setText("This is a checkbox.")
        checkbox.stateChanged.connect(self.show_state)
        
        layout = QHBoxLayout()
        layout.addWidget(checkbox)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        
        self.setCentralWidget(main_widget)

    def show_state(self, state):
        print(state == Qt.CheckState.Checked.value)
        print(state)


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.raise_()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
