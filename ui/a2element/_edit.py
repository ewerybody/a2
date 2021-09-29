import os

import a2mod
import a2ctrl
from a2widget import local_script
from a2ctrl.icons import Icons
from a2qt import QtWidgets, QtCore, QtGui


LOCAL_MENU_PREFIX = 'local: '


class EditAddElem(QtWidgets.QWidget):
    """
    Widget to add an element to a module setup. This will probably go into some popup
    later. This way its a little too clunky I think.

        * include > script1.ahk
                    script2.ahk
                    create new script
        * hotkey
        * checkBox
        * ...
    """
    add_request = QtCore.Signal(dict)

    def __init__(self, main, config, name=None):
        super(EditAddElem, self).__init__()
        self.main = main
        self.config = config

        self.base_layout = QtWidgets.QHBoxLayout(self)
        self.base_layout.setSpacing(5)

        name = 'Add Element' if name is None else name
        self.a2add_button = QtWidgets.QPushButton(name)
        self.a2add_button.setObjectName('a2add_button')
        self.a2add_button.clicked.connect(self.build_menu)
        self.a2add_button.setIcon(Icons.list_add)
        self.base_layout.addWidget(self.a2add_button)

        self.menu = QtWidgets.QMenu(self)
        self.menu_include = None
        self.base_layout.setAlignment(self.a2add_button, QtCore.Qt.AlignLeft)
        self.is_expandable_widget = False

    def build_menu(self):
        self.menu.clear()
        self.menu_include = LocalAHKScriptsMenu(self, self.main)
        self.menu_include.script_selected.connect(self._on_add_include)
        self.menu.addMenu(self.menu_include)

        import a2element

        for name, display_name, icon in a2element.get_list():
            action = self.menu.addAction(display_name, self._on_add_element_action)
            action.setData((name, None))
            if icon:
                action.setIcon(icon)

        self.menu.addSeparator()
        self.menu.addAction(self.main.ui.actionCreate_New_Element)
        self._check_for_local_element_mods()
        self.menu.popup(QtGui.QCursor.pos())

    def _on_add_include(self, file_name, _name):
        self._add_element('include', file_name)

    def _on_add_element_action(self):
        typ, name = self.sender().data()
        self._add_element(typ, name)

    def _add_element(self, typ, name=None):
        """
        Just adds a new dict with the according typ value to the temp_config.
        Only if it's an include we already enter the file selected.
        Every other default value will be handled by the very control element.
        """
        cfg = {'typ': typ}
        if typ == 'include':
            cfg['file'] = name
        elif name:
            cfg['name'] = name

        self.add_request.emit(cfg)

    def _check_for_local_element_mods(self):
        if self.main.mod is None:
            return

        for item in os.scandir(self.main.mod.path):
            if not item.is_file():
                continue
            base, ext = os.path.splitext(item.name)
            if not base.startswith(a2ctrl.LOCAL_ELEMENT_ID) or ext.lower() != '.py':
                continue

            element_module = a2ctrl.get_local_element(item.path)
            if element_module is None:
                continue

            edit_class = getattr(element_module, 'Edit')
            display_name = edit_class.element_name()
            icon = edit_class.element_icon()
            name = base[len(a2ctrl.LOCAL_ELEMENT_ID) + 1 :]
            action = self.menu.addAction(
                LOCAL_MENU_PREFIX + display_name, self._on_add_element_action
            )
            action.setData((a2ctrl.LOCAL_ELEMENT_ID, name))
            if icon:
                action.setIcon(icon)


class LocalAHKScriptsMenu(local_script.BrowseScriptsMenu):
    """Selection menu for module-local Autohotkey scripts."""

    # script_selected = QtCore.Signal(tuple)

    def __init__(self, parent, main):
        super(LocalAHKScriptsMenu, self).__init__(parent, main)
        import a2ahk

        self.setTitle('Include Script')
        self.dialog_title = 'New Autohotkey Script'
        self.dialog_msg = 'Give a name for the new Autohotkey script:'
        self.extension = a2ahk.EXTENSION
        self.on_create_name_check = self.main.mod.check_create_script

    def get_available_scripts(self):
        scripts_used = set()
        # TODO: This needs to be done with the Editor widget! Not by the single element!
        temp_config = self.main.module_view._tmp_cfg
        for cfg in a2ctrl.iter_element_cfg_type(temp_config, 'include'):
            scripts_used.add(cfg['file'].lower())

        available = [name for name in self.main.mod.scripts if name.lower() not in scripts_used]
        return available

    def create_script(self, file_name):
        self.main.mod.create_script(file_name, self.main.devset.author_name)
