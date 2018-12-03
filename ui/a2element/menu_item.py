"""
a2element.menu_item - To create module-custom menu entries
in the main menu bar under module.
"""
import os

from PySide2 import QtWidgets, QtCore

import a2ctrl
import a2core
from a2element import EditCtrl
from a2widget import local_script


log = a2core.get_logger(__name__)
MENU_ITEM_PREFIX = 'a2_menu_item_'
MENU_ITEM_TEMPLATE = '''# a2 menu item script "{name}"

def main(a2, mod):
    """
    :param a2: Main A2 object instance.
    :param mod: Current a2 module instance.
    """
    print('calling {name} ...')
'''


class Draw(QtWidgets.QAction):
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
        file_name = build_script_file_name(self.cfg.get('script_name'))
        self.mod.call_python_script(file_name)


class Edit(EditCtrl):
    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg, add_layout=False)

        from a2element import menu_item_edit_ui
        a2ctrl.check_ui_module(menu_item_edit_ui)
        self.ui = menu_item_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)
        a2ctrl.connect.cfg_controls(self.cfg, self.ui)

        self.menu = MenuItemScriptMenu(self, main)
        self.menu.script_selected.connect(self._on_script_selected)

        self.ui.script_selector.set_selection(
            build_script_file_name(cfg.get('script_name')), cfg.get('script_name'))
        self.ui.script_selector.set_main(main)
        self.ui.script_selector.set_menu(self.menu)

    @staticmethod
    def element_name():
        return 'Menu Item'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().combo

    def _on_script_selected(self, name):
        file_name = build_script_file_name(name)
        self.ui.script_selector.set_selection(file_name, name)
        self.cfg['script_name'] = name

        path = os.path.join(self.main.mod.path, file_name)
        if not os.path.isfile(path):
            with open(path, 'w') as file_object:
                file_object.write(MENU_ITEM_TEMPLATE.format(name=name))


def build_script_file_name(name):
    if name is None:
        return None
    else:
        return MENU_ITEM_PREFIX + name + '.py'


class MenuItemScriptMenu(local_script.BrowseScriptsMenu):
    script_selected = QtCore.Signal(str)

    def __init__(self, parent, main):
        super(MenuItemScriptMenu, self).__init__(parent, main)
        self.extension = '.py'
        self.file_prefix = MENU_ITEM_PREFIX
        self.config_typ = 'menu_item'

    def _on_script_selected(self):
        self.script_selected.emit(self.sender().data())

    def _on_create_script(self):
        from a2widget.a2input_dialog import A2InputDialog
        dialog = A2InputDialog(
            self.main, 'New Menu Item Script',
            self._name_check,
            text='awesome_script',
            msg='Give a name for the new menu item script:')

        dialog.exec_()
        if not dialog.output:
            return

        self.script_selected.emit(dialog.output)


def get_settings(*_args):
    return
