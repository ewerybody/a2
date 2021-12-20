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
        self.hlayout.setContentsMargins(0, 0, 0, 0)
        self._hover_widget = None  # type: QtWidgets.QAbstractButton | None

    def set_hover_widget(self, widget):
        self._hover_widget = widget

    def add_widget(self, widget):
        self.hlayout.addWidget(widget)

    def enterEvent(self, event):
        self._send_hover_event(event)
        return super().enterEvent(event)

    def leaveEvent(self, event):
        if self._hover_widget is not None and self._send_hover_event(event):
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

                if self._rich_text_label_clicked(event):
                    self.clicked.emit()

        return super().mousePressEvent(event)

    def _rich_text_label_clicked(self, event):
        """Mitigate a 11 year old bug that causes QLabels with rich text to
        not pass a `mouseReleaseEvent`. https://bugreports.qt.io/browse/QTBUG-12982

        Unfortunately seems impossible to check if a QLabel is actually containing
        rich-text if it's turned to AutoText!
        """
        app = QtWidgets.QApplication.instance()
        if not isinstance(app, QtWidgets.QApplication):
            return False
        widget = app.widgetAt(event.globalPos())
        if not isinstance(widget, QtWidgets.QLabel):
            return False

        if widget.textFormat() in (QtCore.Qt.RichText, QtCore.Qt.MarkdownText):
            return True

        return widget.textFormat() is QtCore.Qt.AutoText and '<' in widget.text()

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
