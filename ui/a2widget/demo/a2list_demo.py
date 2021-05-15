import uuid
from a2qt import QtWidgets
from a2widget.a2list import A2List, A2ListCompact


class Demo(QtWidgets.QMainWindow):
    def __init__(self):
        super(Demo, self).__init__()
        w = QtWidgets.QWidget(self)
        self.setCentralWidget(w)
        lyt = QtWidgets.QVBoxLayout(w)
        w.setLayout(lyt)

        lyt.addWidget(QtWidgets.QLabel('a simple list:'))
        list_items = 'mango banana apple kiwi apple strawberry'.split()
        self.widget1 = A2List(self, list_items)
        self.widget1.set_multi_selection()
        lyt.addWidget(self.widget1)

        self.widget1.items_selected.connect(self.on_things_selection)
        self.widget1.names_selected.connect(self.on_things_selection)
        self.widget1.single_item_selected.connect(self.on_thing_selection)
        self.widget1.single_name_selected.connect(self.on_thing_selection)
        self.widget1.changed.connect(self.changed1)
        self.widget1.context_menu_requested.connect(self.build_context_menu)

        lyt.addWidget(QtWidgets.QLabel('a height adjusted list:'))
        self.widget2 = A2ListCompact(self)
        lyt.addWidget(self.widget2)

        self.widget2.items_selected.connect(self.on_things_selection)
        self.widget2.names_selected.connect(self.on_things_selection)
        self.widget2.single_item_selected.connect(self.on_thing_selection)
        self.widget2.single_name_selected.connect(self.on_thing_selection)
        self.widget2.changed.connect(self.changed2)

        menu = QtWidgets.QMenu(self)
        menu.addAction('blank action static menu')
        self.widget2.set_context_menu(menu)

        button = QtWidgets.QPushButton('add random')
        button.clicked.connect(self.bla)
        lyt.addWidget(button)

    def bla(self):
        self.widget2.add(str(uuid.uuid4()))

    @staticmethod
    def on_things_selection(things):
        print('things: %s' % things)

    @staticmethod
    def on_thing_selection(thing):
        print('single thing: %s' % thing)

    @staticmethod
    def changed1():
        print('list 1 changed!')

    @staticmethod
    def changed2():
        print('list 2 changed!')

    def build_context_menu(self, menu):
        menu.clear()
        for name in self.widget1.get_selected_names():
            menu.addAction('context_menu for item "%s"' % name)


def show():
    app = QtWidgets.QApplication([])
    win = Demo()
    win.show()
    app.exec_()


if __name__ == '__main__':
    show()
