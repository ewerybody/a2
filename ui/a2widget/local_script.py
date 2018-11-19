from pyside2uic.properties import QtWidgets, QtCore

import a2ctrl
from a2ctrl import Icons

CODE_ICON = Icons.inst().code
EDIT_ICON = Icons.inst().edit


class ScriptSelector(QtWidgets.QWidget):
    file_selected = QtCore.Signal(str)

    def __init__(self, parent):
        super(ScriptSelector, self).__init__(parent)
        self._setup_ui()

        self._script_file = ''

    def _setup_ui(self):
        layout = QtWidgets.QHBoxLayout(self)
        self.button = QtWidgets.QPushButton(self)
        self.button_menu = None
        layout.addWidget(self.button)

        self.edit_button = QtWidgets.QPushButton('edit script')
        self.edit_button.clicked.connect(self.edit_script)
        self.edit_button.setIcon(EDIT_ICON)
        layout.addWidget(self.edit_button)

        layout.setStretch(0, 1)
        # self.base_layout.addItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        # self.mainWidget.setLayout(self.base_layout)

    def set_menu(self, menu_object):
        self.button_menu = menu_object
        self.button_menu.file_selected.connect(self.set_script)
        self.button.setMenu(self.button_menu)


class BrowseScriptsMenu(QtWidgets.QMenu):
    script_selected = QtCore.Signal(str)

    def __init__(self, main):
        super(BrowseScriptsMenu, self).__init__()
        self.main = main
        self.setIcon(CODE_ICON)
        self.aboutToShow.connect(self.build_menu)

    def get_available_scripts(self):
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

    def _on_script_selected(self):
        self.script_selected.emit(self.sender().data())

    def _on_create_script(self):
        from a2widget.a2input_dialog import A2InputDialog
        dialog = A2InputDialog(
            self.main, 'New Script',
            self.main.mod.check_create_script,
            text='awesomeScript',
            msg='Give a name for the new script file:')
        # dialog.okayed.connect(partial(self.set_script, create=True))
        dialog.exec_()
        if not dialog.output:
            return

        name = self.main.mod.create_script(dialog.output, self.main.devset.author_name)
        self.script_selected.emit(name)


class LocalAHKScriptsMenu(BrowseScriptsMenu):
    include_selected = QtCore.signal(tuple)

    def __init__(self, parent, main):
        super(LocalAHKScriptsMenu, self).__init__(parent)
        self.setTitle('Include Script')
        self.main = main
        self.script_selected.connect(self._on_include_selected)

    def get_available_scripts(self):
        scripts_in_use = set()
        for cfg in self.main.temp_config:
            if cfg['typ'] == 'include':
                scripts_in_use.add(cfg['file'])

        return set(self.main.mod.scripts) - scripts_in_use

    def _on_include_selected(self, name):
        self.include_selected.emit(('include', name))


class LocalPyScriptMenu(BrowseScriptsMenu):
    def __init__(self, parent):
        super(LocalPyScriptMenu, self).__init__(parent)
        self.setTitle('Python Script')


if __name__ == '__main__':
    pass
