# -*- coding: utf-8 -*-
"""
Created on 11.09.2017

@author: eric
"""
import os
import inspect

import a2ahk
import a2core
import a2util
import a2runtime
import a2ctrl.connect
from a2widget.a2hotkey import hotkey_common

from . import base_ui, mouse_ui, numpad_ui, cursor_block_ui

from PySide2 import QtGui, QtCore, QtWidgets


log = a2core.get_logger('keyboard_base')
BASE_MODIFIERS = ['alt', 'ctrl', 'shift', 'win']
SIDES = 'lr'
DB_KEY_MOUSE = 'hotkey_dialog_show_mouse'
DB_KEY_NUMPAD = 'hotkey_dialog_show_numpad'
_HERE = os.path.dirname(__file__)
_IGNORE_BUTTONS = ['a2cancel_button', 'a2ok_button']
HOTKEY_HELP_PAGE = 'Hotkey-Setup'
WIN_STANDARD_FILE = 'standard_windows_keys.json'
_WIN_STANDARD_KEYS = {}
GLOBAL_NO_MOD_WARNING = 'Global Hotkeys should have a modifier!'


class KeyboardDialogBase(QtWidgets.QDialog):

    def __init__(self, parent):
        super(KeyboardDialogBase, self).__init__(parent)
        self.setModal(True)

        self.key_dict = {}
        self.modifier = {}
        self.checked_key = ''
        self.checked_modifier = []

        a2ctrl.check_ui_module(base_ui)
        a2ctrl.check_ui_module(mouse_ui)
        a2ctrl.check_ui_module(numpad_ui)
        a2ctrl.check_ui_module(cursor_block_ui)

        self.ui = base_ui.Ui_Keyboard()
        self.ui.setupUi(self)
        self.cursor_block_widget = CursorBlockWidget(self)
        self.numpad_block_widget = NumpadWidget(self)
        self.mouse_block_widget = MouseWidget(self)

        self.scope = Scope(self.scope_data)
        self._fill_key_dict()
        self._ui_styles = {}
        self._setup_ui()

    def set_key(self):
        """
        Sets the dialog to the given key sequence,
        updates key field, dictionaries and toggles the according buttons.
        """
        if not self.key:
            self.checked_key = ''
            self.checked_modifier = []
            return

        buttons = []
        for key in self.key.lower().split('+'):
            button = self.key_dict.get(key)
            # all single buttons
            if button:
                buttons.append(button)
            # in BASE_MODIFIERS means 2 buttons left + right
            elif key in BASE_MODIFIERS:
                button = self.modifier.get('l' + key)
                buddy = self.modifier[button.a2buddy]
                buttons.extend([button, buddy])

            if key in a2ahk.mouse_keys:
                self.mouse_block_widget.setVisible(True)
            elif key in a2ahk.numpad_keys:
                self.numpad_block_widget.setVisible(True)

        for button in buttons:
            button.setChecked(True)
            if button.a2key in self.modifier:
                self._check_modifier(button)
            else:
                self._check_key(button)

        self.ui.key_field.setText(self.key)
        self.update_ui()

    def _setup_ui(self):
        # css debug shortcut
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_R), self, self.refresh_style)

        self.ui.keys_layout.addWidget(self.cursor_block_widget)
        self.ui.keys_layout.addWidget(self.numpad_block_widget)
        self.ui.keys_layout.addWidget(self.mouse_block_widget)

        for i in range(1, 13):
            self.add_key('f%i' % i, self.ui.f_row)

        for i in range(1, 10):
            self.insert_key(i - 1, str(i), self.ui.number_row)

        self.insert_key(9, '0', self.ui.number_row)

        a2ctrl.connect.control_to_db(self.ui.check_numpad, self.a2.db, DB_KEY_NUMPAD)
        a2ctrl.connect.control_to_db(self.ui.check_mouse, self.a2.db, DB_KEY_MOUSE)
        self.ui.check_numpad.clicked[bool].connect(self.numpad_block_widget.setVisible)
        self.ui.check_mouse.clicked[bool].connect(self.mouse_block_widget.setVisible)

        self.ui.a2ok_button.clicked.connect(self.ok)
        self.ui.a2cancel_button.clicked.connect(self.close)
        self.ui.option_button.menu_called.connect(self.build_option_menu)

        self.refresh_style()

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
        button = QtWidgets.QPushButton(self.ui.keys_widget)
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
        button.clicked.connect(self.on_key_press)
        return button

    def on_key_press(self):
        button = self.sender()
        self._check_key(button)
        self.update_ui()

    def on_modifier_press(self):
        button = self.sender()
        self._check_modifier(button)
        self.update_ui()

    def _check_modifier(self, button):
        # modifiers can be toggled however you like
        checked = button.isChecked()
        ctrl_modifier = (QtWidgets.QApplication.keyboardModifiers() ==
                         QtCore.Qt.ControlModifier)

        if checked:
            if button.a2key not in self.checked_modifier:
                self.checked_modifier.append(button.a2key)
            if ctrl_modifier and button.a2buddy not in self.checked_modifier:
                self.checked_modifier.append(button.a2buddy)
                self.modifier[button.a2buddy].setChecked(True)

        else:
            if button.a2key in self.checked_modifier:
                self.checked_modifier.remove(button.a2key)
            if ctrl_modifier and button.a2buddy in self.checked_modifier:
                self.checked_modifier.remove(button.a2buddy)
                self.modifier[button.a2buddy].setChecked(False)

    def _check_key(self, button):
        # there always has to be a trigger key tho:
        if button.a2key == self.checked_key:
            self.key_dict[button.a2key].setChecked(True)
        else:
            if self.checked_key:
                self.key_dict[self.checked_key].setChecked(False)
            self.checked_key = button.a2key

    def update_ui(self):
        new_key_list = []
        handled = []
        for modkeyname in self.checked_modifier:
            if modkeyname in handled:
                continue

            modkey = self.key_dict[modkeyname]
            if modkey.a2buddy in self.checked_modifier:
                handled.append(modkey.a2buddy)
                new_key_list.append(modkey.a2modifier)
            else:
                new_key_list.append(modkeyname)

        new_key_list.append(self.checked_key)

        modifier_string, trigger_key = hotkey_common.get_parts_from_list(new_key_list)
        self.key = hotkey_common.build_string(modifier_string, trigger_key)
        self.ui.key_field.setText(self.key)

        # TODO this might be kicked of delayed after dialog popup
        global_hks, include_hks, exclude_hks = get_current_hotkeys()
        parent_modifier = hotkey_common.parent_modifier_string(modifier_string)
        win_shortcuts, a2_shortcuts = {}, {}

        if self.scope.is_global:
            win_globals = win_standard_keys()
            if not self.checked_modifier:
                win_no_mods, a2_no_mods = win_globals.get(''), global_hks.get('')
                if win_no_mods:
                    print('Possible collisions with Windows Shortcuts:')
                    for key, op in win_no_mods.items():
                        print('  %s: %s' % (key, op))
                    if trigger_key in win_no_mods:
                        print('Actual collisions with Windows Shortcut:\n'
                              '  %s' % win_no_mods[trigger_key])

                if a2_no_mods:
                    print('Possible collisions with a2 Hotkeys:')
                    for key, ops in a2_no_mods.items():
                        print('  %s: %s' % (key, ';'.join([str(o) for o in ops])))
                    if trigger_key in a2_no_mods:
                        print('Actual collisions with a2 Hoykeys:\n'
                              '  %s' % a2_no_mods[trigger_key])

                self.ui.a2ok_button.setText(GLOBAL_NO_MOD_WARNING)
                self.ui.a2ok_button.setEnabled(False)
            else:
                if parent_modifier != modifier_string:
                    if parent_modifier in win_globals:
                        win_shortcuts = win_globals[parent_modifier]
                        print('Possible collisions with Windows Shortcuts '
                              'on %s:' % parent_modifier)
                        for key, op in win_shortcuts.items():
                            print('  %s: %s' % (key, op))
                        if trigger_key in win_shortcuts:
                            print('Actual collisions with Windows Shortcut:\n'
                                  '  %s' % win_shortcuts[trigger_key])

                    if parent_modifier in global_hks:
                        a2_shortcuts = global_hks[parent_modifier]
                        print('Possible collisions with a2 Hotkeys on %s:' % parent_modifier)
                        for key, op in a2_shortcuts.items():
                            print('  %s: %s' % (key, op))
                        if trigger_key in a2_shortcuts:
                            print('Actual collisions with Windows Shortcut:\n'
                                  '  %s' % a2_shortcuts[trigger_key])

                if modifier_string in win_globals:
                    win_shortcuts = win_globals[modifier_string]
                    print('Possible collisions with Windows Shortcuts '
                          'on %s:' % modifier_string)
                    for key, op in win_shortcuts.items():
                        print('  %s: %s' % (key, op))
                    if trigger_key in win_shortcuts:
                        print('Actual collisions with Windows Shortcut:\n'
                              '  %s' % win_shortcuts[trigger_key])

                if modifier_string in global_hks:
                    a2_shortcuts = global_hks[modifier_string]
                    print('Possible collisions with a2 Hotkeys on %s:' % modifier_string)
                    for key, op in a2_shortcuts.items():
                        print('  %s: %s' % (key, op))
                    if trigger_key in a2_shortcuts:
                        print('Actual collisions with a2 Hotkeys:\n'
                              '  %s' % a2_shortcuts[trigger_key])

                self.ui.a2ok_button.setText('OK')
                self.ui.a2ok_button.setEnabled(True)
        else:
            self.scope._scope_data

        self._highlight_keys(win_shortcuts, a2_shortcuts, trigger_key)

    def _highlight_keys(self, win_shortcuts, a2_shortcuts, trigger_key):
        for name, button in self.key_dict.items():
            if button in self.modifier.values():
                continue

            name = name.lower()
            a2_shortcuts = dict([(k.lower(), v) for k, v in a2_shortcuts.items()])
            tooltip = []
            style_sheet = self._ui_styles['default']

            if name in win_shortcuts:
                style_sheet = self._ui_styles['win_button']
                tooltip.append('Windows Shortcut: %s' % win_shortcuts[name])

            if name in a2_shortcuts:
                style_sheet = self._ui_styles['a2_button']
                for command, module in a2_shortcuts[name]:
                    if module is None:
                        tooltip.append('a2: %s' % command)
                    else:
                        tooltip.append('%s: %s' % (module.name, command))

            button.setStyleSheet(style_sheet)
            button.setToolTip('\n'.join(tooltip))

    def _fill_key_dict(self):
        for modkeyname in BASE_MODIFIERS:
            for i in [0, 1]:
                side = SIDES[i]
                key_name = side + modkeyname
                button = getattr(self.ui, key_name)
                button.setCheckable(True)
                button.clicked.connect(self.on_modifier_press)
                button.a2key = key_name
                button.a2modifier = modkeyname
                button.a2buddy = SIDES[int(not i)] + modkeyname

                self.key_dict[key_name] = button
                self.modifier[key_name] = button

        # rather than browsing all the ahk keys
        # we crawl through the ui objects for QPushButtons:
        for ui_obj in [self.ui, self.cursor_block_widget.ui,
                       self.numpad_block_widget.ui, self.mouse_block_widget.ui]:
            for key_name, button in inspect.getmembers(ui_obj, _is_pushbutton):
                if key_name in _IGNORE_BUTTONS:
                    continue
                # skip the already listed modifier keys
                if key_name in self.key_dict:
                    continue

                button.a2key = key_name
                button.setCheckable(True)
                button.clicked.connect(self.on_key_press)
                self.key_dict[key_name] = button

                if not key_name.startswith('_') and key_name not in a2ahk.keys:
                    log.warn('What kind of key is this?!? %s' % key_name)

        self._look_for_unlisted_keys()

    def _look_for_unlisted_keys(self):
        for objname in dir(self.ui):
            if objname in _IGNORE_BUTTONS:
                continue

            obj = getattr(self.ui, objname)
            if not isinstance(obj, QtWidgets.QPushButton):
                continue
            if objname not in self.key_dict:
                log.error('NOT IN!: %s' % objname)

    def build_keyboard(self, keyboard_id):
        from . import layouts
        keyboard_module = layouts.get_module(keyboard_id)
        keyboard_module.main(self)

    def refresh_style(self):
        try:
            css_values = self.a2.win.style.get_value_dict()
        except AttributeError:
            return

        scale = css_values['scale']
        values = a2util.json_read(os.path.join(_HERE, 'style_values.json'))
        # scale values for current screen, skipping the ones with "_*"
        for key, value in values.items():
            if not key.startswith('_'):
                values[key] = value * scale
        # calculating some more values
        values['color'] = css_values['color_yellow']
        values['color_button'] = css_values['color_button']
        values['font_size'] = css_values['font_size'] * values['_font_size_factor']
        values['font_size_small'] = css_values['font_size'] * values['_small_font_factor']
        values['long_key'] = values['key_height'] * 2 + values['small_spacing']
        values['wide_key'] = values['key_width'] * 2 + values['small_spacing']

        self.ui.keys_layout.setSpacing(values['big_spacing'])
        self.ui.main_layout.setSpacing(values['small_spacing'])
        self.cursor_block_widget.set_spacing(values['small_spacing'])
        self.mouse_block_widget.set_spacing(values['small_spacing'])

        main_css = load_css('main') % values
        self.ui.keys_widget.setStyleSheet(main_css)

        cursor_block_css = load_css('cursorblock') % values
        self.cursor_block_widget.setStyleSheet(cursor_block_css)
        self.numpad_block_widget.setStyleSheet(cursor_block_css)

        border_tmp = 'border: %.1fpx solid "%%s";' % css_values['border_radius']
        self._ui_styles['default'] = border_tmp % css_values['color_button']
        self._ui_styles['a2_button'] = border_tmp % css_values['color_yellow']
        self._ui_styles['win_button'] = border_tmp % css_values['color_blue']
        self._ui_styles['orig_button'] = border_tmp % css_values['color_green']

    def build_option_menu(self, menu):
        icons = a2ctrl.Icons.inst()
        if self.key:
            menu.addAction(icons.clear, 'Clear Hotkey', self.clear_hotkey)
        menu.addAction(icons.help, 'Help on Hotket Setup', self.goto_help)

    def _log_size(self):
        """
        Eventually I want to put the dialog under the cursor. But for that we need to
        find out how big the dialog is on different DPI and scale values. I'm gathering
        some values here from my own testings to later be able to estimate the size and
        center point. I don't wanna shift around the dialog after it popped up of course...

        110 dpi, height 313, scale 1.14583
            597 alone
            753 numpad 156
            794 mouse 197
            950 both 353
        216 dpi, h 587 scale 2.1375
            1130 alone
            1432 numpad 302
            1476 mouse 346
            1778 both 648
        """
        try:
            dpi = QtGui.qApp.desktop().physicalDpiX()
            scale = self.a2.win.css_values['scale']
            msg = ('hotkey dialog stats:\n   dpi: %i\n scale: %f\n   w/h: %i/%i'
                   % (dpi, scale, self.width(), self.height()))
            log.info(msg)
        except AttributeError:
            pass

    def clear_hotkey(self):
        self.key = ''

        for modifier in self.checked_modifier:
            self.modifier[modifier].setChecked(False)
        self.checked_modifier = []

        if self.checked_key:
            self.key_dict[self.checked_key].setChecked(False)
        self.checked_key = ''
        self.update_ui()

    def goto_help(self):
        a2util.surf_to(self.a2.urls.wiki + HOTKEY_HELP_PAGE)


