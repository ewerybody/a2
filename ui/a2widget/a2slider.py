"""
A slider widget that emits proper signals when the slider range is clicked,
solves the field<>slider juggling and allows for float values right away.
"""
from functools import partial

from PySide import QtGui, QtCore


class A2Slider(QtGui.QWidget):
    """
    Signals:
    value_changed = immediately emitted on any value change, best for ui updates. Rapid fires on slide!
    editing_finished = emitted when sliding ended OR slider bar was clicked or field changed
    """
    value_changed = QtCore.Signal(float)
    slider_released = QtCore.Signal(float)

    def __init__(self, parent, has_slider=True, has_field=True, value=1.0, mini=0, maxi=100, decimals=1, step_len=1):
        super(A2Slider, self).__init__(parent)
        self.main_layout = QtGui.QHBoxLayout(self)
        self.setLayout(self.main_layout)

        self._slider_pressed = None
        self._ignore_change = False

        self.slider = None
        self.value_ctrl = None
        self.has_field = has_slider
        self.has_slider = has_field

        self._decimals = decimals
        self._min = mini
        self._max = maxi
        self._value = value
        self._step_len = step_len
        self._init_ctrls()

    def _init_ctrls(self):
        """
        Under the hood the slider
        """

    def set_slider_pressed(self, state):
        self._slider_pressed = state

    def set_slider(self, value):
        self._ignore_change = True
        self.slider.setValue(value)
        self._ignore_change = False

    def slider_change(self, value=None):
        if self._ignore_change:
            return

        if value is None:
            value = self.value_ctrl.value()
        else:
            self.value_ctrl.setValue(value)

        if self._slider_pressed:
            return
        print('value: %s' % value)

    @property
    def has_field(self):
        return self.slider is not None

    @has_field.setter
    def has_field(self, state):
        if state and self.value_ctrl is None:
            self.value_ctrl = QtGui.QDoubleSpinBox()
            self.value_ctrl.editingFinished.connect(self.value_changed.emit)
            self.main_layout.addWidget(self.value_ctrl)
        elif not state and self.value_ctrl is not None:
            self.value_ctrl.deleteLater()
            self.value_ctrl = None

    @property
    def has_slider(self):
        return self.slider is not None

    @has_slider.setter
    def has_slider(self, state):
        if state and self.slider is None:
            self.slider = QtGui.QSlider(self)
            self.slider.setOrientation(QtCore.Qt.Horizontal)
            self.slider.valueChanged.connect(self.slider_change)
            self.slider.sliderPressed.connect(partial(self.set_slider_pressed, True))
            self.slider.sliderReleased.connect(partial(self.set_slider_pressed, False))
            self.slider.sliderReleased.connect(self.slider_change)
            if self.value_ctrl is not None:
                self.value_ctrl.valueChanged.connect(self.set_slider)
            print('self.main_layout: %s' % self.main_layout)
            self.main_layout.addWidget(self.slider)
        elif not state and self.slider is not None:
            self.slider.deleteLater()
            self.slider = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.setValue(value)

    def setValue(self, value):
        self._value = value
        if self.value_ctrl is not None:
            self.value_ctrl.setValue(value)
#        if self.slider is not None:
#            self.slider

    @property
    def decimals(self):
        return self._decimals

    @decimals.setter
    def decimals(self, value):
        self.setDecimals(value)

    def setDecimals(self, value):
        self._decimals = value
        if self.value_ctrl is not None:
            self.value_ctrl.setDecimals(value)
#        if self.slider is not None:
#            self.slider

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, value):
        self.setMinimum(value)

    def setMinimum(self, value):
        self._min = value
        if self.value_ctrl is not None:
            self.value_ctrl.setMinimum(value)
#        if self.slider is not None:
#            self.slider

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, value):
        self.setMaximum(value)

    def setMaximum(self, value):
        self._max = value
        if self.value_ctrl is not None:
            self.value_ctrl.setMaximum(value)
#        if self.slider is not None:
#            self.slider

    @property
    def step_len(self):
        return self._step_len

    @step_len.setter
    def step_len(self, value):
        self.setMaximum(value)

    def setSingleStep(self, value):
        self._step_len = value
        if self.value_ctrl is not None:
            self.value_ctrl.setSingleStep(value)

#        if self.slider is not None:
#            self.slider


#            self.slider.setValue(self.value)
#            self.slider.setMinimum(self.min)
#            self.slider.setMaximum(self.max)
#            self.slider.setSingleStep(self.step_len)

#            self.value_ctrl.setMinimum(self.min)
#            self.value_ctrl.setMaximum(self.max)
#            self.value_ctrl.setDecimals(self.decimals)
#            self.value_ctrl.setSingleStep(self.step_len)
#            self.value_ctrl.setValue(self.value)

    def setOrientation(self, orientation):
        if self.slider is not None:
            self.slider.setOrientation(orientation)
