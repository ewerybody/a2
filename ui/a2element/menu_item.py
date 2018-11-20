"""
a2element.menu_item - To create module-custom menu entries
in the main menu bar under module.
"""
import os
import traceback

from PySide2 import QtWidgets, QtCore

import a2ahk
import a2ctrl
import a2core
from a2element import EditCtrl
from a2widget import local_script
import a2util
from importlib import import_module
import sys


log = a2core.get_logger(__name__)
MENU_ITEM_PREFIX = 'a2_menu_item_'
MENU_ITEM_TEMPLATE = '''# a2 menu item script "{name}"

def main(main, mod):
    """
    :param main: Main window instance.
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
        file_name = build_Script_file_name(self.cfg.get('name'))
        if not file_name:
            return

        path = os.path.join(self.mod.path, file_name)
        if os.path.isfile(path):
            if self.mod.path not in sys.path:
                sys.path.append(self.mod.path)

            base, _ = os.path.splitext(file_name)
            try:
                menu_item_module = import_module(base)
            except ImportError:
                log.error(traceback.format_exc().strip())
                log.error('Could not import local menu item module! "%s"' %
                          self.cfg.get('name'))

            try:
                menu_item_module.main(self.main, self.mod)
            except Exception:
                tb = traceback.format_exc().strip()

                if base in sys.modules:
                    log.info('unloading module "%s" ...' % base)
                    del sys.modules[base]

                log.error('\n  Error executing menu item script "%s"\n'
                          '%s\n  path: %s' % (self.cfg.get('name'), tb, path))

            sys.path.remove(self.mod.path)

    def _call_sfdsdf(self, code):
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

    def _call_local_ahk(self, script_name, *args):
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

        self.menu = MenuItemScriptMenu(self, main)
        self.menu.script_selected.connect(self._on_script_selected)

        self.ui.script_selector.set_selection(
            build_Script_file_name(cfg.get('name')), cfg.get('name'))
        self.ui.script_selector.set_main(main)
        self.ui.script_selector.set_menu(self.menu)

    @staticmethod
    def element_name():
        return 'Menu Item'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().combo

    def _on_script_selected(self, name):
        file_name = build_Script_file_name(name)
        self.ui.script_selector.set_selection(file_name, name)
        self.cfg['name'] = name

        path = os.path.join(self.main.mod.path, file_name)
        if not os.path.isfile(path):
            with open(path, 'w') as file_object:
                file_object.write(MENU_ITEM_TEMPLATE.format(name=name))


def build_Script_file_name(name):
    if name is None:
        return None
    else:
        return MENU_ITEM_PREFIX + name + '.py'


class MenuItemScriptMenu(local_script.BrowseScriptsMenu):
    script_selected = QtCore.Signal(str)

    def __init__(self, parent, main):
        super(MenuItemScriptMenu, self).__init__(parent, main)

    def get_available_scripts(self):
        scripts_in_use = set()
        for cfg in self.main.temp_config:
            if cfg['typ'] == 'menu_item':
                this_name = cfg.get('name')
                if this_name:
                    scripts_in_use.add(this_name)

        return self._list_menu_item_scripts() - scripts_in_use

    def _list_menu_item_scripts(self):
        menu_script_files = set()
        for item in os.scandir(self.main.mod.path):
            if item.is_file():
                base, ext = os.path.splitext(item.name)
                if base.startswith(MENU_ITEM_PREFIX) and ext.lower() == '.py':
                    menu_script_files.add(base[len(MENU_ITEM_PREFIX):])
        return menu_script_files

    def _on_script_selected(self):
        self.script_selected.emit(self.sender().data())

    def _name_check(self, name):
        name = os.path.splitext(name)[0]
        black_list = self._list_menu_item_scripts()
        return a2util.standard_name_check(name, black_list)

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
