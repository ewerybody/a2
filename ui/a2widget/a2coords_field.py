from a2qt import QtCore, QtWidgets

import a2ahk
import a2ctrl
import a2core
from a2widget.a2more_button import A2MoreButton


log = a2core.get_logger(__name__)


class A2CoordsField(QtWidgets.QWidget):
    changed = QtCore.Signal()
    changed_to = QtCore.Signal(tuple)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.x_field = QtWidgets.QSpinBox(self)
        self.x_field.setMinimum(-16777214)
        self.x_field.setMaximum(16777215)
        self.x_field.valueChanged.connect(self.change_triggered)
        self.main_layout.addWidget(self.x_field)

        self.y_field = QtWidgets.QSpinBox(self)
        self.y_field.setMinimum(-16777214)
        self.y_field.setMaximum(16777215)
        self.y_field.valueChanged.connect(self.change_triggered)
        self.main_layout.addWidget(self.y_field)

        self.a2option_button = A2MoreButton(self)
        self.a2option_button.menu_called.connect(self.show_menu)
        self.main_layout.addWidget(self.a2option_button)

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
        return [self.x, self.y]

    @value.setter
    def value(self, this):
        self.set_value(this)

    def set_value(self, values, y=None):
        if isinstance(values, (tuple, list)) and len(values) < 2:
            raise ValueError(
                f'A2CoordsField.set_value needs tuple or list '
                f'of 2 integers!\n  received: {values}'
            )

        if isinstance(values, QtCore.QPoint):
            values = [values.x(), values.y()]
        elif isinstance(values, QtCore.QSize):
            values = [values.width(), values.height()]

        self.x_field.blockSignals(True)
        self.y_field.blockSignals(True)
        self.x_field.setValue(values[0])
        self.y_field.setValue(values[1])
        self.x_field.blockSignals(False)
        self.y_field.blockSignals(False)
        self.change_triggered()

    def show_menu(self, menu):
        for func, icon in [
            (self.copy, a2ctrl.Icons.copy),
            (self.paste, a2ctrl.Icons.paste),
            (self.pick, a2ctrl.Icons.number),
        ]:
            menu.addAction(icon, func.__name__.title() + ' Coordinates', func)

    def change_triggered(self):
        self.changed.emit()
        self.changed_to.emit((self.x, self.y))

    def copy(self):
        QtWidgets.QApplication.clipboard().setText('%i, %i' % (self.x, self.y))

    def paste(self):
        text = QtWidgets.QApplication.clipboard().text().strip(' ()\n\t')
        self.set_string_value(text)

    def pick(self):
        text = a2ahk.call_lib_cmd('get_coordinates')
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

    def setValue(self, value):
        """In Designer this might be set so we need to handle ints not to break it."""
        if isinstance(value, int):
            return
        elif isinstance(value, str):
            self.set_string_value(value)
        else:
            self.set_value(value)


if __name__ == '__main__':
    from a2widget.demo import a2coords_field_demo

    a2coords_field_demo.show()
