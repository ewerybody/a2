'''
Created on 08.03.2017

@author: eric
'''
from pprint import pprint
from PySide import QtGui, QtCore

import a2ctrl.connect
from a2widget import A2CoordsField


class CoordsFieldDemo(QtGui.QMainWindow):
    dict_changed = QtCore.Signal(tuple)

    def __init__(self):
        super(CoordsFieldDemo, self).__init__()
        w = QtGui.QWidget(self)
        self.setCentralWidget(w)
        l = QtGui.QVBoxLayout(w)
        w.setLayout(l)

        self.c = A2CoordsField()
        self.c.changed.connect(self.change_received)
        l.addWidget(self.c)

        self.c2 = A2CoordsField()
        l.addWidget(self.c2)

        self.show_current_timer = QtCore.QTimer()
        self.show_current_timer.setInterval(50)
        self.show_current_timer.timeout.connect(self.show_current_pos)
        self.show_current_timer.start()

        self.some_dict = {'some_coords': (23, 42), 'something_else': 'blaaa'}
        self.c3 = A2CoordsField()
        l.addWidget(self.c3)
        a2ctrl.connect.control(self.c3, 'some_coords', self.some_dict, self.dict_changed)
        self.dict_changed.connect(self.show_dict_change)

    def show_current_pos(self):
        self.c2.set_value(QtGui.QCursor.pos())

    def change_received(self, coords):
        print('coords change_received: %s' % str(coords))

    def show_dict_change(self):
        pprint(self.some_dict)


def show():
    app = QtGui.QApplication([])
    win = CoordsFieldDemo()
    win.show()
    app.exec_()

if __name__ == '__main__':
    show()
