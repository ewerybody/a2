"""
Created on 11.09.2017

@author: eric
"""
from enum import Enum
from pprint import pprint

import a2ahk
import a2ctrl
import a2core
import a2widget.keyboard.base_ui
from PySide import QtGui, QtCore


log = a2core.get_logger('keyboard_base')
KEYFONT_SIZE_FACTOR = 0.9
STYLE_BUTTON = """
    QPushButton {
        font-size: %(font-size)ipx;
        padding: 3px;
        min-width: 15px;
        min-height: 22px;
        max-height: 22px;
    }
    """
#    padding-left: 0px;
#    padding-right: 0px;


class KeyboardDialogBase(QtGui.QDialog):
    def __init__(self, parent):
        super(KeyboardDialogBase, self).__init__(parent)
        self.setModal(True)

        self.a2 = a2core.A2Obj.inst()
        self.keydict = {}
        self.modifier = {}

        self._setup_ui()
        self._fill_keydict()

        self._toggle_numpad()
        self._toggle_mouse()

    def _setup_ui(self):
        a2ctrl.check_ui_module(a2widget.keyboard.base_ui)
        self.ui = a2widget.keyboard.base_ui.Ui_Keyboard()
        self.ui.setupUi(self)

        global STYLE_BUTTON
        font_size = self.a2.win.css_values['font_size'] * KEYFONT_SIZE_FACTOR
        STYLE_BUTTON = STYLE_BUTTON % {'font-size': font_size}
        self.ui.keys_widget.setStyleSheet(STYLE_BUTTON)

        self.ui.left.setText('←')
        self.ui.up.setText('↑')
        self.ui.down.setText('↓')
        self.ui.right.setText('→')

        for i in range(1, 13):
            self.add_key('f%i' % i, self.ui.f_row)

        for i in range(0, 10):
            self.insert_key(i, str(i), self.ui.number_row)

        self.insert_key(10, '0', self.ui.number_row)

        self.ui.check_numpad.clicked[bool].connect(self._toggle_numpad)
        self.ui.check_mouse.clicked[bool].connect(self._toggle_mouse)

    def insert_key(self, index, key, layout, label=None, tooltip=None):
        button = self._create_key(key, label, tooltip)
        layout.insertWidget(index, button)

    def add_key(self, key, layout, label=None, tooltip=None):
        button = self._create_key(key, label, tooltip)
        layout.addWidget(button)

    def _create_key(self, key, label, tooltip):
        """
        A key can have different things:
        * printed on it
        * as dictionary name
        #* as an internal name
        * showing as a tooltip
        """
        # name = key + '_key'
        button = QtGui.QPushButton(self.ui.keys_widget)
        # button.setObjectName(name)
        # setattr(self.ui, name, button)

        if label:
            button.setText(label)
        else:
            button.setText(key.upper())

        if tooltip:
            button.setToolTip(tooltip)

        self.keydict[key] = button
        return button

    def _fill_keydict(self):
        for modkeyname in ['alt', 'ctrl', 'shift', 'win']:
            self.keydict[modkeyname] = []
            for side in 'lr':
                button = getattr(self.ui, '%s%s' % (side, modkeyname))
                self.keydict[side + modkeyname] = button
                self.keydict[modkeyname].append(button)

        for keyname in a2ahk.keys:
            try:
                obj = getattr(self.ui, keyname)
                if not isinstance(obj, QtGui.QPushButton):
                    continue
                if keyname not in self.keydict:
                    self.keydict[keyname] = obj
            except AttributeError:
                pass

        # self._check_keys()

    def _check_keys(self):
        for objname in dir(self.ui):
            obj = getattr(self.ui, objname)
            if not isinstance(obj, QtGui.QPushButton):
                continue
            if objname not in self.keydict:
                log.error('NOT IN!: %s' % objname)

    def build_keyboad(self, keyboard_id):
        if keyboard_id == 'en_us':
            import a2widget.keyboard.en_us
            a2widget.keyboard.en_us.main(self)

    def _toggle_numpad(self, state=None):
        if state is None:
            state = self.a2.db.get('hotkey_dialog_show_numpad') or False
            self.ui.check_numpad.setChecked(state)

        self.ui.num_block_widget.setVisible(state)
        self.a2.db.set('hotkey_dialog_show_numpad', state)

    def _toggle_mouse(self, state=None):
        if state is None:
            state = self.a2.db.get('hotkey_dialog_show_mouse') or False
            self.ui.check_mouse.setChecked(state)

        self.ui.mouse_block_widget.setVisible(state)
        self.a2.db.set('hotkey_dialog_show_mouse', state)
