import sys

from qtpy.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QCheckBox, QComboBox, QDateEdit, QDateTimeEdit, 
                            QDial, QDoubleSpinBox, QFontComboBox, QLCDNumber,
                            QLabel, QLineEdit, QProgressBar, QPushButton,
                            QSlider, QSpinBox, QTimeEdit)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("QuickDemo")
        layout = QVBoxLayout()
        widgets = [
            QCheckBox,
            QComboBox,
            QDateEdit,
            QDateTimeEdit,
            QDial,
            QDoubleSpinBox,
            QFontComboBox,
            QLCDNumber,
            QLabel,
            QLineEdit,
            QProgressBar,
            QPushButton,
            QSlider,
            QSpinBox,
            QTimeEdit,
        ]
        
        for widget in widgets:
            layout.addWidget(widget())
            
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

