import json
import pprint

from a2qt import QtWidgets

from a2widget.key_value_table import KeyValueTable
from a2widget.a2text_field import A2CodeField


_DEMO_DATA = {
    'Name': 'Some Body',
    'Surname': 'Body',
    'Street. Nr': 'Thingstreet 8',
    'Street': 'Thingstreet',
    'Nr': '8',
    'PLZ': '12354',
    'City': 'Frankfurt am Main',
    'Phone+': '+1232222222',
    'Phone': '2222222',
    'Country': 'Germany',
}


class Demo(QtWidgets.QMainWindow):
    def __init__(self):
        super(Demo, self).__init__()
        w = QtWidgets.QWidget(self)
        self.setCentralWidget(w)
        lyt = QtWidgets.QVBoxLayout(w)

        self.key_value_table = KeyValueTable(self)
        self.key_value_table.changed.connect(self.table_to_code)
        lyt.addWidget(self.key_value_table)
        btn = QtWidgets.QPushButton('GET DATA')
        btn.clicked.connect(self.get_data)
        lyt.addWidget(btn)

        self.text_field = A2CodeField(self)
        self.text_field.text_changed.connect(self.code_to_table)
        lyt.addWidget(self.text_field)
        btn = QtWidgets.QPushButton('SET DATA')
        btn.clicked.connect(self.set_data)
        lyt.addWidget(btn)

        self.text_field.setText(json.dumps(_DEMO_DATA, indent=2))
        self.set_data()

    def table_to_code(self):
        data = self.key_value_table.get_data()
        self.text_field.setText(json.dumps(data, indent=2))

    def code_to_table(self):
        data = json.loads(self.text_field.text())
        self.key_value_table.set_silent(data)

    def get_data(self):
        data = self.key_value_table.get_data()
        print(data)
        pprint.pprint(data, sort_dicts=False)

    def set_data(self):
        data = json.loads(self.text_field.text())
        self.key_value_table.set_data(data)


def show():
    app = QtWidgets.QApplication([])
    win = Demo()
    win.show()
    app.exec()


if __name__ == '__main__':
    show()
