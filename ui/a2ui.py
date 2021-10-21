"""
a2ui - setup interface for an Autohotkey environment.
"""
import os
import time
from functools import partial

import a2uic
import a2dev
import a2core
import a2ctrl
import a2util

from a2qt import QtGui, QtCore, QtWidgets

log = a2core.get_logger(__name__)
RESTART_DELAY = 300
RUNTIME_WATCH_INTERVAL = 1000
DEFAULT_WIN_SIZE = (700, 480)
TITLE_ONLINE = 'Runtime is Live!'
TITLE_OFFLINE = 'Runtime is Offline!'


class A2Window(QtWidgets.QMainWindow):
    def __init__(self, app):
        super(A2Window, self).__init__(parent=None)
        self.setEnabled(False)
        self.a2 = a2core.A2Obj.inst()
        self.app = app
        self._threads = {}
        self._scroll_anim = None

        self.edit_clipboard = []
        self.selected = []
        self.num_selected = 0
        self.mod = None

        self._style = None
        self.rebuild_css()

        self.devset = a2dev.DevSettings(self.a2)
        if self.devset.loglevel_debug:
            a2core.set_loglevel(debug=True)
            log.debug('Loglevel set to DEBUG!')

        self._init_selection = []
        if self.a2.db.get('remember_last') or False:
            self._init_selection = self.a2.db.get('last_selected') or []

        self._initial_activation_tries = 0
        self._initial_draw_finished = False

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
        from a2widget import a2design_ui

        a2uic.check_module(a2design_ui)
        self.ui = a2design_ui.Ui_a2MainWindow()
        self.ui.setupUi(self)

        self.module_list = self.ui.module_list
        self.module_list.set_item_colors(
            default=self.style.get('font_color'),
            tinted=self.style.get('font_color_tinted'),
        )
        self.module_list.selection_changed.connect(self._module_selected)
        self.module_list.enable_request.connect(self.mod_enable)

        self.module_view = self.ui.module_view
        self.module_view.reload_requested.connect(self.load_runtime_and_ui)
        self.module_view.setup_ui(self)
        self.module_view.enable_request.connect(self.mod_enable)
        self.module_view.edit_mode.connect(self._set_edit_mode)
        self.module_view.okayed.connect(self.edit_submit)

        self._setup_actions()
        self._setup_shortcuts()

        self.check_main_menu_bar()

    def _setup_actions(self):
        Icons = a2ctrl.Icons
        self.ui.actionEdit_module.triggered.connect(self.module_view.edit_mod)
        self.ui.actionEdit_module.setIcon(Icons.edit)

        self.ui.actionDisable_all_modules.triggered.connect(self.mod_disable_all)
        self.ui.actionExplore_to.triggered.connect(self.explore_mod)
        self.ui.actionExplore_to.setIcon(Icons.folder)

        self._make_url_action(self.ui.actionAbout_a2, self.a2.urls.help, Icons.a2help)
        self._make_url_action(self.ui.actionAbout_Autohotkey, self.a2.urls.ahk, Icons.autohotkey)

        self.ui.actionExplore_to_a2_dir.triggered.connect(self.explore_a2)
        self.ui.actionExplore_to_a2_dir.setIcon(Icons.folder)
        self.ui.actionExplore_to_a2_data_dir.triggered.connect(self.explore_a2data)
        self.ui.actionExplore_to_a2_data_dir.setIcon(Icons.folder)
        self.ui.actionA2_settings.triggered.connect(self.module_list.select)
        self.ui.actionA2_settings.setIcon(Icons.a2)
        self.ui.actionExit_a2ui.triggered.connect(self.close)
        self.ui.actionExit_a2ui.setIcon(Icons.clear)
        self.ui.actionRefresh_UI.triggered.connect(self.load_runtime_and_ui)

        self._make_url_action(self.ui.action_report_bug, self.a2.urls.report_bug, Icons.github)
        self._make_url_action(self.ui.action_report_sugg, self.a2.urls.report_sugg, Icons.github)

        self.ui.actionNew_Module_Dialog.triggered.connect(self.create_new_module)
        self.ui.actionNew_Module_Dialog.setIcon(Icons.folder_add)
        self.ui.actionCreate_New_Element.triggered.connect(self.create_new_element)
        self.ui.actionCreate_New_Element.setIcon(Icons.folder_add)
        self.ui.actionBuild_A2_Package.triggered.connect(self.build_package)

        self.ui.actionUnload_a2_Runtime.triggered.connect(self.shut_down_runtime)
        self.ui.actionUnload_a2_Runtime.setIcon(Icons.a2x)
        self.ui.actionReload_a2_Runtime.triggered.connect(self.load_runtime_and_ui)
        self.ui.actionReload_a2_Runtime.setIcon(Icons.a2reload)
        self.ui.actionLoad_a2_Runtime.triggered.connect(self.load_runtime_and_ui)
        self.ui.menuMain.aboutToShow.connect(self._set_runtime_actions_vis)

        self.ui.menuDev.aboutToShow.connect(self.on_dev_menu_build)
        self.ui.menuRollback_Changes.aboutToShow.connect(self.build_rollback_menu)
        self.ui.menuRollback_Changes.setIcon(Icons.rollback)
        self.ui.actionRevert_Settings.triggered.connect(self.on_revert_settings)

        self.ui.menuModule.aboutToShow.connect(self.build_module_menu)

        if os.path.isfile(self.a2.paths.uninstaller):
            self.ui.actionUninstall_a2.setIcon(Icons.a2x)
            self.ui.actionUninstall_a2.triggered.connect(self.on_uninstall_a2)
        else:
            self.ui.actionUninstall_a2.deleteLater()
            self.on_uninstall_a2 = None

    def _make_url_action(self, action: QtGui.QAction, url: str, icon: QtGui.QIcon):
        action.setData(url)
        action.setIcon(icon)
        action.triggered.connect(self._on_url_action)

    def _on_url_action(self):
        action = self.sender()
        if isinstance(action, QtGui.QAction):
            a2util.surf_to(action.data())

    def _setup_shortcuts(self):
        Qt = QtCore.Qt
        scroll_area = self.module_view.ui.a2scroll_area

        for keys, parent, func in (
            (Qt.Key_Escape, self, self.escape),
            (Qt.CTRL + Qt.Key_Enter, self, self.edit_submit),
            (Qt.CTRL + Qt.Key_Return, self, self.edit_submit),
            (Qt.CTRL + Qt.Key_S, self, self.edit_submit),
            (Qt.Key_Home, scroll_area, self.scroll_to_start),
            (Qt.Key_End, scroll_area, self.scroll_to_end),
            (Qt.Key_F1, self, self.module_view.help),
        ):
            shortcut = QtGui.QShortcut(parent)
            shortcut.setKey(QtGui.QKeySequence(keys))
            shortcut.activated.connect(func)

    def check_main_menu_bar(self):
        """Handle main menu item visibility."""
        if self.a2.dev_mode:
            self.ui.menubar.insertAction(
                self.ui.menuHelp.menuAction(), self.ui.menuDev.menuAction()
            )
            module_menu_before_action = self.ui.menuDev.menuAction()
        else:
            self.ui.menubar.removeAction(self.ui.menuDev.menuAction())
            module_menu_before_action = self.ui.menuHelp.menuAction()

        if self.mod is None:
            self.ui.menubar.removeAction(self.ui.menuModule.menuAction())
        else:
            self.ui.menubar.insertAction(module_menu_before_action, self.ui.menuModule.menuAction())

    def edit_submit(self):
        """
        Call module to write `temp_config` to disc.
        If it's enabled only trigger settingsChanged when
        """
        if not self.module_view.editing:
            return

        self.mod.config = self.module_view.editor.get_cfg_copy()
        if self.mod.enabled:
            self.mod.change()
            self.settings_changed()
        self.module_view.draw_mod()

    def mod_enable(self, state: bool):
        """
        Handles the module checkbox to enable/disable one or multiple modules.

        :param bool check: Checkbox state incoming from the module view header.
        """
        for mod in self.selected:
            if mod.enabled != state:
                mod.enabled = state
        self.module_list.set_item_states(self.selected)
        self.module_view.update_header()
        self.settings_changed()

    def mod_disable_all(self):
        self.a2.enabled = {}
        self.load_runtime_and_ui()

    def settings_changed(self, specific=None):
        log.info('Runtime refresh called!')
        self.a2.fetch_modules_if_stale()

        log.info('  Writing includes ...')
        import a2runtime

        a2runtime.write_includes(specific)

        log.info('  Restarting runtime ...')
        self._run_thread('restart', RuntimeCallThread)

    def refresh_ui(self):
        log.info('  Refreshing Ui ...')
        self.rebuild_css()
        self.module_list.draw_modules()
        self.module_view.draw_mod()

    def escape(self):
        if self.module_view.editing:
            if self.module_view.cfg_different():
                if self.module_view.user_cancels():
                    return
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
        self.a2.db.set(
            'windowprefs',
            {'splitter': self.ui.splitter.sizes(), 'geometry': win_geom_str},
        )
        self.a2.db.set('last_selected', [m.key for m in self.selected])

        from a2qt import shiboken

        for thread in self._threads.values():
            if thread is None:
                continue
            if not shiboken.isValid(thread):
                continue
            thread.requestInterruption()
            tries = 10
            while thread.isRunning():
                if tries < 5:
                    log.info(f'Wating for thread: {thread}')
                tries -= 1
                if not tries:
                    log.error(f'Thread NOT stopped: {thread}')
                    break
                time.sleep(0.1)

        QtWidgets.QMainWindow.closeEvent(self, event)

    def restore_ui(self):
        """
        gets window settings from prefs and makes sure the window will be visible
        I let Qt handle that via restoreGeometry. Downside is: It does not put back windows
        that are partially outside of the left,right and bottom desktop border
        """
        win_prefs = self.a2.db.get('windowprefs') or {}
        geometry = win_prefs.get('geometry')
        if geometry is None:
            self.reset_window_geometry()
        else:
            try:
                success = self.restoreGeometry(
                    QtCore.QByteArray().fromBase64(bytes(geometry, 'utf8'))
                )
                if not success:
                    self.reset_window_geometry()
            except Exception as error:
                log.debug('Could not restore the ui geometry with stored data!')
                log.debug(error)

    def reset_window_geometry(self):
        """Initialize window position & size."""
        # create a default geometry
        scale = self.style.get('scale', 1)
        geometry = self.geometry()
        geometry.setSize(QtCore.QSize(DEFAULT_WIN_SIZE[0] * scale, DEFAULT_WIN_SIZE[1] * scale))
        # set to center of active screen
        desktop = QtWidgets.QApplication.instance().desktop()
        current_screen = desktop.screen(desktop.screenNumber(QtGui.QCursor.pos()))
        geometry.moveCenter(current_screen.geometry().center())
        log.info('Initializing window position & size: %s', geometry)
        self.setGeometry(geometry)

    def show_raise(self):
        """
        Call the window to show as currently active window.

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
            self.setWindowState(QtCore.Qt.WindowActive)

        self._initial_activation_tries = 0
        self._activate_window()

    def _activate_window(self):
        """Make sure we're the currently active window."""
        self.activateWindow()
        if self.isActiveWindow():
            return

        if self._initial_activation_tries > 5:
            return

        self.activateWindow()
        self._initial_activation_tries += 1
        QtCore.QTimer(self).singleShot(50, self._activate_window)

    def scroll_to_start(self):
        """Scroll the main view to the top."""
        self._scroll(self.module_view.ui.a2scroll_area, False)

    def scroll_to_end(self):
        """Scroll the main view to the bottom."""
        self._scroll(self.module_view.ui.a2scroll_area, True)

    def _scroll(self, widget, value, extra=0, duration=250):
        """Scroll the main view to the top."""
        scrollbar = widget.verticalScrollBar()
        if value:
            start, end = scrollbar.value(), scrollbar.maximum() + extra
        else:
            start, end = scrollbar.value(), 0

        vscrollbar = widget.verticalScrollBar()
        self._scroll_anim = QtCore.QPropertyAnimation(vscrollbar, b'value')
        self._scroll_anim.setStartValue(start)
        self._scroll_anim.setEndValue(end)
        self._scroll_anim.setDuration(duration)
        self._scroll_anim.setLoopCount(1)
        self._scroll_anim.setEasingCurve(QtCore.QEasingCurve.InOutCubic)
        self._scroll_anim.start()

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
        import a2modsource

        a2modsource.create(name, self.devset.author_name, self.devset.author_url)
        # update the ui without runtime reload
        self.a2.fetch_modules()
        self.module_view.draw_mod()

    @property
    def style(self):
        if self._style is None:
            self._style = self.rebuild_css()
        return self._style

    def rebuild_css(self, user_scale=None):
        if user_scale is None:
            user_scale = self.a2.db.get('ui_scale') or 1.0
        else:
            self.a2.db.set('ui_scale', user_scale)

        if self._style is None:
            import a2style

            self._style = a2style.A2StyleBuilder(self.a2.db.get('ui_theme'))

        css_template = self._style.get_style(user_scale)
        self.app.setStyleSheet(css_template)
        return self._style

    def build_package(self):
        batch_path = os.path.join(self.a2.paths.lib, 'batches')
        batch_name = 'build_py_package.bat'
        _result, _pid = a2util.start_process_detached(
            os.getenv('COMSPEC'), ['/c', 'start %s' % batch_name], batch_path
        )

    def _set_runtime_actions_vis(self):
        live = self._threads['runtime'].is_live
        self.ui.actionUnload_a2_Runtime.setVisible(live)
        self.ui.actionReload_a2_Runtime.setVisible(live)
        self.ui.actionLoad_a2_Runtime.setVisible(not live)

    def shut_down_runtime(self):
        self._run_thread('shutdown', RuntimeCallThread, '--shutdown')

    def load_runtime_and_ui(self):
        self.settings_changed()
        self.refresh_ui()

    def edit_code(self, file_path):
        app_path = self.devset.get_editor()
        if not app_path:
            return
        _result, _pid = a2util.start_process_detached(app_path, file_path)

    def build_module_menu(self):
        menu = self.sender()
        menu.clear()
        menu.addAction(self.ui.actionHelp_on_Module)
        menu.addAction(self.ui.actionRevert_Settings)
        if self.module_view.menu_items:
            menu.addSeparator()
            for action in self.module_view.menu_items:
                menu.addAction(action)

    def on_dev_menu_build(self):
        self.ui.menuRollback_Changes.setEnabled(self.mod is not None)

    def build_rollback_menu(self):
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
                    label = 'version %s - %s ago' % (
                        int(backup_name[-1]),
                        label,
                    )
                except ValueError:
                    continue
                action = menu.addAction(a2ctrl.Icons.rollback, label, self.module_rollback_to)
                action.setData(backup_name)
            menu.addSeparator()
            menu.addAction(a2ctrl.Icons.delete, 'Clear Backups', self.mod.clear_backups)

    def module_rollback_to(self):
        title = self.sender().text()
        file_name = self.sender().data()
        file_path = os.path.join(self.mod.backup_path, file_name)

        from a2dev import RollbackDiffDialog

        dialog = RollbackDiffDialog(self, title, self.mod.config_file, file_path)
        dialog.okayed.connect(partial(self.on_rollback, file_name))
        dialog.show()

    def on_rollback(self, file_name):
        self.mod.rollback(file_name)
        self.settings_changed()

    def on_revert_settings(self):
        if self.mod is None:
            return
        from a2widget.a2input_dialog import A2ConfirmDialog

        module_user_cfg = self.mod.get_user_cfg()
        if module_user_cfg:
            dialog = A2ConfirmDialog(
                self,
                'Revert User Settings',
                msg='This will throw away any user changes!',
            )
            dialog.okayed.connect(self._on_revert_settings)
            dialog.show()
        else:
            dialog = A2ConfirmDialog(
                self,
                'Nothing to Revert!',
                msg='Appears everything is on "factory settings"!',
            )
            dialog.show()

    def _on_revert_settings(self):
        self.mod.clear_user_cfg()
        self.mod.change()
        self.load_runtime_and_ui()

    def check_element(self, name):
        """Find a named element and call its `check` method."""
        self.module_view.check_element(name)

    def _restore_splitter(self, win_prefs=None):
        if win_prefs is None:
            win_prefs = self.a2.db.get('windowprefs') or {}
        splitter_size = win_prefs.get('splitter')
        if splitter_size is not None:
            self.ui.splitter.setSizes(splitter_size)

    def _finish_initial_draw(self):
        self._setup_ui()
        # return
        self.module_list.draw_modules(self._init_selection)
        if not self._init_selection:
            self.module_view.draw_mod()
        self._restore_splitter()
        self.setEnabled(True)

        thread = self._run_thread('runtime', RuntimeWatcher)
        thread.change.connect(self.setWindowTitle)

        log.info('A2Window initialised! (%.3fs)', time.process_time())

    def showEvent(self, event):
        """Override Qt showEvent with window initialization."""
        if not self._initial_draw_finished:
            self.setWindowTitle(a2core.NAME)
            self.setWindowIcon(a2ctrl.Icons.a2)
            widget = QtWidgets.QWidget(self)
            layout = QtWidgets.QVBoxLayout(widget)
            label = QtWidgets.QLabel()
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setPixmap(a2ctrl.Icons.a2tinted.pixmap(256))
            layout.addWidget(label)
            self.setCentralWidget(widget)
            self.restore_ui()
            self._initial_draw_finished = True
            QtCore.QTimer(self).singleShot(250, self._finish_initial_draw)
        return super(A2Window, self).showEvent(event)

    def on_uninstall_a2(self):
        a2util.start_process_detached(self.a2.paths.uninstaller)

    def _run_thread(self, name, thread_class, args=None):
        if args is None:
            thread = thread_class(self)
        else:
            thread = thread_class(self, args)
        self._threads[name] = thread
        thread.finished.connect(thread.deleteLater)
        thread.start()
        return thread

    def _set_edit_mode(self, state):
        self.module_list.setEnabled(not state)
        self.ui.menubar.setEnabled(not state)


