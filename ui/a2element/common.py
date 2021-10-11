"""
The a2 element foundations.
"""
from functools import partial

from a2qt import QtCore, QtGui, QtWidgets

import a2core
import a2ctrl
import a2util
from a2ctrl import Icons

DELAYED_CHECK_DELAY = 500


class DrawCtrlMixin:
    """
    Display widget to host everything that you want to show to the
    user for him to set up on your module.
    """

    def __init__(self, main, cfg, mod, user_cfg=None):
        self.a2 = a2core.A2Obj.inst()
        self.main = main
        self.cfg = cfg
        self.mod = mod

        self._check_scheduled = False
        self.is_expandable_widget = False
        self._check_timer = QtCore.QTimer()
        self._check_timer.setInterval(DELAYED_CHECK_DELAY)
        self._check_timer.timeout.connect(self._check)
        self._check_args = None
        self.user_cfg = user_cfg or {}

    def get_user_value(self, typ, name=None, default=None):
        """
        Get a user value. 'value'
        Name is 'value' by default so you can just get the default value by stating the type. Voila!
        """
        return a2ctrl.get_cfg_value(self.cfg, self.user_cfg, name, typ, default)

    def get_user_dict(self):
        """
        Get element configuration PLUS anything set from the user.
        :return: Dictionary with user values inserted.
        """
        user_dict = {}
        for key in set(list(self.user_cfg) + list(self.cfg)):
            try:
                user_dict[key] = self.user_cfg[key]
            except (TypeError, KeyError):
                user_dict[key] = self.cfg[key]
        return user_dict

    def set_user_value(self, value=None, name=None):
        """
        Set a user value in the module config.
        Name is None by by default so you can just set the default value by ... well:
        passing the value. Voila!
        """
        if value is None:
            value = self.user_cfg

        try:
            self.mod.set_user_cfg(self.cfg, value, name)
        except AttributeError:
            # cannot set config if no module given
            pass

    def has_user_cfg(self):
        """
        Tell if the element has user data saved.
        :rtype: bool
        """
        if self.mod is None:
            return False
        name = a2util.get_cfg_default_name(self.cfg)
        return self.mod.is_in_user_cfg(name)

    def clear_user_cfg(self):
        name = a2util.get_cfg_default_name(self.cfg)
        self.mod.clear_user_cfg_name(name)
        self.main.load_runtime_and_ui()

    def change(self, specific=None):
        """
        Triggers the module to save it's settings to the database and
        a2 include rewrite and restart if the module is enabled.
        """
        if self.mod is None:
            return

        self.mod.change()
        if self.mod.enabled:
            self.main.settings_changed(specific)

    def delayed_check(self, *args):
        """
        Calls the check method with a little delay to prevent spamming reload.
        """
        self._check_args = args
        self._check_timer.start()

    def _check(self):
        if self._check_timer.isActive():
            self._check_timer.stop()
        self.check(*self._check_args)

    def check(self, *args):
        """
        For the element to gather data from the widgets and call change on demand.
        To be re-implemented when subclassing DrawCtrl.
        """
        pass

    def get_ui_value(self):
        raise NotImplementedError('get_ui_value Implementation Missing!')

    def default_check(self, *args):
        if args:
            value = args[0]
        else:
            value = self.get_ui_value()

        # prevent being called double
        if self.value == value:
            return

        self.value = value
        self.set_user_value(value)
        self.change('variables')


class DrawCtrl(QtWidgets.QWidget, DrawCtrlMixin):
    """
    Display widget to host everything that you want to show to the
    user for him to set up on your module.
    """

    def __init__(self, main, cfg, mod, user_cfg=None):
        super(DrawCtrl, self).__init__(parent=main)
        DrawCtrlMixin.__init__(self, main, cfg, mod, user_cfg)


