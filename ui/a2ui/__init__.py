"""
a2ui - Setup User Interface for an Autohotkey runtime.
"""
import os
import time

import a2uic
import a2dev
import a2core
import a2util
import a2mod
import a2style

import a2widget.tools
import a2ui.module_cfg
from a2qt import QtGui, QtCore, QtWidgets

log = a2core.get_logger(__name__)
RESTART_DELAY = 300
RUNTIME_WATCH_INTERVAL = 1000
DEFAULT_WIN_SIZE = (700, 480)
_TITLE_PREFIX = 'Runtime is'
TITLE_ONLINE = _TITLE_PREFIX + ' Live!'
TITLE_OFFLINE = _TITLE_PREFIX + ' Offline!'


class A2Window(QtWidgets.QMainWindow):
    def __init__(self, app):
        super(A2Window, self).__init__(parent=None)
        self.setEnabled(False)
        self.a2 = a2core.get()
        self.app = app
        self._threads = {}
        self._scroll_anim = None

        self.selected = []
        self.num_selected = 0
        self.mod = None  # type: a2mod.Mod | None
        self.mod_cfg = a2ui.module_cfg.ModuleConfig(self)
        self.mod_cfg.reload_requested.connect(self.load_runtime_and_ui)

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

    def showEvent(self, event):
        """Override Qt showEvent with window initialization."""
        if not self._initial_draw_finished:
            from a2ctrl.icons import Icons

            self.setWindowTitle(a2core.NAME)
            self.setWindowIcon(Icons.a2)
            widget = QtWidgets.QWidget(self)
            layout = QtWidgets.QVBoxLayout(widget)
            label = QtWidgets.QLabel()
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setPixmap(Icons.a2tinted.pixmap(256))
            layout.addWidget(label)
            self.setCentralWidget(widget)
            self.restore_ui()
            self._initial_draw_finished = True
            QtCore.QTimer(self).singleShot(250, self._finish_initial_draw)
        return super(A2Window, self).showEvent(event)

    def _finish_initial_draw(self):
        self._setup_ui()
        # return
        self.module_list.draw_modules(self._init_selection)
        if not self._init_selection:
            self.module_view.draw_mod()
        self._restore_splitter()
        self.setEnabled(True)

        thread = self._run_thread('runtime', WinTitleUpdater)
        thread.change.connect(self.setWindowTitle)

        thread = self._run_thread('UpdatesChecker', UpdatesChecker)
        thread.fetched.connect(self._on_updates)

        log.info('A2Window initialised! (%.3fs)', time.process_time())

    def _setup_ui(self):
        from a2ui import a2design_ui

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
        from a2ctrl.icons import Icons

        def _make_url_action(action: QtGui.QAction, url: str, icon: QtGui.QIcon):
            action.setData(url)
            action.setIcon(icon)
            action.triggered.connect(self._on_url_action)

        self.ui.actionEdit_module.triggered.connect(self.module_view.edit_mod)
        self.ui.actionEdit_module.setIcon(Icons.edit)

        self.ui.actionDisable_all_modules.triggered.connect(self.mod_disable_all)
        self.ui.actionExplore_to.triggered.connect(self.explore_mod)
        self.ui.actionExplore_to.setIcon(Icons.folder)

        _make_url_action(self.ui.actiona2_on_github, self.a2.urls.help, Icons.a2help)
        _make_url_action(self.ui.actionAbout_Autohotkey, self.a2.urls.ahk, Icons.autohotkey)

        self.ui.actionAbout_a2.triggered.connect(self.about)
        self.ui.actionAbout_a2.setIcon(Icons.a2help)

        self.ui.actionExplore_to_a2_dir.triggered.connect(self.explore_a2)
        self.ui.actionExplore_to_a2_dir.setIcon(Icons.folder)
        self.ui.actionExplore_to_a2_data_dir.triggered.connect(self.explore_a2data)
        self.ui.actionExplore_to_a2_data_dir.setIcon(Icons.folder)
        self.ui.actionA2_settings.triggered.connect(self.module_list.select)
        self.ui.actionA2_settings.setIcon(Icons.a2)
        self.ui.actionExit_a2ui.triggered.connect(self.close)
        self.ui.actionExit_a2ui.setIcon(Icons.clear)
        self.ui.actionRefresh_UI.triggered.connect(self.load_runtime_and_ui)

        _make_url_action(self.ui.action_report_bug, self.a2.urls.report_bug, Icons.github)
        _make_url_action(self.ui.action_report_sugg, self.a2.urls.report_sugg, Icons.github)

        self.ui.actionNew_Module_Dialog.triggered.connect(self.create_new_module)
        self.ui.actionNew_Module_Dialog.setIcon(Icons.folder_add)
        self.ui.actionCreate_New_Element.triggered.connect(self.create_new_element)
        self.ui.actionCreate_New_Element.setIcon(Icons.folder_add)
        self.ui.actionBuild_A2_Package.triggered.connect(a2dev.build_package)
        self.ui.actionSet_a2_Version.triggered.connect(a2dev.call_version_bump_dialog)

        self.ui.actionUnload_a2_Runtime.triggered.connect(self.shut_down_runtime)
        self.ui.actionUnload_a2_Runtime.setIcon(Icons.a2x)
        self.ui.actionReload_a2_Runtime.triggered.connect(self.load_runtime_and_ui)
        self.ui.actionReload_a2_Runtime.setIcon(Icons.a2reload)
        self.ui.actionLoad_a2_Runtime.triggered.connect(self.load_runtime_and_ui)
        self.ui.menuMain.aboutToShow.connect(self._set_runtime_actions_vis)

        self.ui.menuDev.aboutToShow.connect(self.on_dev_menu_build)
        self.ui.menuRollback_Changes.aboutToShow.connect(self.mod_cfg.build_rollback_menu)
        self.ui.menuRollback_Changes.setIcon(Icons.rollback)
        self.ui.actionRevert_Settings.triggered.connect(self.mod_cfg.revert)
        self.ui.actionRevert_Settings.setIcon(Icons.rollback)
        self.ui.actionExport_Settings.triggered.connect(self.mod_cfg.export)
        self.ui.actionExport_Settings.setIcon(Icons.up)
        self.ui.actionImport_Settings.triggered.connect(self.mod_cfg.load)
        self.ui.actionImport_Settings.setIcon(Icons.file_download)

        self.ui.menuModule.aboutToShow.connect(self.build_module_menu)

        if os.path.isfile(self.a2.paths.uninstaller):
            self.ui.actionUninstall_a2.setIcon(Icons.a2x)
            self.ui.actionUninstall_a2.triggered.connect(self.on_uninstall_a2)
        else:
            self.ui.actionUninstall_a2.deleteLater()

        self.ui.actionHelp_on_Module.triggered.connect(self.module_view.help)
        self.ui.actionHelp_on_Module.setIcon(Icons.help)

        _make_url_action(self.ui.actionChat_on_Gitter, self.a2.urls.gitter, Icons.gitter)
        _make_url_action(self.ui.actionChat_on_Telegram, self.a2.urls.telegram, Icons.telegram)

        self.ui.actionInspect_UI.triggered.connect(self._inspect_ui)
        self.ui.menuUpdates.menuAction().setVisible(False)

        self.ui.menuHelp.aboutToShow.connect(self._on_help_menu_show)
        _make_url_action(self.ui.action_updates, self.a2.urls.latest_release, Icons.github)
        _make_url_action(self.ui.action_update_a2, self.a2.urls.latest_release, Icons.github)

    def _setup_shortcuts(self):
        Qt = QtCore.Qt
        scroll_area = self.module_view.ui.a2scroll_area

        for keys, parent, func in (
            (Qt.Key_Escape, self, self.escape),
            ('Ctrl+Enter', self, self.edit_submit),
            ('Ctrl+Return', self, self.edit_submit),
            ('Ctrl+S', self, self.edit_submit),
            (Qt.Key_Home, scroll_area, self.scroll_to_start),
            (Qt.Key_End, scroll_area, self.scroll_to_end),
            (Qt.Key_F1, self, self.module_view.help),
        ):
            shortcut = QtGui.QShortcut(parent)
            shortcut.setKey(QtGui.QKeySequence(keys))
            shortcut.activated.connect(func)

    def _restore_splitter(self, win_prefs=None):
        if win_prefs is None:
            win_prefs = self.a2.db.get('windowprefs') or {}
        splitter_size = win_prefs.get('splitter')
        if splitter_size is None:
            splitter_size = (self.width() * 0.25, self.width() * 0.75)
        self.ui.splitter.setSizes(splitter_size)

    def _on_url_action(self):
        action = self.sender()
        if isinstance(action, QtGui.QAction):
            a2util.surf_to(action.data())

    def check_main_menu_bar(self):
        """Handle main menu item visibility."""
        self.ui.menuDev.menuAction().setVisible(self.a2.dev_mode)
        self.ui.menuModule.menuAction().setVisible(self.mod is not None)

    def _module_selected(self, module_list):
        self.selected = module_list
        self.num_selected = len(module_list)
        if self.num_selected == 1:
            self.mod = module_list[0]
        else:
            self.mod = None

        self.check_main_menu_bar()
        self.module_view.draw_mod()

    def edit_submit(self):
        """
        Call module to write `temp_config` to disc.
        If it's enabled only trigger settingsChanged when
        """
        if self.mod is None or not self.module_view.editing:
            return

        if self.module_view.editor.check_issues():
            return

        self.mod.config = self.module_view.editor.get_cfg_copy()
        if self.mod.enabled:
            self.mod.change()
            self.settings_changed()
        self.module_view.draw_mod()

    def mod_enable(self, state: bool):
        """
        Handle module checkbox to enable/disable one or multiple modules.
        :param bool check: Checkbox state incoming from the module view header.
        """
        for mod in self.selected:
            if mod.enabled != state:
                mod.enabled = state
        # self.module_list.set_item_states(self.selected)
        self.module_list.draw_modules()
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
        screen = a2widget.tools.get_screen(geometry)
        geometry.moveCenter(screen.geometry().center())
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
        try:
            if state == QtCore.Qt.WindowMinimized:
                self.setWindowState(QtCore.Qt.WindowActive)
            elif state not in QtCore.Qt.WindowState:
                self.setWindowState(QtCore.Qt.WindowActive)
        except TypeError as error:
            if QtCore.__version_info__ < (6, 4):
                raise TypeError(
                    f'Update PySide! (yours: {QtCore.__version__}, need: 6.4)'
                ) from TypeError

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
                if tries < 15:
                    log.debug(f'Wating for thread: {thread}')
                tries -= 1
                if not tries:
                    log.error(f'Thread NOT stopped: {thread}')
                    break
                time.sleep(0.2)

        QtWidgets.QMainWindow.closeEvent(self, event)

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
        dialog.yielded.connect(self._create_local_source)
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

    def rebuild_css(self, user_scale=None) -> a2style.A2StyleBuilder:
        if user_scale is None:
            user_scale = self.a2.db.get('ui_scale') or 1.0
        else:
            self.a2.db.set('ui_scale', user_scale)

        if self._style is None:
            self._style = a2style.A2StyleBuilder(self.a2.db.get('ui_theme'))

        css_template = self._style.get_style(user_scale)
        self.app.setStyleSheet(css_template)
        return self._style

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
        if not isinstance(menu, QtWidgets.QMenu):
            return

        menu.clear()
        menu.addAction(self.ui.actionHelp_on_Module)
        menu.addAction(self.ui.actionRevert_Settings)
        menu.addAction(self.ui.actionExport_Settings)
        menu.addAction(self.ui.actionImport_Settings)

        if self.module_view.menu_items:
            menu.addSeparator()
            for action in self.module_view.menu_items:
                menu.addAction(action)

    def on_dev_menu_build(self):
        self.ui.menuRollback_Changes.setEnabled(self.mod is not None)

    def check_element(self, name):
        """Find a named element and call its `check` method."""
        self.module_view.check_element(name)

    def on_uninstall_a2(self):
        if os.path.isfile(self.a2.paths.uninstaller):
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

    def _on_updates(self, updates):
        """"""
        versions = updates['core']['a2']
        show_menu = False
        if versions[1:]:
            show_menu = True
            self.ui.action_update_a2.setText(f'Get version {versions[1]} on github.com')
            log.info(
                'TODO: Show a2 updated available msg somehow! (%s -> %s)',
                versions[0],
                versions[1],
            )

        self.ui.action_update_packages.setVisible(False)
        for source_name, versions in updates.get('sources', {}).items():
            if len(versions) != 2:
                continue
            # show_menu = True
            log.info(
                'TODO: mark "%s" with "update available!" (%s -> %s)',
                source_name,
                versions[0],
                versions[1],
            )

        self.ui.menuUpdates.menuAction().setVisible(show_menu)

    def _inspect_ui(self):
        import pyside_inspect

        pyside_inspect.InspectMode(self)

    def about(self):
        from a2ui import about_dialog

        dialog = about_dialog.AboutDialog(self)
        dialog.exec()

    def _on_help_menu_show(self):
        if self.a2.is_git():
            self.ui.action_updates.setText('(Development Version)')
            self.ui.action_updates.setEnabled(False)
            return

        new_version = self.a2.updates['core']['a2'][1:]
        if new_version:
            self.ui.action_updates.setText(f'Get version {new_version[0]} on github.com')
            self.ui.action_updates.setEnabled(True)
        else:
            self.ui.action_updates.setText('a2 is up-to-date')
            self.ui.action_updates.setEnabled(False)


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


class WinTitleUpdater(QtCore.QThread):
    """
    Periodically check for running a2 runtime and send title update message in case of change.
    """

    change = QtCore.Signal(str)

    def __init__(self, parent):
        super().__init__(parent)
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


class UpdatesChecker(QtCore.QThread):
    fetched = QtCore.Signal(dict)
    progress = QtCore.Signal(dict)

    def __init__(self, parent):
        super().__init__(parent)

    def run(self):
        a2 = a2core.get()
        updates = {}
        for updates in a2.check_all_updates():
            if self.isInterruptionRequested():
                return
            self.progress.emit(updates)

        self.fetched.emit(updates)


if __name__ == '__main__':
    a2 = a2core.get()
    a2.start_up()

    updates = {}
    for updates in a2.check_all_updates():
        continue
    print('updates: %s' % updates)
