import numpy as np
from PySide2.QtCore import QObject
from PySide2.QtCore import Signal as pyqtSignal
from nmrsim.discrete import AB, AB2, ABX, ABX3, AAXX, AABB


class Model(QObject):
    """Responsible for holding and managing the data/state of the simulation."""
    # value_changed = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.functions = {
            'AB': AB,
            'AB2': AB2,
            'ABX': ABX,
            'ABX3': ABX3,
            'AAXX': AAXX,
            'AABB': AABB
        }

    def update(self, calctype, model, kwargs):
        # model, params = request.items()
        # assert model not in self.data:
        print(f'model received {calctype} {model} {kwargs}')
        print(self.functions[model](*kwargs))


    def _update_y(self):
        self._y = (self._x * self._base) ** self._exp

    # @property
    # def x(self):
    #     return self._x
    #
    # @property
    # def y(self):
    #     return self._y
    #
    # def update(self):
    #     # self._base = base
    #     # self._exp = exp
    #     self._update_y()
    #
    # @property
    # def base(self):
    #     return self._base
    #
    # @base.setter
    # def base(self, value):
    #     self._base = value
    #     self.update()
    #     self.value_changed.emit((self._x, self._y))
    #
    # @property
    # def exp(self):
    #     return self._exp
    #
    # @exp.setter
    # def exp(self, value):
    #     self._exp = value
    #     self.update()
    #     self.value_changed.emit((self._x, self._y))
