import os

import a2ctrl
import a2util

from PySide2 import QtWidgets, QtCore


class BrowseScriptsMenu(QtWidgets.QMenu):
    script_selected = QtCore.Signal(str, str)

    def __init__(self, parent, main):
        super(BrowseScriptsMenu, self).__init__(parent)
        self.main = main
        self.setIcon(a2ctrl.Icons.inst().code)
        self.aboutToShow.connect(self.build_menu)

        self.extension = '.py'
        self.file_prefix = ''
        self.script_template = ''
        self.config_typ = ''
        self._script_default_name = 'awesome_script'
        self.dialog_title = 'dialog_title'
        self.dialog_msg = 'dialog_msg'

    def get_available_scripts(self):
        scripts_in_use = set()
        for cfg in a2ctrl.iter_element_cfg_type(self.main.temp_config, self.config_typ):
            this_name = cfg.get('script_name')
            if this_name:
                scripts_in_use.add(this_name)

        return self._list_scripts() - scripts_in_use

    def _list_scripts(self):
        menu_script_files = set()
        for item in os.scandir(self.main.mod.path):
            if item.is_file():
                base, ext = os.path.splitext(item.name)
                if base.startswith(self.file_prefix) and ext.lower() == self.extension:
                    menu_script_files.add(base[len(self.file_prefix):])
        return menu_script_files

    def _on_script_selected_action(self):
        script_name = self.sender().data()
        self.set_script(script_name)

    def _on_create_script(self):
        from a2widget.a2input_dialog import A2InputDialog
        dialog = A2InputDialog(
            self.main, self.dialog_title,
            self._name_check,
            text=self._script_default_name,
            msg=self.dialog_msg)

        dialog.exec_()
        if not dialog.output:
            return

        self.set_script(dialog.output)

    def set_script(self, name):
        file_name = build_file_name(name, self.file_prefix)
        self.script_selected.emit(file_name, name)

        path = os.path.join(self.main.mod.path, file_name)
        if not os.path.isfile(path):
            with open(path, 'w') as file_object:
                file_object.write(self.script_template.format(name=name))

    def _name_check(self, name):
        name = os.path.splitext(name)[0]
        black_list = self._list_scripts()
        return a2util.standard_name_check(name, black_list)

    def build_menu(self):
        self.clear()
        available = self.get_available_scripts()

        for script_name in available:
            action = self.addAction(a2ctrl.Icons.inst().code, script_name,
                                    self._on_script_selected_action)
            action.setData(script_name)
        if available:
            self.addSeparator()

        self.addAction(a2ctrl.Icons.inst().code, 'Create New', self._on_create_script)


class ScriptSelector(QtWidgets.QWidget):
    def __init__(self, parent, main=None):
        super(ScriptSelector, self).__init__(parent)
        self._setup_ui()
        self._script_file = ''
        self.main = main

    def _setup_ui(self):
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.button = QtWidgets.QPushButton(self, 'None')
        self.button_menu = None
        layout.addWidget(self.button)

        self.edit_button = QtWidgets.QPushButton('edit script')
        self.edit_button.clicked.connect(self.edit_script)
        self.edit_button.setIcon(a2ctrl.Icons.inst().edit)
        layout.addWidget(self.edit_button)
        layout.setStretch(0, 1)

    def set_config(self, prefix, cfg, main, menu):
        self.prefix = prefix
        name = cfg.get('script_name')
        self.set_selection(build_file_name(name, prefix), name)

        self.main = main
        self.set_menu(menu)

    def set_menu(self, menu_object):
        self.button_menu = menu_object
        self.button.setMenu(self.button_menu)

    def set_name(self, name):
        self.button.setText(name)

    def set_selection(self, file_name, display_name=None):
        if display_name is None:
            display_name = file_name

        self.set_name(display_name)
        self._script_file = file_name

    def edit_script(self):
        script_path = os.path.join(self.main.mod.path, self._script_file)
        self.main.edit_code(script_path)


def build_file_name(name, prefix):
    if name is None:
        return None
    else:
        return prefix + name + '.py'
