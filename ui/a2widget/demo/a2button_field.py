import uuid
from a2qt import QtWidgets
from a2widget.a2button_field import A2ButtonField


class Demo(QtWidgets.QMainWindow):
    def __init__(self):
        super(Demo, self).__init__()
        w = QtWidgets.QWidget(self)
        self.setCentralWidget(w)
        lyt = QtWidgets.QVBoxLayout(w)

        lyt.addWidget(QtWidgets.QLabel('with some static actions:'))
        self.bf1 = A2ButtonField()
        lyt.addWidget(self.bf1)
        self.bf1.add_action('Hallo', self.bla)
        self.bf1.add_action('nix')

        lyt.addWidget(QtWidgets.QLabel('with actions build dynamically:'))
        self.bf2 = A2ButtonField()
        lyt.addWidget(self.bf2)
        self.bf2.menu_called.connect(self.about_signal)

    def bla(self):
        self.bf1.value = 'Blaab blaa!'
        print(self.bf1.value)

    def about_signal(self, menu):
        menu.addAction(str(uuid.uuid4()), self.action_handler)

    def action_handler(self):
        action_text = self.sender().text()
        self.bf2.setText(action_text)


def show():
    app = QtWidgets.QApplication([])
    win = Demo()
    win.show()
    app.exec_()


if __name__ == '__main__':
    show()
