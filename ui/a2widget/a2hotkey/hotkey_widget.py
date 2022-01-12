"""Home of the mighty a2Hotkey widget."""
# pylint: disable=C0103,C0111

from a2qt import QtCore, QtWidgets

import a2core
import a2ctrl
from a2widget.a2hotkey.simple_dialog import HotkeyDialog1
from a2widget.a2hotkey.dialogs import HotKeyBoard
from a2widget.a2hotkey.hotkey_common import Vars, get_keys_list

_SCOPE_TOOLTIP = 'Hotkey scope is set '
SCOPE_TOOLTIP_GLOBAL = _SCOPE_TOOLTIP + '"global" so it works anywhere.'
SCOPE_TOOLTIP_INCLUDE = _SCOPE_TOOLTIP + 'to work only in specific windows.'
SCOPE_TOOLTIP_EXCLUDE = _SCOPE_TOOLTIP + 'to exclude specific windows.'
SCOPE_CANNOT_CHANGE = '\nThis cannot be changed!'
SCOPE_GLOBAL_NOCHANGE = 'Global - unchangable'
HOTKEY_CANNOT_CHANGE = 'The hotkey cannot be changed!'
HOTKEY_EMPTY = 'Empty Hotkeys will be ignored!'

DIALOG_CLASSES = [HotKeyBoard, HotkeyDialog1]
DIALOG_DEFAULT = DIALOG_CLASSES[0]
QSS_NAME_WIDGET = 'A2Hotkey'
QSS_NAME_HOTKEY = 'A2HotkeyButton'
QSS_NAME_SCOPE = 'A2HotkeyScope'


