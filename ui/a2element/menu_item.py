"""
a2element.menu_item - To create module-custom menu entries
in the main menu bar under module.
"""
from PySide2 import QtWidgets

import a2ctrl
import a2core
from a2element import EditCtrl
import a2ahk
import os
import traceback


log = a2core.get_logger(__name__)


class Draw(QtWidgets.QAction):
    def __init__(self, main, cfg, mod, *_args):
        super(Draw, self).__init__(main)
        self.main = main
        self.cfg = cfg
        self.mod = mod

        label = cfg.get('label')
        if not label:
            label = 'Menu Item has no label yet!'
            log.error('Menu Item has no label yet!')
        self.setText(label)
        self.triggered.connect(self.call_code)

    def call_code(self):
        code = self.cfg.get('code', '')
        if not code:
            raise RuntimeError('Menu Item has no code to execute!')
        else:
            try:
                # amend the globals dict with some useful info
                globals_dict = globals()
                globals_dict.update(
                    {'module': self.mod,
                     'call_reload': self.main.load_runtime_and_ui,
                     'call_local_ahk': self.call_local_ahk,
                     'call_lib_cmd': a2ahk.call_lib_cmd})
                exec(code, globals_dict)
            except Exception:
                log.error(traceback.format_exc().strip())
                log.error('Failed to call Menu Item code in "%s":\n  %s'
                          % (self.mod.name, code))

    def call_local_ahk(self, script_name, *args):
        script_name = a2ahk.ensure_ahk_ext(script_name)
        script_path = os.path.join(self.mod.path, script_name)
        return a2ahk.call_cmd(script_path, cwd=self.mod.path, *args)


class Edit(EditCtrl):
    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg, add_layout=False)
        # self.helpUrl = 'https://github.com/ewerybody/a2/wiki/Button-element'

        from a2element import menu_item_edit_ui
        a2ctrl.check_ui_module(menu_item_edit_ui)
        self.ui = menu_item_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)
        a2ctrl.connect.cfg_controls(self.cfg, self.ui)

    @staticmethod
    def element_name():
        return 'Menu Item'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().combo


def get_settings(*_args):
    return
