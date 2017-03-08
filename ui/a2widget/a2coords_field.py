"""
Created on 08.03.2017

@author: eric
"""


from PySide import QtGui, QtCore


class A2CoordsField(QtGui.QWidget):
    def __init__(self, parent=None):
        super(A2CoordsField, self).__init__(parent)

        self.main_layout = QtGui.QHBoxLayout(self)

        self.x_field = QtGui.QSpinBox(self)
        self.x_field.setMinimum(-16777214)
        self.x_field.setMaximum(16777215)
        self.main_layout.addWidget(self.x_field)
        self.y_field = QtGui.QSpinBox(self)
        self.y_field.setMinimum(-16777214)
        self.y_field.setMaximum(16777215)
        self.main_layout.addWidget(self.y_field)

        self.tool_button = QtGui.QToolButton(self)
        self.main_layout.addWidget(self.tool_button)

    def set_value(self, values):
        if not isinstance(values, (tuple, list)) or len(values) <= 2:
            raise RuntimeError('A2CoordsField.set_value needs a tuple or list of 2 integers')

        self.x_field.setValue(values[0])
        self.y_field.setValue(values[1])


if __name__ == '__main__':
    import a2widget.demo.a2coords_field
    a2widget.demo.a2coords_field.show()
