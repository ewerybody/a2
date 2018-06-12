from PySide import QtGui, QtCore

from a2widget import A2MoreButton


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
        lyt.addRow('a "more" button', self.button)


def show():
    app = QtGui.QApplication([])
    win = Demo()
    win.show()
    app.exec_()


if __name__ == '__main__':
    show()
