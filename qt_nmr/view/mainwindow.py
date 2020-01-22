import sys

from PySide2.QtWidgets import QMainWindow

from qt_nmr.view.settings import view_defaults
from qt_nmr.view.ui import UiMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.view_state = view_defaults
        self._ui = UiMainWindow()
        self._ui.setupUi(self)


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
