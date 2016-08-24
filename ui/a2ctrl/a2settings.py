"""
a2ctrl.a2settings

@created: 29.02.2016
@author: eric
"""
import ahk
import a2mod
import a2core
from os.path import join, exists
from PySide import QtGui, QtCore
from a2ctrl import a2settings_ui
import subprocess
log = a2core.get_logger(__name__)


class A2Settings(QtGui.QWidget):
    def __init__(self, main):
        super(A2Settings, self).__init__()
        self.a2 = a2core.A2Obj.inst()
        self.main = main
        self._setup_ui()
        self._check_win_startup()
        self._draw_module_sources()

    def _draw_module_sources(self):
        enabled_list = [name for name, data in self.a2.enabled.items() if data[0]]
        print('enabled_list: %s' % enabled_list)
        self.ui.no_sources_msg.setVisible(self.a2.module_sources == {})
        for source in sorted(self.a2.module_sources.values(), key=lambda x: x.name):
            modsourcewidget = ModSourceWidget(source, enabled_list)
            modsourcewidget.toggled.connect(self.main.settings_changed)
            self.ui.mod_source_layout.addWidget(modsourcewidget)

    def _setup_ui(self):
        self.ui = a2settings_ui.Ui_a2settings()
        self.ui.setupUi(self)

        a2_hotkey = self.a2.db.get('a2_hotkey') or a2core.a2default_hotkey
        self.ui.a2hotkey.set_key(a2_hotkey)
        self.ui.a2hotkey.ok_func = self.set_a2_hotkey

        self.ui.dev_box.setChecked(self.main.dev_mode)
        self.ui.dev_box.clicked[bool].connect(self.dev_mode_toggle)

        self.ui.remember_selection.setChecked(self.a2.db.get('remember_last') or False)
        self.ui.remember_selection.clicked[bool].connect(self.remember_last_toggle)

        self.ui.dev_widget.setVisible(self.main.dev_mode)

        self.add_source_menu = QtGui.QMenu(self)
        self.ui.add_source_button.setMenu(self.add_source_menu)
        self.add_source_menu.aboutToShow.connect(self.build_add_source_menu)

    def _check_win_startup(self):
        win_startup_path = ahk.call_cmd('get_win_startup_path')
        win_startup_lnk = join(win_startup_path, 'a2.lnk')
        self.ui.load_on_win_start.setChecked(exists(win_startup_lnk))
        self.ui.load_on_win_start.clicked[bool].connect(a2core.set_windows_startup)

    def dev_mode_toggle(self, dev_mode):
        self.a2.db.set('dev_mode', dev_mode)
        self.main.dev_mode = dev_mode
        self.ui.dev_widget.setVisible(dev_mode)
        self.main.toggle_dev_menu(dev_mode)

    def remember_last_toggle(self, state):
        self.a2.db.set('remember_last', state)

    def set_a2_hotkey(self, key):
        self.a2.db.set('a2_hotkey', key)
        self.main.settings_changed('hotkeys')

    def build_add_source_menu(self):
        self.add_source_menu.clear()
        self.add_source_menu.addAction(
            QtGui.QAction('Create Local', self, triggered=self.create_local_source))
        self.add_source_menu.addAction(QtGui.QAction('Add From URL', self))

    def create_local_source(self):
        a2mod.NewModuleSourceTool(self.main)


class ModSourceWidget(QtGui.QWidget):
    toggled = QtCore.Signal()

    def __init__(self, mod_source, enabled_list):
        super(ModSourceWidget, self).__init__()
        self.mod_source = mod_source
        self.mainlayout = QtGui.QHBoxLayout(self)
        m = 1
        self.mainlayout.setContentsMargins(m, m, m, m)
        self.check = QtGui.QCheckBox(mod_source.name)
        self.check.setChecked(mod_source.name in enabled_list)
        self.mainlayout.addWidget(self.check)
        self.check.clicked[bool].connect(mod_source.toggle)
        self.check.clicked.connect(self.toggled.emit)

        self.mod_count = QtGui.QLabel('%i modules, %i enabled'
                                      % (mod_source.mod_count, mod_source.enabled_count,))
        self.mainlayout.addWidget(self.mod_count)

        self.button = QtGui.QPushButton('settings')
        self.mainlayout.setStretch(0, 1)
        self.mainlayout.setStretch(1, 1)
        self.mainlayout.addWidget(self.button)
        self.setLayout(self.mainlayout)

        self.menu = QtGui.QMenu(self)
        self.button.setMenu(self.menu)
        self.menu.aboutToShow.connect(self.build_menu)

    def build_menu(self):
        self.menu.clear()
        self.menu.addAction(QtGui.QAction('Details...', self, triggered=self.show_details))
        self.menu.addAction(QtGui.QAction('Explore to ...', self, triggered=self.explore_source))

    def show_details(self):
        raise NotImplementedError('Module Source Dialog tbd...')

    def explore_source(self):
        subprocess.Popen(['explorer.exe', self.mod_source.path])
