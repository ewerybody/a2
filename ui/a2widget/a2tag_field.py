from PySide import QtCore, QtGui

import a2ctrl
from a2widget.flowlayout import FlowLayout


class A2TagField(QtGui.QWidget):
    changed = QtCore.Signal(list)

    def __init__(self, parent=None):
        super(A2TagField, self).__init__(parent=parent)
        self.main_layout = FlowLayout(self)

        self.plus_button = QtGui.QToolButton()
        #self.plus_button.setIcon(a2ctrl.Icons().)
        self.plus_button.setText('+')
        self.main_layout.addWidget(self.plus_button)


if __name__ == '__main__':
    pass
