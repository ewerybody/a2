'''
Created on Mar 22, 2016

@author: eRiC
'''
import a2ctrl
import logging
from functools import partial
from PySide import QtGui, QtCore
from a2ctrl import number_edit_ui


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Draw(a2ctrl.DrawCtrl):
    def __init__(self, main, cfg, mod):
        super(Draw, self).__init__(main, cfg, mod)
        value = a2ctrl.get_cfg_value(self.cfg, self.userCfg, 'value', (float, int), 0.0)
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
            #self.slider.sliderReleased.connect(self.slider_change)
            self.slider.sliderPressed.connect(partial(self.set_slider_pressed, True))
            self.slider.sliderReleased.connect(partial(self.set_slider_pressed, False))
            self.slider.sliderReleased.connect(self.slider_change)
            self.layout.addWidget(self.slider)
            
            self.value_ctrl.valueChanged.connect(self.set_slider)

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
        self.mod.set_user_cfg(self.cfg, 'value', self.value)
        self.change('variables')


class Edit(a2ctrl.EditCtrl):
    """
    Checkbox to control boolean values for the a2 runtime.
    We might put them to the db and get and fetch from there or first: just write them into
    code directly and start with the variables include.
    """
    def __init__(self, cfg, main, parentCfg):
        self.ctrlType = 'String'
        super(Edit, self).__init__(cfg, main, parentCfg, addLayout=False)
        self.helpUrl = self.a2.urls.help_number
        
        self.ui = number_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)

        self.ui.internalNameLabel.setMinimumWidth(a2ctrl.labelW)
        
        self.connect_cfg_controls(self.ui, exclude=self.ui.cfg_value)
        
        self.ui.cfg_value.valueChanged.connect(self.set_value)
        if 'value' in self.cfg:
            self.ui.cfg_value.setValue(self.cfg['value'])
        else:
            self.set_value()
        
        self.mainWidget.setLayout(self.ui.editLayout)
        
        for ctrl, set_func in [(self.ui.cfg_min, self.ui.cfg_value.setMinimum),
                               (self.ui.cfg_max, self.ui.cfg_value.setMaximum),
                               (self.ui.cfg_decimals, self.ui.cfg_value.setDecimals),
                               (self.ui.cfg_step_len, self.ui.cfg_value.setSingleStep)]:
            ctrl.valueChanged.connect(set_func)
        self.ui.cfg_decimals.valueChanged.connect(partial(self.set_value, None))

    def set_value(self, value=None, *args):
        if value is None:
            value = self.ui.cfg_value.value()

        self.cfg['value'] = _toggle_type(self.cfg['decimals'], value)


def _toggle_type(decimals, value):
    if decimals == 0:
        value = int(value)
    else:
        value = float(value)
    return value
