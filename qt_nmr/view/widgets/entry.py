from PySide2.QtCore import Signal as pyqtSignal
from PySide2.QtCore import Slot as pyqtSlot
from PySide2.QtGui import QColor, QPalette
from PySide2.QtWidgets import (QWidget, QVBoxLayout, QDoubleSpinBox, QLabel)


class EntryWidget(QWidget):
    value_changed_signal = pyqtSignal(tuple)
    def __init__(self, name, value, layout=QVBoxLayout, entry=QDoubleSpinBox,
                 *args, **kwargs):
        # self.value_changed_signal = pyqtSignal(tuple)
        super(EntryWidget, self).__init__(*args, **kwargs)
        self.name = name
        layout = layout()
        self.entry = entry()
        self.entry_type = type(value)
        if entry == QDoubleSpinBox:
            self.entry.setMinimum(-10000.0)
            self.entry.setMaximum(10000.0)
        # self.signal = pyqtSignal(dict)
        layout.addWidget(QLabel(name))
        layout.addWidget(self.entry)
        self.entry.setValue(value)
        self.setLayout(layout)

        self.entry.valueChanged.connect(self.on_entry_value_changed)
        # print('entry parent is: ', self.entry.parent(), self.entry.parentWidget())

    @pyqtSlot()
    def on_entry_value_changed(self, value):
        # print('on_entry_value_changed')
        # print(f'name: {self.name}')
        # mydict = self.parent().data[self.parent().model_name]
        # print(f'parent data: {self.parent().data}')
        # print(f'my dict: {mydict}')
        # assert self.name in mydict
        # mydict[self.name] = value
        # print('new parent data: ', self.parent().data)
        self.value_changed_signal.emit((self.name, value))


class J_EntryWidget(EntryWidget):
    def __init__(self, coords, j_matrix, *args, **kwargs):
        super(J_EntryWidget, self).__init__(*args, **kwargs)
        self.j_matrix = j_matrix
        self.coords = coords


class Color(QWidget):
    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = EntryWidget('Test', 1.1)
    window.show()
    sys.exit(app.exec_())
