import a2core
from PySide import QtCore
from .keyboard_dialog.base import KeyboardDialogBase


class _HotkeyDialogBase(QtCore.QObject):
    hotkey_set = QtCore.Signal(str)
    label = ''

    def __init__(self, parent, key, scope_data=None):
        self.parent = parent
        self.key = key
        self.scope_data = scope_data
        self.a2 = a2core.A2Obj.inst()


class HotKeyBoard(KeyboardDialogBase, _HotkeyDialogBase):
    label = 'Hotkey Keyboard'

    def __init__(self, parent, key, scope_data=None):
        KeyboardDialogBase.__init__(self, parent)
        _HotkeyDialogBase.__init__(self, parent, key, scope_data)

        keyboard_id = self.a2.db.get('keyboard_id') or 'en_us'
        self.build_keyboard(keyboard_id)
        self.set_key()
        self.okay_state = True

    def ok(self):
        if self.okay_state:
            self.hotkey_set.emit(self.key)
            self.close()
