"""
Created on 11.09.2017

@author: eric
"""
from enum import Enum

import a2ctrl
import a2core
import a2widget.keyboard.base_ui
from PySide import QtGui, QtCore


STYLE_BUTTON = """
    QPushButton {
        padding: 3px;
        min-width: 1px;
        font-size: 12px;
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

        self.ui.left_key.setText('←')
        self.ui.up_key.setText('↑')
        self.ui.down_key.setText('↓')
        self.ui.right_key.setText('→')

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
        self.keydict['left'] = self.ui.left_key
        self.keydict['up'] = self.ui.up_key
        self.keydict['down'] = self.ui.down_key
        self.keydict['right'] = self.ui.right_key

        for modkeyname in ['alt', 'ctrl', 'shift', 'win']:
            self.keydict[modkeyname] = []
            for side in 'lr':
                button = getattr(self.ui, '%s_%s_key' % (side, modkeyname))
                self.keydict[side + modkeyname] = button
                self.keydict[modkeyname].append(button)

    def build_keyboad(self, keyboard_id):
        if keyboard_id == 'en_us':
            import a2widget.keyboard.en_us
            a2widget.keyboard.en_us.main(self)

    def _toggle_numpad(self, state=None):
        if state is None:
            state = self.a2.db.get('hotkey_dialog_show_numpad') or False
            self.ui.check_numpad.setChecked(state)
            #state = not state

        self.ui.num_block_widget.setVisible(state)
        self.a2.db.set('hotkey_dialog_show_numpad', state)

    def _toggle_mouse(self, state=None):
        if state is None:
            state = self.a2.db.get('hotkey_dialog_show_mouse') or False
            self.ui.check_mouse.setChecked(state)
            #state = not state

        self.ui.mouse_block_widget.setVisible(state)
        self.a2.db.set('hotkey_dialog_show_mouse', state)
