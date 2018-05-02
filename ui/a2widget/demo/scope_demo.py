from PySide import QtGui
from a2widget.a2hotkey.edit_scope_widget import ScopeWidget


class Demo(QtGui.QMainWindow):
    def __init__(self):
        super(Demo, self).__init__()
        w = QtGui.QWidget(self)
        self.setCentralWidget(w)
        l = QtGui.QVBoxLayout(w)
        w.setLayout(l)

        self.c = ScopeWidget(self)
        l.addWidget(self.c)
        # self.c.add_action(QtGui.QAction('Hello', self, triggered=self.bla))

    def bla(self):
        self.c.value = 'Blaab blaa!'
        print(self.c.value)


def show():
    app = QtGui.QApplication([])
    win = Demo()
    win.show()
    app.exec_()


if __name__ == '__main__':
    show()
