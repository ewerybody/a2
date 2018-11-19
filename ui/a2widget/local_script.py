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
        self.button_menu = BrowseScriptsMenu(self)
        self.button_menu.script_selected.connect(self.set_script)
        self.button.setMenu(self.button_menu)
        layout.addWidget(self.button)

        self.edit_button = QtWidgets.QPushButton('edit script')
        self.edit_button.clicked.connect(self.edit_script)
        self.edit_button.setIcon(EDIT_ICON)
        layout.addWidget(self.edit_button)

        layout.setStretch(0, 1)
        # self.base_layout.addItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        # self.mainWidget.setLayout(self.base_layout)

    def


class LocalAHKScriptsMenu(BrowseScriptsMenu):
    def __init__(self, parent):
        super(LocalAHKScriptsMenu, self).__init__(parent)
        self.setTitle('Include Script')


class LocalPyScriptMenu(BrowseScriptsMenu):
    def __init__(self, parent):
        super(LocalPyScriptMenu, self).__init__(parent)
        self.setTitle('Use Script')


class BrowseScriptsMenu(QtWidgets.QMenu):
    script_selected = QtCore.Signal(tuple)

    def __init__(self, main):
        super(BrowseScriptsMenu, self).__init__()
        self.main = main
        self.setIcon(CODE_ICON)
        self.aboutToShow.connect(self.build_menu)

    def build_menu(self):
        self.clear()
        scripts_in_use = set()
        for cfg in self.main.temp_config:
            if cfg['typ'] == 'include':
                scripts_in_use.add(cfg['file'])

        scripts_unused = set(self.main.mod.scripts) - scripts_in_use

        for script_name in scripts_unused:
            action = self.addAction(CODE_ICON, script_name, self._on_action_click)
            action.setData(script_name)

        if scripts_unused:
            self.addSeparator()

        self.addAction(CODE_ICON, 'Create New Script', self.set_script)

    def _on_action_click(self):
        self.script_selected.emit(('include', self.sender().data()))

    def set_script(self):
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
        self.script_selected.emit(('include', name))


if __name__ == '__main__':
    pass
