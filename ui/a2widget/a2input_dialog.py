"""
a2widget.a2input_dialog

@created: Sep 3, 2016
@author: eRiC
"""
from PySide import QtGui, QtCore

import a2ctrl
from a2widget import a2input_dialog_ui


class A2InputDialog(QtGui.QDialog):
    okayed = QtCore.Signal(str)
    canceled = QtCore.Signal()

    def __init__(self, parent, title, ok_func=None, check_func=None,
                 text='', msg='', size=None, *args):
        super(A2InputDialog, self).__init__(parent)
        a2ctrl.check_ui_module(a2input_dialog_ui)
        self.ui = a2input_dialog_ui.Ui_A2InputDialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.ok_func = ok_func
        self.check_func = check_func
        self.setWindowTitle(title)
        self.output = None

        if self.check_func is not None:
            self.ui.textField.textChanged.connect(self.check)

        self.ui.a2ok_button.clicked.connect(self.okay)
        self.ui.a2cancel_button.clicked.connect(self.cancel_button_click)
        self.ui.label.setText(msg)

        self._text = text
        self.ui.textField.setText(self._text)
        self.ui.textField.setFocus()

        self.rejected.connect(self.canceled.emit)
        self.show()

    @property
    def text(self):
        return self._text

    def check(self, text=None):
        if text is None:
            text = self.ui.textField.text()

        self._text = text

        if self.check_func is not None:
            answer = self.check_func(text)
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
        if self.ok_func is not None:
            self.ok_func(txt)
        self.okayed.emit(txt)

    def cancel_button_click(self):
        self.close()
        self.canceled.emit()
