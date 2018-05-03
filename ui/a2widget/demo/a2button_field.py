"""
Created on 08.03.2017

@author: eric
"""
import uuid
from PySide import QtGui
from a2widget import A2ButtonField


class ButtonFieldDemo(QtGui.QMainWindow):
    def __init__(self):
        super(ButtonFieldDemo, self).__init__()
        w = QtGui.QWidget(self)
        self.setCentralWidget(w)
        lyt = QtGui.QVBoxLayout(w)
        w.setLayout(lyt)

        lyt.addWidget(QtGui.QLabel('with some static actions:'))
        self.bf1 = A2ButtonField()
        lyt.addWidget(self.bf1)
        self.bf1.add_action(QtGui.QAction('Hello', self, triggered=self.bla))
        self.bf1.add_action('Hallo', self.bla)
        self.bf1.add_action('nix')

        lyt.addWidget(QtGui.QLabel('with actions build dynamically:'))
        self.bf2 = A2ButtonField()
        lyt.addWidget(self.bf2)
        self.bf2.menu_about_to_show.connect(self.about_signal)

    def bla(self):
        self.bf1.value = 'Blaab blaa!'
        print(self.bf1.value)

    def about_signal(self, menu):
        menu.clear()
        menu.addAction(str(uuid.uuid4()), self.action_handler)

    def action_handler(self):
        action_text = self.sender().text()
        self.bf2.setText(action_text)


def show():
    app = QtGui.QApplication([])
    win = ButtonFieldDemo()
    win.show()
    app.exec_()


if __name__ == '__main__':
    show()
