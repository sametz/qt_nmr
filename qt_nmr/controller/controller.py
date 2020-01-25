from nmrsim.discrete import AB, AB2, ABX, ABX3, AAXX, AABB
from PySide2.QtCore import QObject
from PySide2.QtCore import Slot as pyqtSlot

from qt_nmr.controller.adapter import view_to_model
from qt_nmr.view.mainwindow import MainWindow


class Controller(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model
        self.view = MainWindow(self)

    def update_model(self, calctype, model_name, kwargs):
        print(f' controller received {calctype} {model_name} {kwargs}')
        args = view_to_model(model_name, kwargs)
        print(f' controller will send to model {args}')
        x, y = self._model.update(model_name, *args)
        self.view.plot(x, y)


    @pyqtSlot(float)
    def change_base(self, value):
        self._model.base = value

    @pyqtSlot(float)
    def change_exp(self, value):
        self._model.exp = value