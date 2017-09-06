from pprint import pprint

from PySide import QtGui, QtCore

import a2ahk
import a2core
import a2ctrl
import a2widget.keyboard.base_ui


log = a2core.get_logger(__name__)
LEAVE_CLOSE_TIMEOUT = 1000
STYLE_BAD = '* {color:#F00}'
STYLE_GOOD = '* {color:#0F0}'
_dialog_size = None


STYLE_BUTTON = """
    QPushButton {
        padding: 5px;
        min-width: 1px;
        font-size: 12px;
    }
    """
#    padding-left: 0px;
#    padding-right: 0px;


class A2Hotkey(QtGui.QPushButton):
    hotkey_changed = QtCore.Signal(str)

    def __init__(self, parent=None, key=None, ok_func=None):
        super(A2Hotkey, self).__init__(parent)
        self.a2 = a2core.A2Obj.inst()
        self.key = key
        self.ok_func = ok_func
        self.setText(key)
        self.clicked.connect(self.popup_dialog)

        self.dialog_styles = [HotkeyDialog2]
        self.dialog_default = HotkeyDialog1
        self.dialog_styles.append(self.dialog_default)

    def set_key(self, key):
        if key != self.key:
            self.key = key
            self.setText(key)
            self.hotkey_changed.emit(key)
            if self.ok_func is not None:
                log.warning('Avoid using ok_func()! Do it with the hotket_set Signal!')
                self.ok_func(key)

    def popup_dialog(self):
        style = self.a2.db.get('hotkey_dialog_style')
        if style:
            for hotkey_dialog_class in self.dialog_styles:
                if hotkey_dialog_class.__name__ == style:
                    break
        else:
            hotkey_dialog_class = self.dialog_default

        dialog = hotkey_dialog_class(self)
        dialog.hotkey_set.connect(self.set_key)
        dialog.show()


class HotkeyDialog2(QtGui.QDialog):
    hotkey_set = QtCore.Signal(str)
    label = 'Hotkey Keyboard'

    def __init__(self, parent):
        super(HotkeyDialog2, self).__init__(parent)
        self.parent_widget = parent
        self.setModal(True)
        self.a2 = a2core.A2Obj.inst()
        a2ctrl.check_ui_module(a2widget.keyboard.base_ui)
        self.setup_ui()
#        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Enter), self, self.ok)
#        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self, self.close)
#
#        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint)
#
#        self.key = self.parent_widget.key
#        self.okay_state = True
#        self.validate_hotkey(self.key)
#
        self.place_at_cursor()
#        self.show()
        self._init_dialog_size()
