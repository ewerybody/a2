"""
a2ui - setup interface for an Autohotkey environment.
"""
import os
import subprocess
from copy import deepcopy
from functools import partial

import a2core
import a2ctrl
import a2util
import a2runtime
from a2widget import a2design_ui

from PySide import QtGui, QtCore


BASE_DPI = 96.0
log = a2core.get_logger(__name__)
ui_defaults = None
RESTART_DELAY = 300
RUNTIME_WATCH_INTERVAL = 1000


class A2Window(QtGui.QMainWindow):
    # to be triggered whenever a module or module source is dis/enabled
    module_enabled = QtCore.Signal()

    def __init__(self, app=None, *args):
        super(A2Window, self).__init__(parent=None)
        self.a2 = a2core.A2Obj.inst()
        self.app = app
        self._restart_thread = None
        self._shutdown_thread = None

        self.edit_clipboard = []
        self.tempConfig = None
        self.selected = []
        self.mod = None
        self.scopes = {}
        self.css_values = {}
        self.rebuild_css()

        self.dev_mode = self.a2.db.get('dev_mode') or False
        self.devset = DevSettings(self.a2)
        if self.devset.loglevel_debug:
            a2core.set_loglevel(debug=True)
            log.debug('Loglevel set to DEBUG!')

        self._setup_ui()

        self.num_selected = 0
        init_selection = []
        if self.a2.db.get('remember_last') or False:
            init_selection = self.a2.db.get('last_selected') or []
        init_settings_view = init_selection == []
        self.module_list.selection_changed.connect(self._module_selected)
        self.module_list.draw_modules(init_selection)
        if init_settings_view:
            self.module_view.draw_mod()

        self.runtime_watcher = RuntimeWatcher(self)
        self.runtime_watcher.message.connect(self.runtime_watcher_message)
        self.runtime_watcher.start()

        log.info('initialised!')

    def runtime_watcher_message(self, message):
        if not message:
            self.setWindowTitle('a2')
        else:
            self.setWindowTitle('a2 - %s' % message)

    def _module_selected(self, module_list):
        self.selected = module_list
        self.num_selected = len(module_list)
        if self.num_selected == 1:
            self.mod = module_list[0]
        else:
            self.mod = None
        self.module_view.draw_mod()

    def _setup_ui(self):
        if self.dev_mode:
            a2ctrl.check_ui_module(a2design_ui)

        self.ui = a2design_ui.Ui_a2MainWindow()
        self.ui.setupUi(self)
        # shortcuts
        self.module_list = self.ui.module_list
        self.module_view = self.ui.module_view

        self.module_view.setup_ui(self)

        self._setup_actions()
        self._setup_shortcuts()

        self.toggle_dev_menu()
        self.setWindowIcon(a2ctrl.Icons.inst().a2)
        self.restoreA2ui()

    def _setup_actions(self):
        self.ui.actionEdit_module.triggered.connect(self.edit_mod)
        self.ui.actionEdit_module.setShortcut('Ctrl+E')
        self.ui.actionDisable_all_modules.triggered.connect(self.mod_disable_all)
        self.ui.actionExplore_to.triggered.connect(self.explore_mod)
        self.ui.actionExplore_to.setIcon(a2ctrl.Icons.inst().folder)
        self.ui.actionAbout_a2.triggered.connect(partial(a2util.surf_to, self.a2.urls.help))
        self.ui.actionAbout_Autohotkey.triggered.connect(partial(a2util.surf_to, self.a2.urls.ahk))
        self.ui.actionAbout_a2.setIcon(a2ctrl.Icons.inst().a2help)
        self.ui.actionAbout_Autohotkey.setIcon(a2ctrl.Icons.inst().autohotkey)

        self.ui.actionExplore_to_a2_dir.triggered.connect(self.explore_a2)
        self.ui.actionExplore_to_a2_dir.setIcon(a2ctrl.Icons.inst().folder)
        self.ui.actionA2_settings.triggered.connect(partial(self.module_list.select, None))
        self.ui.actionA2_settings.setIcon(a2ctrl.Icons.inst().a2)
        self.ui.actionExit_a2ui.triggered.connect(self.close)
        self.ui.actionExit_a2ui.setIcon(a2ctrl.Icons.inst().clear)
        self.ui.actionRefresh_UI.triggered.connect(self.load_runtime_and_ui)

        self.ui.actionReport_Issue.triggered.connect(partial(a2util.surf_to, self.a2.urls.help_report_issue))
        self.ui.actionReport_Issue.setIcon(a2ctrl.Icons.inst().github)

        self.ui.actionNew_Module_Dialog.triggered.connect(self.create_new_module)
        self.ui.actionCreate_New_Element.triggered.connect(self.create_new_element)
        self.ui.actionBuild_A2_Package.triggered.connect(self.build_package)

        self.ui.actionUnload_a2_Runtime.triggered.connect(self.shut_down_runtime)
        self.ui.actionUnload_a2_Runtime.setIcon(a2ctrl.Icons.inst().a2close)
        self.ui.actionReload_a2_Runtime.triggered.connect(self.load_runtime_and_ui)
        self.ui.actionReload_a2_Runtime.setIcon(a2ctrl.Icons.inst().a2reload)
        self.ui.actionLoad_a2_Runtime.triggered.connect(self.load_runtime_and_ui)
        self.ui.menuMain.aboutToShow.connect(self._set_runtime_actions_vis)

    def _setup_shortcuts(self):
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape),
                        self, self.escape)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Enter),
                        self, self.edit_submit)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Return),
                        self, self.edit_submit)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S),
                        self, self.edit_submit)

        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Home), self.module_view.ui.a2scroll_area,
                        partial(self.scroll_to, True))
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_End), self.module_view.ui.a2scroll_area,
                        partial(self.scroll_to, False))

    def edit_mod(self, keep_scroll=False):
        if self.num_selected == 1:
            self.module_view.edit_mod(keep_scroll)

    def toggle_dev_menu(self, state=None):
        if state is None:
            # state=None happens only on startup
            state = self.a2.db.get('dev_mode') or False
            # if True we dont have to re-add
            if state is True:
                return
        if state:
            self.ui.menubar.insertAction(self.ui.menuHelp.menuAction(),
                                         self.ui.menuDev.menuAction())
        else:
            self.ui.menubar.removeAction(self.ui.menuDev.menuAction())

    def edit_submit(self):
        """
        Calls the mod to write the tempConfig to disc.
        If it's enabled only trigger settingsChanged when

        """
        if not self.module_view.editing:
            return

        self.mod.config = deepcopy(self.tempConfig)
        if self.mod.enabled:
            self.mod.change()
            self.settings_changed()
        self.module_view.draw_mod()

    def mod_enable(self, checked=None):
        """
        Handles the module checkbox to enable/disable one or multiple modules
        """
        check_box = self.module_view.ui.modCheck
        if check_box.isTristate() or not checked:
            for mod in self.selected:
                mod.enabled = False
            checked = False
        else:
            for mod in self.selected:
                mod.enabled = True
            checked = True

        check_box.setTristate(False)
        check_box.setChecked(checked)
        self.settings_changed()

    def mod_disable_all(self):
        self.a2.enabled = {}
        self.settings_changed(refresh_ui=True)

    def settings_changed(self, specific=None, refresh_ui=False):
        if self._restart_thread is not None:
            self._restart_thread.quit()

        # kill old a2 process
        # TODO: make process killing optional:
        #   remember process id, restart, see if old process still there, remove it
        #   if there is only one: keep it like it is,
        # threading.Thread(target=a2core.killA2process).start()
        log.info('Runtime refresh called!')
        log.info('  Refreshing Ui ...')
        self.module_list.draw_modules()

        log.info('  Writing includes ...')
        a2runtime.write_includes(specific)

        log.info('  Restarting runtime ...')
        self._restart_thread = RestartThread(self.a2, self)
        self._restart_thread.start()

        if refresh_ui:
            self.module_view.draw_mod()
        log.info('  Done!')

    def escape(self):
        if self.module_view.editing:
            self.module_view.draw_mod()
        else:
            self.close()

    def explore_mod(self):
        if self.mod is not None:
            subprocess.Popen(['explorer.exe', self.mod.path])

    def explore_a2(self):
        subprocess.Popen(['explorer.exe', self.a2.paths.a2])

    def closeEvent(self, event):
        binprefs = str(self.saveGeometry().toPercentEncoding())
        self.a2.db.set('windowprefs', {'splitter': self.ui.splitter.sizes(), 'geometry': binprefs})
        self.a2.db.set('last_selected', [m.key for m in self.selected])

        for thread in [self._restart_thread, self.runtime_watcher, self._shutdown_thread]:
            if thread is not None:
                thread.quit()

        QtGui.QMainWindow.closeEvent(self, event)

    def restoreA2ui(self):
        """
        gets window settings from prefs and makes sure the window will be visible
        I let Qt handle that via restoreGeometry. Downside is: It does not put back windows
        that are partiall outside of the left,right and bottom desktop border
        """
        winprefs = self.a2.db.get('windowprefs') or {}
        geometry = winprefs.get('geometry')
        if geometry is not None:
            geometry = QtCore.QByteArray().fromPercentEncoding(geometry)
            self.restoreGeometry(geometry)
        splitterSize = winprefs.get('splitter')
        if splitterSize is not None:
            self.ui.splitter.setSizes(winprefs['splitter'])

    def showRaise(self):
        self.show()
        self.activateWindow()
        # self.setFocus()

    def scroll_to(self, value, smooth=False):
        # TODO: reimplement in each widget
        pass

    def create_new_element(self):
        from a2widget import new_element_tool
        new_element_tool.NewElementDialog(self)

    def create_new_module(self):
        from a2widget import new_module_tool
        new_module_tool.NewModulueTool(self)

    def create_local_source(self):
        from a2widget import new_module_source_tool
        new_module_source_tool.NewModuleSourceTool(self)

    def rebuild_css(self, user_scale=None):
        if user_scale is None:
            user_scale = self.a2.db.get('ui_scale') or 1.0
        self.css_values['user_scale'] = user_scale

        local_scale = self.app.desktop().physicalDpiX() / BASE_DPI
        self.css_values['local_scale'] = local_scale
        scale = self.css_values['local_scale'] * user_scale
        self.css_values['scale'] = scale

        css_template_path = os.path.join(self.a2.paths._defaults, 'css_defaults.json')
        css_defaults = a2util.json_read(css_template_path)
        with open(os.path.join(self.a2.paths._defaults, 'a2.css')) as fobj:
            css_template = fobj.read()

        for name, value in css_defaults.items():
            if isinstance(value, int):
                value = int(scale * float(value))
            self.css_values[name] = value

        css_template = css_template % self.css_values
        self.app.setStyleSheet(css_template)
        self.a2.db.set('ui_scale', user_scale)

    def build_package(self):
        batch_path = os.path.join(self.a2.paths.lib, 'batches')
        batch_name = 'build_py_package.bat'
        subprocess.Popen(['cmd.exe', '/c', 'start %s' % batch_name], cwd=batch_path)

    def _set_runtime_actions_vis(self):
        live = self.runtime_watcher.is_live
        self.ui.actionUnload_a2_Runtime.setVisible(live)
        self.ui.actionReload_a2_Runtime.setVisible(live)
        self.ui.actionLoad_a2_Runtime.setVisible(not live)

    def shut_down_runtime(self):
        self._shutdown_thread = ShutdownThread(self)
        self._shutdown_thread.start()

    def load_runtime_and_ui(self):
        self.settings_changed(refresh_ui=True)

    def edit_code(self, file_path):
        if os.path.isfile(self.devset.code_editor):
            subprocess.Popen([self.devset.code_editor, file_path])
        else:
            _TASK_MSG = 'browse for a code editor executable'
            _QUEST_MSG = 'Do you want to %s now?' % _TASK_MSG

            reply = QtGui.QMessageBox.question(
                self, 'No Valid Code Editor Set!', _QUEST_MSG,
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel)

            if reply == QtGui.QMessageBox.Yes:
                exepath, _ = QtGui.QFileDialog.getOpenFileName(
                    self, _TASK_MSG.title(), self.devset.code_editor, 'Executable (*.exe)')
                if exepath:
                    self.devset.set_var('code_editor', exepath)
                    self.edit_code(file_path)


