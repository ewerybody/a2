from a2qt import QtWidgets
from a2widget import a2text_field


class A2ErrorDialog(QtWidgets.QDialog):
    def __init__(self, error, message=None, title=None, parent=None):
        super().__init__(parent)
        # self.setModal(True)

        if title is None:
            title = 'ERROR'
        elif not isinstance(title, str):
            title = str(title)
        self.setWindowTitle(title)

        layout = QtWidgets.QVBoxLayout(self)

        if message is None:
            message = 'An error occured:'
        label = QtWidgets.QLabel(message, self)
        layout.addWidget(label)

        self.error_field = a2text_field.A2CodeField(self)
        self.error_field.setReadOnly(True)
        self.error_field.setPlainText(str(error))
        layout.addWidget(self.error_field)

        self.a2ok_button = QtWidgets.QPushButton(self)
        self.a2ok_button.setText('OK')
        self.a2ok_button.setObjectName("a2ok_button")
        self.a2ok_button.clicked.connect(self.accept)
        layout.addWidget(self.a2ok_button)


def show(error, message=None, title=None, parent=None):
    dialog = A2ErrorDialog(error, message, title, parent)
    dialog.show()
    return dialog


if __name__ == '__main__':
    from a2widget.demo import a2dialog_demo

    a2dialog_demo.show()
