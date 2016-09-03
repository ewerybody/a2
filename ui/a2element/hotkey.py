'''
Created on Dec 28, 2015

@author: eRiC
'''
from PySide import QtCore, QtGui

import ahk
import a2ctrl
import a2core
from a2element import hotkey_func, hotkey_scope, DrawCtrl, EditCtrl
from a2widget.a2hotkey import A2Hotkey


hotkey_edit_ui = None
log = a2core.get_logger(__name__)


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
    # mode can be: ahk, file, key: to execute code, open up sth, send keystroke
    cfg['mode'] = 'ahk'
    """
    def __init__(self, main, cfg, mod):
        super(Draw, self).__init__(main, cfg, mod)
        self._setupUi()

    def _setupUi(self):
        self.ctrllayout = QtGui.QHBoxLayout(self)
        # left, top, right, bottom
        self.ctrllayout.setContentsMargins(0, 0, 0, 0)
        self.labelBoxLayout = QtGui.QVBoxLayout()
        self.labelBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.labelLayout = QtGui.QHBoxLayout()
        if self.cfg['disablable']:
            state = self.get_user_value(bool, 'enabled', True)
            self.check = QtGui.QCheckBox(self)
            cbSize = 27
            self.check.setMinimumSize(QtCore.QSize(cbSize, cbSize))
            self.check.setMaximumSize(QtCore.QSize(cbSize, cbSize))
            self.check.setChecked(state)
            self.check.clicked.connect(self.hotkey_check)
            self.labelLayout.addWidget(self.check)
        self.label = QtGui.QLabel(self.cfg.get('label') or '', self)
        self.label.setWordWrap(True)
        self.labelLayout.addWidget(self.label)
        self.labelBoxLayout.addLayout(self.labelLayout)
        self.labelBoxLayout.addItem(QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))
        self.ctrllayout.addLayout(self.labelBoxLayout)

        self.hotkeyListLayout = QtGui.QVBoxLayout()
        self.hotkeyLayout = QtGui.QHBoxLayout()
        self.hotkeyButton = A2Hotkey(self, self.get_user_value(str, 'key'), self.hotkey_change)
        self.hotkeyButton.setEnabled(self.cfg['keyChange'])
        self.hotkeyLayout.addWidget(self.hotkeyButton)

        self.hotkeyOption = QtGui.QPushButton()
        self.hotkeyOption.setFlat(True)
        self.hotkeyOption.setText('...')
        self.hotkeyLayout.addWidget(self.hotkeyOption)

        self.hotkeyListLayout.addLayout(self.hotkeyLayout)
        self.hotkeyListLayout.addItem(QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))
        self.ctrllayout.addLayout(self.hotkeyListLayout)
        self.ctrllayout.setStretch(2, 1)
        self.setLayout(self.ctrllayout)

    def hotkey_check(self):
        state = self.check.isChecked()
        self.set_user_value(state, 'enabled')
        self.change('hotkeys')

    def hotkey_change(self, newKey):
        self.set_user_value(newKey, 'key')
        self.change('hotkeys')


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
        # mode can be: ahk, file, key
        # to execute code, open up sth, send keystroke
        cfg['mode'] = 'ahk',
        cfg['name'] = 'someModule_hotkey1',
        cfg['label'] = 'do awesome stuff on:'
    """
    def __init__(self, cfg, main, parentCfg):
        self.ctrlType = 'Hotkey'
        super(Edit, self).__init__(cfg, main, parentCfg, addLayout=False)
        defaults = [('key', 'Win+G'), ('mode', 'ahk')]
        for key, value in defaults:
            if key not in self.cfg:
                self.cfg[key] = value

        self.a2 = a2core.A2Obj.inst()
        self.helpUrl = self.a2.urls.helpHotkey

        global hotkey_edit_ui
        if hotkey_edit_ui is None:
            from a2element import hotkey_edit_ui
        if main.dev_mode:
            a2ctrl.check_ui_module(hotkey_edit_ui)

        self.ui = hotkey_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)

        self.ui.hotkey_button.set_key(cfg.get('key') or '')
        self.ui.hotkey_button.ok_func = self.hotkey_change

        self.check_new_name()
        a2ctrl.connect.cfg_controls(self.cfg, self.ui)
        self.func_handler = hotkey_func.Hotkey_Function_Handler(self)
        self.scope_handler = hotkey_scope.Hotkey_Scope_Handler(self)

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

    def hotkey_change(self, newKey):
        self.cfg['key'] = newKey
