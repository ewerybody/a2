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
        self.setup_ui()
        #self.draw_mod_list()

        # TODO: make this optional
        self.scriptEditor = 'C:/Users/eRiC/io/tools/np++/notepad++.exe'
        self.mod = None
        self.editing = False
        self.edit_clipboard = []
        self.tempConfig = None
        self.selected_mod = []
        self.scopes = {}

        # as we don't want to draw the ui more than once, we make sure
        # selecting does not trigger draw already
        if self.a2.db.get('remember_last') or False:
            last_selected = self.a2.db.get('last_selected') or []
            new_selected = [m for m in last_selected if m in self.a2.modules]
            if len(new_selected) > 0:
                self.mod = self.a2.modules[new_selected[0]]
            # to keep controls from triggering yet
            self._draw_phase = True
            #self.select_mod(new_selected)
            self.selected_mod = new_selected
        self._draw_phase = False
        #self.mod_select(True)
        print('self.selected_mod: %s' % self.selected_mod)

        log.info('initialised!')

        print('self.ui.module_list: %s' % self.ui.module_list.ui.list_widget)

    def setup_ui(self):
        if self.dev_mode:
            a2ctrl.check_ui_module(a2design_ui)
            a2ctrl.check_all_ui()
        a2ctrl.adjustSizes(self.app)

        self.ui = a2design_ui.Ui_a2MainWindow()
        self.ui.setupUi(self)
        self.ui.scrollArea.setFont(a2ctrl.fontL)
        self.ui.scrollBar = self.ui.scrollArea.verticalScrollBar()

        self.mainlayout = self.ui.scrollAreaContents.layout()
        self.controls = []
        self.ui.spacer = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum,
                                           QtGui.QSizePolicy.Expanding)
        self.mainlayout.addItem(self.ui.spacer)
        self.settings_widget = self.ui.scrollAreaContents

        self.ui.modCheck.setVisible(False)
        self.ui.modName.setText('a2')
        self.ui.modVersion.setText('v0.1')
        self.ui.modAuthor.setText('')

        self.ui.modCheck.clicked.connect(self.mod_enable)
        self.ui.modInfoButton.clicked.connect(self.modInfo)
        self.ui.actionEdit_module.triggered.connect(self.editMod)
        self.ui.actionEdit_module.setShortcut("Ctrl+E")
        self.ui.actionDisable_all_modules.triggered.connect(self.modDisableAll)
        self.ui.actionExplore_to.triggered.connect(self.exploreMod)
        self.ui.actionAbout_a2.triggered.connect(partial(a2core.surfTo, self.a2.urls.help))
        self.ui.actionAbout_Autohotkey.triggered.connect(partial(a2core.surfTo, self.a2.urls.ahk))
        self.ui.actionAbout_a2.setIcon(a2ctrl.Icons.inst().a2help)
        self.ui.actionAbout_Autohotkey.setIcon(a2ctrl.Icons.inst().autohotkey)

        self.ui.actionExplore_to_a2_dir.triggered.connect(self.exploreA2)
        self.ui.actionNew_module.triggered.connect(self.newModule)
        self.ui.actionA2_settings.triggered.connect(partial(self.select_mod, None))
        self.ui.actionA2_settings.setIcon(a2ctrl.Icons.inst().a2)
        self.ui.actionDev_settings.triggered.connect(partial(self.select_mod, None))
        self.ui.actionExit_a2.setIcon(a2ctrl.Icons.inst().a2close)
        self.ui.actionExit_a2.triggered.connect(self.close)

        self.ui.actionTest_restorewin.triggered.connect(self._testOutOfScreen)

        self.ui.editOKButton.released.connect(self.editSubmit)
        self.ui.editCancelButton.released.connect(self.drawMod)
        #self.ui.modList.itemSelectionChanged.connect(self.mod_select)

        self.restoreA2ui()

        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape),
                        self, self.escape)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Enter),
                        self, self.editSubmit)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Return),
                        self, self.editSubmit)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S),
                        self, self.editSubmit)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F5), self,
                        partial(self.settings_changed, refresh_ui=True))

        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Home), self.ui.scrollArea,
                        partial(self.scroll_to, True))
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_End), self.ui.scrollArea,
                        partial(self.scroll_to, False))

        self.toggle_dev_menu()
        self.setWindowIcon(a2ctrl.Icons.inst().a2)

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

    def draw_mod_list(self, select=None, refresh=False):
        """
        Fills/refills the left module list with according entries
        TODO: connect with tag selection and search

        :param str select: to select a certain entry, by default re-selects last entry
        """
        self._draw_phase = True

        if refresh:
            self.a2.fetch_modules()

        if select is None:
            select = a2ctrl.qlist.get_selected_as_text(self.ui.modList)
        allMods = sorted(self.a2.modules.keys(), key=lambda s: s.lower())
        self.ui.modList.clear()
        self.ui.modList.insertItems(0, allMods)

        if select:
            self.select_mod(select)

        self._draw_phase = False

        if refresh:
            self.mod_select(force=True)

    def select_mod(self, modName):
        """
        to select 1 or more given modulenames in the list
        and update Ui accordingly
        """
        a2ctrl.qlist.select_items(self.ui.modList, modName)

    def mod_select(self, force=False):
        """
        Updates the module settings view to the right of the UI
        when something different is elected in the module list
        """
        if self._draw_phase:
            return

        sel = self.ui.modList.selectedItems()
        numsel = len(sel)
        self.ui.modCheck.setTristate(False)

        if not numsel:
            self.ui.modCheck.setVisible(False)
            self.mod = None
            self.selected_mod = []
            self.ui.modName.setText('a2')

        elif numsel == 1:
            name = sel[0].text()
            # break if sel == previous sel
            if name in self.selected_mod and len(self.selected_mod) == 1 and force is False:
                return
            self.ui.modCheck.setVisible(True)
            self.ui.modName.setText(name)
            enabled = name in self.a2.enabled
            # weird.. need to set false first to fix tristate effect
            self.ui.modCheck.setChecked(False)
            self.ui.modCheck.setChecked(enabled)

            self.mod = self.a2.modules[name]
            self.selected_mod = [name]

        else:
            names = [s.text() for s in sel]
            self.selected_mod = names
            self.ui.modCheck.setVisible(True)
            self.ui.modName.setText('%i modules' % numsel)
            numenabled = len([n for n in names if n in self.a2.enabled])
            if numenabled == 0:
                self.ui.modCheck.setChecked(False)
            elif numenabled == numsel:
                self.ui.modCheck.setChecked(True)
            else:
                self.ui.modCheck.setTristate(True)
                self.ui.modCheck.setCheckState(QtCore.Qt.PartiallyChecked)

        self.drawMod()

    def drawUI(self, keep_scroll=False):
        """
        takes list of controls and arranges them in the scroll layout

        1. I tried to just create layouts for each module unhook them from the
        scroll layout on demand and hook up another one but Qt is spart so it
        deletes the invisible layout which cannot be hooked up again.
        2. I tried to brute force delete everything and building it over again each
        time something else is seleceted in the left list but Qt refuses to
        delete anything visually with destroy() or removeWidget()
        3. We probably need an actual tab layout to do this but I can't find how to
        make the tabs invisible...
        4. I'll try to create an all new layout,
            fill it and switch away from the old one:
        """
        # to refill the scoll layout:
        # take away the spacer from 'mainLayout'
        self.mainlayout.removeItem(self.ui.spacer)
        # create widget to host the module's new layout
        current_height = self.settings_widget.height()
        new_widget = QtGui.QWidget(self)
        if keep_scroll:
            current_scroll_value = self.ui.scrollBar.value()
            new_widget.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                                       QtGui.QSizePolicy.Fixed))
            new_widget.setMinimumHeight(current_height)

        # create new column layout for the module controls
        newLayout = QtGui.QVBoxLayout(new_widget)
        newLayout.setContentsMargins(5, 5, 5, 5)
        newLayout.setSpacing(a2ctrl.UIValues.spacing)
        # turn scroll layout content to new host widget
        self.ui.scrollArea.setWidget(new_widget)

        # make the new inner layout the mainLayout
        # add the controls to it
        for ctrl in self.controls:
            if ctrl:
                newLayout.addWidget(ctrl)
        # amend the spacer
        newLayout.addItem(self.ui.spacer)

        new_widget.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                                   QtGui.QSizePolicy.Maximum))
        if keep_scroll:
            self.ui.scrollBar.setValue(current_scroll_value)

        self.mainlayout = newLayout
        self.settings_widget = new_widget

    def drawMod(self):
        """
        from the modules config creates the usual display controls and
        fills them with the saved settings from the database.
        On change they trigger writing to the db, collect all include info
        and restart a2.
        """
        self.controls = []

        if self.mod is None:
            self.controls.append(a2ctrl.a2settings.A2Settings(self))
            config = [{'typ': 'nfo', 'author': '', 'version': 'v0.1'}]
        else:
            if len(self.selected_mod) > 1:
                config = [{'typ': 'nfo', 'author': '', 'version': '',
                           'description': 'Multiple modules selected. Here goes some '
                                          'useful info in the future...'}]
            else:
                config = self.mod.config

            self.tempConfig = None

        if len(config):
            if config[0].get('typ') != 'nfo':
                log.error('First element of config is not typ nfo! %s' % self.mod.name)
        else:
            config = [{'typ': 'nfo', 'author': '', 'version': '',
                       'description': 'Module Config is currently empty! imagine awesome layout here ...'}]

        self.ui.modAuthor.setText(config[0].get('author', ''))
        self.ui.modVersion.setText(config[0].get('version', ''))

        for cfg in config:
            self.controls.append(a2ctrl.draw(self, cfg, self.mod))

        self.toggleEdit(False)
        self.drawUI()

    def editMod(self, keep_scroll=False):
        """
        From the modules config creates controls to edit the config itself.
        If a header is not found one will be added to the in-edit config.
        On "OK" the config data is collected from the UI and written back to the json.
        On Cancel the in-edit config is discarded and drawMod called which draws the
        UI unchanged.
        """
        if len(self.selected_mod) != 1 or self.selected_mod[0] == 'a2':
            return

        self.controls = []
        if self.tempConfig is None:
            self.tempConfig = deepcopy(self.mod.config)

        #if not mod.config: is None or mod.config is []
        if not len(self.tempConfig):
            newNfo = {'typ': 'nfo',
                      'description': 'Because none existed before this temporary description was '
                                     'created for "%s". Change it to describe what it does with a '
                                     'couple of words.' % self.mod.name,
                      'author': a2core.get_author(),
                      'version': '0.1',
                      'date': a2core.get_date()}
            self.tempConfig.insert(0, newNfo)

        for cfg in self.tempConfig:
            self.controls.append(a2ctrl.edit(cfg, self, self.tempConfig))

        editSelect = a2ctrl.EditAddElem(self, self.tempConfig)
        self.controls.append(editSelect)

        self.drawUI(keep_scroll)
        self.toggleEdit(True)
        self.settings_widget.setFocus()

    def editSubmit(self):
        """
        Calls the mod to write the tempConfig to disc.
        If it's enabled only trigger settingsChanged when

        """
        if not self.editing:
            return

        self.mod.config = deepcopy(self.tempConfig)
        if self.mod.name in self.a2.db.get('enabled') or []:
            self.mod.change()
            self.settings_changed()
        self.drawMod()

    def toggleEdit(self, state):
        self.editing = state
        for button in [self.ui.editCancelButton, self.ui.editOKButton]:
            button.setEnabled(state)
            button.setMaximumSize(QtCore.QSize(16777215, 50 if state else 0))
            self.ui.editOKCancelWidget.setMaximumSize(QtCore.QSize(16777215, 50 if state else 0))

    def mod_enable(self):
        """
        Handles the module checkbox to enable/disable one or multiple modules
        """
        enabled_mods = self.a2.enabled
        checked = self.ui.modCheck.isChecked()
        if self.ui.modCheck.isTristate() or not checked:
            for mod in self.selected_mod:
                if mod in enabled_mods:
                    enabled_mods.remove(mod)
            checked = False
        else:
            enabled_mods += self.selected_mod
            checked = True

        self.a2.enabled = enabled_mods
        self.ui.modCheck.setTristate(False)
        self.ui.modCheck.setChecked(checked)
        self.settings_changed()

    def modDisableAll(self):
        self.a2.enabled = []
        self.mod_select(force=True)
        self.settings_changed()

    def modInfo(self):
        """
        Open help of the selected module or a2 help
        """
        if len(self.selected_mod) != 1:
            a2core.surfTo(self.a2.urls.help)
        else:
            self.mod.help()

    def settings_changed(self, specific=None, refresh_ui=False):
        if self._restart_thread is not None:
            self._restart_thread.quit()

        # kill old a2 process
        threading.Thread(target=ahk.killA2process).start()
        self.draw_mod_list(refresh=refresh_ui)

        a2core.write_includes(specific)

        self._restart_thread = RestartThread(self.a2, self)
        self._restart_thread.start()

    def escape(self):
        if self.editing:
            self.drawMod()
        else:
            self.close()

    def exploreMod(self):
        if isinstance(self.mod, a2mod.Mod):
            subprocess.Popen(['explorer.exe', self.mod.path])

    def exploreA2(self):
        subprocess.Popen(['explorer.exe', self.a2.paths.a2])

    def closeEvent(self, event):
        binprefs = str(self.saveGeometry().toPercentEncoding())
        self.a2.db.set('windowprefs', {'splitter': self.ui.splitter.sizes(), 'geometry': binprefs})
        self.a2.db.set('last_selected', self.selected_mod)
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
        a2ctrl.InputDialog(self, 'New Module', self.newModuleCreate, self.newModuleCheck,
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

    def newModuleCreate(self, name):
        if not self.newModuleCheck(name):
            return
        if not os.access(self.a2.paths.modules, os.W_OK):
            log.error('A2 module directory not writable! %s' % self.a2.paths.modules)
            return

        os.mkdir(join(self.a2.paths.modules, name))
        self.a2.fetch_modules()
        self.draw_mod_list(select=name)
        self.mod_select(force=True)

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
