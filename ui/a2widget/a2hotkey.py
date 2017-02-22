from PySide import QtGui, QtCore

import a2ahk
import a2core


log = a2core.get_logger(__name__)


class A2Hotkey(QtGui.QPushButton):
    def __init__(self, parent=None, key=None, ok_func=None):
        # i'd love to use super here. But it introduces problems with reload
        # super(HotKey, self).__init__()
        QtGui.QPushButton.__init__(self)
        self.key = key
        self.tempKey = key
        self.tempOK = True
        self.ok_func = ok_func
        self.setText(key)

    def set_key(self, key):
        self.key = key
        self.setText(key)

    def mousePressEvent(self, event):
        self.buildPopup(event.globalX(), event.globalY())

    def buildPopup(self, x, y):
        self.popup = Popup(x, y, self)
        self.popup.textEdit = QtGui.QLineEdit(self.popup)
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
        self.popup.place_at_cursor()

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
        if len(key) != 1 and key not in a2ahk.keys:
            msg = 'Invalid key! (%s)' % key
        elif len(hkparts) == 1:
            good = True
        else:
            modifier = [k.strip().lower() for k in hkparts[:-1]]
            if modifier[0].startswith('~'):
                tilde = '~'
                modifier[0] = modifier[0][1:]
            badModifier = [k for k in modifier if k not in a2ahk.modifiers]
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


class Popup(QtGui.QWidget):
    def __init__(self, x, y, parent=None):
        super(Popup, self).__init__(parent=parent)
        self.setpos = (x, y)
        self.leave_close_timeout = 1000
        self._close = False
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape),
                        self, self.close)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint)

        self._close_timer = QtCore.QTimer()
        self._close_timer.setInterval(self.leave_close_timeout)
        self._close_timer.timeout.connect(self.leave_timeout_reached)

    def place_at_cursor(self):
        x, y = self.setpos
        pos = self.pos()
        pos.setX(x - (self.width() / 2))
        pos.setY(y - (self.height() / 2))
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
