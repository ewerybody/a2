from a2qt import QtCore, QtWidgets

import a2uic
from a2widget import a2input_dialog_ui

SIZABLE_FLAGS = QtCore.Qt.Window | QtCore.Qt.WindowCloseButtonHint
FIXED_FLAGS = (
    QtCore.Qt.Window | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.MSWindowsFixedSizeDialogHint
)


class A2ConfirmDialog(QtWidgets.QDialog):
    okayed = QtCore.Signal()
    canceled = QtCore.Signal()

    def __init__(self, parent, title, msg='', ok_func=None):
        super(A2ConfirmDialog, self).__init__(parent)
        # self.setWindowFlags(FIXED_FLAGS)
        a2uic.check_module(a2input_dialog_ui)
        self.ui = a2input_dialog_ui.Ui_A2InputDialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.setWindowTitle(title)
        self._result = False

        if ok_func is not None:
            self.okayed.connect(ok_func)

        self.ui.a2ok_button.clicked.connect(self.okay)
        self.ui.a2cancel_button.clicked.connect(self.reject)

        self.ui.label.setTextFormat(QtCore.Qt.RichText)
        self.ui.label.setText(msg.replace('\n', '<br>'))

        self.rejected.connect(self.canceled.emit)

    def okay(self):
        self._result = True
        self.okayed.emit()
        self.accept()

    @property
    def result(self):
        return self._result

    def resize_delayed(self, timout=50):
        QtCore.QTimer(self).singleShot(timout, self._resize_height)

    def _resize_height(self):
        self.resize(self.width(), self.minimumSizeHint().height())


class A2InputDialog(A2ConfirmDialog):
    okayed = QtCore.Signal()
    yielded = QtCore.Signal(str)
    field_changed = QtCore.Signal(str)

    def __init__(self, parent, title, check_func=None, text='', msg='', ok_func=None):
        """
        :param QWidget parent: The parent widget to pass.
        :param str title: String for the dialogs title bar.
        :param function check_func: Function object to make the OK button
            react to the input.
        :param str text: Text string to display in the input field already.
        :param str msg: Message string for a label over the input field.
        """
        super(A2InputDialog, self).__init__(parent, title, msg, ok_func)

        self.check_func = check_func

        self._output = None
        self._text = text

        self.ui_text_field = QtWidgets.QLineEdit(self)
        self.ui.main_layout.insertWidget(1, self.ui_text_field)
        self.ui_text_field.textChanged.connect(self.check)
        self.ui_text_field.setText(self._text)
        self.ui_text_field.setFocus()

    @property
    def text(self):
        return self._text

    def check(self, text=None):
        if text is None:
            text = self.ui_text_field.text()

        if text != self._text:
            self.field_changed.emit(text)
        self._text = text

        if self.check_func is not None:
            answer = self.check_func(text)
            if answer == '' or answer is True:
                self.ui.a2ok_button.setEnabled(True)
                self.ui.a2ok_button.setText('OK')
                return True
            else:
                self.ui.a2ok_button.setEnabled(False)
                self.ui.a2ok_button.setText(answer)
                return False

    @property
    def output(self):
        return self._output

    def okay(self):
        txt = self.ui_text_field.text()
        result = self.check(txt)
        if result is None or result is True:
            self._output = txt
            self.okayed.emit()
            self.yielded.emit(txt)
            self.accept()


if __name__ == '__main__':
    import a2widget.demo.a2input_dialog_demo

    a2widget.demo.a2input_dialog_demo.show()
