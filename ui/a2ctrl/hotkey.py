'''
Created on Dec 28, 2015

@author: eRiC
'''
import logging
from PySide import QtCore, QtGui

import ahk
import a2ctrl
import a2core
from a2ctrl import hotkey_edit_ui, hotkey_func, hotkey_scope, connect_cfg_controls


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Draw(a2ctrl.DrawCtrl):
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
        self.label.setMinimumHeight(a2ctrl.lenM)
        self.labelLayout.addWidget(self.label)
        self.labelBoxLayout.addLayout(self.labelLayout)
        self.labelBoxLayout.addItem(QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))
        self.ctrllayout.addLayout(self.labelBoxLayout)

        self.hotkeyListLayout = QtGui.QVBoxLayout()
        self.hotkeyLayout = QtGui.QHBoxLayout()
        self.hotkeyButton = HotKey(self, self.get_user_value(str, 'key'), self.hotkey_change)
        self.hotkeyOption = QtGui.QPushButton()
        self.hotkeyOption.setMaximumSize(QtCore.QSize(a2ctrl.lenM, a2ctrl.lenM))
        self.hotkeyOption.setMinimumSize(QtCore.QSize(a2ctrl.lenM, a2ctrl.lenM))
        self.hotkeyOption.setFlat(True)
        self.hotkeyOption.setText('...')
        self.hotkeyLayout.addWidget(self.hotkeyButton)
        self.hotkeyLayout.addWidget(self.hotkeyOption)
        self.hotkeyButton.setEnabled(self.cfg['keyChange'])

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


class Edit(a2ctrl.EditCtrl):
    """
    TODO: Oh boy... this has so many implications but it has to be done. Let's do it!
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
        self.ui = hotkey_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)

        for label in [self.ui.internalNameLabel, self.ui.displayLabelLabel, self.ui.hotkeyLabel,
                      self.ui.functionLabel, self.ui.scopeLabel]:
            label.setMinimumWidth(a2ctrl.labelW)

        self.ui.hotkeyButton = HotKey(self, cfg.get('key') or '', self.hotkey_change)
        self.ui.hotkeyKeyLayout.insertWidget(0, self.ui.hotkeyButton)
        self.mainWidget.setLayout(self.ui.verticalLayout_2)

        self.check_new_name()
        connect_cfg_controls(self.cfg, self.ui)
        self.func_handler = hotkey_func.Hotkey_Function_Handler(self)
        self.scope_handler = hotkey_scope.Hotkey_Scope_Handler(self)

        self.disablableCheck()
        self.ui.cfg_disablable.clicked.connect(self.disablableCheck)

    def disablableCheck(self):
        """would be useless if hotkey is off by default and cannot be changed"""
        state = self.ui.cfg_disablable.isChecked()
        self.ui.cfg_enabled.setEnabled(state)
        self.ui.cfg_enabled.setChecked(True)

    def hotkey_change(self, newKey):
        self.cfg['key'] = newKey


class HotKey(QtGui.QPushButton):
    def __init__(self, parent=None, key=None, ok_func=None):
        # i'd love to use super here. But it introduces problems with reload
        #super(HotKey, self).__init__()
        QtGui.QPushButton.__init__(self)
        self.setMinimumHeight(a2ctrl.lenM)
        self.setMaximumHeight(a2ctrl.lenM)
        self.setStyleSheet('QPushButton {background-color:#FFC23E}')
        self.key = key
        self.tempKey = key
        self.tempOK = True
        self.ok_func = ok_func
        self.setFont(a2ctrl.fontXL)
        self.setText(key)

    def set_key(self, key):
        self.key = key
        self.setText(key)

    def mousePressEvent(self, event):
        self.buildPopup(event.globalX(), event.globalY())

    def buildPopup(self, x, y):
        self.popup = a2ctrl.Popup(x, y, self)
        self.popup.textEdit = QtGui.QLineEdit(self.popup)
        self.popup.textEdit.setFont(a2ctrl.fontXL)
        self.popup.textEdit.setText(self.key)
        self.popup.textEdit.textChanged.connect(self.validateHotkey)
        self.popup.textEdit.returnPressed.connect(self.ok)

        self.popup.buttonLyt = QtGui.QHBoxLayout()
        self.popup.okButton = QtGui.QPushButton("OK")
        self.popup.okButton.clicked.connect(self.ok)
        self.popup.closeButton = QtGui.QPushButton("&Cancel")
        self.popup.closeButton.clicked.connect(self.popup.close)
        self.popup.buttonLyt.addWidget(self.popup.okButton)
        self.popup.buttonLyt.addWidget(self.popup.closeButton)

        self.popup.layout = QtGui.QVBoxLayout()
        self.popup.layout.addWidget(self.popup.textEdit)
        self.popup.layout.addLayout(self.popup.buttonLyt)
        self.popup.setLayout(self.popup.layout)
        self.validateHotkey(self.key)

        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Enter), self.popup, self.ok)

        self.popup.show()
        self.popup.placeAtCursor()

    def ok(self):
        log.info('key: %s' % self.tempKey)
        log.info('ok: %s' % self.tempOK)
        if self.tempOK:
            self.set_key(self.tempKey)
            self.popup.close()
            self.ok_func(self.key)

    def validateHotkey(self, hkstring):
        """
        first implementation: checks for valid modifyers + a single key
        TODO: handle F1-F12, Del, Home...
              handle single keys when in scope,
              check availability ...
        """
        styleBad = '* {color:#F00}'
        styleGood = '* {color:#0F0}'
        good = False
        hkparts = hkstring.split('+')
        key = hkparts[-1].strip().lower()
        modifier = []
        tilde = ''
        # TODO: implement check for joystick keys and scancodes: 2joy4, SCnnn
        # http://www.autohotkey.com/docs/KeyList.htm#SpecialKeys
        if len(key) != 1 and key not in ahk.keys:
            msg = 'Invalid key! (%s)' % key
        elif len(hkparts) == 1:
            good = True
        else:
            modifier = [k.strip().lower() for k in hkparts[:-1]]
            if modifier[0].startswith('~'):
                tilde = '~'
                modifier[0] = modifier[0][1:]
            badModifier = [k for k in modifier if k not in ahk.modifiers]
            if badModifier:
                msg = ('Modifyer not one of Win, Ctrl, Alt or Shift! (%s)' % ', '.join(badModifier))
            else:
                good = True

        if not good:
            self.popup.textEdit.setStyleSheet(styleBad)
            log.error(msg)
        else:
            modifier = [k.title() for k in modifier]
            key = key.title()
            self.tempKey = tilde + '+'.join(modifier + [key])
            log.info('tempKey %s:' % self.tempKey)
            self.popup.textEdit.setStyleSheet(styleGood)

        self.tempOK = good
