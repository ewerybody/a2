from a2qt import QtGui, QtCore, QtWidgets

import a2ctrl


class A2MoreButton(QtWidgets.QToolButton):
    menu_called = QtCore.Signal(QtWidgets.QMenu)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._menu = QtWidgets.QMenu(self)
        self._actions_added = False
        self.clicked.connect(self._on_menu_call)

        self.setAutoRaise(True)
        self.setIcon(a2ctrl.Icons.inst().more)

    @property
    def menu(self):
        return self._menu

    def _on_menu_call(self):
        if not self._actions_added:
            self._menu.clear()
            self.menu_called.emit(self._menu)

        if self._menu.isEmpty():
            action = self._menu.addAction('No actions were added to the Menu!')
            action.setDisabled(True)
        self._menu.popup(QtGui.QCursor.pos())

    def insert_action(self, index, *args):
        """
        Inserts an QAction at the given index to the internal QMenu.
        Adding or inserting makes the menu_called to be skipped.

        :param index: The position for the action.
        :return: The inserted QAction.
        :rtype QAction:
        """
        self._actions_added = True
        return self._menu.insertAction(index, *args)

    def add_action(self, *args):
        """
        Adds a QAction to the internal QMenu.
        Adding or inserting makes the menu_called to be skipped.

        :rtype QAction:
        """
        self._actions_added = True
        return self._menu.addAction(*args)

    def add_note(self, *args):
        """
        Adds a disabled QAction.

        To make a note in the menu or something ...
        """
        action = self._menu.addAction(*args)
        action.setEnabled(False)
        return action

    def add_menu(self, *args):
        """
        :rtype QtWidgets.QMenu:
        """
        self._actions_added = True
        return self._menu.addMenu(*args)


if __name__ == '__main__':
    import a2widget.demo.a2more_button_demo

    a2widget.demo.a2more_button_demo.show()
