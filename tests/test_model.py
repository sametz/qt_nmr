import json
import os
from pathlib import Path

import numpy as np
import pytest

from qt_nmr.controller.adapter import view_to_model
from qt_nmr.model.model import Model
from qt_nmr.view.settings import view_defaults


def model_args(calctype, model, params):
    if calctype == 'nspin':
        return params
    else:
        return view_to_model(model, params)


def read_json(filename):
    data_dir = os.path.join(os.path.dirname(__file__), 'accepted_data')
    file_path = Path(data_dir, filename)
    with file_path.open('r') as f:
        data = json.load(f)
        return data


@pytest.fixture()
def test_model():
    model = Model()
    return model


class TestModel:
    def test_multiplet(self, test_model):
        args = model_args('multiplet', 'AB', view_defaults['multiplet']['AB'])
        # print(args)
        x, y = test_model.update('multiplet', 'AB', *args)
        test_data = [list(x), list(y)]
        expected_data = read_json('multiplet_AB.json')
        print(test_data)
        print(expected_data)
        np.testing.assert_array_almost_equal(test_data, expected_data)
