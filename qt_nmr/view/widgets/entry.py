from PySide2.QtWidgets import QWidget, QVBoxLayout, QDoubleSpinBox, QLabel


class EntryWidget(QWidget):
    def __init__(self, title, value, layout=QVBoxLayout, entry=QDoubleSpinBox,
                 *args, **kwargs):
        layout = layout()
        self.entry = entry()
        super(EntryWidget, self).__init__(*args, **kwargs)
        layout.addWidget(QLabel(title))
        layout.addWidget(self.entry)
        self.entry.setValue(value)
        self.setLayout(layout)
        # print('entry parent is: ', self.entry.parent(), self.entry.parentWidget())


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = EntryWidget('Test', 1.1)
    window.show()
    sys.exit(app.exec_())
