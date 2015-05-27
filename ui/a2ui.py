# a2ui
from PySide import QtGui, QtCore
import os
from os.path import exists, join, splitext, dirname
#from functools import partial
import sys
import a2dblib
import a2ctrl
import json
from datetime import datetime
from a2design_ui import Ui_a2MainWindow

import subprocess
import logging
from copy import deepcopy
logging.basicConfig()
log = logging.getLogger('a2ui')
log.setLevel(logging.DEBUG)

# maybe make this even settable in a dev options dialog?
jsonIndent = 2


class A2Window(QtGui.QMainWindow):
    def __init__(self, parent=None, *args):
        super(A2Window, self).__init__(parent)
        self.ui = Ui_a2MainWindow()
        self.ui.setupUi(self)

        self.initPaths()
        self.dbfile = join(self.a2setdir, 'a2.db')
        self.db = a2dblib.A2db(self.dbfile)

        # TODO: make this optional
        self.scriptEditor = 'C:/Users/eRiC/io/tools/np++/notepad++.exe'
        
        self.mod = None
        self.enabledMods = self.db.gets('enabled')
        self.editing = False

        self.mainlayout = self.ui.scrollAreaContents.layout()
        self.controls = [self.ui.welcomeText]
        self.ctrlDump = []
        self.tempConfig = None
        # create a spacer to arrange the layout
        # NOTE that a spacer is added via addItem! not widget
        self.ui.spacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
                                           QtGui.QSizePolicy.Expanding)
        self.mainlayout.addItem(self.ui.spacer)

        self.fetchModules()
        self.ui.modList.insertItems(0, list(sorted(self.modules.keys())))
        self.ui.modList.itemSelectionChanged.connect(self.modSelect)
        self.selectedMod = None
        
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
        
        self.toggleEdit(False)
        self.ui.editOKButton.pressed.connect(self.editSubmit)
        self.ui.editCancelButton.pressed.connect(self.drawMod)
        
        #TODO: fck reg! do that with the sql db dumbass!
        self.settings = QtCore.QSettings("a2", "a2ui")
        self.restoreA2ui()
    
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape),
                        self, self.escape)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Enter),
                        self, self.editSubmit)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Return),
                        self, self.editSubmit)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("_dump/a2logo 16.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        
        log.info('a2ui initialised!')
    
    def modSelect(self, force=False):
        """
        updates the mod view to the right of the UI
        when something different is elected in the module list
        """
        sel = self.ui.modList.selectedItems()
        numsel = len(sel)
        self.ui.modCheck.setTristate(False)
        if not numsel:
            self.ui.modCheck.setVisible(False)
            self.mod = None
            self.selectedMod = 'a2'
            self.ui.modName.setText('a2')
        
        elif numsel == 1:
            name = sel[0].text()
            if name == self.selectedMod and force is False:
                return
            self.ui.modCheck.setVisible(True)
            self.ui.modName.setText(name)
            self.ui.modCheck.setChecked(name in self.db.gets('enabled'))
            
            self.mod = self.modules[name]
            self.selectedMod = name
        
        else:
            names = [s.text() for s in sel]
            self.selectedMod = names
            log.debug('names: %s' % names)
            self.ui.modCheck.setVisible(True)
            self.ui.modName.setText('%i modules' % numsel)
            numenabled = len([n for n in names if n in self.db.gets('enabled')])
            if numenabled == 0:
                self.ui.modCheck.setChecked(False)
            if numenabled == numsel:
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
        newLayout = QtGui.QWidget(self)
        # create new columnLayout for the module controls
        newInner = QtGui.QVBoxLayout(newLayout)
        
        # turn scroll layout content to new host widget
        self.ui.scrollArea.setWidget(newLayout)
        # make the new inner layout the mainLayout
        # add the controls to it
        for ctrl in self.controls:
            if ctrl:
                newInner.addWidget(ctrl)
        # amend the spacer
        newInner.addItem(self.ui.spacer)
        self.mainlayout = newInner
    
    def drawMod(self):
        """
        from the modules config creates the usual display controls and
        fills them with the saved settings from the database.
        On change they trigger writing to the db, collect all include info
        and restart a2.
        """
        if self.mod is None:
            config = [{'typ': 'nfo',
                      'description': 'Hello user! Welcome to a2! This is a template '
                      'introduction Text. So far there is not much to say. I just '
                      'wanted this to fill up more than one line properly. Voila!',
                      'author': '',
                      'version': 'v0.1'}]
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
        self.controls = []
        
        if config == []:
            self.controls.append(QtGui.QLabel('config.json currently empty. '
                                              'imagine awesome layout here ...'))
        else:
            for element in config:
                self.controls.append(a2ctrl.draw(element))
        
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
        if self.mod is None:
            return
        
        log.debug('editing: %s' % self.mod.name)
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
        
        for element in self.tempConfig:
            self.controls.append(a2ctrl.edit(element, self.mod, self))
        
        editSelect = a2ctrl.EditAddElem(self.mod, self.tempConfig, self.editMod)
        self.controls.append(editSelect)
        
        self.drawUI()
        self.toggleEdit(True)
    
    def editSubmit(self):
        """
        loop the given ctrlDict, query ctrls and feed target mod.config
        """
        if not self.editing:
            return
        
        newcfg = []
        for ctrl in self.controls:
            if hasattr(ctrl, 'getCfg'):
                newcfg.append(ctrl.getCfg())
        
        self.mod.config = newcfg
        self.settingsChanged()
        self.drawMod()
    
    def toggleEdit(self, state):
        self.editing = state
        for button in [self.ui.editCancelButton, self.ui.editOKButton]:
            button.setEnabled(state)
            button.setMaximumSize(QtCore.QSize(16777215, 50 if state else 0))
            self.ui.editOKCancelLayout.setContentsMargins(-1, -1, -1, 5 if state else 0)
    
    def modEnable(self):
        if self.ui.modCheck.isChecked():
            log.debug('enabling: %s ...' % self.selectedMod)
            self.mod.enable()
            self.db.adds('enabled', self.selectedMod)
        else:
            log.debug('disabling: %s ...' % self.selectedMod)
            self.db.dels('enabled', self.selectedMod)
        
        self.settingsChanged()
    
    def modDisableAll(self):
        self.db.set('enabled', '')
        self.modSelect(force=True)
        self.settingsChanged()
    
    def modInfo(self):
        log.debug('calling info on: %s ...' % self.selectedMod)
    
    def settingsChanged(self):
        includeAhk = ["; a2 include.ahk - Don't bother editing! - File is generated automatically!"]
        for modname in self.db.gets('enabled'):
            includes = self.db.gets('include', modname)
            includeAhk += ['#include modules\%s\%s' % (modname, i) for i in includes]
            #log.debug('includes %s: %s' % (e, includes))
            #for c in self.modules[e].config:
            #    if c['typ'] == 'include':
            #        log.info('enabled mod %s file to include: %s' % (e, c['file']))
        log.debug('includeAhk:\n%s' % includeAhk)
        #if os.access(os.W_OK)
        with open(join(self.a2setdir, 'includes.ahk'), 'w') as fobj:
            fobj.write('\n'.join(includeAhk))
        #print('mod: %s' % self.mod.name)
        subprocess.Popen([self.ahkexe, self.a2ahk], cwd=self.a2dir)
    
    def fetchModules(self):
        self.modules = {}
        for modname in os.listdir(self.a2moddir):
            self.modules[modname] = Mod(modname, self)

    def initPaths(self):
        """ makes sure all necessary paths and their variables are available """
        # if run on its own sys.path[0] will be the script dir
        self.a2uidir = sys.path[0]
        if not self.a2uidir:
            #self.a2uidir = 'C:/My Files/code/a2/ui'
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
    
    def escape(self):
        if self.editing:
            self.drawMod()
        else:
            self.close()
    
    def exploreMod(self):
        if isinstance(self.mod, Mod):
            subprocess.Popen(['explorer.exe', self.mod.path])
    
    def getSettingsDir(self):
        """ TODO: temporary under a2dir!! has to be VARIABLE! """
        return join(self.a2dir, 'settings')

    def getAuthor(self):
        return self.db.get('devAuthor') or os.getenv('USERNAME')

    def getDate(self):
        today = datetime.today()
        return '%i %i %i' % (today.year, today.month, today.day)

    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("splitterPos", self.ui.splitter.sizes())
        QtGui.QMainWindow.closeEvent(self, event)

    def restoreA2ui(self):
        #self.setGeometry(QtCore.QRect(250, 250, 1268, 786))
        self.restoreGeometry(self.settings.value("geometry"))
        sizes = self.settings.value("splitterPos")
        if not isinstance(sizes, list):
            sizes = [200, 200]
        else:
            sizes = [int(sizes[0]), int(sizes[1])]
        self.ui.splitter.setSizes(sizes)


class Mod(object):
    """
    WIP! A ui wrapper for an a2 module
    The ui creates such a Mod instance when dealing with it
    from this it gets all information that it displays (hotkey interface,
    buttons, sliders, checkboxes, text, and the language for that)

    also holds the requirements of the module such as local (in the module folder)
    or global (in the a2/libs folder) libs.
    stores the available parts of the module that can be enabled in the ui.
    also the according variables, hotkeys, defaults, inits
    encapsulates the background functions for enabling/disabling a part
    
    config is None at first and filled as soon as the mod is selected in the UI.
    If there is no configFile yet it will be emptied instead of None.
    """
    def __init__(self, modname, main):
        # gather files from module path in local list
        self.name = modname
        self.path = join(main.a2moddir, modname)
        self._config = None
        self.configFile = join(self.path, 'config.json')
        self.db = main.db
        self.ui = None
        self.main = main
    
    @property
    def config(self):
        if self._config is None:
            self.getConfig()
        return self._config
    
    @config.setter
    def config(self, cfgdict):
        self._config = cfgdict
        with open(self.configFile, 'w') as fObj:
            json.dump(self._config, fObj, indent=jsonIndent)
    
    def getConfig(self):
        if exists(self.configFile):
            try:
                with open(self.configFile) as fobj:
                    self._config = json.load(fobj)
                    return
            except Exception as error:
                log.error('config exists but could not be loaded!: %s\nerror: %s' % (self.configFile, error))
        self._config = []
    
    def enable(self):
        """
        sets its own db entries 
        """
        files = [cfg['file'] for cfg in self.config[1:] if cfg['typ'] == 'include']
        self.db.set('include', files, self.name)
    
    @property
    def scripts(self):
        return [f for f in self.files if f.lower().endswith('.ahk')]
    
    @property
    def files(self):
        """ always browses the path for files"""
        return os.listdir(self.path)

    def createConfig(self, main=None):
        """
        TODO: not in use. get rid of this
        """
        log.debug('%s config exists: %s' % (self.name, exists(self.configFile)))
        with open(self.configFile, 'w') as fileObj:
            fileObj.write('')
        log.debug('%s config exists: %s' % (self.name, exists(self.configFile)))
        if main:
            main.modSelect(True)

    def createScript(self):
        scriptName, ok = QtGui.QInputDialog.getText(self.main, 'new script',
                                              'give a name for the new script file:',
                                              QtGui.QLineEdit.Normal, 'awesomeScript')
        if ok and scriptName != '':
            # make sure there is lowercase .ahk as extension 
            scriptName = '%s.ahk' % splitext(scriptName)[0]
            log.debug('text: %s' % scriptName)
            with open(join(self.path, scriptName), 'w') as fObj:
                content = '; %s - %s\n' % (self.name, scriptName)
                content += '; author: %s\n' % self.main.getAuthor() 
                content += '; created: %s\n\n' % self.main.getDate()
                fObj.write(content)
        return scriptName


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    #app.setStyle(QtGui.QStyleFactory.create("Plastique"))
    a2ui = A2Window()
    a2ui.show()
    exit(app.exec_())
