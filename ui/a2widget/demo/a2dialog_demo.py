from functools import partial
from a2qt import QtCore, QtWidgets
from a2widget import a2input_dialog
from a2widget.a2input_dialog import A2InputDialog, A2ConfirmDialog
from a2widget.a2error_dialog import A2ErrorDialog

EXTRA_TEXT = (
    ' here is be some more text to text expanding the dialog<br>horizontally '
    'and vertically until line break would occur<br>'
    'or the boundaries are reached ...'
)


class DialogDemo(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.__class__.__name__)
        widget = QtWidgets.QWidget(self)
        self.setCentralWidget(widget)
        layout = QtWidgets.QVBoxLayout(widget)
        button = QtWidgets.QPushButton('Call an A2InputDialog')
        layout.addWidget(button)

        # build the dialog right away and show it on button `clicked`-Signal
        self.input_dialog = A2InputDialog(
            self,
            'a title',
            text='predefined text',
            msg='some text bla blaaa',
            check_func=self.check_func,
        )
        self.input_dialog.okayed.connect(self.ok_func)
        self.input_dialog.yielded.connect(self.yield_func)
        self.input_dialog.canceled.connect(self.cancel_func)
        self.input_dialog.field_changed.connect(self.field_changed)

        button.clicked.connect(self.input_dialog.show)
        button.clicked.connect(self._change_input_dialog)

        # build the dialog after button is `clicked`
        button2 = QtWidgets.QPushButton('Call an A2ConfirmDialog')
        button2.clicked.connect(self.call_confirm_dialog)
        layout.addWidget(button2)

        button3 = QtWidgets.QPushButton('Call an A2ErrorDialog')
        button3.clicked.connect(self.call_error_dialog)
        layout.addWidget(button3)


    @staticmethod
    def check_func(text):
        if text == '':
            return 'Empty text is NOT OK!'
        return True

    @staticmethod
    def field_changed(text):
        print('text: %s' % text)

    @staticmethod
    def ok_func():
        print('dialog okayed!')

    @staticmethod
    def yield_func(value):
        print('dialog yielded: "%s"' % value)

    @staticmethod
    def cancel_func():
        print('dialog canceled!')

    def call_confirm_dialog(self):
        dialog = A2ConfirmDialog(
            self,
            'A title',
            msg='Some <b>more</b> text bla blaaa with extra formatting and stuff.\n'
            "We wouldn't want it to be <i>too</i> boring, right? 😉 ... wait for it ...",
        )
        dialog.setWindowFlags(a2input_dialog.FIXED_FLAGS)
        dialog.okayed.connect(self.confirm_dialog_okayed)
        dialog.canceled.connect(self.confirm_dialog_canceled)
        dialog.show()
        QtCore.QTimer(self).singleShot(500, partial(self._add_text, dialog))

    def _add_text(self, dialog):
        current = dialog.ui.label.text()
        current += EXTRA_TEXT

        button = QtWidgets.QPushButton('HHaaallo')
        button.setMinimumHeight(100)
        dialog.ui.main_layout.addWidget(button)
        dialog.ui.label.setText(current)

    @staticmethod
    def confirm_dialog_okayed():
        print('confirm_dialog_okayed')

    @staticmethod
    def confirm_dialog_canceled():
        print('confirm_dialog_canceled')

    def _change_input_dialog(self):
        txt = self.input_dialog.ui.label.text()
        if EXTRA_TEXT in txt:
            return
        self.input_dialog.ui.label.setText(f'<b>{txt}</b> {EXTRA_TEXT}')

    def call_error_dialog(self):
        import traceback

        try:
            import asasfnclhjclahfhaksha
        except Exception as error:
            report = traceback.format_exc().strip()
            dialog = A2ErrorDialog(report, f'There was a demo error thrown:\n{error}', error, self)
            dialog.show()


def show():
    app = QtWidgets.QApplication([])
    win = DialogDemo()
    win.show()
    app.exec()


if __name__ == '__main__':
    show()