class RuntimeCallThread(QtCore.QThread):
    def __init__(self, parent, args=None):
        super(RuntimeCallThread, self).__init__(parent)
        self._args = args

    def run(self):
        self.msleep(RESTART_DELAY)

        args = []
        if self._args is None:
            pass
        elif isinstance(self._args, str):
            args.append(self._args)
        elif isinstance(self._args, list):
            args.extend(self._args)
        else:
            raise TypeError('Unable to handle arguments type "%s"' % type(self._args))

        a2 = a2core.A2Obj.inst()
        _retval, _pid = a2util.start_process_detached(a2.paths.a2exe, args, working_dir=a2.paths.a2)


class RuntimeWatcher(QtCore.QThread):
    change = QtCore.Signal(str)

    def __init__(self, parent):
        super(RuntimeWatcher, self).__init__(parent)
        self.is_live = False
        self._lifetime = 0
        self._slept = 0
        self._win_title = None

    def _build_win_title(self, state=None):
        """Update the window title on messages."""
        if state is None:
            self.change.emit(self._win_title)
            return

        if state is True:
            self.change.emit(f'{self._win_title} - {TITLE_ONLINE}')
        else:
            self.change.emit(f'{self._win_title} - {TITLE_OFFLINE}')

    def _build_title_base(self):
        a2 = a2core.A2Obj.inst()
        if os.path.isdir(a2.paths.git):
            import a2ahk

            self._win_title = a2ahk.get_variables(a2.paths.a2_config).get('a2_title', a2core.NAME)
        else:
            self._win_title = a2core.NAME

    def run(self):
        self._build_title_base()
        import a2runtime

        while not self.isInterruptionRequested():
            # take more shorter naps
            if self._slept < RUNTIME_WATCH_INTERVAL:
                self.msleep(50)
                self._slept += 50
                continue
            self._slept = 0

            self.is_live = a2runtime.is_runtime_live()

            if self.is_live:
                self._lifetime += 1
                if self._lifetime < 5:
                    self._build_win_title(True)
                else:
                    self._build_win_title()
            else:
                self._lifetime = 0
                self._build_win_title(False)
