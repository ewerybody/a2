from PySide import QtCore, QtGui

import a2ctrl
import a2core
from a2element import DrawCtrl, EditCtrl
from a2widget.a2hotkey import A2Hotkey
from functools import partial


log = a2core.get_logger(__name__)
DEFAULT_HOTKEY = 'Win+F'


class Draw(DrawCtrl):
    """
    User ui for a Hotkey control.
    shows: label, checkbox if disablable, shortcut(s), controls to add, remove
        additional shortcuts, controls to change scope if that's enabled...

    cfg['label'] == 'Hotkeytest with a MsgBox'
    cfg['typ'] == 'hotkey':
    cfg['name'] == 'modnameHotkey1'
    cfg['enabled'] = True
    cfg['disablable'] = True
    cfg['key'] = 'Win+G'
    cfg['keyChange'] = True
    cfg['multiple'] = True
    cfg['scope'] = ''
    cfg['scopeChange'] = True
    # functionMode can be: ahk, file, key: to execute code, open up sth, send keystroke
    cfg['functionMode'] = 'ahk'
    """
    def __init__(self, main, cfg, mod):
        super(Draw, self).__init__(main, cfg, mod)
        self.hotkey_option_menu = QtGui.QMenu(self)
        self._setup_ui()

    def _setup_hotkey(self):
        self.hotkey_button.set_key(self.get_user_value(str, 'key'))
        self.hotkey_button.set_config(self.cfg)

    def _setup_ui(self):
        self.ctrl_layout = QtGui.QHBoxLayout(self)
        # left, top, right, bottom
        self.ctrl_layout.setContentsMargins(0, 0, 0, 0)
        self.labelBoxLayout = QtGui.QVBoxLayout()
        self.labelBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.labelLayout = QtGui.QHBoxLayout()

        if self.cfg['disablable']:
            state = self.get_user_value(bool, 'enabled', True)
            self.check = QtGui.QCheckBox(self)

            try:
                size = self.main.css_values['icon_size']
            except AttributeError:
                size = 35

            self.check.setMinimumSize(QtCore.QSize(size, size))
            self.check.setMaximumSize(QtCore.QSize(size, size))

            self.check.setChecked(state)
            self.check.clicked.connect(self.hotkey_check)
            self.labelLayout.addWidget(self.check)

        self.label = QtGui.QLabel(self.cfg.get('label') or '', self)
        self.label.setWordWrap(True)
        self.labelLayout.addWidget(self.label)
        self.labelBoxLayout.addLayout(self.labelLayout)
        self.ctrl_layout.addLayout(self.labelBoxLayout)

        self.hotkey_list_layout = QtGui.QVBoxLayout()
        self.hotkey_layout = QtGui.QHBoxLayout()
        self.hotkey_button = A2Hotkey(self)
        self._setup_hotkey()
        self.hotkey_button.hotkey_changed.connect(self.hotkey_change)
        self.hotkey_layout.addWidget(self.hotkey_button)

        self.a2option_button = QtGui.QToolButton(self)
        self.a2option_button.setArrowType(QtCore.Qt.DownArrow)
        self.a2option_button.setAutoRaise(True)
        self.a2option_button.setObjectName('a2option_button')
        self.a2option_button.clicked.connect(self.build_hotkey_options_menu)
        self.hotkey_layout.addWidget(self.a2option_button)

        self.hotkey_list_layout.addLayout(self.hotkey_layout)
        self.ctrl_layout.addLayout(self.hotkey_list_layout)
        self.ctrl_layout.setStretch(2, 1)
        self.setLayout(self.ctrl_layout)

    def hotkey_check(self):
        state = self.check.isChecked()
        self.set_user_value(state, 'enabled')
        self.change('hotkeys')

    def hotkey_change(self, newKey):
        self.set_user_value(newKey, 'key')
        self.change('hotkeys')

    def build_hotkey_options_menu(self):
        menu = self.hotkey_option_menu
        menu.clear()
        action = menu.addAction('Add another Hotkey')
        action.setEnabled(False)
        action = menu.addAction('Revert to Default')
        action.setEnabled(False)

        if not self.hotkey_button.is_clear():
            menu.addAction(a2ctrl.Icons.inst().clear, 'Clear Hotkey',
                           self.hotkey_button.clear)

        menu.addSeparator()

        submenu = QtGui.QMenu('Hotkey Dialog Style', menu)
        current_style = self.a2.db.get('hotkey_dialog_style') or ''
        for hotkey_dialog_style in self.hotkey_button.dialog_styles:
            this_name = hotkey_dialog_style.__name__
            action = submenu.addAction(hotkey_dialog_style.label)
            action.setCheckable(True)
            action.setChecked(current_style == this_name)
            action.triggered.connect(partial(self.a2.db.set, 'hotkey_dialog_style', this_name))

        menu.addMenu(submenu)
        menu.popup(QtGui.QCursor.pos())


