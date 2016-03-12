"""
a2ui - setup interface for an Autohotkey environment.
"""
import os
import time
import logging
import threading
import subprocess
import webbrowser

import ahk
import a2mod
import a2init
import a2ctrl
import a2dblib
import a2design_ui

from copy import deepcopy
from functools import partial
from PySide import QtGui, QtCore
from os.path import exists, join, dirname


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
a2PyModules = [a2dblib, a2ctrl, a2design_ui, a2mod, ahk, a2init]
a2ctrl.checkUiModule(a2design_ui)


class URLs(object):
    a2 = 'https://github.com/ewerybody/a2'
    help = a2 + '#description'
    ahk = 'http://ahkscript.org'
    ahksend = ahk + '/docs/commands/Send.htm'
    helpEditCtrl = a2 + '/wiki/EditCtrls'
    helpHotkey = a2 + '/wiki/Edit-Hotkey-Control'
    helpCheckbox = a2 + '/wiki/Edit-Checkbox-Control'
    helpScopes = a2 + '/wiki/Edit-Scopes'
    ahkWinTitle = ahk + '/docs/misc/WinTitle.htm'
    ahkWinActive = ahk + '/docs/commands/WinActive.htm'


class A2Window(QtGui.QMainWindow):
    def __init__(self, parent=None, app=None, *args):
        super(A2Window, self).__init__(parent)
        self.app = app
        self.urls = URLs()
        
        self.initPaths()
        self.db = a2dblib.A2db(self.dbfile)
        #TODO: remove this:
        self.dbCleanup()
        self.modules = {}
        a2ctrl.adjustSizes(app)
        self.setupUi()
        self.fetchModules()
        self.drawModList()
        
        # TODO: make this optional
        self.scriptEditor = 'C:/Users/eRiC/io/tools/np++/notepad++.exe'
        self.mod = None
        self.enabledMods = self.db.get('enabled') or []
        self.editing = False
        self.edit_clipboard = []
        self.tempConfig = None
        self.selectedMod = []
        self.toggleEdit(False)
        self.scopes = {}
        
        self.drawMod()
        log.info('initialised!')
        self.getUsedScopes()
        self.getUsedHotkeys()

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
        
        self.ui.modCheck.clicked.connect(self.modEnable)
        self.ui.modInfoButton.clicked.connect(self.modInfo)
        self.ui.actionEdit_module.triggered.connect(self.editMod)
        self.ui.actionEdit_module.setShortcut("Ctrl+E")
        self.ui.actionDisable_all_modules.triggered.connect(self.modDisableAll)
        self.ui.actionExplore_to.triggered.connect(self.exploreMod)
        self.ui.actionAbout_a2.triggered.connect(partial(self.surfTo, self.urls.help))
        self.ui.actionAbout_Autohotkey.triggered.connect(partial(self.surfTo, self.urls.ahk))
        self.ui.actionExplore_to_a2_dir.triggered.connect(self.exploreA2)
        self.ui.actionNew_module.triggered.connect(self.newModule)
        
        self.ui.actionTest_restorewin.triggered.connect(self.testOutOfScreen)
        
        self.ui.editOKButton.released.connect(self.editSubmit)
        self.ui.editCancelButton.released.connect(self.drawMod)
        self.ui.modList.itemSelectionChanged.connect(self.modSelect)
                
        self.restoreA2ui()
        
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape),
                        self, self.escape)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Enter),
                        self, self.editSubmit)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Return),
                        self, self.editSubmit)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S),
                        self, self.editSubmit)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F5), self, self.settingsChanged)

        self.toggle_dev_menu()
        self.setWindowIcon(QtGui.QIcon("a2.ico"))
    
    def toggle_dev_menu(self, state=None):
        if state is None:
            state = self.db.get('dev_mode') or False
            # None happens only on startup, if True we dont have to re-add
            if state is True:
                return

        if state:
            self.ui.menubar.insertAction(self.ui.menuHelp.menuAction(),
                                         self.ui.menuDev.menuAction())
        else:
            self.ui.menubar.removeAction(self.ui.menuDev.menuAction())
    
    
    def drawModList(self, select=None):
        if select is None:
            select = [i.text() for i in self.ui.modList.selectedItems()]
        allMods = sorted(self.modules.keys(), key=lambda s: s.lower())
        self.ui.modList.clear()
        self.ui.modList.insertItems(0, allMods)
        
        if select:
            self.selectMod(select)
    
    def selectMod(self, modName):
        """
        to select 1 or more given modulenames in the list
        and update Ui accordingly
        """
        a2ctrl.list_selectItems(self.ui.modList, modName)
    
    def modSelect(self, force=False):
        """
        updates the mod view to the right of the UI
        when something different is elected in the module list
        """
        sel = self.ui.modList.selectedItems()
        numsel = len(sel)
        self.ui.modCheck.setTristate(False)
        enabledMods = self.db.get('enabled') or []
        
        if not numsel:
            self.ui.modCheck.setVisible(False)
            self.mod = None
            self.selectedMod = []
            self.ui.modName.setText('a2')
        
        elif numsel == 1:
            name = sel[0].text()
            # break if sel == previous sel
            if name in self.selectedMod and len(self.selectedMod) == 1 and force is False:
                return
            self.ui.modCheck.setVisible(True)
            self.ui.modName.setText(name)
            enabled = name in enabledMods
            # weird.. need to set false first to fix tristate effect
            self.ui.modCheck.setChecked(False)
            self.ui.modCheck.setChecked(enabled)
            
            self.mod = self.modules[name]
            self.selectedMod = [name]
        
        else:
            names = [s.text() for s in sel]
            self.selectedMod = names
            self.ui.modCheck.setVisible(True)
            self.ui.modName.setText('%i modules' % numsel)
            numenabled = len([n for n in names if n in enabledMods])
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
            if len(self.selectedMod) > 1:
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
                    self.controls.append(a2ctrl.draw(cfg, self.mod))
        
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
        if len(self.selectedMod) != 1 or self.selectedMod[0] == 'a2':
            return

        self.controls = []
        if self.tempConfig is None:
            self.tempConfig = deepcopy(self.mod.config)
        
        #if not mod.config: is None or mod.config is []
        if not len(self.tempConfig):
            s = 'Because none existed before this temporary description was created for "%s". '\
                'Change it to describe what it does with a couple of words.' % self.mod.name
            newNfo = {'typ': 'nfo',
                      'description': s,
                      #'display name': '%s' % mod.name,
                      'author': self.getAuthor(),
                      'version': '0.1',
                      'date': self.getDate()}
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
        if self.mod.name in self.db.get('enabled') or []:
            self.mod.change()
            self.settingsChanged()
        self.drawMod()
    
    def toggleEdit(self, state):
        self.editing = state
        for button in [self.ui.editCancelButton, self.ui.editOKButton]:
            button.setEnabled(state)
            button.setMaximumSize(QtCore.QSize(16777215, 50 if state else 0))
            self.ui.editOKCancelWidget.setMaximumSize(QtCore.QSize(16777215, 50 if state else 0))
    
    def modEnable(self):
        enabledMods = self.db.get('enabled') or []
        
        checked = self.ui.modCheck.isChecked()
        if self.ui.modCheck.isTristate() or not checked:
            for mod in self.selectedMod:
                if mod in enabledMods:
                    enabledMods.remove(mod)
            checked = False
        else:
            enabledMods += self.selectedMod
            checked = True

        self.db.set('enabled', enabledMods)
        self.ui.modCheck.setTristate(False)
        self.ui.modCheck.setChecked(checked)
        self.settingsChanged()
    
    def modDisableAll(self):
        self.db.set('enabled', '')
        self.modSelect(force=True)
        self.settingsChanged()
    
    def modInfo(self):
        """
        Open help of the selected module or a2 help
        """
        if len(self.selectedMod) != 1:
            self.surfTo(self.urls.help)
        else:
            self.mod.help()
    
    def settingsChanged(self):
        # kill old a2 process
        threading.Thread(target=ahk.killA2process).start()
        
        self.fetchModules()
        
        editDisclaimer = ("; a2 %s.ahk - Don't bother editing! - "
                          "File is generated automatically!")
        hkmode = {'1': '#IfWinActive,', '2': '#IfWinNotActive,'}
        
        includeAhk = [editDisclaimer % 'includes']
        hotkeysAhk = {hkmode['1']: ['#+a::a2UI()']}
        variablesAhk = [editDisclaimer % 'variables']
        # TODO: this needs to be implemented dynamically
        libsAhk = [editDisclaimer % 'libs'] + ['#include lib/%s.ahk' % lib for lib in
                                               ['tt', 'functions', 'Explorer_Get']]
        
        # browse the enabled modules to collect the include data
        modSettings = self.db.tables()
        for modname in self.db.get('enabled') or []:
            if modname not in modSettings:
                self.modules[modname].change()
            
            includes = self.db.get('includes', modname)
            
            if not isinstance(includes, list):
                log.warn('includes not a list: %s' % includes)
                includes = [includes]
            
            includeAhk += ['#include modules\%s\%s'
                           % (modname, i) for i in includes]
            
            hotkeys = self.db.get('hotkeys', modname)
            for typ in hotkeys:
                for hk in hotkeys.get(typ) or []:
                    # type 0 is global, append under the #IfWinActive label
                    if typ == '0':
                        hkstring = ahk.translateHotkey(hk[0]) + '::' + hk[1]
                        hotkeysAhk[hkmode['1']].append(hkstring)
                    # assemble type 1 and 2 in hotkeysAhks keys with the hotkey strings listed
                    else:
                        hkstring = ahk.translateHotkey(hk[1]) + '::' + hk[2]
                        for scopeStr in hk[0]:
                            scopeKey = '%s %s' % (hkmode[typ], scopeStr)
                            if scopeKey not in hotkeysAhk:
                                hotkeysAhk[scopeKey] = []
                            hotkeysAhk[scopeKey].append(hkstring)
        
            for var_name, value in (self.db.get('variables', modname) or {}).items():
                if isinstance(value, bool):
                    variablesAhk.append('%s := %s' % (var_name, str(value).lower()))
                elif isinstance(value, str):
                    variablesAhk.append('%s := "%s"' % (var_name, value))
                else:
                    log.error('Please check handling variable type "%s" (%s: %s)'
                              % (type(value), var_name, str(value)))
                    variablesAhk.append('%s := %s' % (var_name, str(value)))
        
        # write all the include files
        with open(join(self.a2setdir, 'variables.ahk'), 'w') as fobj:
            fobj.write('\n'.join(variablesAhk))
        
        with open(join(self.a2setdir, 'libs.ahk'), 'w') as fobj:
            fobj.write('\n'.join(libsAhk))
        
        with open(join(self.a2setdir, 'includes.ahk'), 'w') as fobj:
            fobj.write('\n'.join(includeAhk))
        
        with open(join(self.a2setdir, 'hotkeys.ahk'), 'w') as fobj:
            fobj.write(editDisclaimer % 'hotkeys' + '\n')
            for key in sorted(hotkeysAhk.keys()):
                fobj.write('\n'.join([key] + hotkeysAhk[key]) + '\n\n')
        
        with open(join(self.a2setdir, 'init.ahk'), 'w') as fobj:
            fobj.write(editDisclaimer % 'init' + '\n')
        
        thread = RestartThread(self)
        thread.start()

        self.drawModList()
    
    def fetchModules(self):
        moddirs = os.listdir(self.a2moddir)
        # get rid of modules gone
        [self.modules.pop(m) for m in self.modules if m not in moddirs]
        # register new modules
        for modname in os.listdir(self.a2moddir):
            if modname not in self.modules:
                self.modules[modname] = a2mod.Mod(modname, self)
        return self.modules

    def initPaths(self):
        """
        makes sure all necessary paths and their variables are available.
        """
        self.a2uidir = dirname(__file__)
        if not self.a2uidir:
            cwd = os.getcwd()
            if exists(join(cwd, 'a2ui.py')):
                self.a2uidir = cwd
                log.info('fetched a2ui dir from cwd... %s' % cwd)
            else:
                raise Exception('a2ui start interrupted! '
                                'Could not get main Ui dir!')

        self.a2dir = dirname(self.a2uidir)
        self.a2libdir = join(self.a2dir, 'lib')
        self.a2exe = join(self.a2dir, 'a2Starter.exe')
        self.a2ahk = join(self.a2dir, 'a2.ahk')
        self.a2setdir = self.getSettingsDir()
        self.a2moddir = join(self.a2dir, 'modules')
        # test if all necessary directories are present:
        mainItems = [self.a2ahk, self.a2exe, self.a2libdir, self.a2moddir,
                     self.a2setdir, self.a2uidir]
        missing = [p for p in mainItems if not exists(p)]
        if missing:
            raise Exception('a2ui start interrupted! %s not found in main dir!'
                            % missing)
        if not os.access(self.a2setdir, os.W_OK):
            raise Exception('a2ui start interrupted! %s inaccessable!'
                            % self.a2setdir)
    
        # by default the Autohotkey.exe in the lib should be uses
        # but we need an option for that a user can put it to whatever he wants
        self.ahkexe = join(self.a2libdir, 'AutoHotkey', 'AutoHotkey.exe')
        self.dbfile = join(self.a2setdir, 'a2.db')
    
    def escape(self):
        if self.editing:
            self.drawMod()
        else:
            self.close()
    
    def exploreMod(self):
        if isinstance(self.mod, a2mod.Mod):
            subprocess.Popen(['explorer.exe', self.mod.path])

    def exploreA2(self):
        subprocess.Popen(['explorer.exe', self.a2dir])
    
    def getSettingsDir(self):
        """ TODO: temporary under a2dir!! has to be VARIABLE! """
        return join(self.a2dir, 'settings')

    def getAuthor(self):
        return self.db.get('devAuthor') or os.getenv('USERNAME')

    def getDate(self):
        now = time.localtime()
        return '%i %i %i' % (now.tm_year, now.tm_mon, now.tm_mday)

    def closeEvent(self, event):
        binprefs = str(self.saveGeometry().toPercentEncoding())
        self.db.set('windowprefs', {'splitter': self.ui.splitter.sizes(), 'geometry': binprefs})
        QtGui.QMainWindow.closeEvent(self, event)

    def restoreA2ui(self):
        """
        gets window settings from prefs and makes sure the window will be visible
        I let Qt handle that via restoreGeometry. Downside is: It does not put back windows
        that are partiall outside of the left,right and bottom desktop border
        """
        winprefs = self.db.get('windowprefs') or {}
        geometry = winprefs.get('geometry')
        if geometry is not None:
            geometry = QtCore.QByteArray().fromPercentEncoding(geometry)
            self.restoreGeometry(geometry)
        splitterSize = winprefs.get('splitter')
        if splitterSize is not None:
            self.ui.splitter.setSizes(winprefs['splitter'])

    def surfTo(self, url):
        if url:
            webbrowser.get().open(url)

    def dbCleanup(self):
        for table in self.db.tables():
            if table == 'a2':
                self.db.pop('aValue')
                enabled = self.db.get('enabled', asjson=False)
                if not enabled.startswith('["'):
                    enabled = enabled.split('|')
                    self.db.set('enabled', enabled)
                continue
            
            includes = self.db.get('includes', table, asjson=False)
            include = self.db.get('include', table, asjson=False)
            
            # turn string separated entries into lists
            if includes is None and include is not None:
                includes = include.split('|')
            elif includes is not None and not includes.startswith('['):
                includes = includes.split('|')
            elif includes == '[""]':
                includes = []

            if isinstance(includes, list):
                self.db.set('includes', includes, table)

            if include is not None:
                self.db.pop('include', table)

    def testOutOfScreen(self):
        h = self.app.desktop().height()
        log.debug('h: %s' % h)
        geo = self.geometry()
        geo.setY(geo.x() + h)
        self.setGeometry(geo)
        log.debug('geo: %s' % self.geometry())

    def getUsedScopes(self):
        """
        browses the hotkey setups of enabled modules for scope strings
        TODO: this type of lookup can also be used to get hold of used hotkeys...
        """
        self.scopes = {}
        for modname in self.db.get('enabled'):
            hotkeys = self.db.get('hotkeys', modname)
            if not hotkeys:
                continue
            for i in ['1', '2']:
                for hksetup in hotkeys.get(i) or []:
                    for scope in hksetup[0]:
                        if scope not in self.scopes:
                            self.scopes[scope] = set([modname])
                        else:
                            self.scopes[scope].add(modname)
        return self.scopes

    def getUsedHotkeys(self):
        """
        wip - for a proper hotkey list we might need more than a list. You'd also wanna
        know what the hotkey does... shouldn't our data structure care for this right away?
        """
        self.hotkeys = set()
        for modname in self.db.get('enabled'):
            hotkeys = self.db.get('hotkeys', modname)
            if not hotkeys:
                continue
            for i in ['1', '2']:
                for hksetup in hotkeys.get(i) or []:
                    self.hotkeys.add(hksetup[1])
            for hksetup in hotkeys.get('0') or []:
                self.hotkeys.add(hksetup[0])
        return self.hotkeys

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
        if name.lower() in [m.lower() for m in self.modules]:
            return 'Module name "%s" is already in use!' % name
        return True

    def newModuleCreate(self, name):
        if not self.newModuleCheck(name):
            return
        if not os.access(self.a2moddir, os.W_OK):
            log.error('A2 module directory not writable! %s' % self.a2moddir)
            return
        
        os.mkdir(join(self.a2moddir, name))
        self.fetchModules()
        self.drawModList(select=name)

    def showRaise(self):
        self.show()
        self.activateWindow()
        #self.setFocus()


class RestartThread(QtCore.QThread):
    def __init__(self, parent):
        super(RestartThread, self).__init__(parent)
        self.msleep(300)
        ahkProcess = QtCore.QProcess()
        ahkProcess.startDetached(parent.ahkexe, [parent.a2ahk], parent.a2dir)


if __name__ == '__main__':
    import a2app
    a2app.main()
