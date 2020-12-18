import a2ahk
from PySide6 import QtGui, QtCore, QtWidgets
from .dialogs import _HotkeyDialogBase
import a2core

log = a2core.get_logger(__name__)
LEAVE_CLOSE_TIMEOUT = 1000
STYLE_BAD = '* {color:#F00}'
STYLE_GOOD = '* {color:#0F0}'
_dialog_size = None


class HotkeyDialog1(QtWidgets.QWidget, _HotkeyDialogBase):
    hotkey_set = QtCore.Signal(str)
    label = 'Simple Dialog'

    def __init__(self, parent, key, scope_data=None):
        # super(HotkeyDialog1, self).__init__(parent)
        QtWidgets.QWidget.__init__(self, parent)
        _HotkeyDialogBase.__init__(self, parent, key, scope_data)

        self.setup_ui()

        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Enter), self, self.ok)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self, self.close)

        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint)

        self._close_timer = QtCore.QTimer()
        self._close_timer.setInterval(LEAVE_CLOSE_TIMEOUT)
        self._close_timer.timeout.connect(self.leave_timeout_reached)

        self.okay_state = True
        self.validate_hotkey(self.key)

        self.place_at_cursor()
        self.show()
        self._init_dialog_size()

    def setup_ui(self):
        self.text_edit = QtWidgets.QLineEdit(self)
        self.text_edit.setText(self.key)
        self.text_edit.textChanged.connect(self.validate_hotkey)
        self.text_edit.returnPressed.connect(self.ok)

        self.button_layout = QtWidgets.QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton('OK')
        self.ok_button.clicked.connect(self.ok)
        self.button_layout.addWidget(self.ok_button)

        self.close_button = QtWidgets.QPushButton('&Cancel')
        self.close_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.close_button)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.text_edit)
        self.main_layout.addLayout(self.button_layout)

    def ok(self):
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
        if len(key) != 1 and key not in a2ahk.KEYS:
            msg = 'Invalid key! (%s)' % key
        elif len(hk_parts) == 1:
            okay_state = True
        else:
            modifier = [k.strip().lower() for k in hk_parts[:-1]]
            if modifier[0].startswith('~'):
                tilde = '~'
                modifier[0] = modifier[0][1:]
            bad_modifier = [k for k in modifier if k not in a2ahk.MODIFIERS]
            if bad_modifier:
                msg = 'Modifyer not one of Win, Ctrl, Alt or Shift! (%s)' % ', '.join(bad_modifier)
            else:
                okay_state = True

        if not okay_state:
            self.text_edit.setStyleSheet(STYLE_BAD)
            log.error(msg)
        else:
            modifier = [k.title() for k in modifier]
            key = key.title()
            self.key = tilde + '+'.join(modifier + [key])
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
        return QtWidgets.QWidget.leaveEvent(self, event)

    def enterEvent(self, event):
        if self._close_timer.isActive():
            self._close_timer.stop()
        return QtWidgets.QWidget.enterEvent(self, event)

    def leave_timeout_reached(self):
        self._close_timer.stop()
        self.close()

    def closeEvent(self, event):
        self._close_timer.stop()
        return QtWidgets.QWidget.closeEvent(self, event)

    def _init_dialog_size(self):
        global _dialog_size
        _dialog_size = (self.width(), self.height())
