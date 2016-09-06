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
    editing_finished = emitted when sliding ended OR slider bar was clicked or field change is finished
    """
    value_changed = QtCore.Signal(float)
    editing_finished = QtCore.Signal(float)

    def __init__(self, parent, has_slider=True, has_field=True, value=1.0, mini=0, maxi=100, decimals=1, step_len=1):
        super(A2Slider, self).__init__(parent)
        self.main_layout = QtGui.QHBoxLayout(self)
        self.setLayout(self.main_layout)

        self._slider_pressed = None
        self._slider_ignore = False
        self._field_ignore = False

        self.slider = None
        self.value_ctrl = None
        self.has_field = has_slider
        self.has_slider = has_field

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
        self._slider_factor = pow(10, self._decimals)
        self.setValue(self._value)

    def emit_changed(self):
        self.value_changed.emit(self._value)

    def emit_finished(self):
        self.editing_finished.emit(self._value)

    def _set_slider_pressed(self, state):
        self._slider_pressed = state

    def _slider_change(self, value):
        if self._slider_ignore:
            return

        value = value / self._slider_factor
        if value != self._value:
            self._value = value
            self._field_ignore = True
            self.value_ctrl.setValue(self._value)
            self._field_ignore = False
            self.emit_changed()

        if self._slider_pressed:
            return
        self.emit_finished()

    def _field_change(self, value):
        if self._field_ignore:
            return

        if value != self._value:
            self._value = value
            self.emit_changed()

            if self.slider is not None:
                self._slider_ignore = True
                self.slider.setValue(value * self._slider_factor)
                self._slider_ignore = False

    @property
    def has_field(self):
        return self.slider is not None

    @has_field.setter
    def has_field(self, state):
        if state and self.value_ctrl is None:
            self.value_ctrl = QtGui.QDoubleSpinBox()
            self.value_ctrl.editingFinished.connect(self.emit_finished)
            self.main_layout.addWidget(self.value_ctrl)
            self.value_ctrl.valueChanged.connect(self._field_change)
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
            self.slider.valueChanged.connect(self._slider_change)
            self.slider.sliderPressed.connect(partial(self._set_slider_pressed, True))
            self.slider.sliderReleased.connect(partial(self._set_slider_pressed, False))
            self.slider.sliderReleased.connect(self.emit_finished)
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
        if self.slider is not None:
            self.slider.setValue(value * self._slider_factor)

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
        if self.slider is not None:
            self._slider_factor = pow(10, self._decimals)
            self.setValue(self._value)

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
        if self.slider is not None:
            self.slider.setMinimum(self._min * self._slider_factor)

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
        if self.slider is not None:
            self.slider.setMaximum(self._max * self._slider_factor)

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
        if self.slider is not None:
            self.slider.setSingleStep(self._step_len * self._slider_factor)


    def setOrientation(self, orientation):
        if self.slider is not None:
            self.slider.setOrientation(orientation)


if __name__ == '__main__':
    # a little slider demo
    def finished(x):
        print('    finished: %s' % x)
    def changed(x):
        print('    changed: %s' % x)

    app = QtGui.QApplication([])
    win = QtGui.QMainWindow()
    w = QtGui.QWidget()
    win.setCentralWidget(w)
    l = QtGui.QVBoxLayout(w)
    w.setLayout(l)
    s = A2Slider(w)
    s.setMinimumWidth(500)
    s.setSingleStep(0.1)
    s.setDecimals(2)
    s.setMinimum(0)
    s.setMaximum(2)
    s.editing_finished.connect(finished)
    s.value_changed.connect(changed)
    l.addWidget(s)
    win.show()
    app.exec_()
