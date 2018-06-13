from PySide import QtGui, QtCore

import a2ctrl


class A2MoreButton(QtGui.QToolButton):
    menu_called = QtCore.Signal(QtGui.QMenu)

    def __init__(self, parent=None):
        super(A2MoreButton, self).__init__(parent)
        self.setAutoRaise(True)
        self.setIcon(a2ctrl.Icons.inst().more)
        self._menu = QtGui.QMenu(self)
        self.clicked.connect(self._on_menu_call)

    def _on_menu_call(self):
        self._menu.clear()

        self.menu_called.emit(self._menu)

        if self._menu.isEmpty():
            action = self._menu.addAction('No actions were added to the Menu!')
            action.setDisabled(True)
        self._menu.popup(QtGui.QCursor.pos())


if __name__ == '__main__':
    import a2widget.demo.a2more_button_demo
    a2widget.demo.a2more_button_demo.show()
