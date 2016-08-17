"""
a2ui - setup interface for an Autohotkey environment.
"""
import os
import time
import logging
import threading
import subprocess

import ahk
import a2mod
import a2core
import a2ctrl
import a2ctrl.qlist
import a2design_ui

from copy import deepcopy
from functools import partial
from os.path import join
from PySide import QtGui, QtCore


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
reload_modules = [a2ctrl]


class A2Window(QtGui.QMainWindow):
    # to be triggered whenever a module or module source is dis/enabled
    module_enabled = QtCore.Signal()

    def __init__(self, app=None, *args):
        super(A2Window, self).__init__(parent=None)
        self.a2 = a2core.A2Obj.inst()
        self.app = app
        self._restart_thread = None

        self.dev_mode = self.a2.db.get('dev_mode') or False
        self._setup_ui()

        self.ui.module_list.draw_modules()
        self.ui.module_list.selection_changed.connect(self.module_selected)

        # TODO: make this optional
        self.scriptEditor = 'C:/Users/eRiC/io/tools/np++/notepad++.exe'
        self.edit_clipboard = []
        self.tempConfig = None
        self.selected = []
        self.mod = None
        self.scopes = {}

        init_selection = []
        if self.a2.db.get('remember_last') or False:
            init_selection = self.a2.db.get('last_selected') or []
        self.ui.module_list.select(init_selection)

        log.info('initialised!')

    def module_selected(self, module_list):
        self.selected = module_list
        self.num_selected = len(module_list)
        if self.num_selected == 1:
            self.mod = module_list[0]
        else:
            self.mod = None
        self.ui.module_view.draw_mod()

    def _setup_ui(self):
        if self.dev_mode:
            a2ctrl.check_ui_module(a2design_ui)
            a2ctrl.check_all_ui()
        a2ctrl.adjustSizes(self.app)

        self.ui = a2design_ui.Ui_a2MainWindow()
        self.ui.setupUi(self)

        self.ui.module_view.setup_ui(self)

        self._setup_actions()
        self._setup_shortcuts()

        self.toggle_dev_menu()
        self.setWindowIcon(a2ctrl.Icons.inst().a2)

    def _setup_actions(self):
        self.ui.actionEdit_module.triggered.connect(self.edit_mod)
        self.ui.actionEdit_module.setShortcut("Ctrl+E")
        self.ui.actionDisable_all_modules.triggered.connect(self.modDisableAll)
        self.ui.actionExplore_to.triggered.connect(self.explore_mod)
        self.ui.actionAbout_a2.triggered.connect(partial(a2core.surfTo, self.a2.urls.help))
        self.ui.actionAbout_Autohotkey.triggered.connect(partial(a2core.surfTo, self.a2.urls.ahk))
        self.ui.actionAbout_a2.setIcon(a2ctrl.Icons.inst().a2help)
        self.ui.actionAbout_Autohotkey.setIcon(a2ctrl.Icons.inst().autohotkey)

        self.ui.actionExplore_to_a2_dir.triggered.connect(self.explore_a2)
        self.ui.actionNew_module.triggered.connect(self.newModule)
        self.ui.actionA2_settings.triggered.connect(partial(self.ui.module_list.select, None))
        self.ui.actionA2_settings.setIcon(a2ctrl.Icons.inst().a2)
        self.ui.actionDev_settings.triggered.connect(partial(self.ui.module_list.select, None))
        self.ui.actionExit_a2.setIcon(a2ctrl.Icons.inst().a2close)
        self.ui.actionExit_a2.triggered.connect(self.close)

        self.ui.actionTest_restorewin.triggered.connect(self._testOutOfScreen)
        self.restoreA2ui()

    def _setup_shortcuts(self):
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape),
                        self, self.escape)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Enter),
                        self, self.edit_submit)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Return),
                        self, self.edit_submit)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S),
                        self, self.edit_submit)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F5), self,
                        partial(self.settings_changed, refresh_ui=True))

        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Home), self.ui.module_view.ui.scrollArea,
                        partial(self.scroll_to, True))
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_End), self.ui.module_view.ui.scrollArea,
                        partial(self.scroll_to, False))

    def edit_mod(self):
        if len(self.selected) == 1:
            self.ui.module_view.edit_mod()

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
        if not self.ui.module_view.editing:
            return

        self.mod.config = deepcopy(self.tempConfig)
        if self.mod.name in self.a2.db.get('enabled') or []:
            self.mod.change()
            self.settings_changed()
        self.drawMod()

    def mod_enable(self, checked=None):
        """
        Handles the module checkbox to enable/disable one or multiple modules
        """
        check_box = self.ui.module_view.ui.modCheck
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

    def modDisableAll(self):
        self.a2.enabled = []
        self.mod_select(force=True)
        self.settings_changed()

    def settings_changed(self, specific=None, refresh_ui=False):
        if self._restart_thread is not None:
            self._restart_thread.quit()

        # kill old a2 process
        threading.Thread(target=ahk.killA2process).start()
        self.ui.module_list.draw_modules()

        a2core.write_includes(specific)

        self._restart_thread = RestartThread(self.a2, self)
        self._restart_thread.start()

    def escape(self):
        if self.ui.module_view.editing:
            self.ui.module_view.draw_mod()
        else:
            self.close()

    def explore_mod(self):
        if len(self.selected) == 1:
            subprocess.Popen(['explorer.exe', self.selected[0].path])

    def explore_a2(self):
        subprocess.Popen(['explorer.exe', self.a2.paths.a2])

    def closeEvent(self, event):
        binprefs = str(self.saveGeometry().toPercentEncoding())
        self.a2.db.set('windowprefs', {'splitter': self.ui.splitter.sizes(), 'geometry': binprefs})
        self.a2.db.set('last_selected', [m.key for m in self.selected])
        if self._restart_thread is not None:
            self._restart_thread.quit()
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

    def newModule(self):
        # TODO: Move new module functionality to a2mod
        a2ctrl.InputDialog(self, 'New Module', self.new_module_create, self.newModuleCheck,
                           msg='Name the new module:', text='newModule')

    def newModuleCheck(self, name):
        """
        Run on keystroke when creating new module, to give way to okaying the module creation
        """
        if name == '':
            return 'Name cannot be empty!'
        if name == 'a2':
            return 'You just cannot name your module "a2"! Ok?'
        if name.lower() in [m.lower() for m in self.a2.modules]:
            return 'Module name "%s" is already in use!' % name
        if any([(l in a2core.string.whitespace) for l in name]):
            return 'Name cannot have whitespace! Use _ or - insead!'
        if not all([(l in a2core.ALLOWED_CHARS) for l in name]):
            return 'Name can only have letters, digits, _ and -'
        if not any([(l in a2core.string.ascii_letters) for l in name]):
            return 'Come one have at least 1 letter in the name!'
        return True

    def new_module_create(self, name):
        raise NotImplementedError('TBD!')
