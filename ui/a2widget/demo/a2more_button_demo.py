from a2qt import QtWidgets

import a2ctrl
from a2widget.a2more_button import A2MoreButton
from a2widget.a2path_field import A2PathField
from a2widget.a2button_field import A2ButtonField


class Demo(QtWidgets.QMainWindow):
    def __init__(self):
        super(Demo, self).__init__()
        w = QtWidgets.QWidget(self)
        self.setCentralWidget(w)
        lyt = QtWidgets.QFormLayout(w)
        self.lyt = lyt
        lyt.setSpacing(20)
        w.setLayout(lyt)

        button1 = A2MoreButton(self)
        button1.menu_called.connect(self.build_a_menu)
        self.menu_called_count = 0
        lyt.addRow(
            '<b>A2MoreButton</b> with menu_called Signal:<br>' 'So the menu is always rebuilt',
            button1,
        )

        button2 = A2MoreButton(self)
        button2.add_note('A disabled action')
        action = button2.add_action('An enabled one')
        action.triggered.connect(self.print_something)
        lyt.addRow(
            '<b>A2MoreButton</b> with directly added actions:<br>'
            'The menu is built once and just popps up',
            button2,
        )
        button2.menu_called.connect(self.never_called_function)

        path_field = A2PathField(self)
        lyt.addRow(QtWidgets.QLabel('Path field with A2MoreButton implemented:'))
        lyt.addRow(path_field)

        bfield = A2ButtonField(self)
        bfield.setPlaceholderText('its empty!')
        menu = bfield.add_menu('even more')
        menu.addAction('this is an action')
        lyt.addRow(bfield)

    def build_a_menu(self, menu):
        self.menu_called_count += 1
        menu.addAction(
            a2ctrl.Icons.inst().a2,
            'Some Menu action (call count: %i)' % self.menu_called_count,
            self.some_function,
        )

    def some_function(self):
        print('Action triggered: %s' % self.sender().text())

    @staticmethod
    def print_something():
        print('Passing the actions obviously works')

    @staticmethod
    def never_called_function(menu):
        print('this never gets printed!')


def show():
    app = QtWidgets.QApplication([])
    win = Demo()
    win.show()
    app.exec_()


if __name__ == '__main__':
    show()
