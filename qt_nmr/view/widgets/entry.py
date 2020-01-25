from PySide2.QtCore import Signal as pyqtSignal
from PySide2.QtCore import Slot as pyqtSlot
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


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = EntryWidget('Test', 1.1)
    window.show()
    sys.exit(app.exec_())