#
#        hotkeys = self.a2.get_used_hotkeys()
#        pprint(hotkeys)

    def setup_ui(self):
        self.ui = a2widget.keyboard.base_ui.Ui_Keyboard()
        self.ui.setupUi(self)
        self.ui.keys_widget.setStyleSheet(STYLE_BUTTON)

        self.ui.left_key.setText('←')
        self.ui.up_key.setText('↑')
        self.ui.down_key.setText('↓')
        self.ui.right_key.setText('→')

        for i in range(1, 13):
            self.add_key('f%i_key' % i, 'F%i' % i, self.ui.f_row)

        # TODO: This needs to be subclassed for an english keyboard
        self.add_key('tick_key', '`', self.ui.number_row, 0)
        for i in range(1, 10):
            self.add_key('digit%i_key' % i, str(i), self.ui.number_row, i)
        for i, l, name in [(10, '0', 'digit0'), (11, '-', 'minus'), (12, '=', 'equals')]:
            self.add_key('%s_key' % name, l, self.ui.number_row, i)

        for l in 'qwertyuiop':
            self.add_key('%s_key' % l, l, self.ui.letter_row_top)
        self.add_key('bracke_open_key', '[', self.ui.letter_row_top)
        self.add_key('bracke_close_key', ']', self.ui.letter_row_top)
        self.add_key('backslash_key', '\\', self.ui.letter_row_top)

        for l in 'asdfghjkl':
            self.add_key('%s_key' % l, l, self.ui.letter_row_middle)
        self.add_key('semicolon_key', ';', self.ui.letter_row_middle)
        self.add_key('quote_key', "'", self.ui.letter_row_middle)
        self.add_key('return_key', "Enter", self.ui.letter_row_middle)

        letters = 'zxcvbnm'
        for i in range(len(letters)):
            self.add_key('%s_key' % letters[i], letters[i], self.ui.letter_row_bottom, i + 1)
        for i, l, name in [(8, ',', 'comma'), (9, '.', 'dot'), (10, '/', 'slash')]:
            self.add_key('%s_key' % name, l, self.ui.letter_row_bottom, i)


    def add_key(self, name, label, layout, index=None):
        button = QtGui.QPushButton(self.ui.keys_widget)
        button.setObjectName(name)
        button.setText(label)
        if index is None:
            layout.addWidget(button)
        else:
            layout.insertWidget(index, button)
        setattr(self.ui, name, button)

    def ok(self):
        log.info('key: %s' % self.key)
        log.info('ok: %s' % self.okay_state)
        if self.okay_state:
            self.hotkey_set.emit(self.key)
            self.close()

    def validate_hotkey(self, hk_string):
        """
        first implementation: checks for valid modifiers + a single key
        TODO: handle F1-F12, Del, Home...
              handle single keys when in scope,
              check availability ...
        """
        okay_state = False
        hk_parts = hk_string.split('+')
        key = hk_parts[-1].strip().lower()
        modifier = []
        tilde = ''
        # TODO: implement check for joystick keys and scancodes: 2joy4, SCnnn
        # http://www.autohotkey.com/docs/KeyList.htm#SpecialKeys
        if len(key) != 1 and key not in a2ahk.keys:
            msg = 'Invalid key! (%s)' % key
        elif len(hk_parts) == 1:
            okay_state = True
        else:
            modifier = [k.strip().lower() for k in hk_parts[:-1]]
            if modifier[0].startswith('~'):
                tilde = '~'
                modifier[0] = modifier[0][1:]
            bad_modifier = [k for k in modifier if k not in a2ahk.modifiers]
            if bad_modifier:
                msg = ('Modifyer not one of Win, Ctrl, Alt or Shift! (%s)' % ', '.join(bad_modifier))
            else:
                okay_state = True

        if not okay_state:
            self.text_edit.setStyleSheet(STYLE_BAD)
            log.error(msg)
        else:
            modifier = [k.title() for k in modifier]
            key = key.title()
            self.key = tilde + '+'.join(modifier + [key])
            log.info('tempKey %s:' % self.key)
            self.text_edit.setStyleSheet(STYLE_GOOD)

        self.okay_state = okay_state

    def place_at_cursor(self):
        cursor_pos = QtGui.QCursor.pos()
        pos = self.pos()
        dialog_size = _dialog_size if _dialog_size else (200, 100)
        pos.setX(cursor_pos.x() - (dialog_size[0] / 2))
        pos.setY(cursor_pos.y() - (dialog_size[1] / 2))
        self.move(pos)

    def closeEvent(self, event):
        return QtGui.QWidget.closeEvent(self, event)

    def _init_dialog_size(self):
        global _dialog_size
        _dialog_size = (self.width(), self.height())


