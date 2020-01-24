from PySide2.QtCore import QObject
from PySide2.QtCore import Slot as pyqtSlot


class Controller(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model

    def update_model(self, *args, **kwargs):
        print(f' controller received {args} {kwargs}')

    @pyqtSlot(float)
    def change_base(self, value):
        self._model.base = value

    @pyqtSlot(float)
    def change_exp(self, value):
        self._model.exp = value