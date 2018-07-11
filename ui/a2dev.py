'''
Created on 11.07.2018

@author: eric
'''
from a2widget.a2input_dialog import A2ConfirmDialog
from PySide2 import QtWidgets, QtCore


class RollbackDiffDialog(A2ConfirmDialog):
    diff = QtCore.Signal()

    def __init__(self, parent, title, msg):
        super(RollbackDiffDialog, self).__init__(parent, title, msg)

        self.ui.diff_button = QtWidgets.QPushButton('Diff', self)
        self.ui.diff_button.setObjectName("a2ok_button")
        self.ui.horizontalLayout.insertWidget(1, self.ui.diff_button)
        self.ui.diff_button.clicked.connect(self.diff.emit)
