"""
a2ctrl.path_field

@created: Jun 19, 2016
@author: eRiC
"""
from PySide import QtGui, QtCore
from functools import partial


class BrowseType(object):
    file = 0
    folder = 1


class PathField(QtGui.QWidget):
    textChanged = QtCore.Signal(str)
    editingFinished = QtCore.Signal(str)

    def __init__(self, parent):
        super(PathField, self).__init__(parent)
        self.main_layout = QtGui.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.line_field = QtGui.QLineEdit(self)
        self.line_field.textChanged.connect(self.textChanged.emit)
        self.main_layout.addWidget(self.line_field)
        self.browse_button = QtGui.QPushButton('Browse...', self)
        self.browse_button.clicked.connect(self.browse)
        self.main_layout.addWidget(self.browse_button)
        self._value = ''

        self.save_mode = False
        self.writable = False
        self.browse_type = BrowseType.file
        self.label_text = None

        self.text = self.line_field.text
        self.setText = self.line_field.setText
        self.setReadOnly = self.line_field.setReadOnly

    def set_writable(self, state):
        if state == self.writable:
            return
        self.writable = state
        if state:
            self.line_field.editingFinsished.connect(self.editingFinished.emit)
        else:
            self.line_field.editingFinsished.disconnect(self.editingFinished.emit)

    def browse(self):
        if self.browse_type == BrowseType.file:
            if self.save_mode:
                filepath = QtGui.QFileDialog.getSaveFileName(self, caption=self.label_text, dir=self._value)
            else:
                filepath = QtGui.QFileDialog.getOpenFileName(self, caption=self.label_text, dir=self._value)

        else:
            filepath = QtGui.QFileDialog.getExistingDirectory(self, caption=self.label_text, dir=self._value)
        print('filepath: %s' % str(filepath))

        if filepath[0]:
            self.line_field.setText(filepath[0])
