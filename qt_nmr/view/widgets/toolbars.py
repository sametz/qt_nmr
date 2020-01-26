from PySide2.QtWidgets import QWidget, QHBoxLayout, QStackedWidget, QSpinBox
from PySide2.QtCore import Signal as pyqtSignal
from PySide2.QtCore import Slot as pyqtSlot
from qt_nmr.view.widgets.entry import EntryWidget


class BaseToolbar(QWidget):
    def __init__(self, mainwindow, model, params, *args, **kwargs):
        super(BaseToolbar, self).__init__(*args, **kwargs)
        self.mainwindow = mainwindow
        self.model = model
        self.data = params
        print(f'toolbar model {self.model} has params {self.data}')

        layout = QHBoxLayout()
        self.setLayout(layout)
        self._set_name()
        # self._set_data()
        # self._set_state()
        self._add_widgets()

    def _set_name(self):
        pass

    def _set_data(self):
        pass

    # def _set_state(self):
    #     pass

    def _add_widgets(self):
        pass

    def reset(self, setting):
        pass


class MultipletBar(BaseToolbar):
    def __init__(self, *args, **kwargs):
        super(MultipletBar, self).__init__(*args, **kwargs)
        print(f'{self.objectName()} has data {self.data}')

    def _set_name(self):
        self.setObjectName(f'multiplet_{self.model}_toolbar')

    def _add_widgets(self):
        widgets = [EntryWidget(key, val) for key, val in self.data.items()]
        for widget in widgets:
            self.layout().addWidget(widget)
            widget.value_changed_signal.connect(self.on_value_changed)

    @pyqtSlot(tuple)
    def on_value_changed(self, data):
        name, value = data
        print(f'change request: name {name}, value {value}')
        print(f'before change: toolbar data {self.data}')
        print(f'before change: mainwindow state {self.mainwindow.view_state}')
        self.data[name] = value
        # self._set_data()
        # self._set_state()
        print(f'after change: toolbar data {self.data}')
        print(f'after change: mainwindow state {self.mainwindow.view_state}')
        self.request_update()

    def request_update(self):
        self.mainwindow.update('multiplet', self.model)

    @pyqtSlot(dict)
    def update(self):
        pass


class FirstOrderBar(MultipletBar):
    def __init__(self, *args, **kwargs):
        super(FirstOrderBar, self).__init__(*args, **kwargs)

    def _add_widgets(self):
        widgets = []
        for key, val in self.data.items():
            if '#' in key:
                widgets.append(EntryWidget(key, val, entry=QSpinBox))
                assert widgets[-1].entry_type is int
            else:
                widgets.append(EntryWidget(key, val))
                assert widgets[-1].entry_type is float
        for widget in widgets:
            self.layout().addWidget(widget)
            widget.value_changed_signal.connect(self.on_value_changed)


class DNMR_Bar(MultipletBar):
    def __int__(self, *args, **kwargs):
        """Currently DNMR_Bar is similar enough to MultipletBar that it can
        be a subclass.
        """
        super(MultipletBar, self).__init__(*args, **kwargs)

    def _set_name(self):
        self.setObjectName(f'{self.model}')


def toolbar_stack(mainwindow, settings):
    stack_toolbars = QStackedWidget()
    stack_toolbars.setObjectName('toolbar_stack')
    for model, params in settings['multiplet'].items():
        if model == '1stOrd':
            toolbar = FirstOrderBar(mainwindow, model, params)
        else:
            toolbar = MultipletBar(mainwindow, model, params)
        # toolbar.setObjectName(f'multiplet_{model_name}_toolbar')
        stack_toolbars.addWidget(toolbar)
        mainwindow.toolbars[f'multiplet_{model}'] = toolbar
    for model, params in settings['dnmr'].items():
        toolbar = DNMR_Bar(mainwindow, model, params)
        stack_toolbars.addWidget(toolbar)
        mainwindow.toolbars[toolbar.objectName()] = toolbar
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
