import a2ctrl.connect
from a2widget.a2combo import A2Combo
from a2qt import QtGui, QtCore, QtWidgets

LIST_ITEMS = 'mango banana apple kiwi apple strawberry'.split()

class ComboDemo(QtWidgets.QMainWindow):
    dict_changed = QtCore.Signal(tuple)

    def __init__(self):
        super().__init__()
        sa = QtWidgets.QScrollArea(self)
        sa.setWidgetResizable(True)
        self.setCentralWidget(sa)
        w = QtWidgets.QWidget(sa)
        sa.setWidget(w)
        vlay = QtWidgets.QVBoxLayout(w)

        spacer_widget1 = QtWidgets.QWidget(self)
        spacer_widget1.setMinimumHeight(200)
        vlay.addWidget(spacer_widget1)

        self.c = A2Combo()
        self.c.addItems(LIST_ITEMS)
        # self.c.changed.connect(self.change_received)

        self.c2 = A2Combo()
        self.c2.addItems(LIST_ITEMS)

        self.c3 = A2Combo()
        self.c3.addItems(LIST_ITEMS)
        # a2ctrl.connect.control(self.c3, 'some_coords', self.some_dict, self.dict_changed)

        for w in self.c, self.c2, self.c3:
            vlay.addWidget(w)

        spacer_widget2 = QtWidgets.QWidget(self)
        spacer_widget2.setMinimumHeight(300)
        vlay.addWidget(spacer_widget2)


def show():
    app = QtWidgets.QApplication([])
    win = ComboDemo()
    win.show()
    app.exec()


if __name__ == '__main__':
    show()
