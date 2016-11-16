'''
Created on Mar 22, 2016

@author: eRiC
'''
import a2ctrl
from functools import partial
from PySide import QtGui, QtCore
from a2element import number_edit_ui, DrawCtrl, EditCtrl


class Draw(DrawCtrl):
    def __init__(self, main, cfg, mod):
        super(Draw, self).__init__(main, cfg, mod)
        value = self.get_user_value((float, int), default=0.0)
        self.value = _toggle_type(self.cfg['decimals'], value)

        self._setupUi()
        self.slider_pressed = None
        self.ignore_change = False

    def _setupUi(self):
        self.layout = QtGui.QHBoxLayout(self)
        self.label_text = self.cfg.get('label', '')
        self.label = QtGui.QLabel(self.label_text, self)
        self.layout.addWidget(self.label)

        self.value_ctrl = QtGui.QDoubleSpinBox()
        self.value_ctrl.setMinimum(self.cfg.get('min', 0))
        self.value_ctrl.setMaximum(self.cfg.get('max', 100))
        self.value_ctrl.setDecimals(self.cfg.get('decimals', 1))
        self.value_ctrl.setSingleStep(self.cfg.get('step_len', 1))
        self.value_ctrl.setValue(self.value)
        self.value_ctrl.editingFinished.connect(self.delayed_check)
        self.layout.addWidget(self.value_ctrl)

        if self.cfg.get('suffix'):
            self.suffix_label = QtGui.QLabel(self.cfg.get('suffix'))
            self.layout.addWidget(self.suffix_label)
        if self.cfg.get('slider'):
            self.slider = QtGui.QSlider(self)
            self.slider.setValue(self.value)
            self.slider.setOrientation(QtCore.Qt.Horizontal)
            self.slider.setMinimum(self.cfg.get('min', 0))
            self.slider.setMaximum(self.cfg.get('max', 100))
            self.slider.setSingleStep(self.cfg.get('step_len', 1))

            self.slider.valueChanged.connect(self.slider_change)
            self.slider.sliderPressed.connect(partial(self.set_slider_pressed, True))
            self.slider.sliderReleased.connect(partial(self.set_slider_pressed, False))
            self.slider.sliderReleased.connect(self.slider_change)
            self.value_ctrl.valueChanged.connect(self.set_slider)

            self.layout.addWidget(self.slider)

        self.setLayout(self.layout)

    def set_slider_pressed(self, state):
        self.slider_pressed = state

    def set_slider(self, value):
        self.ignore_change = True
        self.slider.setValue(value)
        self.ignore_change = False

    def slider_change(self, value=None):
        if self.ignore_change:
            return

        if value is None:
            value = self.value_ctrl.value()
        else:
            self.value_ctrl.setValue(value)

        if self.slider_pressed:
            return
        self.delayed_check()

    def check(self, value=None):
        if value is None:
            value = self.value_ctrl.value()

        # prevent being called double
        if self.value == value:
            return

        self.value = _toggle_type(self.cfg.get('decimals', 0), value)
        self.set_user_value(self.value)
        self.change('variables')
        super(Draw, self).check()


class Edit(EditCtrl):
    """
    Edit-control for Numbers: integer OR float!
    """
    def __init__(self, cfg, main, parentCfg):
        super(Edit, self).__init__(cfg, main, parentCfg, add_layout=False)
        self.helpUrl = self.a2.urls.help_number

        self.ui = number_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)

        self.check_new_name()
        a2ctrl.connect.cfg_controls(self.cfg, self.ui)

        self.ui.value.valueChanged.connect(self.set_value)
        if 'value' in self.cfg:
            self.ui.value.setValue(self.cfg['value'])
        else:
            self.set_value()

        for ctrl, set_func in [(self.ui.cfg_min, self.ui.value.setMinimum),
                               (self.ui.cfg_max, self.ui.value.setMaximum),
                               (self.ui.cfg_decimals, self.ui.value.setDecimals),
                               (self.ui.cfg_step_len, self.ui.value.setSingleStep)]:
            ctrl.valueChanged.connect(set_func)
        self.ui.cfg_decimals.valueChanged.connect(partial(self.set_value, None))

    def set_value(self, value=None, *args):
        if value is None:
            value = self.ui.value.value()

        self.cfg['value'] = _toggle_type(self.cfg['decimals'], value)

    @staticmethod
    def element_name():
        return 'Number'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().number


def _toggle_type(decimals, value):
    if decimals == 0:
        value = int(value)
    else:
        value = float(value)
    return value


def get_settings(module_key, cfg, db_dict, user_cfg):
    db_dict.setdefault('variables', {})
    value = a2ctrl.get_cfg_value(cfg, user_cfg, typ=(int, float), default=0.0)
    db_dict['variables'][cfg['name']] = value
