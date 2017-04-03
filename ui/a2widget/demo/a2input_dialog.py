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

        button = QtGui.QPushButton('Call a A2InputDialog')
        l.addWidget(button)
        # vanilla A2InputDialog
        self.c = A2InputDialog(self, 'a title', text='predefined text',
                               msg='some text bla blaaa',
                               ok_func=self.ok_func)
        print('self.c: %s' % self.c)
        self.c.okayed.connect(self.ok_func)
        self.c.canceled.connect(self.cancel_func)
        button.clicked.connect(self.c.show)

    def ok_func(self, value):
        print('ok_func called! value: "%s"' % value)

    def cancel_func(self):
        print('cancel_func called!')


def show():
    app = QtGui.QApplication([])
    win = InputDialogDemo()
    win.show()
    app.exec_()

if __name__ == '__main__':
    show()
