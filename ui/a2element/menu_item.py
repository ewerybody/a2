"""
a2element.menu_item - To create module-custom menu entries
in the main menu bar under module.
"""
import traceback
from a2qt import QtGui

import a2uic
import a2ctrl
import a2core
from a2element import EditCtrl
from a2widget import local_script, a2error_dialog


log = a2core.get_logger(__name__)
MENU_ITEM_PREFIX = 'a2_menu_item_'
MENU_ITEM_TEMPLATE = '''# a2 menu item script "{name}"

def main(a2, mod):
    """
    :param a2: Main A2 object instance.
    :param mod: Current a2 module instance.
    """
    print('calling menu script "{name}" main() ...')
'''


class Draw(QtGui.QAction):
    def __init__(self, main, cfg, mod, *_args):
        super(Draw, self).__init__(main)
        self.main = main
        self.cfg = cfg
        self.mod = mod

        label = cfg.get('label')
        if not label:
            label = 'Menu Item has no label yet!'
            log.error(label)
        self.setText(label)
        self.triggered.connect(self.call_code)

    def call_code(self):
        script_name = self.cfg.get('script_name')
        file_name = local_script.build_file_name(script_name, MENU_ITEM_PREFIX)
        try:
            self.mod.call_python_script(file_name)
        except Exception as error:
            a2error_dialog.A2ErrorDialog(
                traceback.format_exc().strip(),
                f'There was an error trying to execute the script "{script_name}":',
                error,
                self
            )


class Edit(EditCtrl):
    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg, add_layout=False)

        from a2element import menu_item_edit_ui

        a2uic.check_module(menu_item_edit_ui)
        self.ui = menu_item_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)
        a2ctrl.connect.cfg_controls(self.cfg, self.ui)

        self.menu = local_script.BrowseScriptsMenu(self, main)
        self.menu.file_prefix = MENU_ITEM_PREFIX
        self.menu.script_template = MENU_ITEM_TEMPLATE
        self.menu.config_typ = 'menu_item'
        self.menu.dialog_title = 'New Menu Item Script'
        self.menu.dialog_msg = 'Give a name for the new menu item script:'
        self.menu.script_selected.connect(self._on_script_selected)
        self.ui.script_selector.set_config(MENU_ITEM_PREFIX, cfg, main, self.menu)

    @staticmethod
    def element_name():
        return 'Menu Item'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().combo

    def _on_script_selected(self, file_name, name):
        self.cfg['script_name'] = name
        self.ui.script_selector.set_selection(file_name, name)


def get_settings(*_args):
    return
