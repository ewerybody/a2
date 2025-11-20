import sys

from PySide6 import QtCore, QtWidgets, QtGui
import a2ctrl


class TestWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)
        self.setWindowIcon(a2ctrl.Icons.a2)

        layout = QtWidgets.QFormLayout(widget)
        font = QtGui.QFont()
        font.setPointSize(20)
        layout.addRow('Python:', QtWidgets.QLabel(sys.version))
        layout.addRow('Qt:', QtWidgets.QLabel(QtCore.qVersion()))


def show():
    app = QtWidgets.QApplication([])
    win = TestWindow()
    win.show()
    app.exec()


if __name__ == '__main__':
    show()
