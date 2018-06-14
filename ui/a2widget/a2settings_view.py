"""
a2ctrl.a2settings

@created: 29.02.2016
@author: eric
"""
import os

from PySide import QtGui, QtCore

import a2ahk
import a2core
import a2util
import a2ctrl.connect
from a2widget import a2settings_view_ui, a2module_source


log = a2core.get_logger(__name__)


class A2Settings(QtGui.QWidget):
    dev_setting_changed = QtCore.Signal(str)

    def __init__(self, main):
        super(A2Settings, self).__init__()
        self.a2 = a2core.A2Obj.inst()
        self.main = main
        self._setup_ui()
        self._check_win_startup()
        self._source_widgets = {}
        self._draw_module_sources()
        self.is_expandable_widget = True

    def _draw_module_sources(self):
        enabled_list = [name for name, data in self.a2.enabled.items() if data[0]]
        self.ui.no_sources_msg.setVisible(self.a2.module_sources == {})
        for module_source in sorted(self.a2.module_sources.values(), key=lambda x: x.name):
            widget = a2module_source.ModSourceWidget(
                self.main, module_source,
                show_enabled=module_source.name in enabled_list)
            widget.toggled.connect(self.main.load_runtime_and_ui)
            widget.changed.connect(self.main.load_runtime_and_ui)
            self.ui.mod_source_layout.addWidget(widget)
            self._source_widgets[module_source] = widget

    def _setup_ui(self):
        a2ctrl.check_ui_module(a2settings_view_ui)
        self.ui = a2settings_view_ui.Ui_a2settings()
        self.ui.setupUi(self)

        a2_hotkey = self.a2.db.get('a2_hotkey') or a2core.A2DEFAULT_HOTKEY
        self.ui.a2hotkey.set_key(a2_hotkey)
        self.ui.a2hotkey.hotkey_changed.connect(self.set_a2_hotkey)

        self.ui.dev_box.setChecked(self.a2.dev_mode)
        self.ui.dev_box.clicked[bool].connect(self.dev_mode_toggle)

        self.ui.remember_selection.setChecked(self.a2.db.get('remember_last') or False)
        self.ui.remember_selection.clicked[bool].connect(self.remember_last_toggle)

        self.ui.dev_widget.setVisible(self.a2.dev_mode)

        self.add_source_menu = QtGui.QMenu(self)
        self.ui.a2add_button.clicked.connect(self.build_add_source_menu)
        self.ui.a2add_button.setIcon(a2ctrl.Icons.inst().list_add)

        self.ui.code_editor.file_types = "Executables (*.exe)"
        self.ui.code_editor.writable = False
        self.ui.loglevel_debug.clicked[bool].connect(a2core.set_loglevel)

        self.dev_set_dict = self.main.devset.get()
        a2ctrl.connect.control_list([self.ui.author_name, self.ui.author_url,
                                     self.ui.code_editor, self.ui.json_indent,
                                     self.ui.loglevel_debug],
                                    self.dev_set_dict,
                                    self.dev_setting_changed)
        self.dev_setting_changed.connect(self.on_dev_setting_changed)

        self.ui.settings_folder.setText(self.a2.paths.settings)
        self.ui.module_folder.setText(self.a2.paths.modules)
        self.ui.python_executable.setText(self.a2.paths.python)

        self.ui.autohotkey.writable = False
        self.ui.autohotkey.setText(self.a2.paths.autohotkey)
        self.ui.autohotkey.file_types = "Autohotkey Executable (%s)" % a2ahk.EXECUTABLE_NAME
        self.ui.autohotkey.changed.connect(self.set_autohotkey)

        self.ui.show_console.setChecked(os.path.basename(self.a2.paths.python).lower() == 'python.exe')
        self.ui.show_console.clicked[bool].connect(self.toggle_console)

        ahk_vars = a2ahk.get_variables(self.a2.paths.settings_ahk)
        self.ui.startup_tooltips.setChecked(ahk_vars['a2_startup_tool_tips'])
        self.ui.startup_tooltips.clicked[bool].connect(self.toggle_startup_tooltips)
        self.ui.ui_scale_slider.setValue(self.a2.db.get('ui_scale') or 1.0)
        self.ui.ui_scale_slider.editing_finished.connect(self.main.rebuild_css)

        self.ui.db_print_all_button.clicked.connect(self.get_db_digest)

    def toggle_console(self, state):
        base_name = ['pythonw.exe', 'python.exe'][state]
        new_path = os.path.join(os.path.dirname(self.a2.paths.python), base_name)
        a2ahk.set_variable(self.a2.paths.settings_ahk, 'a2_python', new_path)
        self.a2.paths.python = new_path
        self.ui.python_executable.setText(new_path)

    def toggle_startup_tooltips(self, state):
        a2ahk.set_variable(self.a2.paths.settings_ahk, 'a2_startup_tool_tips', state)

    def set_autohotkey(self, path):
        if os.path.basename(path).lower() != a2ahk.EXECUTABLE_NAME:
            self.ui.autohotkey.changed.disconnect(self.set_autohotkey)
            self.ui.autohotkey.value = self.a2.paths.autohotkey
            self.ui.autohotkey.changed.connect(self.set_autohotkey)
            return

        rel = os.path.relpath(path, self.a2.paths.a2)
        if rel.startswith('..'):
            a2ahk.set_variable(self.a2.paths.settings_ahk, 'a2_ahk', path)
        else:
            a2ahk.set_variable(self.a2.paths.settings_ahk, 'a2_ahk', rel)
        self.a2.paths.autohotkey = path
        self.main.settings_changed()

    def on_dev_setting_changed(self, *args):
        self.main.devset.set(self.dev_set_dict)

    def _check_win_startup(self):
        win_startup_path = a2ahk.call_lib_cmd('get_win_startup_path')
        win_startup_lnk = os.path.join(win_startup_path, 'a2.lnk')
        self.ui.load_on_win_start.setChecked(os.path.exists(win_startup_lnk))
        self.ui.load_on_win_start.clicked[bool].connect(a2util.set_windows_startup)

    def dev_mode_toggle(self, state):
        self.a2.set_dev_mode(state)
        self.ui.dev_widget.setVisible(state)
        self.main.toggle_dev_menu(state)

    def remember_last_toggle(self, state):
        self.a2.db.set('remember_last', state)

    def set_a2_hotkey(self, key):
        self.a2.db.set('a2_hotkey', key)
        self.main.settings_changed('hotkeys')

    def build_add_source_menu(self):
        icons = a2ctrl.Icons.inst()
        menu = self.add_source_menu

        menu.clear()
        menu.addAction(icons.folder_add, 'Create Local', self.main.create_local_source)
        menu.addAction(icons.cloud_download, 'Add From URL', self.add_source_url)

        featured_path = os.path.join(self.a2.paths.defaults, 'featured_packages.json')
        featured_packages = a2util.json_read(featured_path)
        available = set(featured_packages).difference(self.a2.module_sources)
        if available:
            submenu = menu.addMenu('Featured:')
            for pack_name in available:
                action = submenu.addAction(icons.file_download, pack_name, self.on_add_featured)
                action.setData(featured_packages[pack_name])
        menu.popup(QtGui.QCursor.pos())

    def get_db_digest(self):
        self.ui.db_printout.clear()
        self.ui.db_printout.setText(self.a2.db._get_digest())

    def on_add_featured(self):
        self.add_source_url(self.sender().data())

    def add_source_url(self, url=None):
        dialog = a2module_source.AddSourceDialog(self.main, url)
        dialog.okayed.connect(self.main.load_runtime_and_ui)
        dialog.show()
