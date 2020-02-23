import numpy as np
from PySide2.QtCore import QObject
from nmrsim.discrete import AB, AB2, ABX, ABX3, AAXX, AABB
from nmrsim.dnmr import dnmr_two_singlets, dnmr_AB
from nmrsim.firstorder import multiplet
from nmrsim.plt import add_lorentzians
from nmrsim.qm import qm_spinsystem


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
            'AABB': AABB,
            '1stOrd': multiplet,
            'dnmr_two_singlets': dnmr_two_singlets,
            'dnmr_ab': dnmr_AB
        }

    def _linspace(self, peaklist, margin=50, resolution=0.1):
        peaklist.sort()
        min_ = peaklist[0][0]
        max_ = peaklist[-1][0]
        # if min_ > max_:
        #     print(f'WARNING min {min_} greater than max {max_}')
        lin_min, lin_max = min_ - margin, max_ + margin
        window = lin_max - lin_min  # Hz
        datapoints = round(window / resolution)
        print(f'making linspace for {min_} {max_} {resolution}')
        return np.linspace(lin_min, lin_max, datapoints)

    def update(self, calctype, model_name, *args):
        print('-'*10)
        print(f'update received calctype {calctype} model {model_name}')
        if calctype == 'multiplet':
            x, y = self.update_multiplet(model_name, *args)
        elif calctype == 'nspin':
            print(f'qm args {args}')
            for arg in args:
                print(arg)
            x, y = self.update_qm(*args)
            print(f'qm x, y {x[:10], y[:10]}')
        elif calctype == 'dnmr':
            x, y = self.functions[model_name](*args)
        else:
            print(f'calctype {calctype} not implemented')
            return(calctype)
        return x, y

    def update_multiplet(self, model_name, *args):
        peaklist = self.functions[model_name](*args)
        return self.peaklist_to_xy(peaklist)

    def update_qm(self, *args):
        peaklist = qm_spinsystem(*args)
        return self.peaklist_to_xy(peaklist)

    def peaklist_to_xy(self, peaklist):
        x = self._linspace(peaklist)
        y = add_lorentzians(x, peaklist, w=0.5)
        return x, y
