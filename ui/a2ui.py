# a2ui
from PySide import QtGui, QtCore
import os
from os.path import exists, join
from functools import partial
import sys
import a2dblib
import a2ctrl
import json
from a2design_ui import Ui_a2MainWindow

import logging
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

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("_dump/a2logo 16.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.initPaths()
        self.dbfile = join(self.a2setdir, 'a2.db')
        # create db connection: use test\a2dbtest.py to test it
        self.db = a2dblib.A2db(self.dbfile)

        self.enabledMods = self.db.gets('enabled')
        log.info('enabledMods: %s' % self.enabledMods)

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
        self.toggleEditCtrls(False)
        self.ui.editOKButton.pressed.connect(self.editSubmit)
        self.ui.editCancelButton.pressed.connect(self.drawMod)
        
        #TODO: remember size and window position
        self.setGeometry(QtCore.QRect(250, 250, 1268, 786))

        log.info('a2ui initialised!')

    def modSelect(self, force=False):
        """
        updates the mod view to the right of the UI
        when something different is elected in the module list 
        """
        name = self.ui.modList.selectedItems()[0].text()
        if name == self.selectedMod and force is False:
            return
        self.mod = self.modules[name]
        
        self.ui.modCheck.setVisible(True)
        self.ui.modName.setText(name)
        self.ui.modCheck.setChecked(name in self.db.gets('enabled'))
        
        # TODO: make selectedMod rather the object? 
        self.selectedMod = name
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
        log.debug('drawing: %s' % self.mod.name)
        self.tempConfig = None

#        if self.controls:
#            print('self.controls: %s' % self.controls)
#         for ctrl in self.controls:
#             #self.mainlayout.removeItem(self.ui.spacer)
#             try:
#                 #self.mainlayout.removeWidget(ctrl)
#                 #del(ctrl)
#                 pass
#             except Exception as ex:
#                 log.error('self.mainlayout.removeWidget(%s) threw exceptption %s' % (ctrl, ex))

        author = ''
        version = ''
        if len(self.mod.config):
            if self.mod.config[0].get('typ') != 'nfo':
                log.error('First element of config is not typ nfo! %s' % self.mod.name)
            author = self.mod.config[0].get('author') or ''
            version = self.mod.config[0].get('version') or ''
        self.ui.modAuthor.setText(author)
        self.ui.modVersion.setText(version)
        self.controls = []
        
        if self.mod.config == []:
            self.controls.append(QtGui.QLabel('config.json currently empty. '
                                         'imagine awesome layout here ...'))
        else:
            for element in self.mod.config:
                self.controls.append(a2ctrl.draw(element))
        
        self.toggleEditCtrls(False)
        self.drawUI()
        
    def editMod(self):
        """
        From the modules config creates controls to edit the config itself.
        If a header is not found one will be added to the in-edit config.
        On "OK" the config data is collected from the UI and written back to the json.
        On Cancel the in-edit config is discarded and drawMod called which draws the
        UI unchanged.
        """
        log.debug('editing: %s' % self.mod.name)
        self.controls = []
        
        if self.tempConfig is None:
            self.tempConfig = list(self.mod.config)
        
        #if not mod.config: is None or mod.config is []
        if not len(self.tempConfig):
            s = 'Because none existed before this temporary description was created for "%s". '\
                'Change it to describe what it does with a couple of words.' % self.mod.name
            newNfo = {'typ': 'nfo',
                       'description': s,
                      #'display name': '%s' % mod.name,
                      'author': 'your name',
                      'version': '0.1',
                      'date': '2015'}
            self.tempConfig.insert(0, newNfo)
            print('config: %s' % self.tempConfig)
        
        for element in self.tempConfig:
            self.controls.append(a2ctrl.edit(element, self.mod))
        
        editSelect = a2ctrl.EditAddElem(self.mod, self.tempConfig, self.editMod)
        self.controls.append(editSelect)
        
        self.drawUI()
        self.toggleEditCtrls(True)
    
    def editSubmit(self):
        """
        loop the given ctrlDict, query ctrls and feed target mod.config
        """
        newcfg = []
        for ctrl in self.controls:
            if hasattr(ctrl, 'getCfg'):
                newcfg.append(ctrl.getCfg())
        
        self.mod.saveConfig(newcfg)
        self.drawMod()
    
    def toggleEditCtrls(self, state):
        for button in [self.ui.editCancelButton, self.ui.editOKButton]:
            button.setEnabled(state)
            button.setMaximumSize(QtCore.QSize(16777215, 50 if state else 0))
    
    def modEnable(self):
        if self.ui.modCheck.checkState():
            log.debug('enabling: %s ...' % self.selectedMod)
            enabled = self.db.adds('enabled', self.selectedMod)
        else:
            log.debug('disabling: %s ...' % self.selectedMod)
            enabled = self.db.dels('enabled', self.selectedMod)
        for e in enabled:
            for c in self.modules[e].config:
                if c['typ'] == 'include':
                    log.info('enabled mod %s file to include: %s' % (e, c['file']))
        
        

    def modInfo(self):
        log.debug('calling info on: %s ...' % self.selectedMod)
    
    def settingsChanged(self, mod):
        print('mod: ' + str(self.modules[mod]))
    
    def fetchModules(self):
        self.modules = {}
        for mod in os.listdir(self.a2moddir):
            self.modules[mod] = Mod(mod, self.a2moddir, self.db)

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

        self.a2dir = os.path.dirname(self.a2uidir)
        self.a2libdir = self.a2dir + '/' + 'lib/'
        self.a2exe = self.a2dir + '/a2Starter.exe'
        self.a2ahk = self.a2dir + '/a2.ahk'
        self.a2setdir = self.getSettingsDir()
        self.a2moddir = self.a2dir + '/' + 'modules/'
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

    def getSettingsDir(self):
        """ TODO: temporary under a2dir!! has to be VARIABLE! """
        return join(self.a2dir, 'settings')


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
    def __init__(self, modname, a2moddir, db):
        # gather files from module path in local list
        self.name = modname
        self.path = join(a2moddir, modname)
        self._config = None
        self.configFile = join(self.path, 'config.json')
        self.db = db
        self.ui = None
        self._files = None
        self._scripts = None
    
    @property
    def config(self):
        if self._config is None:
            self.getConfig()
        return self._config
    
    def getConfig(self):
        if exists(self.configFile):
            try:
                with open(self.configFile) as fobj:
                    self._config = json.load(fobj)
                    return
            except Exception as error:
                log.error('config exists but could not be loaded!: %s\nerror: %s' % (self.configFile, error))
        self._config = []
    
    @property
    def scripts(self):
        if self._scripts is None:
            self.getScripts()
        return self._scripts
    
    def getScripts(self):
        self._scripts = [f for f in self.getFiles() if f.lower().endswith('.ahk')]
        return self._scripts

    @property
    def files(self):
        if self._files is None:
            self._files = self.getFiles()
        return self._files

    def getFiles(self):
        """
        browses the modules folder for files that belong to a module part
        # script file - the filename to be enlisted to the includes
        # defaults file - variable defaults and hotkey suggestions
        # language file - for ui and runtime
        """
        self._files = os.listdir(self.path)
        return self._files

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

    def saveConfig(self, cfgdict):
        self._config = cfgdict
        with open(self.configFile, 'w') as fObj:
            json.dump(self._config, fObj, indent=jsonIndent)
        

class A2Obj(object):
    """
    WIP!: this doesn't really work well... somhow I'd like a console
    that can talk to the running ui window. Gotta learn more Qt...
    """
    def __init__(self):
        self.app = QtGui.QApplication([])
        self.ui = A2Window()
        self.ui.show()
        log.info('aaaand its gone!')
        #exit(self.app.exec_())


if __name__ == '__main__':
    # if in main thread, run the ui directly
    app = QtGui.QApplication(sys.argv)
    a2ui = A2Window()
    a2ui.show()
    exit(app.exec_())
else:
    # otherwise offer a scripting interface
    log.error('__name__ != "__main__": %s' % __name__)
    log.info('fetch an A2Obj e.g.:\n\ta2 = a2ui.A2Obj()\n')


def a2reload():
    # engages the a2.ahk runtime to shutdown and restart
    # preferably in another thread?
    pass


def r():
    # debug wrapper to reload a2ui in py env
    __import__(sys.modules['a2ui'])
    __import__(sys.modules['a2dblib'])
    return A2Window()
