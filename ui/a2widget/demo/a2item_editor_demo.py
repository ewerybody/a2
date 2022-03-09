import uuid

import a2element.hotkey
from a2qt import QtWidgets
from a2widget.a2item_editor import A2ItemEditor

ITEMS = {
    'mango🥭': {'color': 'green/yellow', 'peel': 2, 'seed': 'Huge!'},
    'banana🍌': {'color': 'Yellow', 'peel': 6, 'seed': 'very tiny'},
    'apple🍎': {'color': 'green/red', 'peel': 1, 'seed': 'small'},
    'kiwi🥝': {'color': 'dark green/brown', 'peel': 1, 'seed': 'small'},
    'poop💩': {'color': 'brownish', 'yummy': False},
    'strawberry🍓': {'color': 'red', 'seed': 'small and on the outside'},
}


class Demo(QtWidgets.QMainWindow):
    def __init__(self):
        super(Demo, self).__init__()
        w = QtWidgets.QWidget(self)
        self.setCentralWidget(w)
        lyt = QtWidgets.QVBoxLayout(w)
        self.setWindowTitle('A2ItemEditor Demo')

        # Most of the times this is subclassed but one can use it straight
        # like this as well:
        self.editor = A2ItemEditor(self)
        lyt.addWidget(self.editor)
        self.editor.set_data(ITEMS)

        color_field = QtWidgets.QLineEdit(self)
        self.editor.add_data_label_widget(
            'color', color_field, color_field.setText, color_field.textChanged, ''
        )
        peel_field = QtWidgets.QSpinBox(self)
        peel_field.setSuffix('mm')
        self.editor.add_data_label_widget(
            'peel', peel_field, peel_field.setValue, peel_field.valueChanged, 0
        )
        yummy_check = QtWidgets.QCheckBox(self)
        self.editor.add_data_label_widget(
            'yummy', yummy_check, yummy_check.setChecked, peel_field.valueChanged, True
        )

        # Now with a changed label: By default the label is taken from key name.
        seed_field = QtWidgets.QLineEdit(self)
        self.editor.add_data_label_widget(
            value_name='seed',
            widget=seed_field,
            set_function=seed_field.setText,
            change_signal=seed_field.textChanged,
            default_value='🤷‍♀️',
            label='Seed Appearance',
        )

        hotkey_cfg = {}
        hotkey = a2element.hotkey.Draw(self, hotkey_cfg)
        self.editor.add_data_widget('hotkey', hotkey, hotkey.set_config, hotkey.changed, hotkey_cfg)
        self.editor.data_changed.connect(self.on_data_change)

    def on_data_change(self):
        print('data_changed!')


def show():
    app = QtWidgets.QApplication([])
    win = Demo()
    win.show()
    app.exec()


if __name__ == '__main__':
    show()
