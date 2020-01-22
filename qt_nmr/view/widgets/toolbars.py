from PySide2.QtWidgets import QWidget
from PySide2.QtCore import Signal as pyqtSignal


class BaseToolbar(QWidget):
    def __init__(self, mainwindow, *args, **kwargs):
        super(BaseToolbar, self).__init__(*args, **kwargs)
        self.mainwindow = mainwindow
        self.data = {}

    def reset(self, setting):
        pass

class TestClass(QWidget):
    value_changed = pyqtSignal(tuple)


class TestSubclass(TestClass):
    pass


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication
    app = QApplication(sys.argv)
    a = TestSubclass()
    b = TestSubclass()
    print(a.value_changed)
    print(b.value_changed)
    assert a.value_changed is b.value_changed