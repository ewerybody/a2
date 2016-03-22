"""
a2ui - setup interface for an Autohotkey environment.
"""
import os
import logging
import threading
import subprocess

import ahk
import a2mod
import a2core
import a2ctrl
import a2design_ui

from os.path import join
from copy import deepcopy
from functools import partial
from PySide import QtGui, QtCore


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
reload_modules = [a2ctrl]


class A2Window(QtGui.QMainWindow):
    def __init__(self, app=None, *args):
        super(A2Window, self).__init__(parent=None)
        self.a2 = a2core.A2Obj.inst()
        self.app = app

        self.dev_mode = self.a2.db.get('dev_mode') or False
        if self.dev_mode:
            a2ctrl.check_ui_module(a2design_ui)
            a2ctrl.check_all_ui()
        a2ctrl.adjustSizes(app)
        self.setupUi()
        self.draw_mod_list()
        
        # TODO: make this optional
        self.scriptEditor = 'C:/Users/eRiC/io/tools/np++/notepad++.exe'
        self.mod = None
        self.editing = False
        self.edit_clipboard = []
        self.tempConfig = None
        self.selected_mod = []
        self.toggleEdit(False)
        self.scopes = {}

        if self.a2.db.get('remember_last') or False:
            last_selected = self.a2.db.get('last_selected')
            new_selected = [m for m in last_selected if m in self.a2.modules]
            if len(new_selected) == 1:
                self.mod = self.a2.modules[new_selected[0]]
            else:
                self.mod_selected = new_selected
            self.select_mod(new_selected)
        
        self.drawMod()
        log.info('initialised!')

    def setupUi(self):
        self.ui = a2design_ui.Ui_a2MainWindow()
        self.ui.setupUi(self)
        self.ui.scrollArea.setFont(a2ctrl.fontL)
        self.ui.scrollBar = self.ui.scrollArea.verticalScrollBar()

        self.mainlayout = self.ui.scrollAreaContents.layout()
        self.controls = []
        # create a spacer to arrange the layout
        # NOTE that a spacer is added via addItem! not widget
        self.ui.spacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
                                           QtGui.QSizePolicy.Expanding)
        self.mainlayout.addItem(self.ui.spacer)
                
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
        self.ui.actionExplore_to_a2_dir.triggered.connect(self.exploreA2)
        self.ui.actionNew_module.triggered.connect(self.newModule)
        self.ui.actionA2_settings.triggered.connect(partial(self.select_mod, None))
        self.ui.actionDev_settings.triggered.connect(partial(self.select_mod, None))
        
        self.ui.actionTest_restorewin.triggered.connect(self._testOutOfScreen)
        
        self.ui.editOKButton.released.connect(self.editSubmit)
        self.ui.editCancelButton.released.connect(self.drawMod)
        self.ui.modList.itemSelectionChanged.connect(self.mod_select)

        self.restoreA2ui()

        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape),
                        self, self.escape)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Enter),
                        self, self.editSubmit)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Return),
                        self, self.editSubmit)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S),
                        self, self.editSubmit)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F5), self, self.settings_changed)

        self.toggle_dev_menu()
        self.setWindowIcon(QtGui.QIcon("a2.ico"))

    def toggle_dev_menu(self, state=None):
        if state is None:
            state = self.a2.db.get('dev_mode') or False
            # state=None happens only on startup, if True we dont have to re-add
            if state is True:
                return

        if state:
            self.ui.menubar.insertAction(self.ui.menuHelp.menuAction(),
                                         self.ui.menuDev.menuAction())
        else:
            self.ui.menubar.removeAction(self.ui.menuDev.menuAction())

    def draw_mod_list(self, select=None):
        self.__drawing_mod_list = True
        if select is None:
            select = [i.text() for i in self.ui.modList.selectedItems()]
        allMods = sorted(self.a2.modules.keys(), key=lambda s: s.lower())
        self.ui.modList.clear()
        self.ui.modList.insertItems(0, allMods)
        
        if select:
            self.select_mod(select)
        self.__drawing_mod_list = False

    def select_mod(self, modName):
        """
        to select 1 or more given modulenames in the list
        and update Ui accordingly
        """
        a2ctrl.list_selectItems(self.ui.modList, modName)

    def mod_select(self, force=False):
        """
        updates the mod view to the right of the UI
        when something different is elected in the module list
        """
        if self.__drawing_mod_list:
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
        
    def drawUI(self):
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
        newWidget = QtGui.QWidget(self)
        newWidget.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                                  QtGui.QSizePolicy.Maximum))
        # create new column layout for the module controls
        newLayout = QtGui.QVBoxLayout(newWidget)
        
        # turn scroll layout content to new host widget
        self.ui.scrollArea.setWidget(newWidget)
        # make the new inner layout the mainLayout
        # add the controls to it
        for ctrl in self.controls:
            if ctrl:
                newLayout.addWidget(ctrl)
        # amend the spacer
        newLayout.addItem(self.ui.spacer)
        self.mainlayout = newLayout
    
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
            config = [{'typ': 'nfo',
                       'description': 'Hello user! Welcome to a2! This is a template '
                       'introduction Text. So far there is not much to say. I just '
                       'wanted this to fill up more than one line properly. Voila!',
                       'author': '',
                       'version': 'v0.1'}]
        else:
            if len(self.selected_mod) > 1:
                config = [{'typ': 'nfo',
                           'description': 'Multiple modules selected. Here goes some '
                                          'useful info in the future...',
                           'author': '',
                           'version': ''}]
            else:
                config = self.mod.config

            self.tempConfig = None

            author = ''
            version = ''
            if len(config):
                if config[0].get('typ') != 'nfo':
                    log.error('First element of config is not typ nfo! %s' % self.mod.name)
                author = config[0].get('author') or ''
                version = config[0].get('version') or ''
            self.ui.modAuthor.setText(author)
            self.ui.modVersion.setText(version)
            
            if config == []:
                self.controls.append(QtGui.QLabel('config.json currently empty. '
                                                  'imagine awesome layout here ...'))
            else:
                for cfg in config:
                    self.controls.append(a2ctrl.draw(self, cfg, self.mod))
        
        self.toggleEdit(False)
        self.drawUI()
        
    def editMod(self):
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
        
        self.drawUI()
        self.toggleEdit(True)
    
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
    
    def settings_changed(self, specific=None):
        # kill old a2 process
        threading.Thread(target=ahk.killA2process).start()
        a2core.write_includes(specific)
        
        thread = RestartThread(self.a2, self)
        thread.start()
        
        self.draw_mod_list()
    
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

    def showRaise(self):
        self.show()
        self.activateWindow()
        #self.setFocus()

    def _testOutOfScreen(self):
        h = self.app.desktop().height()
        log.debug('h: %s' % h)
        geo = self.geometry()
        geo.setY(geo.x() + h)
        self.setGeometry(geo)
        log.debug('geo: %s' % self.geometry())


class RestartThread(QtCore.QThread):
    def __init__(self, a2, parent):
        super(RestartThread, self).__init__(parent)
        self.msleep(300)
        ahkProcess = QtCore.QProcess()
        ahkProcess.startDetached(a2.paths.autohotkey, [a2.paths.a2_script], a2.paths.a2)


if __name__ == '__main__':
    import a2app
    a2app.main()
