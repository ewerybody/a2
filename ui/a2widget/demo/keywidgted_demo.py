from a2qt import QtCore, QtWidgets
import a2ctrl

class TestWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)
        self.setWindowIcon(a2ctrl.Icons.a2)

        layout = QtWidgets.QVBoxLayout(widget)
        kse = QtWidgets.QKeySequenceEdit(self)
        layout.addWidget(kse)

def show():
    app = QtWidgets.QApplication([])
    win = TestWindow()
    win.show()
    app.exec()


if __name__ == '__main__':
    show()
