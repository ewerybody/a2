import a2core
from PySide import QtGui, QtCore

import a2ctrl
from a2widget.a2hotkey.simple_dialog import HotkeyDialog1
from a2widget.a2hotkey.dialogs import HotKeyBoard

SCOPE_TOOLTIP_GLOBAL = 'Hotkey scope is set "global" so it works anywhere.'
SCOPE_TOOLTIP_INCLUDE = 'Hotkey scope is set to work only in specific windows.'
SCOPE_TOOLTIP_EXCLUDE = 'Hotkey scope is set to exclude specific windows.'
SCOPE_CANNOT_CHANGE = '\nThis cannot be changed!'
SCOPE_GLOBAL_NOCHANGE = 'Global - unchangable'


class Vars(object):
    scope = 'scope'
    scope_mode = 'scopeMode'
    scope_change = 'scopeChange'


class A2Hotkey(QtGui.QWidget):
    hotkey_changed = QtCore.Signal(str)
    scope_changed = QtCore.Signal(dict)

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
        self._cfg = None
        self._edit_mode = False
        self.scope_data = scope_data

        self._layout = QtGui.QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._hotkey_button = QtGui.QPushButton(self)
        self._hotkey_button.setObjectName('A2HotkeyButton')
        self._scope_button = QtGui.QPushButton(self)
        self._scope_button.setObjectName('A2HotkeyScope')
        self._layout.addWidget(self._hotkey_button)
        self._layout.addWidget(self._scope_button)
        self._scope_button.clicked.connect(self.scope_clicked)
        self._hotkey_button.clicked.connect(self.popup_dialog)
        self.setText(key)

        self.dialog_styles = [HotKeyBoard]
        self.dialog_default = HotkeyDialog1
        self.dialog_styles.append(self.dialog_default)
        self.set_config(None)

    def set_config(self, config_dict):
        self._cfg = config_dict or {}

        # selecting the right items for this configuration
        tooltip, icon = [
            (SCOPE_TOOLTIP_GLOBAL, a2ctrl.Icons.inst().scope_global),
            (SCOPE_TOOLTIP_INCLUDE, a2ctrl.Icons.inst().scope),
            (SCOPE_TOOLTIP_EXCLUDE, a2ctrl.Icons.inst().scope_exclude)][
            self._cfg.get(Vars.scope_mode, 0)]

        if self._cfg.get(Vars.scope_change, True):
            tooltip += SCOPE_CANNOT_CHANGE

        self._scope_button.setIcon(icon)
        self._scope_button.setToolTip(tooltip)
        self.key = self._cfg.get('key', '')
        self.setText(self.key)

    def setText(self, text):
        self._hotkey_button.setText(text)

    def set_key(self, key):
        if key != self.key:
            self.key = key
            self.setText(key)
            self.hotkey_changed.emit(key)

    def popup_dialog(self):
        class_name = self.a2.db.get('hotkey_dialog_style')
        hotkey_dialog_class = None  # type: class
        if class_name:
            for hotkey_dialog_class in self.dialog_styles:
                if hotkey_dialog_class.__name__ == class_name:
                    break
        if hotkey_dialog_class is None:
            hotkey_dialog_class = self.dialog_default

        dialog = hotkey_dialog_class(self, self.key, self.scope_data)
        dialog.hotkey_set.connect(self.set_key)
        dialog.show()

    def build_scope_menu(self):
        # TODO: we might not need this
        menu = QtGui.QMenu(self)
        mode = self._cfg.get(Vars.scope_mode, 0)
        if not self.is_edit_mode and not self._cfg.get(Vars.scope_change, True):
            pass
        if mode == 0:
            menu.addAction('global!')
        elif mode == 1:
            menu.addAction('scope only in ...')
        else:
            menu.addAction('scope not in ...')
        menu.popup(QtGui.QCursor.pos())

    def scope_clicked(self):
        is_global = self._cfg.get(Vars.scope_mode, 0) == 0
        scope_change = self._cfg.get(Vars.scope_change, True)
        if not self.is_edit_mode and not scope_change and is_global:
            from a2widget import A2ConfirmDialog
            dialog = A2ConfirmDialog(self, SCOPE_GLOBAL_NOCHANGE, SCOPE_TOOLTIP_GLOBAL + SCOPE_CANNOT_CHANGE)
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
        return self.key == ''

    @property
    def is_edit_mode(self):
        return self._edit_mode

    def set_edit_mode(self, state):
        self._edit_mode = state

    def get_scope_cfg_copy(self):
        current_cfg = {Vars.scope: self._cfg.get(Vars.scope),
                       Vars.scope_mode: self._cfg.get(Vars.scope_mode)}
        if self.is_edit_mode:
            current_cfg[Vars.scope_change] = True
        else:
            current_cfg[Vars.scope_change] = self._cfg.get(Vars.scope_change)
        return current_cfg

    def on_scope_edit(self, scope_cfg):
        current_cfg = self.get_scope_cfg_copy()
        if scope_cfg != current_cfg:
            self._cfg[Vars.scope] = scope_cfg[Vars.scope]
            self._cfg[Vars.scope_mode] = scope_cfg[Vars.scope_mode]
            self.scope_changed.emit(scope_cfg)


if __name__ == '__main__':
    import a2widget.demo.scope_demo
    a2widget.demo.scope_demo.show()