class Scope(object):
    def __init__(self, scope_data):
        self._scope_data = scope_data

        self.scope_mode = self._scope_data.get(hotkey_common.Vars.scope_mode)
        self.is_global = self.scope_mode == 0
        self.is_include = self.scope_mode == 1
        self.is_exclude = self.scope_mode == 2


class CursorBlockWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(CursorBlockWidget, self).__init__(parent)
        self.ui = cursor_block_ui.Ui_CursorBlock()
        self.ui.setupUi(self)

        self.ui.left.setText('←')
        self.ui.up.setText('↑')
        self.ui.down.setText('↓')
        self.ui.right.setText('→')

    def set_spacing(self, spacing):
        pass


class NumpadWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(NumpadWidget, self).__init__(parent)
        self.a2 = parent.a2
        self.ui = numpad_ui.Ui_Numpad()
        self.ui.setupUi(self)
        self.setVisible(self.a2.db.get(DB_KEY_NUMPAD) or False)


class MouseWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(MouseWidget, self).__init__(parent)
        self.a2 = parent.a2
        self.ui = mouse_ui.Ui_Mouse()
        self.ui.setupUi(self)
        self.setVisible(self.a2.db.get(DB_KEY_MOUSE) or False)

    def set_spacing(self, spacing):
        self.ui.main_layout.setSpacing(spacing)
        self.ui.middle_layout.setSpacing(spacing)


