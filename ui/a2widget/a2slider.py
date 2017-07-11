"""
A Qt/PySide slider widget that:
* emits proper signals when the slider range is clicked,
* solves the field<>slider juggling and
* allows for float values right away
"""
from functools import partial

from PySide import QtGui, QtCore


class A2Slider(QtGui.QWidget):
    #: Immediately emitted on any value change, best for ui updates. Rapid fires on slide!
    value_changed = QtCore.Signal(float)
    #: Emitted when sliding ended OR slider bar was clicked or field change is finished.
    editing_finished = QtCore.Signal(float)

    def __init__(self, parent=None, has_field=True, value=1.0, mini=0, maxi=100, decimals=2, step_len=1):
        super(A2Slider, self).__init__(parent)
        self.main_layout = QtGui.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        self._slider_pressed = None
        self._slider_ignore = False
        self._field_ignore = False

        self.value_ctrl = None
        self.has_field = has_field
        self.slider = self._build_slider()

        self._decimals = decimals
        self._min = mini
        self._max = maxi
        self._value = value
        self._step_len = step_len
        self._slider_factor = 1.0
        self._init_ctrls()

    def _init_ctrls(self):
        """
        Under the hood the slider always uses integers. So according to the decimals
        we're displaying we multiply the values * 10
        """
        self.setDecimals()
        self.setMinimum()
        self.setMaximum()
        self.setValue()
        self.setSingleStep()

    def _build_slider(self):
        slider = QtGui.QSlider(self)
        slider.setOrientation(QtCore.Qt.Horizontal)
        slider.valueChanged.connect(self._slider_change)
        slider.sliderPressed.connect(partial(self._set_slider_pressed, True))
        slider.sliderReleased.connect(partial(self._set_slider_pressed, False))
        slider.sliderReleased.connect(self._emit_finished)
        self.main_layout.addWidget(slider)
        return slider

    def _emit_changed(self):
        self.value_changed.emit(self._value)

    def _emit_finished(self):
        self.editing_finished.emit(self._value)

    def _set_slider_pressed(self, state):
        self._slider_pressed = state

    def _slider_change(self, value):
        if self._slider_ignore:
            return

        value = value / self._slider_factor
        if value != self._value:
            self._value = value
            if self.has_field:
                self._field_ignore = True
                self.value_ctrl.setValue(self._value)
                self._field_ignore = False
            self._emit_changed()

        if self._slider_pressed:
            return
        self._emit_finished()

    def _field_change(self, value):
        if self._field_ignore:
            return

        value = round(value, self.decimals)
        if value != self._value:
            self._value = value
            self._emit_changed()

            self._slider_ignore = True
            self.slider.setValue(value * self._slider_factor)
            self._slider_ignore = False

    @property
    def has_field(self):
        """
        Queries if the widget has a number input child widget.
        :rtype: bool
        """
        return self.value_ctrl is not None

    @has_field.setter
    def has_field(self, state):
        """
        :param bool state: To set if the widget shall hava a number input child widget.
        """
        if state and self.value_ctrl is None:
            self.value_ctrl = QtGui.QDoubleSpinBox()
            self.main_layout.addWidget(self.value_ctrl)
            self.value_ctrl.valueChanged.connect(self._field_change)
            self.value_ctrl.editingFinished.connect(self._emit_finished)
        elif not state and self.has_field:
            self.value_ctrl.deleteLater()
            self.value_ctrl = None

    @property
    def value(self):
        """
        Returns the current value of the widget.
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the current value of the widget.
        :param float value: The value.
        """
        self.setValue(value)

    def setValue(self, value=None):
        """
        Sets the current value of the widget.
        :param float value: The value.
        """
        if value is not None:
            self._value = value

        if self.has_field:
            self.value_ctrl.setValue(self._value)
        self.slider.setValue(self._value * self._slider_factor)

    @property
    def decimals(self):
        """
        Gets the number of digits after the comma.
        :rtype: int
        """
        return self._decimals

    @decimals.setter
    def decimals(self, value):
        """
        Sets the number of digits after the comma.
        :param int value: The number of digits.
        """
        self.setDecimals(value)

    def setDecimals(self, value=None):
        """
        Sets the number of digits after the comma.
        :param int value: The number of digits.
        """
        if value is not None:
            self._decimals = value

        if self.has_field:
            self.value_ctrl.setDecimals(self._decimals)
        self._slider_factor = pow(10, self._decimals)
        self.setMinimum()
        self.setMaximum()
        self.setValue(self._value)

    @property
    def min(self):
        """
        Gets the widgets numerical minimum.
        :rtype: float
        """
        return self._min

    @min.setter
    def min(self, value):
        """
        Sets the widgets numerical minimum.
        :param float value: Minimum value the widget can have.
        """
        self.setMinimum(value)

    def setMinimum(self, value=None):
        """
        Sets the widgets numerical minimum.
        :param float value: Minimum value the widget can have.
        """
        if value is not None:
            self._min = value

        if self.has_field:
            self.value_ctrl.setMinimum(self._min)
        self.slider.setMinimum(self._min * self._slider_factor)

    @property
    def max(self):
        """
        Gets the widgets numerical maximum.
        :rtype: float
        """
        return self._max

    @max.setter
    def max(self, value):
        """
        Sets the widgets numerical maximum.
        :param float value: Maximum value the widget can have.
        """
        self.setMaximum(value)

    def setMaximum(self, value=None):
        """
        Sets the widgets numerical maximum.
        :param float value: Maximum value the widget can have.
        """
        if value is not None:
            self._max = value

        if self.has_field:
            self.value_ctrl.setMaximum(self._max)
        self.slider.setMaximum(self._max * self._slider_factor)

    @property
    def minmax(self):
        """
        Gets both minimum and maximum values.
        :rtype: tuple
        """
        return (self._min, self._max)

    @minmax.setter
    def minmax(self, these):
        """
        Sets both minimum and maximum values.
        :param tuple these: Tuple of floats with minimum & maximum.
        """
        self.setMinimum(these[0])
        self.setMaximum(these[1])

    @property
    def step_len(self):
        """
        Gets step length or single step for both the slider and the field, if any.
        :rtype: float
        """
        return self._step_len

    @step_len.setter
    def step_len(self, value):
        """
        Sets step length or single step for both the slider and the field, if any.

        When the user uses the arrows to change the spin box's value the value will
         be incremented/decremented by the amount ...

        :param float value: Length/amount of a single step.
        """
        self.setSingleStep(value)

    def setSingleStep(self, value=None):
        """
        Sets step length or single step for both the slider and the field, if any.

        When the user uses the arrows to change the spin box's value the value will
         be incremented/decremented by the amount ...

        :param float value: Length/amount of a single step.
        """
        if value is not None:
            self._step_len = value

        if self.has_field:
            self.value_ctrl.setSingleStep(self._step_len)
        self.slider.setSingleStep(self._step_len * self._slider_factor)

    def setOrientation(self, orientation):
        """
        Just to be consistent with promoting from QSlider. It works! ... but:
        This is not really supported as there would be things to be amended visually.

        :param orientation: QtCore.Qt.Vertical or QtCore.Qt.Horizontal
        """
        self.slider.setOrientation(orientation)


if __name__ == '__main__':
    import a2widget.demo.a2slider
    a2widget.demo.a2slider.show()
