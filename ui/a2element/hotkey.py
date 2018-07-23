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

from PySide2 import QtCore, QtWidgets

import a2ctrl
import a2core
from a2element import DrawCtrl, EditCtrl
from a2widget import A2MoreButton
from a2widget.a2hotkey import A2Hotkey, Vars
from functools import partial


log = a2core.get_logger(__name__)


class Draw(DrawCtrl):
    """
    User ui for a Hotkey control.
    shows: label, checkbox if disablable, shortcut(s), controls to add, remove
        additional shortcuts, controls to change scope if that's enabled...
    """
    def __init__(self, *args):
        super(Draw, self).__init__(*args)
        self._setup_ui()

    def _setup_hotkey(self):
        user_dict = self.get_user_dict()
        self.hotkey_button.set_config(user_dict)

    def _setup_ui(self):
        self.ctrl_layout = QtWidgets.QHBoxLayout(self)
        # left, top, right, bottom
        self.ctrl_layout.setContentsMargins(0, 0, 0, 0)
        self.labelBoxLayout = QtWidgets.QVBoxLayout()
        self.labelBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.labelLayout = QtWidgets.QHBoxLayout()

        if self.cfg['disablable']:
            state = self.get_user_value(bool, 'enabled', True)
            self.checkbox = QtWidgets.QCheckBox(self)

            try:
                size = self.main.style.get('icon_size')
            except AttributeError:
                size = 35

            self.checkbox.setMinimumSize(QtCore.QSize(size, size))
            self.checkbox.setMaximumSize(QtCore.QSize(size, size))

            self.checkbox.setChecked(state)
            self.checkbox.clicked.connect(self.hotkey_check)
            self.labelLayout.addWidget(self.checkbox)

        self.label = QtWidgets.QLabel(self.cfg.get('label') or '', self)
        self.label.setWordWrap(True)
        self.labelLayout.addWidget(self.label)
        self.labelBoxLayout.addLayout(self.labelLayout)
        self.ctrl_layout.addLayout(self.labelBoxLayout)

        self.hotkey_list_layout = QtWidgets.QVBoxLayout()
        self.hotkey_layout = QtWidgets.QHBoxLayout()
        self.hotkey_button = A2Hotkey(self)
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
        self.set_user_value(state, 'enabled')
        self.change('hotkeys')

    def hotkey_change(self, new_key):
        self.set_user_value(new_key, 'key')
        self.change('hotkeys')

    def scope_change(self, scope, scope_mode):
        self.set_user_value(scope, 'scope')
        self.set_user_value(scope_mode, 'scopeMode')
        self.change('hotkeys')

    def build_hotkey_options_menu(self, menu):
        action = menu.addAction('Add another Hotkey')
        action.setEnabled(False)
        if self.has_user_cfg():
            menu.addAction('Revert to Default', self.clear_user_cfg)

        if self.cfg.get(Vars.key_change, True) and not self.hotkey_button.is_clear:
            menu.addAction(a2ctrl.Icons.inst().clear, 'Clear Hotkey',
                           self.hotkey_button.clear)

        menu.addSeparator()

        submenu = QtWidgets.QMenu('Hotkey Dialog Style', menu)
        current_style = self.a2.db.get('hotkey_dialog_style') or ''
        for hotkey_dialog_style in self.hotkey_button.dialog_styles:
            this_name = hotkey_dialog_style.__name__
            action = submenu.addAction(hotkey_dialog_style.label)
            action.setCheckable(True)
            action.setChecked(current_style == this_name)
            action.triggered.connect(partial(self.a2.db.set, 'hotkey_dialog_style', this_name))

        menu.addMenu(submenu)


class Edit(EditCtrl):
    """
    Oh boy... this has so many implications but it has to be done. Let's do it!
    First: Have the edit ctrl, then the display one, Then we need checks when a mod
    config change is about to be committed. The change will not be able to be OKed as long
    as there are conflicts with hotkeys, or missing includes or ...
    """
    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg, add_layout=False)

        # deferred because pretty huge & not needed by non dev users
        from a2widget.a2hotkey import edit_widget_ui, edit_func_widget_ui
        for module in [edit_func_widget_ui, edit_widget_ui]:
            a2ctrl.check_ui_module(module)

        self.ui = edit_widget_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)

        self.helpUrl = self.a2.urls.helpHotkey

        self.ui.hotkey_button.set_edit_mode(True)
        self.ui.hotkey_button.set_config(self.cfg)
        self.ui.hotkey_button.hotkey_changed.connect(self.hotkey_change)

        self.check_new_name()
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

    def hotkey_change(self, new_key):
        self.cfg['key'] = new_key

    @staticmethod
    def element_name():
        return 'Hotkey'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().hotkey


def get_settings(_module_key, cfg, db_dict, user_cfg):
    key = a2ctrl.get_cfg_value(cfg, user_cfg, 'key', str)
    scope = a2ctrl.get_cfg_value(cfg, user_cfg, Vars.scope, list)
    scope_mode = a2ctrl.get_cfg_value(cfg, user_cfg, Vars.scope_mode, int)
    func = cfg.get(
        [Vars.function_code, Vars.function_url, Vars.function_send]
        [cfg.get(Vars.function_mode, 0)],
        '')

    db_dict.setdefault('hotkeys', {})
    db_dict['hotkeys'].setdefault(scope_mode, [])
    # save a global if global scope set or all-but AND scope is empty
    if scope_mode == 0 or scope_mode == 2 and scope == '':
        db_dict['hotkeys'][0].append([key, func])
    else:
        db_dict['hotkeys'][scope_mode].append([scope, key, func])
