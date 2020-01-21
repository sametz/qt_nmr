from pyqtgraph import PlotWidget
from PySide2.QtCore import Slot as pyqtSlot
from PySide2.QtWidgets import (QMainWindow, QHBoxLayout, QLabel,
                               QDoubleSpinBox, QVBoxLayout, QWidget)

class UiMainWindow:
    def setupUi(self, main_window):
        main_window.setObjectName('main_window')
        main_window.setWindowTitle('qt_mvc Demo')
        main_window.resize(800, 600)

        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName('centralwidget')
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setObjectName('centrallayout')
        self.top_bar_layout = QHBoxLayout()
        self.top_bar_layout.setObjectName('top_barlayout')
        self.base_label = QLabel('Base: ')
        self.base_entry = QDoubleSpinBox()
        self.base_entry.setObjectName('base_entry')
        self.exp_label = QLabel('Exponent: ')
        self.exp_entry = QDoubleSpinBox()
        self.exp_entry.setObjectName('exp_entry')
        self.base_entry.setValue(1)
        self.base_entry.setMinimum(0.1)
        self.exp_entry = QDoubleSpinBox()
        self.exp_entry.setValue(2)
        for widget in [self.base_label, self.base_entry,
                       self.exp_label, self.exp_entry]:
            self.top_bar_layout.addWidget(widget)
        self.central_layout.addLayout(self.top_bar_layout)
        self.plot = PlotWidget()
        self.central_layout.addWidget(self.plot)

        main_window.setCentralWidget(self.central_widget)