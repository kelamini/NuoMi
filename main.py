import sys
import os
import os.path as osp

from qtpy import QtCore
from qtpy import QtWidgets

from app import MainWindow
from utils import newIcon

__appname__ = "NuoMi"


def main():



    translator = QtCore.QTranslator()
    translator.load(
        QtCore.QLocale.system().name(),
        osp.join(osp.dirname(osp.abspath(__file__)), "translate"),
    )
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(__appname__)
    app.setWindowIcon(newIcon("icon"))
    app.installTranslator(translator)
    win = MainWindow()

    # if reset_config:
    #     logger.info("Resetting Qt config: %s" % win.settings.fileName())
    #     win.settings.clear()
    #     sys.exit(0)

    win.show()
    win.raise_()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
