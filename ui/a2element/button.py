# -*- coding: utf-8 -*-
"""
Some element description ...

@created: 2016 11 14
@author: Eric Werner
"""
import a2ahk
import a2ctrl
from PySide2 import QtGui, QtWidgets
from a2element import DrawCtrl, EditCtrl, button_edit_ui
from a2core import get_logger
import traceback
import os


log = get_logger(__name__)


class Draw(DrawCtrl):
    """
    The frontend widget visible to the user with options
    to change the default behavior of the element.
    """
    def __init__(self, main, cfg, mod):
        super(Draw, self).__init__(main, cfg, mod)

        self.button_layout = QtWidgets.QHBoxLayout(self)
        labeltext = self.cfg.get('labeltext', '')
        if labeltext:
            label = QtWidgets.QLabel(labeltext)
            self.button_layout.addWidget(label)

        self.button = QtWidgets.QPushButton(self.cfg.get('buttontext', ''))
        self.button.clicked.connect(self.call_code)
        self.button_layout.addWidget(self.button)
        # self.setLayout(self.main_layout)

    def call_code(self):
        code = self.cfg.get('code', '')
        if not code:
            raise RuntimeError('Button has no code to execute!')
        else:
            try:
                # amend the globals dict with some useful info
                globals_dict = globals()
                globals_dict.update({'a2path': self.mod.path,
                                     'call_local_ahk': self.call_local_ahk,
                                     'call_lib_cmd': a2ahk.call_lib_cmd})
                exec(code, globals_dict)
            except Exception:
                log.error(traceback.format_exc().strip())
                log.error('Failed to call button code in "%s":\n  %s'
                          % (self.mod.name, code))

    def call_local_ahk(self, script_name, *args):
        script_name = a2ahk.ensure_ahk_ext(script_name)
        script_path = os.path.join(self.mod.path, script_name)
        return a2ahk.call_cmd(script_path, cwd=self.mod.path, *args)


class Edit(EditCtrl):
    """
    The background widget that sets up how the user can edit the element,
    visible when editing the module.
    """
    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg, add_layout=False)
        self.helpUrl = 'https://github.com/ewerybody/a2/wiki/Button-element'
        a2ctrl.check_ui_module(button_edit_ui)
        self.ui = button_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)
        a2ctrl.connect.cfg_controls(self.cfg, self.ui)

    @staticmethod
    def element_name():
        """The elements display name shown in UI"""
        return 'Button'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().button


def get_settings(module_key, cfg, db_dict, user_cfg):
    pass
