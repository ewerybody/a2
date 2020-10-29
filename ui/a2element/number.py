from functools import partial

import a2ctrl

from PySide2 import QtWidgets

from a2widget.a2slider import A2Slider
from a2element import number_edit_ui, DrawCtrl, EditCtrl


class Draw(DrawCtrl):
    def __init__(self, *args):
        super(Draw, self).__init__(*args)

        value = self.get_user_value((float, int), default=0.0)
        self.value = _toggle_type(self.cfg['decimals'], value)

        self.suffix_label = None
        self._setup_ui()

    def _setup_ui(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.label_text = self.cfg.get('label', '')
        self.label = QtWidgets.QLabel(self.label_text, self)
        self.main_layout.addWidget(self.label)

        if self.cfg.get('suffix'):
            self.suffix_label = QtWidgets.QLabel(self.cfg.get('suffix'))

        if self.cfg.get('slider'):
            self.slider = A2Slider(self)
            self.slider.value = self.value
            self.slider.minmax = (self.cfg.get('min', 0), self.cfg.get('max', 100))
            self.slider.setSingleStep(self.cfg.get('step_len', 1))
            self.slider.editing_finished.connect(self.delayed_check)
            self.main_layout.addWidget(self.slider)
            if self.cfg.get('suffix'):
                self.slider.main_layout.insertWidget(1, self.suffix_label)
        else:
            self.value_ctrl = QtWidgets.QDoubleSpinBox()
            self.value_ctrl.setMinimum(self.cfg.get('min', 0))
            self.value_ctrl.setMaximum(self.cfg.get('max', 100))
            self.value_ctrl.setDecimals(self.cfg.get('decimals', 1))
            self.value_ctrl.setSingleStep(self.cfg.get('step_len', 1))
            self.value_ctrl.setValue(self.value)
            self.value_ctrl.editingFinished.connect(self.delayed_check)
            self.main_layout.addWidget(self.value_ctrl)
            if self.cfg.get('suffix'):
                self.main_layout.addWidget(self.suffix_label)

        self.setLayout(self.main_layout)

    def check(self, *args):
        if args:
            value = args[0]
        else:
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

    The actual 'value' field is not covered by cfg_controls because
    we want to change the int/float type according to the decimals value.
    """
    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg, add_layout=False)
        self.helpUrl = self.a2.urls.help_number

        a2ctrl.check_ui_module(number_edit_ui)
        self.ui = number_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)

        self.check_new_name()
        a2ctrl.connect.cfg_controls(self.cfg, self.ui)

        # Make value widget adapt to changes of other settings.
        for ctrl, set_func in (
            (self.ui.cfg_min, self.ui.value.setMinimum),
            (self.ui.cfg_max, self.ui.value.setMaximum),
            (self.ui.cfg_decimals, self.ui.value.setDecimals),
            (self.ui.cfg_step_len, self.ui.value.setSingleStep)
        ):
            if ctrl.objectName().startswith('cfg_'):
                set_func(self.cfg.get(ctrl.objectName()[4:], ctrl.value()))
            ctrl.valueChanged.connect(set_func)
        # Make sure valueChanged signal does not pass a value into set_value
        self.ui.cfg_decimals.valueChanged.connect(partial(self.set_value, None))

        # Setting actual value widget just after all specs have been set.
        if 'value' in self.cfg:
            self.ui.value.setValue(self.cfg['value'])
        else:
            self.set_value()
        self.ui.value.valueChanged.connect(self.set_value)

    def set_value(self, value=None, *_args):
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


def get_settings(_module_key, cfg, db_dict, user_cfg):
    db_dict.setdefault('variables', {})
    value = a2ctrl.get_cfg_value(cfg, user_cfg, typ=(int, float), default=0.0)
    db_dict['variables'][cfg['name']] = value
