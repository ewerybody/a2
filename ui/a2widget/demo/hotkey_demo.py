from copy import deepcopy

from a2qt import QtCore, QtWidgets

import a2uic
import a2element.hotkey
from a2widget.a2text_field import A2CodeField
from a2widget.a2hotkey import scope_widget_ui, edit_widget_ui


config = {
    'typ': 'hotkey',
    'key': ['Alt+H', 'Alt+D'],
    'name': '_my_module_Hotkey2',
    'label': 'Standard Hotkey',
    'enabled': True,
    'disablable': True,
    'scope': ['WhatsApp - Mozilla Firefox ahk_exe firefox.exe'],
    'scopeMode': 1,
    'scopeChange': False,
    'functionCode': 'MsgBox Hello World!',
    'functionMode': 0,
    'functionSend': '',
    'functionURL': '',
    'keyChange': True,
    'multiple': True,
}


class Demo(QtWidgets.QMainWindow):
    def __init__(self):
        super(Demo, self).__init__()

        a2uic.check_module(edit_widget_ui)
        a2uic.check_module(scope_widget_ui)

        w = QtWidgets.QWidget(self)
        self.setCentralWidget(w)
        lyt = QtWidgets.QFormLayout(w)
        self.lyt = lyt
        lyt.setSpacing(20)
        w.setLayout(lyt)

        self.hotkey = a2element.hotkey.Edit(config, self, {})
        lyt.addRow(self.hotkey)

        self.code = A2CodeField(self)
        lyt.addRow('code', self.code)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.check_changes)
        self.timer.start()
        self._config_backup = None

        self.user_hotkey = None
        lyt.addRow(QtWidgets.QLabel('user hotkey:'))

    def check_changes(self):
        if self._config_backup != config:
            self.code.setText(config)
            self._config_backup = deepcopy(config)

            if self.user_hotkey is not None:
                self.user_hotkey.deleteLater()
            new_user_hotkey = a2element.hotkey.Draw(self, config, None)
            new_user_hotkey.changed.connect(self.user_change)
            self.user_hotkey = new_user_hotkey
            self.lyt.addRow(self.user_hotkey)

    def user_change(self):
        user_cfg = self.user_hotkey.get_user_dict()
        changed = False
        for key in set(user_cfg).union(self._config_backup):
            user_value = user_cfg.get(key)
            if user_value != self._config_backup.get(key):
                print(f'User change: {key}: {user_value}')
                changed = True
        if not changed:
            print('All values original!')


def show():
    app = QtWidgets.QApplication([])
    win = Demo()
    win.show()
    app.exec()


if __name__ == '__main__':
    show()