class Edit(EditCtrl):
    """
    Oh boy... this has so many implications but it has to be done. Let's do it!
    First: Have the edit ctrl, then the display one, Then we need checks when a mod
    config change is about to be comitted. The change will not be able to be OKed as long
    as there are conflicts with hotkeys, or missing includes or ...

    elif cfg['typ'] == 'hotkey':
        cfg['enabled'] = True
        cfg['disablable'] = True
        cfg['key'] = 'Win+G'
        cfg['keyChange'] = True
        cfg['multiple'] = True
        cfg['scope'] = ''
        cfg['scopeChange'] = True
        # functionMode can be: ahk, file, key
        # to execute code, open up sth, send keystroke
        cfg['functionMode'] = 'ahk',
        cfg['name'] = 'someModule_hotkey1',
        cfg['label'] = 'do awesome stuff on:'
    """
    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg, add_layout=False)

        # deferred because pretty huge & not needed by non dev users
        from a2widget.a2hotkey import edit_widget_ui, edit_func_widget_ui
        for module in [edit_func_widget_ui, edit_widget_ui]:
            a2ctrl.check_ui_module(module)

        self.ui = edit_widget_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)

        for key, value in [('key', DEFAULT_HOTKEY), ('functionMode', 'ahk')]:
            if key not in self.cfg:
                self.cfg[key] = value

        self.helpUrl = self.a2.urls.helpHotkey

        self.ui.hotkey_button.set_key(cfg.get('key') or '')
        self.ui.hotkey_button.hotkey_changed.connect(self.hotkey_change)

        self.check_new_name()
        a2ctrl.connect.cfg_controls(self.cfg, self.ui)
        a2ctrl.connect.cfg_controls(self.cfg, self.ui.func_widget.ui)
        self.ui.func_widget.set_config(self.cfg)

        # a2ctrl.connect.cfg_controls(self.cfg, self.ui.scope_widget.ui)
        # self.ui.scope_widget.set_config(self.cfg)

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


def get_settings(module_key, cfg, db_dict, user_cfg):
    key = a2ctrl.get_cfg_value(cfg, user_cfg, 'key', str)
    scope = a2ctrl.get_cfg_value(cfg, user_cfg, 'scope', list)
    scope_mode = a2ctrl.get_cfg_value(cfg, user_cfg, 'scopeMode', int)
    function = cfg.get(
        ['functionCode', 'functionURL', 'functionSend'][
            cfg['functionMode']],
        '')

    db_dict.setdefault('hotkeys', {})
    db_dict['hotkeys'].setdefault(scope_mode, [])
    # save a global if global scope set or all-but AND scope is empty
    if scope_mode == 0 or scope_mode == 2 and scope == '':
        db_dict['hotkeys'][0].append([key, function])
    else:
        db_dict['hotkeys'][scope_mode].append([scope, key, function])
