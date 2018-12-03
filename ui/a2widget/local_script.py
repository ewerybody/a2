import os

import a2ctrl
import a2util

from PySide2 import QtWidgets


CODE_ICON = a2ctrl.Icons.inst().code
EDIT_ICON = a2ctrl.Icons.inst().edit


class BrowseScriptsMenu(QtWidgets.QMenu):
    def __init__(self, parent, main):
        super(BrowseScriptsMenu, self).__init__(parent)
        self.main = main
        self.setIcon(CODE_ICON)
        self.aboutToShow.connect(self.build_menu)

        self.extension = '.py'
        self.file_prefix = ''
        self.config_typ = ''

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

    def _on_script_selected(self):
        raise NotImplementedError()

    def _on_create_script(self):
        raise NotImplementedError()

    def _name_check(self, name):
        name = os.path.splitext(name)[0]
        black_list = self._list_scripts()
        return a2util.standard_name_check(name, black_list)

    def build_menu(self):
        self.clear()
        available = self.get_available_scripts()

        for script_name in available:
            action = self.addAction(CODE_ICON, script_name, self._on_script_selected)
            action.setData(script_name)
        if available:
            self.addSeparator()

        self.addAction(CODE_ICON, 'Create New', self._on_create_script)


class ScriptSelector(QtWidgets.QWidget):
    def __init__(self, parent, main=None):
        super(ScriptSelector, self).__init__(parent)
        self._setup_ui()
        self._script_file = ''
        self.main = main

    def set_main(self, main):
        self.main = main

    def _setup_ui(self):
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.button = QtWidgets.QPushButton(self, 'None')
        self.button_menu = None
        layout.addWidget(self.button)

        self.edit_button = QtWidgets.QPushButton('edit script')
        self.edit_button.clicked.connect(self.edit_script)
        self.edit_button.setIcon(EDIT_ICON)
        layout.addWidget(self.edit_button)
        layout.setStretch(0, 1)

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


if __name__ == '__main__':
    pass
