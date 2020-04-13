from PySide2 import QtWidgets
from a2widget.a2path_field import A2PathField


class Demo(QtWidgets.QMainWindow):
    def __init__(self):
        super(Demo, self).__init__()
        w = QtWidgets.QWidget(self)
        self.setCentralWidget(w)
        lyt = QtWidgets.QVBoxLayout(w)
        w.setLayout(lyt)

        lyt.addWidget(QtWidgets.QLabel('a simple list:'))
        self.widget1 = A2PathField(self)
        lyt.addWidget(self.widget1)

        self.write_check = QtWidgets.QCheckBox('writable')
        lyt.addWidget(self.write_check)

        self.write_check.clicked[bool].connect(self.set_write_state)
        self.set_write_state()

    def set_write_state(self, state=False):
        self.widget1.writable = state


def show():
    app = QtWidgets.QApplication([])
    win = Demo()
    win.show()
    app.exec_()


if __name__ == '__main__':
    show()
