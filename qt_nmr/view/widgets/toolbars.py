from PySide2.QtWidgets import (QWidget, QHBoxLayout, QStackedWidget, QSpinBox,
                               QPushButton, QDialog, QGridLayout, QLabel,
                               QVBoxLayout)
from PySide2.QtCore import Signal as pyqtSignal
from PySide2.QtCore import Slot as pyqtSlot
from PySide2.QtGui import QColor, QPalette
from qt_nmr.view.widgets.entry import (EntryWidget, V_EntryWidget,
                                       J_EntryWidget, Color)


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
        self._add_popup()
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
        self.v_widgets = []
        for i in range(self.n):
            name = 'V' + str(i + 1)
            value = self.v[i]
            widget = V_EntryWidget(name=name,
                                   value=value,
                                   index = i,
                                   v_array = self.v)  # TODO remove redundancy
            # widgets.append(widget))
            widget.value_changed_signal.connect(self.on_v_toolbar_change)
            self.layout().addWidget(widget)
            self.v_widgets.append(widget)

    def _add_peakwidth_widget(self):
        pass

    def _add_J_button(self):
        j_button = QPushButton('Enter Js')
        self.layout().addWidget(j_button)
        j_button.clicked.connect(self.on_jbutton_clicked)

    def _add_popup(self):
        print(f'creating a popup for {self.n}')
        self.popup = J_Popup(self)


    @pyqtSlot()
    def on_jbutton_clicked(self):
        print('j button clicked')
        self.popup.show()

    @pyqtSlot(tuple)
    def on_v_toolbar_change(self, data):
        index, value = data
        print(f'on_v_toolbar_change received {index, value}')
        self.v[index] = value  # TODO: remove redundancy with on_v_popup_change
        print(f'self.v is now {self.v}')
        self.popup.reset()  # TODO: make sure popup v update doesn't trigger
                            # multiple calls
        self.request_update()

    @pyqtSlot(tuple)
    def on_v_popup_change(self, data):
        index, value = data
        print(f'index {index} {type(index)}')
        print(f'value {value} {type(value)}')
        # self.v[index] = value
        toolbar_widget = self.v_widgets[index]
        toolbar_widget.entry.setValue(value)
        # self.request_update()

        # i = int(name[-1]) - 1
        # # print(f'change request: name {name}, value {value}')
        # # print(f'before change: toolbar data {self.data}')
        # # print(f'before change: mainwindow state {self.mainwindow.view_state}')
        # self.v[i] = value
        # # self._set_data()
        # # self._set_state()
        # print(f'after change: {self.v}')
        # print(f'after change: mainwindow state {self.mainwindow.view_state}')
        # self.request_update()

    @pyqtSlot(tuple)
    def on_j_change(self, data):
        coords, value = data
        i, j = coords
        print('j {coord} changed to {value}')
        self.j[i, j] = value
        self.j[j, i] = value
        self.request_update()

    def request_update(self):
        self.mainwindow.update('nspin', self.n)

    def reset(self):
        for i, widget in enumerate(self.v_widgets):
            self.v[i] = widget.value()
        self.request_update()


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


class J_Popup(QDialog):

    def __init__(self, caller, parent=None):
        super(J_Popup, self).__init__(parent)
        self.caller = caller
        self.setObjectName('j_popup' + str(caller.n))
        self.setWindowTitle('Spin ' + str(caller.n))
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('darkGray'))
        self.setPalette(palette)
        layout = QGridLayout()
        print(f'J_Popup construction with {caller.n, caller.v}')
        # Set dialog layout
        layout.addWidget(self.grey())
        self.v_widgets = []
        self.j_widgets = {}
        for col in range(1, caller.n + 1):
            label = QLabel(f'V{col}')
            labelbox = self.add_background(label)
            layout.addWidget(labelbox, 0, col)
        for row in range(1, caller.n + 1):
            entry = V_EntryWidget(name=f'V{row}',
                                  value=caller.v[row - 1],
                                  index = row - 1,
                                  v_array = caller.v  # TODO remove redundancy
                                  )
            self.v_widgets.append(entry)

                                  # v_array caller.v[row - 1])
            entry.value_changed_signal.connect(caller.on_v_popup_change)
            entrybox = self.add_background(entry)
            layout.addWidget(entrybox, row, 0)
        for col in range(1, caller.n + 1):
            self.j_widgets[col - 1] = {}
            for row in range(1, caller.n + 1):
            # for col in range(1, caller.n):
            #     self.j_widgets[col - 1] = {}
                if col < row:
                    j_entry = J_EntryWidget(name=f'J{col}{row}',
                                            value=caller.j[col - 1, row - 1],
                                            coords=(col - 1, row - 1),
                                            j_matrix=caller.j
                                            )
                    self.j_widgets[col - 1][row - 1] = j_entry
                    j_entry.value_changed_signal.connect(caller.on_j_change)
                                 # controller=self.request_plot)
                    j_entrybox = self.add_background(j_entry)
                    layout.addWidget(j_entrybox, row, col)
                else:
                    layout.addWidget(self.grey(), row, col)
                # else:
                #     Label(datagrid, bg='grey').grid(
                #         row=row, column=col, sticky=NSEW, padx=1, pady=1)
        self.setLayout(layout)

    def reset(self):
        print(f'j dump for spin {self.caller.n}:')
        print(f'{self.j_widgets}')
        for i, widget in enumerate(self.v_widgets):
            widget.entry.setValue(self.caller.v[i])
        for i in range(0, self.caller.n):
            for j in range(1, self.caller.n):
                if i < j:
                    print(f'i {i} j {j}')
                    print(f'matrix {self.j_widgets}')
                    print(f'found j_widgets[i][j]')
                    self.j_widgets[i][j].entry.setValue(self.caller.j[i, j])

    def grey(self):
        return Color('lightGray')

    def add_background(self, widget, color='lightGray'):
        backing = Color(color)
        layout = QVBoxLayout()
        layout.addWidget(widget)
        backing.setLayout(layout)
        return backing
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
