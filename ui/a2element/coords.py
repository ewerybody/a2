# -*- coding: utf-8 -*-
"""
Some element description ...

@created: 2017 3 13
@author: Eric Werner
"""
import a2ctrl
from PySide2 import QtWidgets
from a2element import coords_edit_ui, DrawCtrl, EditCtrl
from a2widget import A2CoordsField


class Draw(DrawCtrl):
    """
    The frontend widget visible to the user with options
    to change the default behavior of the element.
    """
    def __init__(self, main, cfg, mod):
        super(Draw, self).__init__(main, cfg, mod)
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


def get_settings(module_key, cfg, db_dict, user_cfg):
    """
    Called by the module on "change" to get an elements data thats
    eventually written into the runtime includes.

    Passed into is all you might need:
    :param str module_key: "module_source_name|module_name" combo used to identify module in db
    :param dict cfg: Standard element configuration dictionary.
    :param dict db_dict: Dictionary that's used to write the include data with "hotkeys", "variables" and "includes" keys
    :param dict user_cfg: This elements user edits saved in the db

    To make changes to the:
    * "variables" - a simple key, value dictionary in db_dict

    Get the current value via get_cfg_value() given the default cfg and user_cfg.
    If value name is found it takes the value from there, otherwise from cfg or given default.

        value = a2ctrl.get_cfg_value(cfg, user_cfg, typ=bool, default=False)

    write the key and value to the "variables" dict:

        db_dict['variables'][cfg['name']] = value

    * "hotkeys" - a dictionary with scope identifiers

    * "includes" - a simple list with ahk script paths
    """
    value = a2ctrl.get_cfg_value(cfg, user_cfg, typ=list, default=[0, 0])
    db_dict.setdefault('variables', {})[cfg['name']] = value