class RestartThread(QtCore.QThread):
    def __init__(self, a2, parent):
        super(RestartThread, self).__init__(parent)
        self.a2 = a2

    def run(self, *args, **kwargs):
        self.msleep(RESTART_DELAY)
        ahk_process = QtCore.QProcess()
        _retval, _pid = ahk_process.startDetached(
            self.a2.paths.autohotkey, [self.a2.paths.a2_script], self.a2.paths.a2)
        return QtCore.QThread.run(self, *args, **kwargs)


class ShutdownThread(QtCore.QThread):
    def __init__(self, parent):
        super(ShutdownThread, self).__init__(parent)

    def run(self, *args, **kwargs):
        pid = a2runtime.kill_a2_process()
        if pid:
            log.info('Shut down process with PID: %s' % pid)
        return QtCore.QThread.run(self, *args, **kwargs)


class RuntimeWatcher(QtCore.QThread):
    message = QtCore.Signal(str)

    def __init__(self, parent):
        super(RuntimeWatcher, self).__init__(parent)
        self.lifetime = 0
        self.is_live = False
        self.stopped = False

    def quit(self, *args, **kwargs):
        self.stopped = True
        self.terminate()

    def run(self, *args, **kwargs):
        while not self.stopped:
            self.msleep(RUNTIME_WATCH_INTERVAL)
            self.is_live = a2runtime.is_runtime_live()

            if self.is_live:
                self.lifetime += 1
                if self.lifetime < 5:
                    self.message.emit('Runtime is Live!')
                else:
                    self.message.emit('')
            else:
                self.lifetime = 0
                self.message.emit('Runtime is Offline!')

        return QtCore.QThread.run(self, *args, **kwargs)


class DevSettings(object):
    def __init__(self, a2):
        self._enabled = False
        self.author_name = ''
        self.author_url = ''
        self.code_editor = ''
        self.json_indent = 2
        self.loglevel_debug = False

        self._a2 = a2
        self._defaults = {
            'author_name': os.getenv('USERNAME'),
            'author_url': '',
            'code_editor': '',
            'json_indent': 2,
            'loglevel_debug': False}
        self.get()

        log.info('self.loglevel_debug: %s' % self.loglevel_debug)
        log.debug('self.loglevel_debug: %s' % self.loglevel_debug)

    def _get_from_db(self):
        return self._a2.db.get_changes('dev_settings', self._defaults)

    def get(self):
        settings = self._get_from_db()
        self._set_attrs(settings)
        return settings

    def _set_attrs(self, settings):
        for key, value in settings.items():
            setattr(self, key, value)

    def set(self, these):
        self._a2.db.set_changes('dev_settings', these, self._defaults)
        self._set_attrs(these)

    def set_var(self, key, value):
        settings = self._get_from_db()
        settings[key] = value
        self.set(settings)


if __name__ == '__main__':
    import a2app
    a2app.main()
