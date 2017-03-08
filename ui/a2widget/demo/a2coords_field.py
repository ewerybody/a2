'''
Created on 08.03.2017

@author: eric
'''
from a2widget import A2CoordsField
from PySide import QtGui


class CoordsFieldDemo(QtGui.QMainWindow):
    def __init__(self):
        super(CoordsFieldDemo, self).__init__()
        w = QtGui.QWidget(self)
        self.setCentralWidget(w)
        l = QtGui.QVBoxLayout(w)
        w.setLayout(l)

        c = A2CoordsField()
        l.addWidget(c)


def show():
    app = QtGui.QApplication([])
    win = CoordsFieldDemo()
    win.show()
    app.exec_()

if __name__ == '__main__':
    show()
