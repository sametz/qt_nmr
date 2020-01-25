from PySide2.QtCore import QObject
from PySide2.QtCore import Slot as pyqtSlot

from qt_nmr.controller.adapter import view_to_model


class Controller(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model

    def update_model(self, calctype, model, kwargs):
        print(f' controller received {calctype} {model} {kwargs}')
        args = view_to_model(model, kwargs)
        print(f' controller will send to model {args}')
        # self._model.update(calctype, model, kwargs)

    @pyqtSlot(float)
    def change_base(self, value):
        self._model.base = value

    @pyqtSlot(float)
    def change_exp(self, value):
        self._model.exp = value