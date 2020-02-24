import numpy as np
import pytest
# from pytestqt import qtbot
from PySide2 import QtCore

from qt_nmr.controller.controller import Controller
from qt_nmr.model.model import Model
from tests.accepted_data.utils import load_lineshape



# class App(QApplication):
#     def __init__(self, sys_argv):
#         super(App, self).__init__(sys_argv)
#         self.model = Model()
#         self.main_controller = Controller(self.model)
#         self.main_view = self.main_controller.view
#         self.main_view.show()
# @pytest.fixture(scope='class')
# def app():
#     model = Model()
#     controller = Controller(model)
#     view = controller.view
#     yield model, controller, view
#
#
# @pytest.mark.usefixtures("app")
# class TestFixture:
#     def test_fixture(self):
#         print(model, controller, view)
#         assert 1 == 1


class TestApp:
    def mvc(self):
        model = Model()
        controller = Controller(model)
        view = controller.view
        return model, view, controller

    def test_instantiation(self, qtbot):
        # model = Model()
        # controller = Controller(model)
        # view = controller.view
        model, view, controller = self.mvc()
        view.show()
        qtbot.addWidget(view)
        dataitem = view._ui.plot.listDataItems()[0]
        view_data = dataitem.getData()
        expected_data = load_lineshape('multiplet_AB.json')
        np.testing.assert_array_almost_equal(view_data, expected_data)

    def test_nspins(self, qtbot):
        model, view, controller = self.mvc()
        view.show()
        qtbot.addWidget(view)
        abc_button = view._ui.calctype.abc_button
        assert abc_button
        qtbot.mouseClick(abc_button, QtCore.Qt.LeftButton)
        dataitem = view._ui.plot.listDataItems()[0]
        view_data = dataitem.getData()
        expected_data = load_lineshape('nspin_2.json')
        np.testing.assert_array_almost_equal(view_data, expected_data)



# def test_basic_search(qtbot, tmpdir):
#     """
#     test to ensure basic find files functionality is working.
#     """
#     tmpdir.join('video1.avi').ensure()
#     tmpdir.join('video1.srt').ensure()
#
#     tmpdir.join('video2.avi').ensure()
#     tmpdir.join('video2.srt').ensure()
#     window = Window()
#     window.show()
#     qtbot.addWidget(window)
#     window.fileComboBox.clear()
#     qtbot.keyClicks(window.fileComboBox, '*.avi')
#
#     window.directoryComboBox.clear()
#     qtbot.keyClicks(window.directoryComboBox, str(tmpdir))
#     qtbot.mouseClick(window.findButton, QtCore.Qt.LeftButton)
#     assert window.filesTable.rowCount() == 2
#     assert window.filesTable.item(0, 0).text() == 'video1.avi'
#     assert window.filesTable.item(1, 0).text() == 'video2.avi'
