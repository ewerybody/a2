import a2core
from PySide2 import QtCore
from .keyboard_dialog.base import KeyboardDialogBase


from a2widget.a2hotkey.keyboard_dialog import layouts


class _HotkeyDialogBase(QtCore.QObject):
    hotkey_set = QtCore.Signal(str)
    label = ''

    def __init__(self, parent, key, scope_data=None):
        self.parent = parent
        self.key = key
        self.scope_data = scope_data
        self.a2 = a2core.A2Obj.inst()


class HotKeyBoard(KeyboardDialogBase, _HotkeyDialogBase):
    hotkey_set = QtCore.Signal(str)
    label = 'Hotkey Keyboard'

    def __init__(self, parent, key, scope_data=None):
        _HotkeyDialogBase.__init__(self, parent, key, scope_data)
        KeyboardDialogBase.__init__(self, parent)

        self.build_keyboard(layouts.get_current())
        self.set_key()
        self.okay_state = True

    def ok(self):
        if self.okay_state:
            self.hotkey_set.emit(self.key)
            self.close()
