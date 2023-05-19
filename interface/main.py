import sys
import os
import os.path as osp

from qtpy import QtCore
from qtpy import QtWidgets

from app import MainWindow
from utils import newIcon

__appname__ = "NuoMi"


def main():
    config_video_path = "assets/videos.mp4"
    
    translator = QtCore.QTranslator()
    translator.load(
        QtCore.QLocale.system().name(),
        osp.join(osp.dirname(osp.abspath(__file__)), "translate"),
    )
    
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(__appname__)
    app.setWindowIcon(newIcon("icon"))
    app.installTranslator(translator)
    win = MainWindow(config_video_path)
    
    win.show()
    win.raise_()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
