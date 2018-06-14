from PySide import QtGui, QtCore

import a2ctrl


class MenuMixin(object):
    menu_called = QtCore.Signal(QtGui.QMenu)

    def __init__(self):
        self._menu = QtGui.QMenu(self)
        self._actions_added = False
        self.clicked.connect(self._on_menu_call)

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

    def add_menu(self, *args):
        """
        :rtype QtGui.QMenu:
        """
        self._actions_added = True
        return self._menu.addMenu(*args)


class A2MoreButton(QtGui.QToolButton, MenuMixin):
    def __init__(self, parent=None):
        super(A2MoreButton, self).__init__(parent)
        MenuMixin.__init__(self)
        self.setAutoRaise(True)
        self.setIcon(a2ctrl.Icons.inst().more)


if __name__ == '__main__':
    import a2widget.demo.a2more_button_demo
    a2widget.demo.a2more_button_demo.show()