class EditCtrl(QtWidgets.QGroupBox):
    """
    frame widget for an edit control which enables basic arrangement of the
    control up & down as well as deleting the control.

    It's made to work with handwritten and compiled Uis right away.
    To embedd a compiled ui tell it so add_layout=False in the super()-statement:
        super(MyNewCtrl, self).__init__(add_layout=False)
    state the mainWidget in setupUi:
        self.ui.setupUi(self.mainWidget)
    and then set the self.mainWidget-layout to your top layout in the compiled ui:
        self.mainWidget.setLayout(self.ui.mytoplayout)

    TODO: currently this is embedded as menuitems on a button which is pretty shitty.
        I'd like to have some actual up/down buttons and an x to indicate delete
        functionality
    """

    changed = QtCore.Signal()
    menu_requested = QtCore.Signal()

    def __init__(self, cfg, main, parent_cfg, add_layout=True):
        super(EditCtrl, self).__init__()
        self.a2 = a2core.A2Obj.inst()
        self.cfg = cfg # type: dict[str, bool | int | float | str | list[str]]
        self.main = main
        self.parent_cfg = parent_cfg

        self._setup_ui(add_layout)
        self.help_url = ''
        self.is_expandable_widget = False

    @staticmethod
    def element_name():
        return 'EditCtrl'

    @staticmethod
    def element_icon():
        return None

    def _setup_ui(self, add_layout):
        # self.setTitle(self.cfg['typ'])
        self.setTitle(self.element_name())
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum
        )
        self.setSizePolicy(size_policy)

        self._ctrl_layout = QtWidgets.QGridLayout(self)
        self._ctrl_layout.setContentsMargins(0, 0, 0, 0)
        self._sub_layout = QtWidgets.QHBoxLayout()

        margin = self.get_style_value('margin', 8)
        self._sub_layout.setContentsMargins(margin, margin, margin, margin)

        self.mainWidget = QtWidgets.QWidget(self)
        self._sub_layout.addWidget(self.mainWidget)
        self._ctrl_layout.addLayout(self._sub_layout, 0, 0, 1, 1)

        if add_layout:
            self.mainLayout = QtWidgets.QVBoxLayout()
            spacing = self.get_style_value('small_spacing', 5)
            self.mainLayout.setContentsMargins(spacing, spacing, spacing, spacing)
            self.mainWidget.setLayout(self.mainLayout)

        self._ctrl_button_layout = QtWidgets.QVBoxLayout()
        self._ctrl_button_layout.setSpacing(0)
        self._ctrl_button_layout.setContentsMargins(0, 0, 0, 0)

        self._ctrl_button = QtWidgets.QToolButton(self)
        self._ctrl_button.setIcon(Icons.more)
        button_size = self.get_style_value('icon_size', 32)
        self._ctrl_button.setMinimumSize(QtCore.QSize(button_size, button_size))
        self._ctrl_button.setMaximumSize(QtCore.QSize(button_size, button_size))
        self._ctrl_button.setIconSize(QtCore.QSize(button_size, button_size))
        self._ctrl_button.setAutoRaise(True)
        self._ctrl_button_layout.addWidget(self._ctrl_button)

        self._ctrl_button_layout.setAlignment(
            self._ctrl_button, QtCore.Qt.AlignTop | QtCore.Qt.AlignRight
        )

        self._ctrl_layout.addLayout(self._ctrl_button_layout, 0, 0, 1, 1)

        self._ctrl_button.clicked.connect(self.menu_requested.emit)
        self._ctrl_button.setVisible(False)

    def enterEvent(self, event):
        self._ctrl_button.setVisible(True)
        return QtWidgets.QGroupBox.enterEvent(self, event)

    def leaveEvent(self, event):
        self._ctrl_button.setVisible(False)
        return QtWidgets.QGroupBox.leaveEvent(self, event)

    def get_style_value(self, value_name, default=None):
        """Retrieve a value from the main style builder."""
        try:
            return self.main.style.get(value_name, default)
        except AttributeError:
            return default
