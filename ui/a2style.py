import os
import a2util
from PySide2 import QtWidgets


BASE_DPI = 96.0
DEFAULT_STYLE = 'light'
TEMPLATE_NAME = 'css.template'
DEFAULTS_NAME = 'css_defaults.json'
STYLE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'style')


class A2StyleBuilder(object):
    def __init__(self, style_name=None):
        if style_name is None:
            style_name = DEFAULT_STYLE

        self._user_scale = None
        self._last_style = None
        self._css_values = {}
        self.template = None
        self.defaults = {}

        self.get_local_scale()
        self.load_style(style_name)

    def get_local_scale(self):
        physical_dpi = QtWidgets.QApplication.instance().desktop().physicalDpiX()
        local_scale = physical_dpi / BASE_DPI
        self._css_values['local_scale'] = local_scale

    def load_style(self, style_name):
        template_path = os.path.join(STYLE_PATH, style_name, DEFAULTS_NAME)
        self.defaults = a2util.json_read(template_path)
        with open(os.path.join(STYLE_PATH, style_name, TEMPLATE_NAME)) as fobj:
            self.template = fobj.read()

    def get(self, value_name, default=None):
        return self._css_values.get(value_name, default)

    def get_value_dict(self):
        from copy import deepcopy
        return deepcopy(self._css_values)

    def get_style(self, user_scale=1.0):
        if user_scale == self._user_scale and self._last_style is not None:
            return self._last_style

        self._user_scale = user_scale
        self._css_values['user_scale'] = user_scale
        scale = self._css_values['local_scale'] * user_scale
        self._css_values['scale'] = scale

        for name, value in self.defaults.items():
            if isinstance(value, int):
                value = int(scale * float(value))
            self._css_values[name] = value

        return self.template % self._css_values

    @property
    def user_scale(self):
        return self._user_scale
