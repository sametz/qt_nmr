from PySide2.QtWidgets import (QWidget, QHBoxLayout, QStackedWidget, QSpinBox,
                               QPushButton)
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


class SecondOrderBar(BaseToolbar):
    def __init__(self, *args, **kwargs):
        super(SecondOrderBar, self).__init__(*args, **kwargs)
        self.v, self.j = self.data
        print(self.v, self.j)
        self.n = len(self.v)
        print(self.n)
        assert self.n == int(self.model)
        self._add_nspin_widgets()
    #     self.w_array = np.array([[0.5]])
    #
    def _set_name(self):
        self.setObjectName('nuclei_bar' + str(self.model))

    def _add_widgets(self):
        pass  # must initialize widgets after super init

    def _add_nspin_widgets(self):
        self._add_frequency_widgets()
        self._add_peakwidth_widget()
        self._add_J_button()

    def _add_frequency_widgets(self):
        # widgets = []
        for i in range(self.n):
            name = 'V' + str(i + 1)
            value = self.v[i]
            widget = EntryWidget(name, value)
            # widgets.append(widget))
            self.layout().addWidget(widget)
            widget.value_changed_signal.connect(self.on_v_changed)

    def _add_peakwidth_widget(self):
        pass

    def _add_J_button(self):
        j_button = QPushButton('Enter Js')
        self.layout().addWidget(j_button)
        j_button.clicked.connect(self.on_jbutton_clicked)

    @pyqtSlot()
    def on_jbutton_clicked(self):
        print('j button clicked')

    @pyqtSlot(tuple)
    def on_v_changed(self, data):
        name, value = data
        print(f'{name} ends in {int(name[-1])}')
        # WARNING if n ever > 9 this will break
        i = int(name[-1]) - 1
        # print(f'change request: name {name}, value {value}')
        # print(f'before change: toolbar data {self.data}')
        # print(f'before change: mainwindow state {self.mainwindow.view_state}')
        self.v[i] = value
        # self._set_data()
        # self._set_state()
        print(f'after change: {self.v}')
        print(f'after change: mainwindow state {self.mainwindow.view_state}')
        self.request_update()

    def request_update(self):
        self.mainwindow.update('nspin', self.n)
    # def add_frequency_widgets(self, n):
    #     for freq in range(n):
    #         vbox = ArrayBox(self, array=self.v, coord=(0, freq),
    #                         name='V' + str(freq + 1),
    #                         controller=self.request_plot)
    #         vbox.pack(side=LEFT)
    #
    # def add_peakwidth_widget(self):
    #     wbox = ArrayBox(self, array=self.w_array, coord=(0, 0), name="W",
    #                     controller=self.request_plot)
    #     wbox.pack(side=LEFT)
    #
    # def add_J_button(self, n):
    #     vj_button = Button(self, text="Enter Js",
    #                        command=lambda: self.vj_popup(n))
    #     vj_button.pack(side=LEFT, expand=N, fill=NONE)
    #
    # def vj_popup(self, n):
    #     """
    #     Creates a new Toplevel window that provides entries for both
    #     frequencies and J couplings, and updates self.v and self.j when
    #     entries change.
    #     :param n: number of spins
    #     """
    #     tl = Toplevel()
    #     Label(tl, text='Second-Order Simulation').pack(side=TOP)
    #     datagrid = Frame(tl)
    #
    #     # For gridlines, background set to the line color (e.g. 'black')
    #     datagrid.config(background='black')
    #
    #     Label(datagrid, bg='gray90').grid(row=0, column=0, sticky=NSEW,
    #                                       padx=1, pady=1)
    #     for col in range(1, n + 1):
    #         Label(datagrid, text='V%d' % col, width=8, height=3,
    #               bg='gray90').grid(
    #             row=0, column=col, sticky=NSEW, padx=1, pady=1)
    #
    #     for row in range(1, n + 1):
    #         vtext = "V" + str(row)
    #         v = ArrayBox(datagrid, array=self.v,
    #                      coord=(0, row - 1),  # V1 stored in v[0, 0], etc.
    #                      name=vtext, color='gray90',
    #                      controller=self.request_plot)
    #         v.grid(row=row, column=0, sticky=NSEW, padx=1, pady=1)
    #         for col in range(1, n + 1):
    #             if col < row:
    #                 j = ArrayBox(datagrid, array=self.j,
    #                              # J12 stored in j[0, 1] (and j[1, 0]) etc
    #                              coord=(col - 1, row - 1),
    #                              name="J%d%d" % (col, row),
    #                              controller=self.request_plot)
    #                 j.grid(row=row, column=col, sticky=NSEW, padx=1, pady=1)
    #             else:
    #                 Label(datagrid, bg='grey').grid(
    #                     row=row, column=col, sticky=NSEW, padx=1, pady=1)
    #
    #     datagrid.pack()
    #
    # def request_plot(self):
    #     """Adapt 2D array data to kwargs of correct type for the controller."""
    #     kwargs = {'v': self.v[0, :],  # controller takes 1D array of freqs
    #               'j': self.j,
    #               'w': self.w_array[0, 0]}  # controller takes float for w
    #
    #     self.controller.update_view_plot('nspin', **kwargs)


class DNMR_Bar(MultipletBar):
    def __int__(self, *args, **kwargs):
        """Currently DNMR_Bar is similar enough to MultipletBar that it can
        be a subclass.
        """
        super(MultipletBar, self).__init__(*args, **kwargs)

    def _set_name(self):
        self.setObjectName(f'{self.model}')

    def request_update(self):
        self.mainwindow.update('dnmr', self.model)


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

    for spins, params in settings['nspin'].items():
        # model = str(spins)  # need str so BaseToolbar name inits
        toolbar = SecondOrderBar(mainwindow, spins, params)
        stack_toolbars.addWidget(toolbar)
        mainwindow.toolbars[toolbar.objectName()] = toolbar

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
