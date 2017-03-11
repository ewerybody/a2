"""
Created on 08.03.2017

@author: eric
"""
from PySide import QtGui, QtCore
from collections import OrderedDict

import a2ahk
import a2core


class A2CoordsField(QtGui.QWidget):
    changed = QtCore.Signal(tuple)

    def __init__(self, parent=None):
        super(A2CoordsField, self).__init__(parent)

        self.main_layout = QtGui.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

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
        self.tool_button.clicked.connect(self.show_menu)
        self.main_layout.addWidget(self.tool_button)

        self.menu_items = OrderedDict()
        self.menu_items['copy'] = QtGui.QAction('Copy Coordinates', self, triggered=self.copy)
        self.menu_items['paste'] = QtGui.QAction('Paste Coordinates', self, triggered=self.paste)
        self.menu_items['pick'] = QtGui.QAction('Pick Coordinates', self, triggered=self.pick)
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

        self.x_field.setValue(values[0])
        self.y_field.setValue(values[1])

    def show_menu(self):
        self.menu.clear()
        for action in self.menu_items.values():
            self.menu.addAction(action)
        # copy coordinates
        # paste coordinates
        # pick coordinates
        self.menu.popup(QtGui.QCursor.pos())

    def change_triggered(self):
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
        if ',' in text:
            x, y = text.split(',')
        elif ' ' in text:
            x, y = text.split()
        self.value = (int(x.strip()), int(y.strip()))

if __name__ == '__main__':
    import a2widget.demo.a2coords_field
    a2widget.demo.a2coords_field.show()
