"""
Created on 11.09.2017

@author: eric
"""
import a2ahk
import a2ctrl
import a2core
import a2widget.keyboard.base_ui
from PySide import QtGui, QtCore

log = a2core.get_logger('keyboard_base')

BASE_MODIFIERS = ['alt', 'ctrl', 'shift', 'win']
SIDES = 'lr'
KEYFONT_SIZE_FACTOR = 0.8
STYLE_BUTTON = """
    QPushButton {
        font-size: %(font-size)ipx;
        padding: %(padding)ipx;
        min-width: 15px;
        min-height: 22px;
        max-height: 22px;
    }
    QPushButton:checked {
        background-color: "%(color)s";
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
        self.checked_key = None
        self.checked_modifier = []

        self._setup_ui()
        self._fill_keydict()

        self._toggle_numpad()
        self._toggle_mouse()

    def set_key(self):
        if not self.key:
            return

        keys = self.key.lower().split('+')
        buttons = []
        for k in keys:
            button = self.keydict.get(k)
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
        a2ctrl.check_ui_module(a2widget.keyboard.base_ui)
        self.ui = a2widget.keyboard.base_ui.Ui_Keyboard()
        self.ui.setupUi(self)

        global STYLE_BUTTON
        scale = self.a2.win.css_values['scale']
        print('scale: %i' % scale)
        color = self.a2.win.css_values['color_yellow']

        font_size = self.a2.win.css_values['font_size'] * KEYFONT_SIZE_FACTOR
        STYLE_BUTTON = STYLE_BUTTON % {'font-size': font_size, 'color': color, 'padding': scale * 3}
        STYLE_BUTTON += '\nQPushButton#_mouse_body {min-height: %ipx;}' % (30 * scale)
        STYLE_BUTTON += '\nQPushButton#lbutton {min-height: %ipx;}' % (50 * scale)
        STYLE_BUTTON += '\nQPushButton#wheelleft {min-height: %ipx;max-width: %ipx;}' % (50 * scale, 5 * scale)
        STYLE_BUTTON += '\nQPushButton#wheelright {min-height: %ipx;max-width: %ipx;}' % (50 * scale, 5 * scale)
        STYLE_BUTTON += '\nQPushButton#mbutton {min-height: %ipx;}' % (30 * scale)
        STYLE_BUTTON += '\nQPushButton#rbutton {min-height: %ipx;}' % (50 * scale)
        self.ui.keys_widget.setStyleSheet(STYLE_BUTTON)

        self.ui.mouse_layout_1.setSpacing(scale * 2)
        # self.ui.mouse_layout_2.setSpacing(scale * 2)

        self.ui.left.setText('←')
        self.ui.up.setText('↑')
        self.ui.down.setText('↓')
        self.ui.right.setText('→')

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

        self.keydict[key] = button
        button.a2key = key
        button.clicked.connect(self._key_press)
        return button

    def _key_press(self, button=None, update_label=True):
        if button is None:
            button = self.sender()

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
                self.keydict[button.a2key].setChecked(True)
            else:
                if self.checked_key is not None:
                    self.keydict[self.checked_key].setChecked(False)
                self.checked_key = button.a2key

        if update_label:
            new_key_label = []
            handled = []
            for modkeyname in self.checked_modifier:
                if modkeyname in handled:
                    continue

                modkey = self.keydict[modkeyname]
                if modkey.a2buddy in self.checked_modifier:
                    handled.append(modkey.a2buddy)
                    new_key_label.append(modkey.a2modifier)
                else:
                    new_key_label.append(modkeyname)
            new_key_label.append(self.checked_key)

            self.key = '+'.join([k.title() for k in new_key_label])
            self.ui.key_field.setText(self.key)

    def _fill_keydict(self):
        for modkeyname in BASE_MODIFIERS:
            for i in [0, 1]:
                side = SIDES[i]
                keyname = side + modkeyname
                button = getattr(self.ui, keyname)
                button.setCheckable(True)
                button.clicked.connect(self._key_press)
                button.a2key = keyname
                button.a2modifier = modkeyname
                button.a2buddy = SIDES[int(not i)] + modkeyname

                self.keydict[keyname] = button
                self.modifier[keyname] = button

        for keyname in a2ahk.keys:
            try:
                obj = getattr(self.ui, keyname)
                if isinstance(obj, QtGui.QPushButton):
                    if keyname not in self.keydict:
                        obj.a2key = keyname
                        obj.setCheckable(True)
                        obj.clicked.connect(self._key_press)
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

    def build_keyboard(self, keyboard_id):
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
