# import json
# import os
# from pathlib import Path

import numpy as np
import pytest

from qt_nmr.controller.controller import Controller
from qt_nmr.model.model import Model
# from qt_nmr.view.settings import view_defaults
from tests.accepted_data.utils import load_lineshape


# def model_args(calctype, model, params):
#     if calctype == 'nspin':
#         return params
#     else:
#         return view_to_model(model, params)

#
# def read_json(filename):
#     data_dir = os.path.join(os.path.dirname(__file__), 'accepted_data')
#     file_path = Path(data_dir, filename)
#     with file_path.open('r') as f:
#         data = json.load(f)
#         return data


# @pytest.fixture()
# def test_controller():
#     model = Model()
#     controller = Controller(model)
#     return controller
#
#
# def test_smoke(test_controller):
#     assert 1 == 1
#
#
# class TestConroller:
#     def get_view_plotdata(self, controller):
#         dataitem = controller.view._ui.plot.listDataItems()[0]
#         data = dataitem.getData()
#         return data
#
#     def test_instantiation(self, test_controller):
#         # view_data = self.get_view_plotdata(test_controller)
#         dataitem = test_controller.view._ui.plot.listDataItems()[0]
#         view_data = dataitem.getData()
#         expected_data = load_lineshape('multiplet_AB.json')
#         np.testing.assert_array_almost_equal(view_data, expected_data)

    # def test_multiplet(self, test_controller):
    #     args = model_args('multiplet', 'AB', view_defaults['multiplet']['AB'])
    #     # print(args)
    #     x, y = test_model.update('multiplet', 'AB', *args)
    #     test_data = [list(x), list(y)]
    #     expected_data = read_json('multiplet_AB.json')
    #     print(test_data)
    #     print(expected_data)
    #     np.testing.assert_array_almost_equal(test_data, expected_data)
    #
    # def test_all(self, test_model):
    #     for calctype, model_dict in view_defaults.items():
    #         for model, params in model_dict.items():
    #             args = model_args(calctype, model, params)
    #             x, y = test_model.update(calctype, model, *args)
    #             test_data = [list(x), list(y)]
    #             expected_datafile = f'{calctype}_{str(model)}.json'
    #             expected_data = read_json(expected_datafile)
    #             np.testing.assert_array_almost_equal(test_data, expected_data)
    #
    # def test_bad_modelname(self, test_model):
    #     args = model_args('multiplet', 'AB', view_defaults['multiplet']['AB'])
    #     response = test_model.update('maltypet', 'AB', *args)
    #     assert response == 'maltypet'
