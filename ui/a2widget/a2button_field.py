"""
Created on 09.03.2017

@author: eric
"""
from PySide import QtGui, QtCore


class A2ButtonField(QtGui.QWidget):
    textChanged = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(A2ButtonField, self).__init__(parent)
        self.main_layout = QtGui.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.menu = QtGui.QMenu()
        self.field = QtGui.QLineEdit(self)
        self.field.textChanged.connect(self.textChanged.emit)
        self.main_layout.addWidget(self.field)
        self.button = QtGui.QToolButton(self)
        self.button.setObjectName('a2option_button')
        self.button.setAutoRaise(True)
        self.button.setArrowType(QtCore.Qt.DownArrow)
        self.button.clicked.connect(self.show_menu)
        self.main_layout.addWidget(self.button)

    def show_menu(self):
        self.menu.popup(QtGui.QCursor.pos())

    def add_action(self, action, index=None):
        """
        Adds a QAction to the menu
        """
        if index is not None:
            self.menu.insertAction(index, action)
        else:
            self.menu.addAction(action)

    def setEnabled(self, *args, **kwargs):
        self.field.setEnabled(*args, **kwargs)

    def setReadOnly(self, *args, **kwargs):
        self.field.setReadOnly(*args, **kwargs)

    def text(self):
        return self.field.text()

    def setText(self, text):
        self.field.setText(text)

    @property
    def value(self):
        return self.field.text()

    @value.setter
    def value(self, this):
        self.setText(this)

    def insert(self, text):
        self.field.insert(text)


if __name__ == '__main__':
    import a2widget.demo.a2button_field
    a2widget.demo.a2button_field.show()
