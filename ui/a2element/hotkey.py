"""
A hotkey configuration can have a lot of stuff to it:

 cfg['typ'] == 'hotkey':
 cfg['enabled'] = True
 cfg['disablable'] = True
 cfg['key'] = 'Win+G'
 cfg['keyChange'] = True
 cfg['multiple'] = True
 cfg['scope'] = ''
 cfg['scopeChange'] = True
 # functionMode can be: ahk, file, key
 # to execute 0: code, 1: run/open up sth, 2: send keystroke
 cfg['functionMode'] = 0,
 cfg['name'] = 'someModule_hotkey1',
 cfg['label'] = 'do awesome stuff on:'

"""

from a2qt import QtCore, QtGui, QtWidgets

import a2uic
import a2core
import a2ctrl.connect
import a2util
from a2element import DrawCtrl, EditCtrl
from a2widget import a2hotkey
from a2widget.a2hotkey.hotkey_common import Vars, SEND_MODES, strip_mode
from a2widget.a2more_button import A2MoreButton


log = a2core.get_logger(__name__)


class Draw(DrawCtrl):
    """
    User ui for a Hotkey control.
    shows: label, checkbox if disablable, shortcut(s), controls to add, remove
        additional shortcuts, controls to change scope if that's enabled...
    """
    changed = QtCore.Signal()

    def __init__(self, *args):
        super(Draw, self).__init__(*args)
        self._setup_ui()

    def _setup_hotkey(self):
        user_dict = self.ctrl.get_user_dict()
        self.hotkey_button.set_config(user_dict)

    def _setup_ui(self):
        self.ctrl_layout = QtWidgets.QHBoxLayout(self)
        # left, top, right, bottom
        self.ctrl_layout.setContentsMargins(0, 0, 0, 0)
        self.labelBoxLayout = QtWidgets.QVBoxLayout()
        self.labelBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.labelLayout = QtWidgets.QHBoxLayout()

        if self.ctrl.cfg.get('disablable', True):
            state = self.ctrl.get_user_value(bool, 'enabled', True)
            self.checkbox = QtWidgets.QCheckBox(self)

            try:
                size = self.ctrl.main.style.get('icon_size')
            except AttributeError:
                size = 35

            self.checkbox.setMinimumSize(QtCore.QSize(size, size))
            self.checkbox.setMaximumSize(QtCore.QSize(size, size))

            self.checkbox.setChecked(state)
            self.checkbox.clicked.connect(self.hotkey_check)
            self.labelLayout.addWidget(self.checkbox)

        self.label = QtWidgets.QLabel(self.ctrl.cfg.get('label') or '', self)
        self.label.setWordWrap(True)
        self.labelLayout.addWidget(self.label)
        self.labelBoxLayout.addLayout(self.labelLayout)
        self.ctrl_layout.addLayout(self.labelBoxLayout)

        self.hotkey_list_layout = QtWidgets.QVBoxLayout()
        self.hotkey_layout = QtWidgets.QHBoxLayout()
        self.hotkey_button = a2hotkey.A2Hotkey(self)
        self._setup_hotkey()
        self.hotkey_button.hotkey_changed.connect(self.hotkey_change)
        self.hotkey_button.scope_changed.connect(self.scope_change)
        self.hotkey_layout.addWidget(self.hotkey_button)

        self.a2option_button = A2MoreButton(self)
        self.a2option_button.menu_called.connect(self.build_hotkey_options_menu)
        self.hotkey_layout.addWidget(self.a2option_button)

        self.hotkey_list_layout.addLayout(self.hotkey_layout)
        self.ctrl_layout.addLayout(self.hotkey_list_layout)
        self.ctrl_layout.setStretch(2, 1)
        self.setLayout(self.ctrl_layout)

    def hotkey_check(self):
        state = self.checkbox.isChecked()
        self.ctrl.set_user_value(state, 'enabled')
        self.ctrl.change('hotkeys')
        self.changed.emit()

    def hotkey_change(self, new_keys):
        self.ctrl.set_user_value(new_keys, 'key')
        self.ctrl.change('hotkeys')
        self.changed.emit()

    def scope_change(self, scope, scope_mode):
        self.ctrl.set_user_value(scope, 'scope')
        self.ctrl.set_user_value(scope_mode, 'scopeMode')
        self.ctrl.change('hotkeys')
        self.changed.emit()

    def build_hotkey_options_menu(self, menu):
        if self.ctrl.has_user_cfg():
            menu.addAction('Revert to Default', self.ctrl.clear_user_cfg)

        if self.ctrl.cfg.get(Vars.key_change, True):
            build_hotkey_menu(menu, self.hotkey_button)

        menu.addSeparator()

        submenu = QtWidgets.QMenu('Hotkey Dialog Style', menu)
        current_style = a2hotkey.get_current_style()
        for name, label in a2hotkey.iter_dialog_styles():
            action = submenu.addAction(label)
            action.setCheckable(True)
            action.setChecked(current_style == name)
            action.triggered.connect(self._on_hotkey_dialog_style_change)
        menu.addMenu(submenu)

    def _on_hotkey_dialog_style_change(self):
        action = self.sender()
        if isinstance(action, QtGui.QAction):
            a2hotkey.set_dialog_style(action.text())

    def set_config(self, cfg):
        """For manual re-configuration! Set ALL the sub-elements in one go:
        Checkbox, Hotkey and Scope-widget."""
        self.user_cfg = cfg
        self.checkbox.blockSignals(True)
        self.hotkey_button.blockSignals(True)
        self.hotkey_button.set_config(cfg)
        self.checkbox.setChecked(cfg.get('enabled', True))
        self.checkbox.blockSignals(False)
        self.hotkey_button.blockSignals(False)


