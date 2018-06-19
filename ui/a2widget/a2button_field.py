from PySide2 import QtCore, QtWidgets

from a2widget import A2MoreButton


class A2ButtonField(QtWidgets.QWidget):
    textChanged = QtCore.Signal(str)
    menu_called = QtCore.Signal(QtWidgets.QMenu)

    def __init__(self, parent=None):
        super(A2ButtonField, self).__init__(parent)
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.field = QtWidgets.QLineEdit(self)
        self.field.textChanged.connect(self.textChanged.emit)
        self.main_layout.addWidget(self.field)
        self.a2option_button = A2MoreButton(self)
        self.a2option_button.menu_called.connect(self.menu_called.emit)
        self.main_layout.addWidget(self.a2option_button)

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

    def setFocus(self):
        self.field.setFocus()

    def setPlaceholderText(self, text):
        self.field.setPlaceholderText(text)

    def insert_action(self, index, *args):
        """
        Inserts an QAction at the given index to the internal QMenu.
        Adding or inserting makes the menu_called to be skipped.

        :param index: The position for the action.
        :return: The inserted QAction.
        :rtype QAction:
        """
        return self.a2option_button.insert_action(index, *args)

    def add_action(self, *args):
        """
        Adds a QAction to the internal QMenu.
        Adding or inserting makes the menu_called to be skipped.

        :rtype QAction:
        """
        return self.a2option_button.add_action(*args)

    @property
    def menu(self):
        return self.a2option_button._menu

    def add_menu(self, *args):
        """
        :rtype QtWidgets.QMenu:
        """
        return self.a2option_button.add_menu(*args)


if __name__ == '__main__':
    import a2widget.demo.a2button_field
    a2widget.demo.a2button_field.show()
