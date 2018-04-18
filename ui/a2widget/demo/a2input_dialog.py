from a2widget import A2InputDialog, A2ConfirmDialog
from PySide import QtGui


class InputDialogDemo(QtGui.QMainWindow):
    def __init__(self):
        super(InputDialogDemo, self).__init__()
        self.setWindowTitle(self.__class__.__name__)
        widget = QtGui.QWidget(self)
        self.setCentralWidget(widget)
        layout = QtGui.QVBoxLayout(widget)
        button = QtGui.QPushButton('Call a A2InputDialog')
        layout.addWidget(button)

        self.c = A2InputDialog(self, 'a title', text='predefined text',
                               msg='some text bla blaaa',
                               check_func=self.check_func)
        self.c.okayed.connect(self.ok_func)
        self.c.canceled.connect(self.cancel_func)
        self.c.field_changed.connect(self.field_changed)

        button.clicked.connect(self.c.show)

        button2 = QtGui.QPushButton('Call a A2ConfirmDialog')
        button2.clicked.connect(self.call_confirm_dialog)
        layout.addWidget(button2)

    def check_func(self, text):
        if text == '':
            return 'Empty text is NOT OK!'
        return True

    def field_changed(self, text):
        print('text: %s' % text)

    def ok_func(self, value):
        print('dialog okayed! value: "%s"' % value)

    def cancel_func(self):
        print('dialog canceled!')

    def call_confirm_dialog(self):
        dialog = A2ConfirmDialog(self, 'A title', msg='some text bla blaaa')
        dialog.okayed.connect(self.confirm_dialog_okayed)
        dialog.canceled.connect(self.confirm_dialog_canceled)
        dialog.show()

    def confirm_dialog_okayed(self):
        print('confirm_dialog_okayed')

    def confirm_dialog_canceled(self):
        print('confirm_dialog_canceled')


def show():
    app = QtGui.QApplication([])
    win = InputDialogDemo()
    win.show()
    app.exec_()


if __name__ == '__main__':
    show()