#        if not self.newModuleCheck(name):
#            return
#        if not os.access(self.a2.paths.modules, os.W_OK):
#            log.error('A2 module directory not writable! %s' % self.a2.paths.modules)
#            return
#
#        os.mkdir(join(self.a2.paths.modules, name))
#        self.a2.fetch_modules()
#        self.draw_mod_list(select=name)
#        self.mod_select(force=True)

    def showRaise(self):
        self.show()
        self.activateWindow()
        #self.setFocus()

    def scroll_to(self, value, smooth=False):
        if self.ui.modList.hasFocus():
            if isinstance(value, bool):
                a2ctrl.qlist.deselect_all(self.ui.modList)
                if value:
                    item = self.ui.modList.item(0)
                else:
                    item = self.ui.modList.item(self.ui.modList.count() - 1)
                item.setSelected(True)
                self.ui.modList.setCurrentItem(item)
                self.ui.modList.scrollToItem(item)
        else:
            #print('self.ui.scrollArea.hasFocus(): %s' % self.ui.scrollArea.hasFocus())
            current = self.ui.scrollBar.value()
            scroll_end = self.ui.scrollBar.maximum()
            if isinstance(value, bool):
                value = 0 if value else self.ui.scrollBar.maximum()

            if value == current or scroll_end == 0:
                return

            if not smooth:
                self.ui.scrollBar.setValue(value)
            else:
                pass
    #             tmax = 0.3
    #             curve = QtCore.QEasingCurve(QtCore.QEasingCurve.OutQuad)
    #             res = 0.01
    #             steps = tmax / res
    #             tsteps = 1 / steps
    #             t = 0.0
    #
    #             rng = value - current
    #             while t <= 1.0:
    #                 time.sleep(res)
    #                 t += tsteps
    #                 v = curve.valueForProgress(t)
    #                 scrollval = current + (v * rng)
    #                 self.ui.scrollBar.setValue(scrollval)

    def _testOutOfScreen(self):
        h = self.app.desktop().height()
        log.debug('h: %s' % h)
        geo = self.geometry()
        geo.setY(geo.x() + h)
        self.setGeometry(geo)
        log.debug('geo: %s' % self.geometry())


class RestartThread(QtCore.QThread):
    def __init__(self, a2, parent):
        self.a2 = a2
        super(RestartThread, self).__init__(parent)

    def run(self, *args, **kwargs):
        self.msleep(300)
        ahkProcess = QtCore.QProcess()
        ahkProcess.startDetached(self.a2.paths.autohotkey, [self.a2.paths.a2_script], self.a2.paths.a2)
        return QtCore.QThread.run(self, *args, **kwargs)


if __name__ == '__main__':
    import a2app
    a2app.main()
