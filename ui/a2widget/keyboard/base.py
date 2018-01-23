"""
Created on 11.09.2017

@author: eric
"""
import os
import a2ahk
import a2ctrl
import a2core
from a2widget.keyboard import base_ui, mouse_ui, numpad_ui

from PySide import QtGui, QtCore


log = a2core.get_logger('keyboard_base')
BASE_MODIFIERS = ['alt', 'ctrl', 'shift', 'win']
SIDES = 'lr'
KEYFONT_SIZE_FACTOR = 0.5
KEYFONT_SIZE_FACTOR_SMALL = 0.2
DB_KEY_MOUSE = 'hotkey_dialog_show_mouse'
DB_KEY_NUMPAD = 'hotkey_dialog_show_numpad'


class KeyboardDialogBase(QtGui.QDialog):

    def __init__(self, parent):
        super(KeyboardDialogBase, self).__init__(parent)
        self.setModal(True)

        self.a2 = a2core.A2Obj.inst()
        self.key_dict = {}
        self.modifier = {}
        self.checked_key = None
        self.checked_modifier = []

        a2ctrl.check_ui_module(base_ui)
        a2ctrl.check_ui_module(mouse_ui)
        a2ctrl.check_ui_module(numpad_ui)
        self.ui = base_ui.Ui_Keyboard()
        self.ui.setupUi(self)
        self.ui.num_block_widget = numpad_ui.Ui_Numpad()
        self.ui.num_block_widget.setupUi(self)

        self._fill_key_dict()
        self._setup_ui()

        self._toggle_numpad()
        self._toggle_mouse()

    def set_key(self):
        if not self.key:
            return

        keys = self.key.lower().split('+')
        buttons = []
        for k in keys:
            button = self.key_dict.get(k)
            if button:
                buttons.append(button)
            elif k in BASE_MODIFIERS:
                button = self.modifier.get('l' + k)
                buddy = self.modifier[button.a2buddy]
                buttons += [button, buddy]

        for button in buttons:
            button.setChecked(True)
            self._key_press(button, False)

        self.ui.key_field.setText(self.key)

    def _setup_ui(self):
        scale = self.a2.win.css_values['scale']
        color = self.a2.win.css_values['color_yellow']
        font_size = self.a2.win.css_values['font_size'] * KEYFONT_SIZE_FACTOR
        font_size_small = self.a2.win.css_values['font_size'] * KEYFONT_SIZE_FACTOR_SMALL
        key_height = scale * 25

        css = load_css('main')
        css = css.format(font_size=font_size, color=color, font_size_small=font_size_small,
                         key_height=key_height)

        # for key_name in ['pgup', 'pgdn', 'scrolllock', 'printscreen']:
        #     self.key_dict[key_name].setMaximumHeight(key_height)

        self.ui.mouse_block_widget = MouseWidget(self)
        self.ui.keys_layout.addWidget(self.ui.mouse_block_widget)
        self.ui.mouse_block_widget.set_style(scale)

        self.ui.keys_layout.setSpacing(scale * 20)
        self.ui.main_block.setSpacing(scale * 5)
        self.ui.cursor_block.setSpacing(scale * 5)

        self.ui.left.setText('←')
        self.ui.up.setText('↑')
        self.ui.down.setText('↓')
        self.ui.right.setText('→')
        self.ui.keys_widget.setStyleSheet(css)

        for i in range(1, 13):
            self.add_key('f%i' % i, self.ui.f_row)

        for i in range(1, 10):
            self.insert_key(i - 1, str(i), self.ui.number_row)

        self.insert_key(9, '0', self.ui.number_row)

        self.ui.check_numpad.clicked[bool].connect(self._toggle_numpad)
        self.ui.check_mouse.clicked[bool].connect(self._toggle_mouse)

        self.ui.a2ok_button.clicked.connect(self.ok)
        self.ui.a2cancel_button.clicked.connect(self.close)

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
        * as an internal name
        * showing as a tooltip
        """
        # name = key + '_key'
        button = QtGui.QPushButton(self.ui.keys_widget)
        button.setCheckable(True)
        # button.setObjectName(name)
        # setattr(self.ui, name, button)

        if label:
            button.setText(label)
        else:
            button.setText(key.upper())

        if tooltip:
            button.setToolTip(tooltip)

        self.key_dict[key] = button
        button.a2key = key
        button.clicked.connect(self._key_press)
        return button

    def _key_press(self, button=None, update_hotkey_label=True):
        if button is None:
            button = self.sender()

        height = button.height()
        print('height: %s' % height)

        # modifiers can be toggled however you like
        if button.a2key in self.modifier:
            checked = button.isChecked()
            if checked and button.a2key not in self.checked_modifier:
                self.checked_modifier.append(button.a2key)
            elif not checked and button.a2key in self.checked_modifier:
                self.checked_modifier.remove(button.a2key)
        # there always has to be a trigger key tho:
        else:
            if button.a2key == self.checked_key:
                self.key_dict[button.a2key].setChecked(True)
            else:
                if self.checked_key is not None:
                    self.key_dict[self.checked_key].setChecked(False)
                self.checked_key = button.a2key

        if update_hotkey_label:
            new_key_label = []
            handled = []
            for modkeyname in self.checked_modifier:
                if modkeyname in handled:
                    continue

                modkey = self.key_dict[modkeyname]
                if modkey.a2buddy in self.checked_modifier:
                    handled.append(modkey.a2buddy)
                    new_key_label.append(modkey.a2modifier)
                else:
                    new_key_label.append(modkeyname)
            new_key_label.append(self.checked_key)

            self.key = '+'.join([k.title() for k in new_key_label])
            self.ui.key_field.setText(self.key)

    def _fill_key_dict(self):
        for modkeyname in BASE_MODIFIERS:
            for i in [0, 1]:
                side = SIDES[i]
                key_name = side + modkeyname
                button = getattr(self.ui, key_name)
                button.setCheckable(True)
                button.clicked.connect(self._key_press)
                button.a2key = key_name
                button.a2modifier = modkeyname
                button.a2buddy = SIDES[int(not i)] + modkeyname

                self.key_dict[key_name] = button
                self.modifier[key_name] = button

        for key_name in a2ahk.keys:
            try:
                obj = getattr(self.ui, key_name)
                if isinstance(obj, QtGui.QPushButton):
                    if key_name not in self.key_dict:
                        obj.a2key = key_name
                        obj.setCheckable(True)
                        obj.clicked.connect(self._key_press)
                        self.key_dict[key_name] = obj
            except AttributeError:
                pass

        # self._check_keys()

    def _check_keys(self):
        for objname in dir(self.ui):
            obj = getattr(self.ui, objname)
            if not isinstance(obj, QtGui.QPushButton):
                continue
            if objname not in self.key_dict:
                log.error('NOT IN!: %s' % objname)

    def build_keyboard(self, keyboard_id):
        if keyboard_id == 'en_us':
            import a2widget.keyboard.en_us
            a2widget.keyboard.en_us.main(self)

    def _toggle_numpad(self, state=None):
        if state is None:
            state = self.a2.db.get(DB_KEY_NUMPAD) or False
            self.ui.check_numpad.setChecked(state)
        #self.ui.num_block_widget.setVisible(state)
        self.a2.db.set(DB_KEY_NUMPAD, state)

    def _toggle_mouse(self, state=None):
        if state is None:
            state = self.a2.db.get(DB_KEY_MOUSE) or False
            self.ui.check_mouse.setChecked(state)
        self.ui.mouse_block_widget.setVisible(state)
        self.a2.db.set(DB_KEY_MOUSE, state)


class MouseWidget(QtGui.QWidget):
    def __init__(self, parent):
        super(MouseWidget, self).__init__(parent)
        self.ui = mouse_ui.Ui_Mouse()
        self.ui.setupUi(self)

    def set_style(self, scale):
        css = load_css('mouse').format(big_radius=scale * 30)
        self.setStyleSheet(css)


def load_css(name):
    template_file = os.path.join(os.path.dirname(__file__), '%s.css.template' % name)
    with open(template_file) as fobj:
        css = fobj.read()
    return css
