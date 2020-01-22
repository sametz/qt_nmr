from PySide2.QtWidgets import QWidget, QHBoxLayout, QStackedWidget
from PySide2.QtCore import Signal as pyqtSignal

from qt_nmr.view.widgets.entry import EntryWidget


class BaseToolbar(QWidget):
    def __init__(self, mainwindow, params, *args, **kwargs):
        super(BaseToolbar, self).__init__(*args, **kwargs)
        self.mainwindow = mainwindow
        self.params = params
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.add_widgets()

    def add_widgets(self):
        widgets = [EntryWidget(key, val) for key, val in self.params.items()]
        for widget in widgets:
            self.layout().addWidget(widget)

    def reset(self, setting):
        pass


def toolbar_stack(mainwindow, settings):
    stack_toolbars = QStackedWidget()
    stack_toolbars.setObjectName('toolbar_stack')
    for model, params in settings['multiplet'].items():
        toolbar = BaseToolbar(mainwindow, params)
        toolbar.setObjectName(f'multiplet_{model}_toolbar')
        stack_toolbars.addWidget(toolbar)
        mainwindow.toolbars[f'multiplet_{model}'] = toolbar
    stack_toolbars.setCurrentWidget(mainwindow.toolbars['multiplet_AB'])
    return stack_toolbars


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)
    params = {'Jab': 12.0, 'Vab': 15.0, 'Vcentr': 150.0}
    toolbar = BaseToolbar(None, params)
    window = QMainWindow()
    window.setCentralWidget(toolbar)
    window.show()
    sys.exit(app.exec_())
