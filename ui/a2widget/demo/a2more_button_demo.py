from PySide import QtGui, QtCore

import a2ctrl
from a2widget import A2MoreButton, A2PathField, A2ButtonField


class Demo(QtGui.QMainWindow):
    def __init__(self):
        super(Demo, self).__init__()
        w = QtGui.QWidget(self)
        self.setCentralWidget(w)
        lyt = QtGui.QFormLayout(w)
        self.lyt = lyt
        lyt.setSpacing(20)
        w.setLayout(lyt)

        button1 = A2MoreButton(self)
        button1.menu_called.connect(self.build_a_menu)
        self.menu_called_count = 0
        lyt.addRow('<b>A2MoreButton</b> with menu_called Signal:<br>'
                   'So the menu is always rebuilt', button1)

        button2 = A2MoreButton(self)
        action = button2.add_action('A disabled action')
        action.setEnabled(False)
        action = button2.add_action('An enabled one')
        action.triggered.connect(self.print_something)
        lyt.addRow('<b>A2MoreButton</b> with directly added actions:<br>'
                   'The menu is built once and just popps up', button2)
        button2.menu_called.connect(self.never_called_function)



        path_field = A2PathField(self)
        lyt.addRow(QtGui.QLabel('Path field with A2MoreButton implemented:'))
        lyt.addRow(path_field)

        bfield = A2ButtonField(self)
        bfield.setPlaceholderText('its empty!')
        menu = bfield.add_menu('even more')
        menu.addAction('this is an action')
        lyt.addRow(bfield)

    def build_a_menu(self, menu):
        self.menu_called_count += 1
        menu.addAction(a2ctrl.Icons.inst().a2,
                       'Some Menu action (call count: %i)' % self.menu_called_count, self.some_function)

    def some_function(self):
        print('Action triggered: %s' % self.sender().text())

    def print_something(self):
        print('Passing the actions obviously works')

    def never_called_function(self, menu):
        print('this never gets printed!')


def show():
    app = QtGui.QApplication([])
    win = Demo()
    win.show()
    app.exec_()


if __name__ == '__main__':
    show()
