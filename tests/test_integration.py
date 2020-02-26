import time

import numpy as np
import pytest
# from pytestqt import qtbot
from PySide2 import QtCore

from qt_nmr.controller.controller import Controller
from qt_nmr.model.model import Model
from tests.accepted_data.utils import load_lineshape

# There's a lot of repetition in the test code, but trying to reduce repetition
# by e.g. using pytest fixtures runs into problems with trying to create
# more than one Singleton.

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


def view_buttons(view):
    buttons = {
        'calctype': {
            'multiplet': view._ui.calctype.multiplet_button,
            'abc': view._ui.calctype.abc_button,
            'dnmr': view._ui.calctype.dnmr_button
        },
        'multiplet': {
            'AB': view._ui.multiplet_menu.AB_button,
            'AB2': view._ui.multiplet_menu.AB2_button,
            'ABX': view._ui.multiplet_menu.ABX_button,
            'ABX3': view._ui.multiplet_menu.ABX3_button,
            'AAXX': view._ui.multiplet_menu.AAXX_button,
            '1stOrd': view._ui.multiplet_menu.firstorder_button,
            'AABB': view._ui.multiplet_menu.AABB_button
        },
        'nspin': view._ui.abc_menu.buttons,
        'dnmr': {
            'dnmr_two_singlets': view._ui.dnmr_menu.dnmr_twospin_button,
            'dnmr_ab': view._ui.dnmr_menu.dnmr_ab_button
        }
    }
    return buttons


def view_lineshape(view):
    return view._ui.plot.listDataItems()[0].getData()


class TestApp:
    def mvc(self):
        model = Model()
        controller = Controller(model)
        view = controller.view
        view.show()
        return model, view, controller

    def test_instantiation(self, qtbot):
        # model = Model()
        # controller = Controller(model)
        # view = controller.view
        model, view, controller = self.mvc()
        # view.show()
        qtbot.addWidget(view)
        dataitem = view._ui.plot.listDataItems()[0]
        view_data = dataitem.getData()
        expected_data = load_lineshape('multiplet_AB.json')
        np.testing.assert_array_almost_equal(view_data, expected_data)

    def test_nspins(self, qtbot):
        model, view, controller = self.mvc()
        # view.show()
        qtbot.addWidget(view)
        abc_button = view._ui.calctype.abc_button
        assert abc_button
        qtbot.mouseClick(abc_button, QtCore.Qt.LeftButton)
        dataitem = view._ui.plot.listDataItems()[0]
        view_data = dataitem.getData()
        expected_data = load_lineshape('nspin_2.json')
        np.testing.assert_array_almost_equal(view_data, expected_data)

    def test_stack_widget(self, qtbot):
        model, view, controller = self.mvc()
        qtbot.addWidget(view)
        buttons = view_buttons(view)
        model_selections = {
            'multiplet': view._ui.multiplet_menu,
            'abc': view._ui.abc_menu,
            'dnmr': view._ui.dnmr_menu
        }
        for calctype in ['abc', 'dnmr', 'multiplet']:
            qtbot.mouseClick(buttons['calctype'][calctype],
                             QtCore.Qt.LeftButton)
            stackedwidget = view._ui.stack_model_selections
            assert stackedwidget.currentWidget() is model_selections[calctype]

    def test_all_multiplets(self, qtbot):
        model, view, controller = self.mvc()
        qtbot.addWidget(view)
        buttons = view_buttons(view)
        for model, button in buttons['multiplet'].items():
            # qtbot.wait(1000)
            # time.sleep(1)
            qtbot.mouseClick(button, QtCore.Qt.LeftButton)
            filename = f'multiplet_{model}.json'
            dataitem = view._ui.plot.listDataItems()[0]
            view_data = dataitem.getData()
            expected_data = load_lineshape(filename)
            np.testing.assert_array_almost_equal(view_data, expected_data)

    def test_all_dnmr(self, qtbot):
        model, view, controller = self.mvc()
        qtbot.addWidget(view)
        buttons = view_buttons(view)
        qtbot.mouseClick(buttons['calctype']['dnmr'], QtCore.Qt.LeftButton)
        for model, button in buttons['dnmr'].items():
            qtbot.mouseClick(button, QtCore.Qt.LeftButton)
            filename = f'dnmr_{model}.json'
            # dataitem = view._ui.plot.listDataItems()[0]
            # view_data = dataitem.getData()
            view_data = view_lineshape(view)
            expected_data = load_lineshape(filename)
            np.testing.assert_array_almost_equal(view_data, expected_data)

    def test_all_nspin(self, qtbot):
        # currently not working. For some reason, qtbot clicking the nspin
        # buttons isn't working.
        model, view, controller = self.mvc()
        qtbot.addWidget(view)
        buttons = view_buttons(view)
        qtbot.mouseClick(buttons['calctype']['abc'], QtCore.Qt.LeftButton)
        np.testing.assert_array_almost_equal(view_lineshape(view),
                                             load_lineshape('nspin_2.json'))
        for number, button in buttons['nspin'].items():
            print(number, button)
            qtbot.mouseClick(button, QtCore.Qt.LeftButton)
            # qtbot.wait(1000)
            # time.sleep(1)
        # n3button = buttons['nspin']['3']
        n3button = view._ui.abc_menu.buttons['3']
        assert n3button.objectName() == 'nuclei_button3'
        qtbot.mouseClick(n3button, QtCore.Qt.LeftButton)
        qtbot.wait(1000)
        time.sleep(1)
        current_nbutton = view._ui.stack_model_selections.currentWidget().buttongroup.checkedButton()
        print('current nbutton: ', current_nbutton.objectName())

        print('current toolbar: ', view._ui.toolbars.currentWidget().objectName())
        np.testing.assert_array_almost_equal(view_lineshape(view),
                                             load_lineshape('nspin_3.json'))
        #
        # dataitem = view._ui.plot.listDataItems()[0]
        # view_data = dataitem.getData()
        # expected_data = load_lineshape('nspin_3.json')
        # qtbot.wait(1000)
        # time.sleep(1)
        # np.testing.assert_array_almost_equal(view_data, expected_data)


    def test_nspin_entries(self, qtbot):
        # Started to write test, but nspin button clicks not working
        # spun off as test_all_nspin to find problem
        model, view, controller = self.mvc()
        qtbot.addWidget(view)
        buttons = view_buttons(view)
        qtbot.wait(1000)
        time.sleep(1)
        qtbot.mouseClick(buttons['calctype']['abc'], QtCore.Qt.LeftButton)
        qtbot.wait(1000)
        time.sleep(1)
        n3button = buttons['nspin']['3']
        assert n3button.objectName() == 'nuclei_button3'
        qtbot.mouseClick(n3button, QtCore.Qt.LeftButton)

        dataitem = view._ui.plot.listDataItems()[0]
        view_data = dataitem.getData()
        expected_data = load_lineshape('nspin_3.json')
        qtbot.wait(1000)
        time.sleep(1)
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
