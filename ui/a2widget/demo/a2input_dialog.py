from a2widget import A2InputDialog


from PySide import QtGui


class InputDialogDemo(QtGui.QMainWindow):
    def __init__(self):
        super(InputDialogDemo, self).__init__()
        self.setWindowTitle(self.__class__.__name__)
        w = QtGui.QWidget(self)
        self.setCentralWidget(w)
        l = QtGui.QVBoxLayout(w)
        w.setLayout(l)

        # vanilla A2InputDialog
        self.c = A2InputDialog(self, 'muppets')


def show():
    app = QtGui.QApplication([])
    win = InputDialogDemo()
    win.show()
    app.exec_()

if __name__ == '__main__':
    show()
