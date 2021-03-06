"""
A combobox that doesn't accidentally change if you scroll over it.

Scolling a layout with a combobox underneath the cursor never
triggers enterEvent! But we wouldn't want to have these as valued
inputs anyway. So there is now a timestamp set on enter.
So hovering and changing the value via wheel still works while
scrolling over is properly ignored.
"""
import time
from a2qt import QtWidgets, QtCore


class A2Combo(QtWidgets.QComboBox):
    def __init__(self, *args, **kwargs):
        super(A2Combo, self).__init__(*args, **kwargs)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self._in_time = None

    def focusInEvent(self, event):
        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        super(A2Combo, self).focusInEvent(event)

    def focusOutEvent(self, event):
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        super(A2Combo, self).focusOutEvent(event)

    def enterEvent(self, event: QtCore.QEvent) -> None:
        self._in_time = time.time()
        return super().enterEvent(event)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        self._in_time = None
        return super().leaveEvent(event)

    def wheelEvent(self, event):
        if not self.hasFocus():
            if self._in_time is None:
                event.ignore()
                return
            # make it possible to hover over the combo to scroll it.
            if time.time() - self._in_time < 0.4:
                event.ignore()
                return

        return super(A2Combo, self).wheelEvent(event)
