"""
a2widget.a2item_editor

@created: Sep 26, 2016
@author: eRiC
"""
import a2ctrl
from PySide import QtGui
from a2widget import a2item_editor_ui


class A2ItemEditor(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(A2ItemEditor, self).__init__(*args, **kwargs)
        a2ctrl.check_ui_module(a2item_editor_ui)
        self.ui = a2item_editor_ui.Ui_A2ItemEditor()
        self.ui.setupUi(self)
