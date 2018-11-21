import a2ctrl

from a2ctrl import Icons

from PySide2 import QtWidgets, QtCore
import os


CODE_ICON = Icons.inst().code
EDIT_ICON = Icons.inst().edit


class BrowseScriptsMenu(QtWidgets.QMenu):
    def __init__(self, parent, main):
        super(BrowseScriptsMenu, self).__init__(parent)
        self.main = main
        self.setIcon(CODE_ICON)
        self.aboutToShow.connect(self.build_menu)

    def get_available_scripts(self):
        raise NotImplementedError()

    def _on_script_selected(self):
        raise NotImplementedError()

    def _on_create_script(self):
        raise NotImplementedError()

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
