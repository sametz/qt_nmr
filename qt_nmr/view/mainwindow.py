import sys

from PySide2.QtCore import Slot as pyqtSlot
from PySide2.QtWidgets import QMainWindow, QRadioButton, QButtonGroup, QWidget

from qt_nmr.view.settings import view_defaults
from qt_nmr.view.ui import UiMainWindow


class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.view_state = view_defaults
        self.toolbars = {}
        self._ui = UiMainWindow()
        self._ui.setupUi(self)
        self.connect_widgets()
        print(f'after mainwindow init, toolbars = {self.toolbars}')

    def connect_widgets(self):
        # multiplet_button = self.findChild(QRadioButton, 'multiplet_button')
        # abc_button = self.findChild(QRadioButton, 'abc_button')
        # dnmr_button = self.findChild(QRadioButton, 'dnmr_button')
        #
        # calctype_buttongroup = self.findChild(QButtonGroup, 'calctype_buttongroup')
        # print('found buttongroup ', calctype_buttongroup)
        self._ui.calctype.buttongroup.buttonClicked.connect(
            self.select_calctype)
        self._ui.multiplet_menu.buttongroup.buttonClicked.connect(
            self.select_toolbar)
        self._ui.abc_menu.buttongroup.buttonClicked.connect(
            self.select_toolbar)
        self._ui.dnmr_menu.buttongroup.buttonClicked.connect(
            self.select_toolbar)
        self._ui.stack_model_selections.currentChanged.connect(
            self.refresh_toolbar
            # self.select_toolbar(self._ui.stack_model_selections.b)
        )
        self._ui.toolbars.currentChanged.connect(self.on_toolbar_change)

    @pyqtSlot()
    def refresh_toolbar(self):
        print(f'refresh_toolbar called')
        current_modelframe = self._ui.stack_model_selections.currentWidget()
        current_modelbutton = current_modelframe.buttongroup.checkedButton()
        self.select_toolbar(current_modelbutton)
        # self._ui.calctype.buttongroup.buttonClicked(abc_button).connect(
        #     self.select_abc_menu)
        # self._ui.calctype.buttongroup.buttonClicked(dnmr_button).connect(
        #     self.select_dnmr_menu)
        # calctype_buttongroup.buttonClicked(multiplet_button).connect(
        #     self.select_multiplet_menu)
        # calctype_buttongroup.buttonClicked(abc_button).connect(
        #     self.select_abc_menu)
        # calctype_buttongroup.buttonClicked(dnmr_button).connect(
        #     self.select_dnmr_menu)

    @pyqtSlot(QRadioButton)
    def select_calctype(self, button):
        print('select_calctype called')
        name = button.objectName()
        options = {'multiplet_button': self.select_multiplet_menu,
                   'abc_button': self.select_abc_menu,
                   'dnmr_button': self.select_dnmr_menu}
        if not name in options:
            print('ERROR button name mismatch')
        else:
            options[name]()

    def select_multiplet_menu(self):
        print('multiplet menu selected')
        self._ui.stack_model_selections.setCurrentWidget(self._ui.multiplet_menu)

    def select_abc_menu(self):
        print('ABC... menu selected')
        self._ui.stack_model_selections.setCurrentWidget(self._ui.abc_menu)

    def select_dnmr_menu(self):
        print('DNMR menu selected')
        self._ui.stack_model_selections.setCurrentWidget(self._ui.dnmr_menu)

    @pyqtSlot(QRadioButton)
    def select_toolbar(self, button):
        name = button.objectName()
        print(f'current model button is {name}')
        button_bars = {
            'AB_button': 'multiplet_AB',
            'AB2_button': 'multiplet_AB2',
            'ABX_button': 'multiplet_ABX',
            'ABX3_button': 'multiplet_ABX3',
            'AAXX_button': 'multiplet_AAXX',
            '1stOrd_button': 'multiplet_1stOrd',
            'AABB_button': 'multiplet_AABB',
            'nuclei_button2': 'nuclei_bar2',
            'nuclei_button3': 'nuclei_bar3',
            'nuclei_button4': 'nuclei_bar4',
            'nuclei_button5': 'nuclei_bar5',
            'nuclei_button6': 'nuclei_bar6',
            'nuclei_button7': 'nuclei_bar7',
            'nuclei_button8': 'nuclei_bar8',
            'dnmr_twospin_button': 'dnmr_two_singlets',
            'dnmr_ab_button': 'dnmr_ab'
        }
        print('toolbar dump ', self.toolbars)
        print(f'button {name} corresponds to toolbar {button_bars[name]}')
        print(f'which is {self.toolbars[button_bars[name]]}')
        self._ui.toolbars.setCurrentWidget(self.toolbars[button_bars[name]])
        print(f'the active bar is now {self._ui.toolbars.currentWidget()}')

    @pyqtSlot()
    def on_toolbar_change(self):
        current_toolbar = self._ui.toolbars.currentWidget()
        current_toolbar.request_update()

    def update(self, calctype, model):
        # print(f'old view state: {self.view_state}')
        # self.view_state[calctype][model_name] = data[model_name]
        # print(f'new view state: {self.view_state}')
        # print('multiplet contents: ')
        # self._dump_calctype(calctype)
        print(f'data to send to controller for {calctype} {model}: ')
        print(f'{self.view_state[calctype][model]}')
        if calctype == 'nspin':
            print(f'view update will send:')
            print(self.view_state[calctype][model])
        self.controller.update_model(calctype, model,
                                     self.view_state[calctype][model])

    def plot(self, x, y):
        self._ui.plot.clearPlots()
        print(f'mainwindow plot received {x[:10], y[:10]}')
        self._ui.plot.plot(x, y, pen='b')

    # def _dump_calctype(self, calctype):
    #     """temp method for debugging."""
    #     for model, params in self.view_state[calctype].items():
    #         print(model)
    #         print([key for key in params])
    #         print([val for val in params.values()])




if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
