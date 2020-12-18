from pprint import pprint
from PySide6 import QtGui, QtCore, QtWidgets
import a2ctrl.connect
from a2widget.a2coords_field import A2CoordsField


class CoordsFieldDemo(QtWidgets.QMainWindow):
    dict_changed = QtCore.Signal(tuple)

    def __init__(self):
        super(CoordsFieldDemo, self).__init__()
        w = QtWidgets.QWidget(self)
        self.setCentralWidget(w)
        vlay = QtWidgets.QVBoxLayout(w)

        self.c = A2CoordsField()
        self.c.changed.connect(self.change_received)

        self.c2 = A2CoordsField()

        self.show_current_timer = QtCore.QTimer()
        self.show_current_timer.setInterval(100)
        self.show_current_timer.timeout.connect(self.show_current_pos)
        self.show_current_timer.start()

        self.some_dict = {'some_coords': (23, 42), 'something_else': 'blaaa'}
        self.c3 = A2CoordsField()
        a2ctrl.connect.control(self.c3, 'some_coords', self.some_dict, self.dict_changed)
        self.dict_changed.connect(self.show_dict_change)

        for l, w in [
            ('Simple field:', self.c),
            ('Constantly updated:', self.c2),
            ('Dictionary connected:', self.c3),
        ]:
            vlay.addWidget(QtWidgets.QLabel(l))
            vlay.addWidget(w)

    def show_current_pos(self):
        self.c2.set_value(QtGui.QCursor.pos())

    @staticmethod
    def change_received(coords):
        print('coords change_received: %s' % str(coords))

    def show_dict_change(self):
        pprint(self.some_dict)


def show():
    app = QtWidgets.QApplication([])
    win = CoordsFieldDemo()
    win.show()
    app.exec_()


if __name__ == '__main__':
    show()
