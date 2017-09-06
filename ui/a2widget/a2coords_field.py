"""
Created on 08.03.2017

@author: eric
"""
from PySide import QtGui, QtCore

import a2ahk
import a2ctrl
import a2core


log = a2core.get_logger(__name__)


class A2CoordsField(QtGui.QWidget):
    changed = QtCore.Signal(tuple)

    def __init__(self, parent=None):
        super(A2CoordsField, self).__init__(parent)

        self.main_layout = QtGui.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self._internal_change = False

        self.x_field = QtGui.QSpinBox(self)
        self.x_field.setMinimum(-16777214)
        self.x_field.setMaximum(16777215)
        self.x_field.valueChanged.connect(self.change_triggered)
        self.main_layout.addWidget(self.x_field)

        self.y_field = QtGui.QSpinBox(self)
        self.y_field.setMinimum(-16777214)
        self.y_field.setMaximum(16777215)
        self.y_field.valueChanged.connect(self.change_triggered)
        self.main_layout.addWidget(self.y_field)

        self.tool_button = QtGui.QToolButton(self)
        self.tool_button.setAutoRaise(True)
        self.tool_button.setObjectName('a2option_button')
        self.tool_button.clicked.connect(self.show_menu)
        self.tool_button.setArrowType(QtCore.Qt.DownArrow)
        self.main_layout.addWidget(self.tool_button)

        self.menu = QtGui.QMenu()

    @property
    def x(self):
        return self.x_field.value()

    @x.setter
    def x(self, this):
        self.x_field.setValue(this)

    @property
    def y(self):
        return self.y_field.value()

    @y.setter
    def y(self, this):
        self.y_field.setValue(this)

    @property
    def value(self):
        return (self.x, self.y)

    @value.setter
    def value(self, this):
        self.set_value(this)

    def set_value(self, values, y=None):
        if isinstance(values, (tuple, list)) and len(values) < 2:
            raise RuntimeError('A2CoordsField.set_value needs a tuple or list of 2 integers!\n'
                               '  received: %s' % str(values))
        elif isinstance(values, QtCore.QPoint):
            values = values.x(), values.y()
        elif isinstance(values, QtCore.QSize):
            values = values.width(), values.height()

        self._internal_change = True
        self.x_field.setValue(values[0])
        self._internal_change = False
        self.y_field.setValue(values[1])
        # self.changed.emit((self.x, self.y))

    def show_menu(self):
        self.menu.clear()
        for func, icon in [(self.copy, a2ctrl.Icons.inst().copy),
                           (self.paste, a2ctrl.Icons.inst().paste),
                           (self.pick, a2ctrl.Icons.inst().number)]:
            self.menu.addAction(icon, '%s Coordinates' % func.__name__.title(), func)
        self.menu.popup(QtGui.QCursor.pos())

    def change_triggered(self):
        if self._internal_change:
            return
        self.changed.emit((self.x, self.y))

    def copy(self):
        QtGui.QApplication.clipboard().setText('%i, %i' % (self.x, self.y))

    def paste(self):
        text = QtGui.QApplication.clipboard().text().strip(' ()\n\t')
        self.set_string_value(text)

    def pick(self):
        a2 = a2core.A2Obj().inst()
        text = a2ahk.call_lib_cmd('get_coordinates', cwd=a2.paths.a2)
        self.set_string_value(text)

    def set_string_value(self, text):
        if not isinstance(text, str):
            log.error('Cannot set non-string value!')
            return

        if not text.strip():
            log.error('Nothing to set!')
            return

        try:
            if ',' in text:
                x, y = text.split(',')
            elif ' ' in text:
                x, y = text.split()
            else:
                log.error('No separator found to split values!')
                return

            ints = [int(x), int(y)]

        except ValueError:
            log.error('Unable to split clipboard string to values!')
            return

        self.value = (ints[0], ints[1])


if __name__ == '__main__':
    import a2widget.demo.a2coords_field
    a2widget.demo.a2coords_field.show()