class HotkeyDialog1(QtGui.QWidget):
    hotkey_set = QtCore.Signal(str)
    label = 'Simple Dialog'

    def __init__(self, parent):
        super(HotkeyDialog1, self).__init__(parent)
        self.parent_widget = parent
        self.a2 = a2core.A2Obj.inst()
        self.setup_ui()

        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Enter), self, self.ok)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self, self.close)

        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint)

        self._close_timer = QtCore.QTimer()
        self._close_timer.setInterval(LEAVE_CLOSE_TIMEOUT)
        self._close_timer.timeout.connect(self.leave_timeout_reached)

        self.key = self.parent_widget.key
        self.okay_state = True
        self.validate_hotkey(self.key)

        self.place_at_cursor()
        self.show()
        self._init_dialog_size()

        hotkeys = self.a2.get_used_hotkeys()
        pprint(hotkeys)

    def setup_ui(self):
        self.text_edit = QtGui.QLineEdit(self)
        self.text_edit.setText(self.parent_widget.key)
        self.text_edit.textChanged.connect(self.validate_hotkey)
        self.text_edit.returnPressed.connect(self.ok)

        self.button_layout = QtGui.QHBoxLayout()
        self.ok_button = QtGui.QPushButton("OK")
        self.ok_button.clicked.connect(self.ok)
        self.button_layout.addWidget(self.ok_button)

        self.close_button = QtGui.QPushButton("&Cancel")
        self.close_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.close_button)

        self.main_layout = QtGui.QVBoxLayout(self)
        self.main_layout.addWidget(self.text_edit)
        self.main_layout.addLayout(self.button_layout)

    def ok(self):
        log.info('key: %s' % self.key)
        log.info('ok: %s' % self.okay_state)
        if self.okay_state:
            self.hotkey_set.emit(self.key)
            self.close()

    def validate_hotkey(self, hk_string):
        """
        first implementation: checks for valid modifiers + a single key
        TODO: handle F1-F12, Del, Home...
              handle single keys when in scope,
              check availability ...
        """
        okay_state = False
        hk_parts = hk_string.split('+')
        key = hk_parts[-1].strip().lower()
        modifier = []
        tilde = ''
        # TODO: implement check for joystick keys and scancodes: 2joy4, SCnnn
        # http://www.autohotkey.com/docs/KeyList.htm#SpecialKeys
        if len(key) != 1 and key not in a2ahk.keys:
            msg = 'Invalid key! (%s)' % key
        elif len(hk_parts) == 1:
            okay_state = True
        else:
            modifier = [k.strip().lower() for k in hk_parts[:-1]]
            if modifier[0].startswith('~'):
                tilde = '~'
                modifier[0] = modifier[0][1:]
            bad_modifier = [k for k in modifier if k not in a2ahk.modifiers]
            if bad_modifier:
                msg = ('Modifyer not one of Win, Ctrl, Alt or Shift! (%s)' % ', '.join(bad_modifier))
            else:
                okay_state = True

        if not okay_state:
            self.text_edit.setStyleSheet(STYLE_BAD)
            log.error(msg)
        else:
            modifier = [k.title() for k in modifier]
            key = key.title()
            self.key = tilde + '+'.join(modifier + [key])
            log.info('tempKey %s:' % self.key)
            self.text_edit.setStyleSheet(STYLE_GOOD)

        self.okay_state = okay_state

    def place_at_cursor(self):
        cursor_pos = QtGui.QCursor.pos()
        pos = self.pos()
        dialog_size = _dialog_size if _dialog_size else (200, 100)
        pos.setX(cursor_pos.x() - (dialog_size[0] / 2))
        pos.setY(cursor_pos.y() - (dialog_size[1] / 2))
        self.move(pos)

    def leaveEvent(self, event):
        self._close_timer.start()
        return QtGui.QWidget.leaveEvent(self, event)

    def enterEvent(self, event):
        if self._close_timer.isActive():
            self._close_timer.stop()
        return QtGui.QWidget.enterEvent(self, event)

    def leave_timeout_reached(self):
        self._close_timer.stop()
        self.close()

    def closeEvent(self, event):
        self._close_timer.stop()
        return QtGui.QWidget.closeEvent(self, event)

    def _init_dialog_size(self):
        global _dialog_size
        _dialog_size = (self.width(), self.height())
