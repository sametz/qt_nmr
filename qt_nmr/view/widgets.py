from PySide2.QtWidgets import (QGroupBox, QRadioButton, QVBoxLayout,
                               QMainWindow, QStackedWidget, QWidget,
                               QGridLayout, QToolBar, QLabel, QButtonGroup)

class CalcTypeButtonGroup(QGroupBox):
    """
    A widget of radio buttons that will determine which QStackedWidget is
    displayed.
    """

    # It seems that in order for the buttonClicked signal to work,
    # self.ButtonGroup and not ButtonGroup is necessary. Does not work
    # with out 'self.' prefix!!!
    def __init__(self, *args, **kwargs):
        super(CalcTypeButtonGroup, self).__init__(*args, **kwargs)
        self.multiplet_button = QRadioButton('Multiplet')
        self.multiplet_button.setObjectName('multiplet_button')
        self.abc_button = QRadioButton('ABC...')
        self.abc_button.setObjectName('abc_button')
        self.dnmr_button = QRadioButton('DNMR')
        self.dnmr_button.setObjectName('dnmr_button')

        self.layout = QVBoxLayout()
        self.buttongroup = QButtonGroup()
        for button in [self.multiplet_button, self.abc_button, self.dnmr_button]:
            self.layout.addWidget(button)
            self.buttongroup.addButton(button)
        # self.layout.addWidget(self.multiplet_button)
        # self.layout.addWidget(self.abc_button)
        # self.layout.addWidget(self.dnmr_button)
        self.setLayout(self.layout)

        self.multiplet_button.setChecked(True)


class ABC_ButtonGroup(QGroupBox):
    def __init__(self, *args, **kwargs):
        super(ABC_ButtonGroup, self).__init__(*args, **kwargs)
        self.buttons = {}
        self.layout = QVBoxLayout()
        self.buttongroup = QButtonGroup()
        for i in range(2, 9):  # 2 to 8 nuclei
            button = QRadioButton(str(i))
            self.buttons[str(i)] = button
            button.setObjectName('nuclei_button' + str(i))
            self.layout.addWidget(button)
            self.buttongroup.addButton(button)
        self.setLayout(self.layout)

        self.buttons['2'].setChecked(True)


class myGui(QMainWindow):

    def __init__(self, *args, **kwargs):

        super(myGui, self).__init__(*args, **kwargs)
        self.setupCentral()
        self.setupButtonToolBar()

    def setupCentral(self):

        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        windowA = QWidget()
        windowALayout = QGridLayout()
        windowALayout.addWidget(QLabel('Window A'))
        windowALayout.addWidget(CalcTypeButtonGroup('Calc Type'))

        windowB = QWidget()
        windowBLayout = QGridLayout()
        windowBLayout.addWidget(QLabel('Window B'))
        windowBLayout.addWidget(ABC_ButtonGroup('Number of Spins'))

        windowA.setLayout(windowALayout)
        windowB.setLayout(windowBLayout)

        self.stackedWidget.addWidget(windowA)
        self.stackedWidget.addWidget(windowB)
        self.stackedWidget.setCurrentIndex(0)

    def setupButtonToolBar(self):

        buttonBar = QToolBar()
        buttonBar.addWidget(self.modelButtonGroup())
        self.addToolBar(buttonBar)

    def modelButtonGroup(self):

        modelsWidget = QWidget()
        modelsLayout = QVBoxLayout()
        self.ButtonGroup = QButtonGroup()

        windowA_Button = QRadioButton('Window A')
        windowA_Button.setChecked(True)
        self.ButtonGroup.addButton(windowA_Button, 0)

        windowB_Button = QRadioButton('Window B')
        self.ButtonGroup.addButton(windowB_Button, 1)

        self.ButtonGroup.buttonClicked[int].connect(self.switchdisplay)

        modelsLayout.addWidget(windowA_Button)
        modelsLayout.addWidget(windowB_Button)
        modelsWidget.setLayout(modelsLayout)

        return modelsWidget

    def switchdisplay(self, id):
        print('button %d has been pressed' % id)
        self.stackedWidget.setCurrentIndex(id)


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = myGui()
    window.show()
    sys.exit(app.exec_())
