"""
a2ctrl.a2settings

@created: 29.02.2016
@author: eric
"""
import os

from PySide2 import QtGui, QtCore, QtWidgets

import a2ahk
import a2core
import a2util
import a2ctrl.connect
import a2widget.a2hotkey.keyboard_dialog.layouts
from a2widget import a2settings_view_ui, a2module_source, a2hotkey

log = a2core.get_logger(__name__)
_PROXY_ITEMS = 'user', 'pass', 'server', 'port'
LICENSES_TAB_NAME = 'licenses'


class A2Settings(QtWidgets.QWidget):
    dev_setting_changed = QtCore.Signal(str)

    def __init__(self, main):
        super(A2Settings, self).__init__(parent=main)
        self.a2 = a2core.A2Obj.inst()
        self.main = main
        self._setup_ui()
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

        a2ui_hotkey = self.a2.db.get('a2_hotkey') or a2core.A2DEFAULT_HOTKEY
        self.ui.a2hotkey.set_config({'key': a2ui_hotkey})
        self.ui.a2hotkey.hotkey_changed.connect(self.set_a2_hotkey)

        self.ui.dev_box.setChecked(self.a2.dev_mode)
        self.ui.dev_box.clicked[bool].connect(self.dev_mode_toggle)

        self.ui.remember_selection.setChecked(self.a2.db.get('remember_last') or False)
        self.ui.remember_selection.clicked[bool].connect(self.remember_last_toggle)

        self.ui.dev_widget.setVisible(self.a2.dev_mode)

        self.add_source_menu = QtWidgets.QMenu(self)
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

        self.ui.data_folder.setText(self.a2.paths.data)
        self.ui.python_executable.setText(self.a2.paths.python)
        self.ui.autohotkey.setText(self.a2.paths.autohotkey)

        self.ui.show_console.setChecked(os.path.basename(self.a2.paths.python).lower() == 'python.exe')
        self.ui.show_console.clicked[bool].connect(self.toggle_console)

        # TODO: #182
        # ahk_vars = a2ahk.get_variables(self.a2.paths.settings_ahk)
        # self.ui.startup_tooltips.setChecked(ahk_vars['a2_startup_tool_tips'])
        self.ui.startup_tooltips.clicked[bool].connect(self.toggle_startup_tooltips)
        self.ui.ui_scale_slider.setValue(self.a2.db.get('ui_scale') or 1.0)
        self.ui.ui_scale_slider.setPageStep(0.1)
        self.ui.ui_scale_slider.editing_finished.connect(self.main.rebuild_css)

        self.ui.db_print_all_button.clicked.connect(self.get_db_digest)

        self._setup_hotkey_dialog()

        self.ui.a2settings_tab.setCurrentIndex(0)
        self.ui.a2settings_tab.currentChanged.connect(self.on_tab_changed)

        self.ui.load_on_win_start.clicked[bool].connect(self._set_windows_startup)
        self._check_win_startup()
        self.ui.add_desktop_shortcut.clicked[bool].connect(self._set_desktop_link)
        self._check_desktop_link()

        # filling proxy ui
        self.ui.proxy_box.setChecked(self.a2.db.get('proxy_enabled') or False)
        settings = self.a2.db.get('proxy_settings') or {}
        self.ui.proxy_http.setCurrentIndex(
            ('http', 'https').index(settings.get('http') or 'http'))
        proxy_line_widgets = (self.ui.proxy_user, self.ui.proxy_pass,
                              self.ui.proxy_server, self.ui.proxy_port)
        for i, name in enumerate(_PROXY_ITEMS):
            value = settings.get(name) or ''
            proxy_line_widgets[i].setText(value)

        self.ui.proxy_box.clicked.connect(self._check_proxy_settings)
        self.ui.proxy_http.currentIndexChanged.connect(self._check_proxy_settings)
        for widget in proxy_line_widgets:
            widget.textChanged.connect(self._check_proxy_settings)

    def _check_win_startup(self):
        startup_path = a2ahk.call_lib_cmd('get_win_startup_path')
        if not startup_path:
            self.ui.load_on_win_start.setChecked(False)
        else:
            startup_path = os.path.normpath(startup_path)
            is_current_path = startup_path == self.a2.paths.a2exe
            if not is_current_path:
                log.warn('Different Windows Startup path set!\n  %s' % startup_path)
            self.ui.load_on_win_start.setChecked(is_current_path)

    def _set_windows_startup(self, state):
        a2ahk.call_lib_cmd('set_windows_startup', self.a2.paths.a2, int(state))

    def _check_desktop_link(self):
        desktop_path = a2ahk.call_lib_cmd('get_desktop_link_path')
        if not desktop_path:
            self.ui.add_desktop_shortcut.setChecked(False)
        else:
            desktop_path = os.path.normpath(desktop_path)
            is_current_path = desktop_path == self.a2.paths.a2uiexe
            self.ui.add_desktop_shortcut.setChecked(is_current_path)

    def _set_desktop_link(self, state):
        a2ahk.call_lib_cmd('set_desktop_link', self.a2.paths.a2, int(state))

    def _setup_hotkey_dialog(self):
        current_style = a2hotkey.get_current_style()
        index = 0
        for i, (style, label) in enumerate(a2hotkey.iter_dialog_styles()):
            self.ui.hk_dialog_style.addItem(label)
            if style == current_style:
                index = i
        self.ui.hk_dialog_style.setCurrentIndex(index)
        self.ui.hk_dialog_style.currentTextChanged.connect(a2hotkey.set_dialog_style)

        layouts = a2widget.a2hotkey.keyboard_dialog.layouts
        current_layout = layouts.get_current()
        index = 0
        for i, (keyboard_id, label) in enumerate(layouts.iterate()):
            self.ui.hk_dialog_layout.addItem(label)
            if keyboard_id == current_layout:
                index = i
        self.ui.hk_dialog_layout.setCurrentIndex(index)
        self.ui.hk_dialog_layout.currentTextChanged.connect(layouts.set_layout)

    def toggle_console(self, state):
        base_name = ['pythonw.exe', 'python.exe'][state]
        new_path = os.path.join(os.path.dirname(self.a2.paths.python), base_name)
        a2ahk.set_variable(self.a2.paths.settings_ahk, 'a2_python', new_path)
        self.a2.paths.python = new_path
        self.ui.python_executable.setText(new_path)

    def toggle_startup_tooltips(self, state):
        a2ahk.set_variable(self.a2.paths.settings_ahk, 'a2_startup_tool_tips', state)

    def on_dev_setting_changed(self, *args):
        self.main.devset.set(self.dev_set_dict)

    def dev_mode_toggle(self, state):
        self.a2.set_dev_mode(state)
        self.ui.dev_widget.setVisible(state)
        self.main.check_main_menu_bar()

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

    def on_tab_changed(self, tab_index):
        widget = self.ui.a2settings_tab.widget(tab_index)
        # to build the licenses tab on demand only
        if widget.objectName() == LICENSES_TAB_NAME:
            if widget.children():
                return
            from a2widget import a2licenses_widget_ui
            a2ctrl.check_ui_module(a2licenses_widget_ui)
            ui = a2licenses_widget_ui.Ui_Form()
            ui.setupUi(self.ui.a2settings_tab)
            widget.setLayout(ui.license_layout)

    def _check_proxy_settings(self):
        self.a2.db.set('proxy_enabled', self.ui.proxy_box.isChecked())
        settings = {'http': ('http', 'https')[self.ui.proxy_http.currentIndex()]}
        for item in _PROXY_ITEMS:
            widget = getattr(self.ui, 'proxy_' + item)
            text = widget.text()
            if text:
                settings[item] = text
        self.a2.db.set('proxy_settings', settings)
        a2core.setup_proxy(self.a2)
