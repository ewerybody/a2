import os
from pathlib import Path
import a2util
from PySide6 import QtWidgets, QtCore

import a2core
import a2toolbox.reg

BASE_DPI = 96.0
DARK_THEME = 'dark'
LIGHT_THEME = 'light'
TEMPLATE_NAME = 'template.qss'
DEFAULTS_NAME = 'qss_defaults.json'

WIN_REG_THEME_PATH = r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize'
WIN_REG_THEME_ATTR = 'AppsUseLightTheme'

_TEMP = {}


def get() -> str:
    user_theme = get_user()
    if user_theme:
        return user_theme
    return get_system()


def get_user() -> str:
    a2 = a2core.get()
    theme = a2.db.get('theme')
    if theme and os.path.isdir(os.path.join(a2.paths.theme, theme)):
        return theme

    if temp_theme := _TEMP.get('temp_theme'):
        return temp_theme
    return ''


def get_system() -> str:
    if a2toolbox.reg.read_value(WIN_REG_THEME_PATH, WIN_REG_THEME_ATTR):
        return LIGHT_THEME
    return DARK_THEME


class A2StyleBuilder(QtCore.QObject):
    def __init__(self, style_name=None):
        super(A2StyleBuilder, self).__init__()
        if style_name is None:
            style_name = get()
        self._user_scale = None
        self._last_style = None
        self._css_values = {}
        self.template = ''
        self.defaults = {}

        self.get_local_scale()
        self.load_style(style_name)

    def get_local_scale(self):
        physical_dpi = QtWidgets.QApplication.primaryScreen().physicalDotsPerInchY()
        local_scale = physical_dpi / BASE_DPI
        self._css_values['local_scale'] = local_scale
        return local_scale

    def load_style(self, style_name):
        a2 = a2core.get()
        template_path = os.path.join(a2.paths.theme, style_name, DEFAULTS_NAME)
        self.defaults = a2util.json_read(template_path)
        target_template = Path(os.path.join(a2.paths.theme, style_name, TEMPLATE_NAME))
        self.template = target_template.read_text()

    def get(self, value_name, default=None):
        """
        Get a specific value from the calculated ones.
        :param str value_name: Name of the value to retrieve.
        :param float default: Default value in case there is None among the calculated ones.
        :rtype: float
        """
        return self._css_values.get(value_name, default)

    def get_value_dict(self):
        """
        Get the dictionary of calculated styling values.
        :rtype: dict
        """
        from copy import deepcopy

        return deepcopy(self._css_values)

    def get_style(self, user_scale=1.0):
        """
        Build stylesheet code from the user scale and default variables.

        :param user_scale float: User defined factor to modify the variable sizes by.
        :return: QSS Style sheet code with calculated values.
        :rtype: str
        """
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

    def scale(self, value):
        """
        Multiply a value by resulting scale.

        Which is calculated from local physical ui scale and user set scale factor.
        """
        return self.get('scale', 1) * value
