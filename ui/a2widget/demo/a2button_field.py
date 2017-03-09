'''
Created on 08.03.2017

@author: eric
'''
from PySide import QtGui
from a2widget import A2ButtonField


class ButtonFieldDemo(QtGui.QMainWindow):
    def __init__(self):
        super(ButtonFieldDemo, self).__init__()
        w = QtGui.QWidget(self)
        self.setCentralWidget(w)
        l = QtGui.QVBoxLayout(w)
        w.setLayout(l)

        self.c = A2ButtonField()
        l.addWidget(self.c)
        self.c.add_action(QtGui.QAction('Hello', self, triggered=self.bla))

    def bla(self):
        self.c.value = 'Blaab blaa!'
        print(self.c.value)


def show():
    app = QtGui.QApplication([])
    win = ButtonFieldDemo()
    win.show()
    app.exec_()

if __name__ == '__main__':
    show()
