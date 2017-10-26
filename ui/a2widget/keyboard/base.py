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


STYLE_BUTTON = """
    QPushButton {
        padding: 15px;
        min-width: 10px;
        min-height: 25px;
        max-height: 25px;
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

        self.ui.keys_widget.setStyleSheet(STYLE_BUTTON)

        self.ui.left.setText('←')
        self.ui.up.setText('↑')
        self.ui.down.setText('↓')
        self.ui.right.setText('→')

        for i in range(1, 13):
            self.add_key('f%i' % i, self.ui.f_row)

        for i in range(0, 10):
            self.insert_key(i, str(i), self.ui.number_row)
        # for i, l, name in [(10, '0', 'digit0'), (11, '-', 'minus'), (12, '=', 'equals')]:
        for i, k in [(10, '0'), (11, '-'), (12, '=')]:
            self.insert_key(i, k, self.ui.number_row)

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
        self.keydict['left'] = self.ui.left
        self.keydict['up'] = self.ui.up
        self.keydict['down'] = self.ui.down
        self.keydict['right'] = self.ui.right

        for modkeyname in ['alt', 'ctrl', 'shift', 'win']:
            self.keydict[modkeyname] = []
            for side in 'lr':
                button = getattr(self.ui, '%s_%s_key' % (side, modkeyname))
                self.keydict[side + modkeyname] = button
                self.keydict[modkeyname].append(button)

        pprint(self.keydict)
        for key in a2ahk.keys:
            print(key)

        for objname in dir(self.ui):
            obj = getattr(self.ui, objname)
            if not isinstance(obj, QtGui.QPushButton):
                continue

            if objname in self.keydict or objname + '_key' in self.keydict:
                print('IS IN!: %s' % objname)
            else:
                print('NOT IN!: %s' % objname)

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
