from PySide import QtGui, QtCore


class A2MoreButton(QtGui.QToolButton):
    menu_called = QtCore.Signal(QtGui.QMenu)

    def __init__(self, parent=None):
        super(A2MoreButton, self).__init__(parent)
        #self.button.setObjectName('a2option_button')
        self.setAutoRaise(True)
        # self.button.setArrowType(QtCore.Qt.DownArrow)
        #self.button.setIcon(a2ctrl.Icons.inst().more)
        self._menu = QtGui.QMenu(self)
        self.clicked.connect(self.on_menu_call)

    def on_menu_call(self):
        self._menu.clear()

        self.menu_called.emit(self._menu)

        self._menu.popup(QtGui.QCursor.pos())


if __name__ == '__main__':
    import a2widget.demo.a2more_button_demo
    a2widget.demo.a2more_button_demo.show()
