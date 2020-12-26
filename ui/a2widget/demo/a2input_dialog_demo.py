# import _demo_env
from a2widget.a2input_dialog import A2InputDialog, A2ConfirmDialog
from a2qt import QtWidgets


class InputDialogDemo(QtWidgets.QMainWindow):
    def __init__(self):
        super(InputDialogDemo, self).__init__()
        self.setWindowTitle(self.__class__.__name__)
        widget = QtWidgets.QWidget(self)
        self.setCentralWidget(widget)
        layout = QtWidgets.QVBoxLayout(widget)
        button = QtWidgets.QPushButton('Call a A2InputDialog')
        layout.addWidget(button)

        self.c = A2InputDialog(
            self,
            'a title',
            text='predefined text',
            msg='some text bla blaaa',
            check_func=self.check_func,
        )
        self.c.okayed.connect(self.ok_func)
        self.c.canceled.connect(self.cancel_func)
        self.c.field_changed.connect(self.field_changed)

        button.clicked.connect(self.c.show)

        button2 = QtWidgets.QPushButton('Call a A2ConfirmDialog')
        button2.clicked.connect(self.call_confirm_dialog)
        layout.addWidget(button2)

    @staticmethod
    def check_func(text):
        if text == '':
            return 'Empty text is NOT OK!'
        return True

    @staticmethod
    def field_changed(text):
        print('text: %s' % text)

    @staticmethod
    def ok_func(value):
        print('dialog okayed! value: "%s"' % value)

    @staticmethod
    def cancel_func():
        print('dialog canceled!')

    def call_confirm_dialog(self):
        dialog = A2ConfirmDialog(
            self,
            'A title',
            msg='Some <b>more</b> text bla blaaa with extra formatting and stuff.\n'
            "We wouldn't want it to be <i>too</i> boring, right? 😉",
        )
        dialog.okayed.connect(self.confirm_dialog_okayed)
        dialog.canceled.connect(self.confirm_dialog_canceled)
        dialog.show()

    @staticmethod
    def confirm_dialog_okayed():
        print('confirm_dialog_okayed')

    @staticmethod
    def confirm_dialog_canceled():
        print('confirm_dialog_canceled')


def show():
    app = QtWidgets.QApplication([])
    win = InputDialogDemo()
    win.show()
    app.exec_()


if __name__ == '__main__':
    show()
