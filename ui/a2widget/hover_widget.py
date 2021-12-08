from a2qt import QtCore, QtGui, QtWidgets


class FancyCheck(QtWidgets.QWidget):
    def __init__(self, text='', parent=None):
        super().__init__(parent)
        self.hlayout = QtWidgets.QHBoxLayout(self)
        self.check = QtWidgets.QCheckBox(self)
        self.hlayout.addWidget(self.check)

        self.hover = HoverWidget(self)
        self.hover.set_hover_widget(self.check)
        self.label = QtWidgets.QLabel(text)
        self.label.setWordWrap(True)
        self.hover.add_widget(self.label)
        self.hover.clicked.connect(self.check.toggle)
        self.hlayout.addWidget(self.hover)
        self.hlayout.setStretch(1, 1)


class HoverWidget(QtWidgets.QWidget):
    clicked = QtCore.Signal()
    context_menu_requested = QtCore.Signal()

    mouse_pressed = QtCore.Signal()
    mouse_released = QtCore.Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.hlayout = QtWidgets.QHBoxLayout(self)
        self._hover_widget = None

    def set_hover_widget(self, widget):
        self._hover_widget = widget

    def add_widget(self, widget):
        self.hlayout.addWidget(widget)

    def enterEvent(self, event):
        self._send_hover_event(event)
        return super().enterEvent(event)

    def leaveEvent(self, event):
        if self._send_hover_event(event):
            self._hover_widget.setDown(False)
        return super().leaveEvent(event)

    def _send_hover_event(self, event):
        if self._hover_widget is None:
            return False

        pos = self._hover_widget.pos()
        pos1 = QtCore.QPoint(-1, -1)
        if event.type() == QtCore.QEvent.Enter:
            hovevent = QtGui.QHoverEvent(QtGui.QHoverEvent.HoverLeave, pos, pos1)
        else:
            hovevent = QtGui.QHoverEvent(QtGui.QHoverEvent.HoverLeave, pos1, pos)
        QtWidgets.QApplication.sendEvent(self._hover_widget, hovevent)
        QtWidgets.QApplication.sendEvent(self._hover_widget, event)
        return True

    def mousePressEvent(self, event):
        self.mouse_pressed.emit()
        if self._hover_widget is not None:
            if self._hover_widget.isEnabled() and event.button() == QtCore.Qt.LeftButton:
                self._hover_widget.setDown(True)
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.mouse_released.emit()
        if event.button() == QtCore.Qt.RightButton:
            self.context_menu_requested.emit()
        elif self._hover_widget is not None:
            if self._hover_widget.isEnabled() and event.button() == QtCore.Qt.LeftButton:
                self.clicked.emit()
            self._hover_widget.setDown(False)
        return super().mouseReleaseEvent(event)


if __name__ == '__main__':
    from a2widget.demo import hover_widget_demo

    hover_widget_demo.show()
