# -*- coding: utf-8 -*-
import a2ctrl

from PySide2 import QtWidgets
from a2element import coords_edit_ui, DrawCtrl, EditCtrl
from a2widget import A2CoordsField


class Draw(DrawCtrl):
    """
    The frontend widget visible to the user with options
    to change the default behavior of the element.
    """
    def __init__(self, *args):
        super(Draw, self).__init__(*args)
        self.value = self.get_user_value((list, tuple), default=(0, 0))
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        self.label = QtWidgets.QLabel(self.cfg.get('label', ''), self)
        self.main_layout.addWidget(self.label)

        self.value_ctrl = A2CoordsField(self)
        self.value_ctrl.value = self.value
        self.main_layout.addWidget(self.value_ctrl)
        self.value_ctrl.changed.connect(self.delayed_check)

    def check(self, *args):
        value = args[0]

        # prevent being called double
        if self.value == value:
            return

        self.value = value
        self.set_user_value(value)
        self.change('variables')


class Edit(EditCtrl):
    """
    The background widget that sets up how the user can edit the element,
    visible when editing the module.
    """
    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg, add_layout=False)
        a2ctrl.check_ui_module(coords_edit_ui)

        self.ui = coords_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)
        self.check_new_name()
        a2ctrl.connect.cfg_controls(self.cfg, self.ui)

    @staticmethod
    def element_name():
        """The elements display name shown in UI"""
        return 'Coords Field'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().number


def get_settings(_module_key, cfg, db_dict, user_cfg):
    value = a2ctrl.get_cfg_value(cfg, user_cfg, typ=list, default=[0, 0])
    db_dict.setdefault('variables', {})[cfg['name']] = value