class A2Hotkey(QtWidgets.QWidget):
    hotkey_changed = QtCore.Signal(list)
    scope_changed = QtCore.Signal(list, int)

    def __init__(self, parent=None):
        """
        :param QWidget parent: Parent Qt object.
        :param str or list key: Key string or list of key stings.
        :param dict scope_data: [optional] Dictionary object for Hotkey dialog to look
            up scope information.
        """
        super(A2Hotkey, self).__init__(parent)
        self.a2 = a2core.A2Obj.inst()
        self.key = None
        self._cfg = {}
        self._edit_mode = False
        self._locked = None

        uber_layout = QtWidgets.QHBoxLayout(self)
        uber_widget = QtWidgets.QWidget(self)
        uber_widget.setObjectName(QSS_NAME_WIDGET)
        uber_layout.addWidget(uber_widget)
        uber_layout.setContentsMargins(0, 0, 0, 0)

        self._vlayout = QtWidgets.QVBoxLayout(uber_widget)
        self._vlayout.setSpacing(0)
        self._layout = QtWidgets.QHBoxLayout()
        self._vlayout.addLayout(self._layout)
        self._layout.setSpacing(0)
        self._hotkey_buttons = [QtWidgets.QPushButton(self)]
        self._hotkey_buttons[0].setObjectName(QSS_NAME_HOTKEY)
        self._hotkey_index = 0
        self._scope_button = QtWidgets.QPushButton(self)
        self._scope_button.setObjectName(QSS_NAME_SCOPE)
        self._layout.addWidget(self._hotkey_buttons[0])
        self._layout.addWidget(self._scope_button)
        self._scope_button.clicked.connect(self.scope_clicked)
        self._hotkey_buttons[0].clicked.connect(self.popup_dialog)

    def set_config(self, config_dict):
        self._cfg = config_dict or {}
        self.setup_scope_button()
        self.set_key(self._cfg.get('key', ''))

    def setText(self, key):
        if isinstance(key, list):
            key = key[0]
        self._hotkey_buttons[0].setText(key)

    def set_key(self, key):
        key_list = get_keys_list(key)
        change = key_list != self.key

        if change:
            self.key = key_list
            num_keys, num_buttons = len(key_list), len(self._hotkey_buttons)
            if num_keys > num_buttons:
                for i in range(num_buttons, num_keys):
                    button = QtWidgets.QPushButton(self)
                    button.clicked.connect(self.popup_dialog)
                    button.setObjectName(QSS_NAME_HOTKEY)
                    self._vlayout.addWidget(button)
                    self._hotkey_buttons.append(button)
            elif num_keys < num_buttons:
                for i in range(num_keys, num_buttons):
                    self._hotkey_buttons[i].deleteLater()
                self._hotkey_buttons = self._hotkey_buttons[:num_keys]

        locked = not self.is_edit_mode and not self._cfg.get(Vars.key_change, True)
        if change or self._locked is None or self._locked != locked:
            self._locked = locked
            for i, button in enumerate(self._hotkey_buttons):
                button.setText(key_list[i])
                button.setEnabled(not locked)
                if locked:
                    button.setToolTip(HOTKEY_CANNOT_CHANGE)
                elif key_list[i] == '':
                    button.setToolTip(HOTKEY_EMPTY)

        if change:
            self.hotkey_changed.emit(key_list)

    def popup_dialog(self):
        class_name = self.a2.db.get(Vars.dialog_style_setting)
        hotkey_dialog_class = None  # type: QtWidgets.QWidget | None
        if class_name:
            for _class in DIALOG_CLASSES:
                if _class.__name__ == class_name:
                    hotkey_dialog_class = _class
                    break
        if hotkey_dialog_class is None:
            hotkey_dialog_class = DIALOG_DEFAULT

        if isinstance(self.key, str):
            key = self.key
        elif isinstance(self.key, list):
            hotkey_index = self._hotkey_buttons.index(self.sender())
            key = self.key[hotkey_index]
            self._hotkey_index = hotkey_index

        dialog = hotkey_dialog_class(self, key, self.get_scope_cfg_copy())
        dialog.hotkey_set.connect(self._dialog_set_key)
        dialog.show()

    def _dialog_set_key(self, key):
        current_keys = self.get_keys_list()
        current_keys[self._hotkey_index] = key
        self.set_key(current_keys)

    def scope_clicked(self):
        is_global = self._cfg.get(Vars.scope_mode, 0) == 0
        scope_change = self._cfg.get(Vars.scope_change, False)
        if not self.is_edit_mode and not scope_change and is_global:
            from a2widget.a2input_dialog import A2ConfirmDialog

            dialog = A2ConfirmDialog(
                self, SCOPE_GLOBAL_NOCHANGE, SCOPE_TOOLTIP_GLOBAL + SCOPE_CANNOT_CHANGE
            )
            dialog.show()
        else:
            from a2widget.a2hotkey import scope_dialog

            dialog = scope_dialog.ScopeDialog(self, self.get_scope_cfg_copy())
            dialog.okayed.connect(self.on_scope_edit)
            dialog.show()

    def clear(self):
        """
        Sets the hotkey button to '', None aka "nothing".
        """
        self.set_key('')

    @property
    def is_clear(self):
        """
        :return: False if a key is set. True if no key is set.
        :rtype: bool
        """
        return self.key == [''] or self.key == ''

    @property
    def is_edit_mode(self):
        return self._edit_mode

    def set_edit_mode(self, state):
        self._edit_mode = state

    def get_scope_cfg_copy(self):
        current_cfg = {
            Vars.scope: self._cfg.get(Vars.scope, []),
            Vars.scope_mode: self._cfg.get(Vars.scope_mode, 0),
        }
        if self.is_edit_mode:
            current_cfg[Vars.scope_change] = True
        else:
            current_cfg[Vars.scope_change] = self._cfg.get(Vars.scope_change)
        return current_cfg

    def on_scope_edit(self, scope_cfg):
        current_cfg = self.get_scope_cfg_copy()
        if scope_cfg != current_cfg:
            scope_list, scope_mode = scope_cfg[Vars.scope], scope_cfg[Vars.scope_mode]
            self._cfg[Vars.scope] = scope_list
            self._cfg[Vars.scope_mode] = scope_mode
            self.scope_changed.emit(scope_list, scope_mode)
            self.setup_scope_button()

    def setup_scope_button(self):
        """
        selecting the right items for this configuration
        """
        scope_ui_map = (
            (SCOPE_TOOLTIP_GLOBAL, a2ctrl.Icons.scope_global),
            (SCOPE_TOOLTIP_INCLUDE, a2ctrl.Icons.scope),
            (SCOPE_TOOLTIP_EXCLUDE, a2ctrl.Icons.scope_exclude),
        )
        tooltip, icon = scope_ui_map[self._cfg.get(Vars.scope_mode, 0)]

        if not self._cfg.get(Vars.scope_change, False):
            tooltip += SCOPE_CANNOT_CHANGE

        self._scope_button.setIcon(icon)
        self._scope_button.setToolTip(tooltip)

    @property
    def has_empty(self):
        return '' in self.get_keys_list()

    def add_hotkey(self):
        """
        Adds an Empty string to the hotkey list if there is none already.
        """
        keys = self.get_keys_list()
        if '' in keys:
            return
        self.set_key(keys + [''])

    @property
    def has_multiple(self):
        if isinstance(self.key, list) and len(self.key) > 1:
            return True
        return False

    def on_remove_key_action(self):
        key = self.sender().data()
        current_keys = self.get_keys_list()
        current_keys.remove(key)
        self.set_key(current_keys)

    def get_keys_list(self):
        return get_keys_list(self.key)


if __name__ == '__main__':
    import a2widget.demo.hotkey_demo

    a2widget.demo.hotkey_demo.show()
