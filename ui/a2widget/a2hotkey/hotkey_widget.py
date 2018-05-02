import a2core
from PySide import QtGui, QtCore
from .simple_dialog import HotkeyDialog1
from .dialogs import HotKeyBoard


class A2Hotkey(QtGui.QPushButton):
    hotkey_changed = QtCore.Signal(str)

    def __init__(self, parent=None, key=None, scope_data=None):
        """
        :param QWidget parent: Parent Qt object.
        :param str key: Key string
        :param dict scope_data: [optional] Dictionary object for Hotkey dialog to look
            up scope information.
        """
        super(A2Hotkey, self).__init__(parent)
        self.a2 = a2core.A2Obj.inst()
        self.key = key or ''
        self.setText(key)
        self.scope_data = scope_data
        self.clicked.connect(self.popup_dialog)

        self.dialog_styles = [HotKeyBoard]
        self.dialog_default = HotkeyDialog1
        self.dialog_styles.append(self.dialog_default)

    def set_key(self, key):
        if key != self.key:
            self.key = key
            self.setText(key)
            self.hotkey_changed.emit(key)

    def popup_dialog(self):
        class_name = self.a2.db.get('hotkey_dialog_style')
        if class_name:
            for hotkey_dialog_class in self.dialog_styles:
                if hotkey_dialog_class.__name__ == class_name:
                    break
        else:
            hotkey_dialog_class = self.dialog_default

        dialog = hotkey_dialog_class(self, self.key, self.scope_data)
        dialog.hotkey_set.connect(self.set_key)
        dialog.show()

    def clear(self):
        """
        Sets the hotkey button to '', None aka "nothing".
        """
        self.set_key('')

    def is_clear(self):
        """
        :return: False if a key is set. True if no key is set.
        :rtype: bool
        """
        return self.key == ''
