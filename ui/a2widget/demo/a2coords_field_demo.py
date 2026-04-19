from pprint import pprint
from PySide6 import QtGui, QtCore, QtWidgets
import a2ctrl.connect
from a2widget.a2coords_field import A2CoordsField


class CoordsFieldDemo(QtWidgets.QMainWindow):
    def __init__(self):
        super(CoordsFieldDemo, self).__init__()
        self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, True)
        self.setWindowIcon(a2ctrl.Icons.a2)
        w = QtWidgets.QWidget(self)
        self.setCentralWidget(w)
        v_layout = QtWidgets.QVBoxLayout(w)

        self.c = A2CoordsField()
        self.c.changed_to.connect(self.change_received)

        self.c2 = A2CoordsField()

        self.show_current_timer = QtCore.QTimer()
        self.show_current_timer.setInterval(100)
        self.show_current_timer.timeout.connect(self.show_current_pos)
        self.show_current_timer.start()

        self.some_dict = {'some_coords': (23, 42), 'something_else': 'bla bla bla'}
        self.c3 = A2CoordsField()
        a2ctrl.connect.control(self.c3, 'some_coords', self.some_dict)
        self.c3.changed.connect(self.show_dict_change)

        for label, widget in [
            ('Simple field:', self.c),
            ('Constantly updated:', self.c2),
            ('Dictionary connected:', self.c3),
        ]:
            v_layout.addWidget(QtWidgets.QLabel(label))
            v_layout.addWidget(widget)

    def show_current_pos(self):
        self.c2.set_value(QtGui.QCursor.pos())

    @staticmethod
    def change_received(coords: tuple[int, int]):
        print('coords change_received: %i/%i' % (coords[0], coords[1]))

    def show_dict_change(self):
        pprint(self.some_dict)


def show():
    app = QtWidgets.QApplication([])
    win = CoordsFieldDemo()
    win.show()
    app.exec()


if __name__ == '__main__':
    show()
