"""The executable file for the qt_nmr app"""
import sys

from PySide2.QtWidgets import QApplication

from qt_nmr.controller.controller import Controller
from qt_nmr.model.model import Model
from qt_nmr.view.mainwindow import MainWindow


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = Model()
        self.main_controller = Controller(self.model)
        self.main_view = MainWindow(self.main_controller)
        self.main_view.show()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())