class Edit(EditCtrl):
    """
    Oh boy... this has so many implications but it has to be done. Let's do it!
    First: Have the edit ctrl, then the display one, Then we need checks when a mod
    config change is about to be committed. The change will not be able to be OKed as long
    as there are conflicts with hotkeys, or missing includes or ...
    """

    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg, add_layout=False)
        self.cfg.setdefault('name', '')
        # deferred because pretty huge & not needed by non dev users
        from a2widget.a2hotkey import edit_widget_ui, edit_func_widget_ui

        for module in [edit_func_widget_ui, edit_widget_ui]:
            a2uic.check_module(module)

        self.ui = edit_widget_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)

        self.ui.hotkey_button.set_edit_mode(True)
        self.ui.hotkey_button.set_config(self.cfg)
        self.ui.hotkey_button.hotkey_changed.connect(self.hotkey_change)

        self.ui.a2option_button.menu_called.connect(self.build_edit_menu)

        a2ctrl.connect.cfg_controls(self.cfg, self.ui)
        a2ctrl.connect.cfg_controls(self.cfg, self.ui.func_widget.ui)
        self.ui.func_widget.set_config(self.cfg)

        self.disablable_check()
        self.ui.cfg_disablable.clicked[bool].connect(self.disablable_check)

    def disablable_check(self, state=None):
        """Would be useless if hotkey is off by default and cannot be changed."""
        if state is None:
            # happens only initially
            if not self.cfg['disablable']:
                self.cfg['enabled'] = True
                self.ui.cfg_enabled.setEnabled(False)
                self.ui.cfg_enabled.setChecked(True)
        else:
            self.ui.cfg_enabled.setEnabled(state)
            self.ui.cfg_enabled.setChecked(True)

    def hotkey_change(self, new_keys):
        self.cfg['key'] = new_keys

    def build_edit_menu(self, menu):
        build_hotkey_menu(menu, self.ui.hotkey_button)

    @staticmethod
    def element_name():
        return 'Hotkey'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().keyboard


def hotkey_help():
    a2 = a2core.A2Obj.inst()
    a2util.surf_to(a2.urls.helpHotkey)


def build_hotkey_menu(menu, button):
    icons = a2ctrl.Icons.inst()
    if not button.has_empty:
        menu.addAction(icons.list_add, 'Add another Hotkey', button.add_hotkey)
    if button.has_multiple:
        del_menu = menu.addMenu(icons.delete, 'Remove Hotkey')
        for key in button.get_keys_list():
            name = key if key != '' else '"" (Empty)'
            action = del_menu.addAction(icons.delete, name, button.on_remove_key_action)
            action.setData(key)
    else:
        if not button.is_clear:
            menu.addAction(icons.clear, 'Clear Hotkey', button.clear)

    menu.addAction(icons.help, 'Help on Hotkey Setup', hotkey_help)


def get_settings(module_key, cfg, db_dict, user_cfg):
    key = a2ctrl.get_cfg_value(cfg, user_cfg, 'key')
    if not key or key == ['']:
        return
    if not a2ctrl.get_cfg_value(cfg, user_cfg, 'enabled', bool):
        return

    scope = a2ctrl.get_cfg_value(cfg, user_cfg, Vars.scope, list)
    scope_mode = a2ctrl.get_cfg_value(cfg, user_cfg, Vars.scope_mode, int)
    code = cfg.get(
        [Vars.function_code, Vars.function_url, Vars.function_send][cfg.get(Vars.function_mode, 0)],
        '',
    )

    # Avoid setting hotstrings with no code on send modes (`Send, `).
    _code, _ = strip_mode(code, SEND_MODES)
    if not _code.strip():
        log.warning('Empty Send code on "%s" hotkey (%s): "%s"', module_key, key, code)
        return

    db_dict.setdefault('hotkeys', {})
    db_dict['hotkeys'].setdefault(scope_mode, [])
    # save a global if global scope set or all-but AND scope is empty
    if scope_mode == 0 or scope_mode == 2 and scope == '':
        db_dict['hotkeys'][0].append([key, code])
    else:
        db_dict['hotkeys'][scope_mode].append([scope, key, code])
