from pyqtgraph import PlotWidget
from PySide2.QtWidgets import (QHBoxLayout, QLabel, QStackedWidget,
                               QVBoxLayout, QWidget)

from qt_nmr.view.widgets.toolbars import toolbar_stack
from qt_nmr.view.widgets.buttons import (
    CalcTypeButtonGroup, ABC_ButtonGroup, MultipletButtonGroup,
    DNMR_ButtonGroup)

class UiMainWindow:
    def setupUi(self, main_window):
        main_window.setObjectName('main_window')
        main_window.setWindowTitle('qt_mvc Demo')
        main_window.resize(800, 600)

        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName('centralwidget')
        self.central_layout = QHBoxLayout(self.central_widget)
        self.central_layout.setObjectName('centrallayout')
        self.left_bar_layout = QVBoxLayout()
        self.left_bar_layout.setObjectName('left_bar_layout')
        self.main_layout = QVBoxLayout()
        self.main_layout.setObjectName('main_layout')
        self.central_layout.addLayout(self.left_bar_layout)
        self.central_layout.addLayout(self.main_layout)

        self.calctype = CalcTypeButtonGroup('Calc Type')
        self.calctype.setObjectName('calctype_menu')
        self.stack_model_selections = QStackedWidget()
        self.stack_model_selections.setObjectName('model_selection_stack')
        self.multiplet_menu = MultipletButtonGroup('Multiplet')
        self.multiplet_menu.setObjectName('multiplet_menu')
        self.abc_menu = ABC_ButtonGroup('Number of Spins')
        self.abc_menu.setObjectName('abc_menu')
        self.dnmr_menu = DNMR_ButtonGroup('DNMR')
        self.dnmr_menu.setObjectName('dnmr_menu')
        for menu in [self.multiplet_menu, self.abc_menu, self.dnmr_menu]:
            self.stack_model_selections.addWidget(menu)
        self.stack_model_selections.setCurrentWidget(self.multiplet_menu)
        self.left_bar_layout.addWidget(self.calctype)
        self.left_bar_layout.addWidget(self.stack_model_selections)

        # self.left_bar_layout.addWidget(self.multiplet_menu)
        # self.left_bar_layout.addWidget(self.abc_menu)
        # self.left_bar_layout.addWidget(self.dnmr_menu)
        # self.left_bar_layout.addLayout(self.calctype_layout)
        # self.left_bar_layout.addLayout(self.multiplet_layout)

        # following will eventually be a stacked widget
        # self.varbar_layout = QHBoxLayout()
        # self.varbar_layout.setObjectName('varbar_layout')

        # self.base_label = QLabel('Base: ')
        # self.base_entry = QDoubleSpinBox()
        # self.base_entry.setObjectName('base_entry')
        # self.exp_label = QLabel('Exponent: ')
        # self.exp_entry = QDoubleSpinBox()
        # self.exp_entry.setObjectName('exp_entry')
        # self.base_entry.setValue(1)
        # self.base_entry.setMinimum(0.1)
        # self.exp_entry = QDoubleSpinBox()
        # self.exp_entry.setValue(2)
        # for widget in [self.base_label, self.base_entry,
        #                self.exp_label, self.exp_entry]:
        #     self.top_bar_layout.addWidget(widget)
        # self.central_layout.addLayout(self.top_bar_layout)
        self.toolbars = toolbar_stack(main_window, main_window.view_state)
        self.plot = PlotWidget()
        self.plot.getViewBox().invertX(True)  # Reverse x axis "NMR style"
        self.main_layout.addWidget(self.toolbars)
        self.main_layout.addWidget(self.plot)

        # self.calctype_layout.addWidget(QLabel('Calc Type'))
        # self.multiplet_layout.addWidget(QLabel('Multiplet'))

        # self.varbar_layout.addWidget(QLabel('Toolbar widgets will go here'))

        main_window.setCentralWidget(self.central_widget)