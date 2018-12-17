"""
a2ui - setup interface for an Autohotkey environment.
"""
import os
import time
from copy import deepcopy
from functools import partial

import a2dev
import a2core
import a2ctrl
import a2util
import a2runtime
from a2widget import a2design_ui

from PySide2 import QtGui, QtCore, QtWidgets


log = a2core.get_logger(__name__)
ui_defaults = None
RESTART_DELAY = 300
RUNTIME_WATCH_INTERVAL = 1000


class A2Window(QtWidgets.QMainWindow):

    def __init__(self, app=None):
        super(A2Window, self).__init__(parent=None)
        self.a2 = a2core.A2Obj.inst()
        self.app = app
        self._restart_thread = None
        self._shutdown_thread = None

        self.edit_clipboard = []
        self.temp_config = None
        self.selected = []
        self.mod = None

        self.style = None
        self.rebuild_css()

        self.devset = a2dev.DevSettings(self.a2)
        if self.devset.loglevel_debug:
            a2core.set_loglevel(debug=True)
            log.debug('Loglevel set to DEBUG!')

        self._setup_ui()

        self.num_selected = 0
        init_selection = []
        if self.a2.db.get('remember_last') or False:
            init_selection = self.a2.db.get('last_selected') or []
        self.module_list.selection_changed.connect(self._module_selected)
        self.module_list.draw_modules(init_selection)
        if not init_selection:
            self.module_view.draw_mod()

        self.runtime_watcher = RuntimeWatcher(self)
        self.runtime_watcher.message.connect(self.runtime_watcher_message)
        self.runtime_watcher.start()

        log.info('A2Window initialised!')

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

        self.check_main_menu_bar()
        self.module_view.draw_mod()

    def _setup_ui(self):
        a2ctrl.check_ui_module(a2design_ui)
        self.ui = a2design_ui.Ui_a2MainWindow()
        self.ui.setupUi(self)
        # shortcuts
        self.module_list = self.ui.module_list
        self.module_list.set_item_colors(
            default=self.style.get('font_color'),
            tinted=self.style.get('font_color_tinted'))
        self.module_view = self.ui.module_view

        self.module_view.setup_ui(self)

        self._setup_actions()
        self._setup_shortcuts()

        self.check_main_menu_bar()
        self.setWindowIcon(a2ctrl.Icons.inst().a2)
        self.restore_ui()

    def _setup_actions(self):
        icons = a2ctrl.Icons.inst()
        self.ui.actionEdit_module.triggered.connect(self.edit_mod)
        self.ui.actionEdit_module.setIcon(icons.edit)

        self.ui.actionDisable_all_modules.triggered.connect(self.mod_disable_all)
        self.ui.actionExplore_to.triggered.connect(self.explore_mod)
        self.ui.actionExplore_to.setIcon(icons.folder)

        self.ui.actionAbout_a2.triggered.connect(partial(a2util.surf_to, self.a2.urls.help))
        self.ui.actionAbout_a2.setIcon(icons.a2help)
        self.ui.actionAbout_Autohotkey.triggered.connect(partial(a2util.surf_to, self.a2.urls.ahk))
        self.ui.actionAbout_Autohotkey.setIcon(icons.autohotkey)

        self.ui.actionExplore_to_a2_dir.triggered.connect(self.explore_a2)
        self.ui.actionExplore_to_a2_dir.setIcon(icons.folder)
        self.ui.actionExplore_to_a2_data_dir.triggered.connect(self.explore_a2data)
        self.ui.actionExplore_to_a2_data_dir.setIcon(icons.folder)
        self.ui.actionA2_settings.triggered.connect(partial(self.module_list.select, None))
        self.ui.actionA2_settings.setIcon(icons.a2)
        self.ui.actionExit_a2ui.triggered.connect(self.close)
        self.ui.actionExit_a2ui.setIcon(icons.clear)
        self.ui.actionRefresh_UI.triggered.connect(self.load_runtime_and_ui)

        self.ui.actionReport_Issue.triggered.connect(partial(a2util.surf_to, self.a2.urls.help_report_issue))
        self.ui.actionReport_Issue.setIcon(icons.github)

        self.ui.actionNew_Module_Dialog.triggered.connect(self.create_new_module)
        self.ui.actionNew_Module_Dialog.setIcon(icons.folder_add)
        self.ui.actionCreate_New_Element.triggered.connect(self.create_new_element)
        self.ui.actionCreate_New_Element.setIcon(icons.folder_add)
        self.ui.actionBuild_A2_Package.triggered.connect(self.build_package)

        self.ui.actionUnload_a2_Runtime.triggered.connect(self.shut_down_runtime)
        self.ui.actionUnload_a2_Runtime.setIcon(icons.a2close)
        self.ui.actionReload_a2_Runtime.triggered.connect(self.load_runtime_and_ui)
        self.ui.actionReload_a2_Runtime.setIcon(icons.a2reload)
        self.ui.actionLoad_a2_Runtime.triggered.connect(self.load_runtime_and_ui)
        self.ui.menuMain.aboutToShow.connect(self._set_runtime_actions_vis)

        self.ui.menuDev.aboutToShow.connect(self.on_dev_menu_build)
        self.ui.menuRollback_Changes.aboutToShow.connect(self.build_rollback_menu)
        self.ui.menuRollback_Changes.setIcon(icons.rollback)
        self.ui.actionRevert_Settings.triggered.connect(self.on_revert_settings)

        self.ui.menuModule.aboutToShow.connect(self.build_module_menu)

    def _setup_shortcuts(self):
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape),
                            self, self.escape)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Enter),
                            self, self.edit_submit)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Return),
                            self, self.edit_submit)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S),
                            self, self.edit_submit)

        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Home),
                            self.module_view.ui.a2scroll_area,
                            partial(self.scroll_to, True))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_End),
                            self.module_view.ui.a2scroll_area,
                            partial(self.scroll_to, False))
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F1),
                            self, self.module_view.help)

    def edit_mod(self):
        if self.num_selected == 1:
            self.module_view.edit_mod()

    def check_main_menu_bar(self):
        dev_mode = self.a2.dev_mode
        if dev_mode:
            self.ui.menubar.insertAction(self.ui.menuHelp.menuAction(),
                                         self.ui.menuDev.menuAction())
            module_menu_before_action = self.ui.menuDev.menuAction()
        else:
            self.ui.menubar.removeAction(self.ui.menuDev.menuAction())
            module_menu_before_action = self.ui.menuHelp.menuAction()

        if self.mod is None:
            self.ui.menubar.removeAction(self.ui.menuModule.menuAction())
        else:
            self.ui.menubar.insertAction(module_menu_before_action,
                                         self.ui.menuModule.menuAction())

    def edit_submit(self):
        """
        Calls the mod to write the temp_config to disc.
        If it's enabled only trigger settingsChanged when

        """
        if not self.module_view.editing:
            return

        self.mod.config = deepcopy(self.temp_config)
        if self.mod.enabled:
            self.mod.change()
            self.settings_changed()
        self.module_view.draw_mod()

    def mod_enable(self, check):
        """
        Handles the module checkbox to enable/disable one or multiple modules.

        :param bool check: Checkbox state incoming from the module view header.
        """
        check_box = self.module_view.ui.modCheck
        check = not check_box.isTristate() and check
        for mod in self.selected:
            mod.enabled = check
        self.module_list.set_item_states(self.selected)
        check_box.setTristate(False)
        check_box.setChecked(check)
        self.settings_changed()

    def mod_disable_all(self):
        self.a2.enabled = {}
        self.settings_changed(refresh_ui=True)

    def settings_changed(self, specific=None, refresh_ui=False):
        log.info('Runtime refresh called!')
        self.a2.fetch_modules()

        log.info('  Writing includes ...')
        a2runtime.write_includes(specific)

        log.info('  Restarting runtime ...')
        self._restart_thread = RestartThread(self.a2, self)
        self._restart_thread.finished.connect(self._restart_thread.deleteLater)
        self._restart_thread.start()

        if refresh_ui:
            log.info('  Refreshing Ui ...')
            self.module_list.draw_modules()
            self.module_view.draw_mod()
        log.info('  Done!')

    def escape(self):
        if self.module_view.editing:
            log.debug('Exiting Module edit mode!')
            self.module_view.draw_mod()
        else:
            log.info('Exiting a2 Ui! okithxbye')
            self.close()

    def explore_mod(self):
        if self.mod is not None:
            a2util.explore(self.mod.path)
        else:
            self.explore_a2()

    def explore_a2(self):
        a2util.explore(self.a2.paths.a2)

    def explore_a2data(self):
        a2util.explore(self.a2.paths.data)

    def closeEvent(self, event):
        win_geom_str = self.saveGeometry().toBase64().data().decode()
        self.a2.db.set('windowprefs', {'splitter': self.ui.splitter.sizes(),
                                       'geometry': win_geom_str})
        self.a2.db.set('last_selected', [m.key for m in self.selected])

        for thread in [self._restart_thread, self.runtime_watcher, self._shutdown_thread]:
            if thread is not None:
                try:
                    thread.quit()
                except RuntimeError:
                    pass

        QtWidgets.QMainWindow.closeEvent(self, event)

    def restore_ui(self):
        """
        gets window settings from prefs and makes sure the window will be visible
        I let Qt handle that via restoreGeometry. Downside is: It does not put back windows
        that are partially outside of the left,right and bottom desktop border
        """
        win_prefs = self.a2.db.get('windowprefs') or {}
        geometry = win_prefs.get('geometry')
        if geometry is not None:
            try:
                geometry = QtCore.QByteArray().fromBase64(bytes(geometry, 'utf8'))
                self.restoreGeometry(geometry)
            except Exception as error:
                log.debug('Could not restore the ui geometry with stored data!')
                log.debug(error)

        splitter_size = win_prefs.get('splitter')
        if splitter_size is not None:
            self.ui.splitter.setSizes(splitter_size)

    def showRaise(self):
        """
        Calls the window to show as currently active window.

        btw: These aren't random shots to make the window appear somehow.
        Each step has its purpose and is needed.
        """
        # call to render the window
        self.show()
        # restore the window from minimized state
        state = self.windowState()
        if state == QtCore.Qt.WindowMinimized:
            self.setWindowState(QtCore.Qt.WindowActive)
        elif state not in QtCore.Qt.WindowState.values.values():
            log.info('Window state undefined! %s' % state)
            self.setWindowState(QtCore.Qt.WindowActive)
        # make it the currently active window
        self.activateWindow()

    def scroll_to(self, value, smooth=False):
        # TODO: reimplement in each widget
        pass

    def create_new_element(self):
        from a2widget import new_element_tool
        new_element_tool.NewElementDialog(self).show()

    def create_new_module(self):
        from a2widget import new_module_tool
        new_module_tool.NewModulueTool(self).show()

    def create_local_source(self):
        from a2widget import new_module_source_tool
        dialog = new_module_source_tool.NewModuleSourceTool(self)
        dialog.okayed.connect(self._create_local_source)
        dialog.show()

    def _create_local_source(self, name):
        import a2mod
        path = a2mod.create_module_source_dir(name)
        # write empty cfg json so its found by the package lister
        cfg = a2mod.get_default_package_cfg()
        cfg['name'] = name
        cfg['maintainer'] = self.devset.author_name
        cfg['url'] = self.devset.author_url
        a2util.json_write(os.path.join(path, a2mod.MOD_SOURCE_NAME), cfg)
        # update the ui without runtime reload
        self.a2.fetch_modules()
        self.module_view.draw_mod()

    def rebuild_css(self, user_scale=None):
        if user_scale is None:
            user_scale = self.a2.db.get('ui_scale') or 1.0
        else:
            self.a2.db.set('ui_scale', user_scale)

        if self.style is None:
            import a2style
            self.style = a2style.A2StyleBuilder(self.a2.db.get('ui_theme'))

        css_template = self.style.get_style(user_scale)
        self.app.setStyleSheet(css_template)

    def build_package(self):
        batch_path = os.path.join(self.a2.paths.lib, 'batches')
        batch_name = 'build_py_package.bat'
        _result, _pid = a2util.start_process_detached(
            os.getenv('COMSPEC'), ['/c', 'start %s' % batch_name], batch_path)

    def _set_runtime_actions_vis(self):
        live = self.runtime_watcher.is_live
        self.ui.actionUnload_a2_Runtime.setVisible(live)
        self.ui.actionReload_a2_Runtime.setVisible(live)
        self.ui.actionLoad_a2_Runtime.setVisible(not live)

    def shut_down_runtime(self):
        self._shutdown_thread = ShutdownThread(self)
        self._shutdown_thread.finished.connect(self._shutdown_thread.deleteLater)
        self._shutdown_thread.start()

    def load_runtime_and_ui(self):
        self.settings_changed(refresh_ui=True)

    def edit_code(self, file_path):
        if os.path.isfile(self.devset.code_editor):
            _result, _pid = a2util.start_process_detached(self.devset.code_editor, file_path)

        else:
            _TASK_MSG = 'browse for a code editor executable'
            _QUEST_MSG = 'Do you want to %s now?' % _TASK_MSG

            reply = QtWidgets.QMessageBox.question(
                self, 'No Valid Code Editor Set!', _QUEST_MSG,
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)

            if reply == QtWidgets.QMessageBox.Yes:
                exepath, _ = QtWidgets.QFileDialog.getOpenFileName(
                    self, _TASK_MSG.title(), self.devset.code_editor, 'Executable (*.exe)')
                if exepath:
                    self.devset.set_var('code_editor', exepath)
                    self.edit_code(file_path)

    def build_module_menu(self):
        menu = self.sender()
        menu.clear()
        menu.addAction(self.ui.actionHelp_on_Module)
        menu.addAction(self.ui.actionRevert_Settings)
        if self.module_view.menu_items:
            menu.addSeparator()
            for action in self.module_view.menu_items:
                menu.addAction(action)

    def diff_files(self, file1, file2):
        if os.path.isfile(self.devset.diff_app):
            _result, _pid = a2util.start_process_detached(self.devset.diff_app, [file1, file2])
        else:
            _TASK_MSG = 'browse for a Diff executable'
            _QUEST_MSG = 'Do you want to %s now?' % _TASK_MSG

            reply = QtWidgets.QMessageBox.question(
                self, 'No Diff application set!', _QUEST_MSG,
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)

            if reply == QtWidgets.QMessageBox.Yes:
                exepath, _ = QtWidgets.QFileDialog.getOpenFileName(
                    self, _TASK_MSG.title(), self.devset.diff_app, 'Executable (*.exe)')
                if exepath:
                    self.devset.set_var('diff_app', exepath)
                    self.diff_files(file1, file2)

    def on_dev_menu_build(self):
        self.ui.menuRollback_Changes.setEnabled(self.mod is not None)

    def build_rollback_menu(self):
        icons = a2ctrl.Icons.inst()
        menu = self.ui.menuRollback_Changes
        menu.clear()
        backups_sorted = self.mod.get_config_backups()
        if not backups_sorted:
            action = menu.addAction('Nothing to roll back to!')
            action.setEnabled(False)
        else:
            now = time.time()
            for this_time, backup_name in backups_sorted[:15]:
                try:
                    label = a2util.unroll_seconds(now - this_time, 2)
                    label = 'version %s - %s ago' % (int(backup_name[-1]), label)
                except ValueError:
                    continue
                action = menu.addAction(icons.rollback, label, self.module_rollback_to)
                action.setData(backup_name)
            menu.addSeparator()
            menu.addAction(icons.delete, 'Clear Backups', self.mod.clear_backups)

    def module_rollback_to(self):
        title = self.sender().text()
        file_name = self.sender().data()
        file_path = os.path.join(self.mod.backup_path, file_name)

        from a2dev import RollbackDiffDialog
        dialog = RollbackDiffDialog(self, title)
        dialog.diff.connect(partial(self.diff_files, self.mod.config_file, file_path))
        dialog.okayed.connect(partial(self.on_rollback, file_name))
        dialog.show()

    def on_rollback(self, file_name):
        self.mod.rollback(file_name)
        self.settings_changed()

    def on_help_action(self):
        text = self.sender().text()
        print('text: %s' % text)
        print('self.a2.urls.help: %s' % self.a2.urls.help)
        a2util.surf_to(self.a2.urls.help)

    def on_revert_settings(self):
        if self.mod is None:
            return
        from a2widget import A2ConfirmDialog

        module_user_cfg = self.mod.get_user_cfg()
        if module_user_cfg:
            dialog = A2ConfirmDialog(self, 'Revert User Settings',
                                     msg='This will throw away any user changes!')
            dialog.okayed.connect(self._on_revert_settings)
            dialog.show()
        else:
            dialog = A2ConfirmDialog(self, 'Nothing to Revert!',
                                     msg='Appears everything is on "factory settings"!')
            dialog.show()

    def _on_revert_settings(self):
        self.mod.clear_user_cfg()
        self.mod.change()
        self.load_runtime_and_ui()


class RestartThread(QtCore.QThread):
    def __init__(self, a2, parent):
        super(RestartThread, self).__init__(parent)
        self.a2 = a2

    def run(self):
        self.msleep(RESTART_DELAY)
        _retval, _pid = a2util.start_process_detached(
            self.a2.paths.autohotkey, [self.a2.paths.a2_script], self.a2.paths.a2)


class ShutdownThread(QtCore.QThread):
    def __init__(self, parent):
        super(ShutdownThread, self).__init__(parent)

    def run(self):
        pid = a2runtime.kill_a2_process()
        if pid:
            log.info('Shut down process with PID: %s' % pid)


class RuntimeWatcher(QtCore.QThread):
    message = QtCore.Signal(str)

    def __init__(self, parent):
        super(RuntimeWatcher, self).__init__(parent)
        self.lifetime = 0
        self.is_live = False
        self.stopped = False

    def quit(self):
        self.stopped = True
        self.terminate()

    def run(self):
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


if __name__ == '__main__':
    import a2app
    a2app.main()
