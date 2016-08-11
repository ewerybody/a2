"""
a2ctrl.a2settings

@created: 29.02.2016
@author: eric
"""
import ahk
import a2core
import a2ctrl
import logging
from os.path import join, exists
from PySide import QtGui
from a2ctrl import a2settings_ui


class A2Settings(QtGui.QWidget):
    def __init__(self, main):
        super(A2Settings, self).__init__()
        self.a2 = a2core.A2Obj.inst()
        self.main = main
        self.ui = a2settings_ui.Ui_a2settings()
        self.ui.setupUi(self)

        a2_hotkey = self.a2.db.get('a2_hotkey') or a2core.a2default_hotkey
        self.ui.a2hotkey.set_key(a2_hotkey)
        self.ui.a2hotkey.ok_func = self.set_a2_hotkey

        win_startup_path = ahk.call_cmd('get_win_startup_path')
        win_startup_lnk = join(win_startup_path, 'a2.lnk')
        self.ui.loadOnWinStart.setChecked(exists(win_startup_lnk))
        self.ui.loadOnWinStart.clicked[bool].connect(a2core.set_windows_startup)

        self.ui.dev_box.setChecked(self.main.dev_mode)
        self.ui.dev_box.clicked[bool].connect(self.dev_mode_toggle)

        self.ui.rememberLastSel.setChecked(self.a2.db.get('remember_last') or False)
        self.ui.rememberLastSel.clicked[bool].connect(self.remember_last_toggle)

        self.ui.dev_widget.setVisible(self.main.dev_mode)

    def dev_mode_toggle(self, dev_mode):
        self.a2.db.set('dev_mode', dev_mode)
        self.main.dev_mode = dev_mode
        self.ui.dev_widget.setVisible(dev_mode)
        self.main.toggle_dev_menu(dev_mode)

    def remember_last_toggle(self, state):
        self.a2.db.set('remember_last', state)

    def set_a2_hotkey(self, key):
        self.a2.db.set('a2_hotkey', key)
        self.main.settings_changed('hotkeys')


if __name__ == '__main__':
    pass
