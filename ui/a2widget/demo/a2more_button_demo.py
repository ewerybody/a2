from PySide import QtGui, QtCore

import a2ctrl
from a2widget import A2MoreButton, A2PathField


class Demo(QtGui.QMainWindow):
    def __init__(self):
        super(Demo, self).__init__()
        w = QtGui.QWidget(self)
        self.setCentralWidget(w)
        lyt = QtGui.QFormLayout(w)
        self.lyt = lyt
        lyt.setSpacing(20)
        w.setLayout(lyt)

        self.button = A2MoreButton(self)
        lyt.addRow('a "more" button:', self.button)
        self.button.menu_called.connect(self.build_a_menu)

        path_field = A2PathField(self)
        lyt.addRow(QtGui.QLabel('Path field with A2MoreButton implemented:'))
        lyt.addRow(path_field)

    def build_a_menu(self, menu):
        menu.addAction(a2ctrl.Icons.inst().a2, 'Some Menu action ...', self.some_function)

    def some_function(self):
        print('Action triggered: %s' % self.sender().text())


def show():
    app = QtGui.QApplication([])
    win = Demo()
    win.show()
    app.exec_()


if __name__ == '__main__':
    show()
