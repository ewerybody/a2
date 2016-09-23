"""
a2widget.a2input_dialog

@created: Sep 3, 2016
@author: eRiC
"""
from PySide import QtGui

import a2ctrl
from a2widget import a2input_dialog_ui


class A2InputDialog(QtGui.QDialog):
    def __init__(self, parent, title, okFunc=None, checkFunc=None,
                 text='', msg='', size=None, *args):
        super(A2InputDialog, self).__init__(parent)
        a2ctrl.check_ui_module(a2input_dialog_ui)
        self.ui = a2input_dialog_ui.Ui_A2InputDialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.okFunc = okFunc
        self.checkFunc = checkFunc
        self.setWindowTitle(title)
        self.output = None

        if self.checkFunc is not None:
            self.ui.textField.textChanged.connect(self.check)

        self.ui.a2ok_button.clicked.connect(self.okay)
        self.ui.a2cancel_button.clicked.connect(self.close)
        self.ui.label.setText(msg)
        self.ui.textField.setText(text)
        self.ui.textField.setFocus()

        self.show()

    def check(self, name=None):
        if name is None:
            name = self.ui.textField.text()

        if self.checkFunc is not None:
            answer = self.checkFunc(name)
            if answer is True:
                self.ui.a2ok_button.setEnabled(True)
                self.ui.a2ok_button.setText('OK')
            else:
                self.ui.a2ok_button.setEnabled(False)
                self.ui.a2ok_button.setText(answer)

    def okay(self):
        txt = self.ui.textField.text()
        self.output = txt
        self.close()
        if self.okFunc is not None:
            self.okFunc(txt)