def _is_pushbutton(obj):
    return isinstance(obj, QtWidgets.QPushButton)


def load_css(name):
    template_file = os.path.join(_HERE, '%s.css.template' % name)
    with open(template_file) as fobj:
        css = fobj.read()
    return css


def win_standard_keys():
    global _WIN_STANDARD_KEYS
    if not _WIN_STANDARD_KEYS:
        _WIN_STANDARD_KEYS = a2util.json_read(
            os.path.join(_HERE, WIN_STANDARD_FILE))
    return _WIN_STANDARD_KEYS


def get_current_hotkeys():
    global_hks, include_hks, exclude_hks = a2runtime.collect_hotkeys()
    modifiers_global = _sort_hotkey_modifiers(global_hks)

    modifiers_include, modifiers_exclude = {}, {}
    for from_dict, to_dict in [(include_hks, modifiers_include),
                               (exclude_hks, modifiers_exclude)]:
        for scope, hotkey_dict in from_dict.items():
            to_dict[scope] = _sort_hotkey_modifiers(hotkey_dict)

    return modifiers_global, modifiers_include, modifiers_exclude


def _sort_hotkey_modifiers(hotkey_dict):
    modifier_dict = {}
    for key, call in hotkey_dict.items():
        mod_string, trigger_key = hotkey_common.get_sorted_parts(key)
        modifier_dict.setdefault(mod_string, {}).setdefault(
            trigger_key, []).extend(call)
    return modifier_dict
