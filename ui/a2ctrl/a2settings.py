"""
a2ctrl.a2settings

@created: 29.02.2016
@author: eric
"""
import a2ctrl
import logging
from PySide import QtGui
from a2ctrl import a2settings_ui


class A2Settings(QtGui.QWidget):
    def __init__(self):
        super(A2Settings, self).__init__()
        self.ui = a2settings_ui.Ui_a2settings()
        self.ui.setupUi(self)


if __name__ == '__main__':
    pass
