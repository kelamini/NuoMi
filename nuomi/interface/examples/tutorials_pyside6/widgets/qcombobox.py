import sys

from qtpy.QtCore import Qt
from qtpy.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QComboBox)

"""
知识点：
1. 
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("QLabel")
        
        combobox = QComboBox()
        combobox_value_list = ["One", "Tow", "Three"]
        combobox.addItems(combobox_value_list)
        
        # ------------------ 设置为可编辑状态 ---------------------
        # combobox.setEditable(True)  # 编辑的值将作为新值插入到列表最后
        # combobox.setInsertPolicy(QComboBox.NoInsert)            # 不可插入
        # combobox.setInsertPolicy(QComboBox.InsertAtTop)         # 在顶端插入
        # combobox.setInsertPolicy(QComboBox.InsertAtCurrent)     # 在当前项插入
        # combobox.setInsertPolicy(QComboBox.InsertAtBottom)      # 在底端插入
        # combobox.setInsertPolicy(QComboBox.InsertAfterCurrent)  # 在当前项之前插入
        # combobox.setInsertPolicy(QComboBox.InsertBeforeCurrent) # 在当前项之后插入
        # combobox.setInsertPolicy(QComboBox.InsertAlphabetically)# 按字母顺序插入
        # -------------------------------------------------------
        
        combobox.setMaxCount(10)    # 设置最大数量
        
        combobox.currentIndexChanged.connect(self.index_changed)
        combobox.currentTextChanged.connect(self.text_changed)
        
        layout = QHBoxLayout()
        layout.addWidget(combobox)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        
        self.setCentralWidget(main_widget)
        
    def index_changed(self, index):
        print(index)
        
    def text_changed(self, text):
        print(text)


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.raise_()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
