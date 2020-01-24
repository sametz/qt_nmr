import sys

from PySide2.QtCore import Slot as pyqtSlot
from PySide2.QtWidgets import QMainWindow, QRadioButton, QButtonGroup

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
        button_bars = {
            'AB_button': 'multiplet_AB',
            'AB2_button': 'multiplet_AB2',
            'ABX_button': 'multiplet_ABX',
            'ABX3_button': 'multiplet_ABX3',
            'AAXX_button': 'multiplet_AAXX',
            '1stOrd_button': 'multiplet_1stOrd',  # not implemented yet
            'AABB_button': 'multiplet_AABB'
        }
        print('toolbar dump ', self.toolbars)
        self._ui.toolbars.setCurrentWidget(self.toolbars[button_bars[name]])

    def update(self, calctype, model):
        # print(f'old view state: {self.view_state}')
        # self.view_state[calctype][model] = data[model]
        # print(f'new view state: {self.view_state}')
        print(f'data to send to controller: '
              f'{model}, {self.view_state[calctype][model]}')
        self.controller.update_model(calctype, model,
                                     self.view_state[calctype][model])


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
