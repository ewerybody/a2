'''
Created on Jul 9, 2015

@author: eRiC
'''
from PySide import QtGui
import os
from os.path import join, exists, splitext
import json
import logging
logging.basicConfig()
log = logging.getLogger('a2ui')
log.setLevel(logging.DEBUG)
# maybe make this even settable in a dev options dialog?
jsonIndent = 2


class Mod(object):
    """
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
                log.error('config exists but could not be loaded!: '
                          '%s\nerror: %s' % (self.configFile, error))
        self._config = []

    def change(self):
        """
        sets its own db entries
        """
        includes = []
        hotkeys = {}
        for cfg in self.config[1:]:
            if cfg['typ'] == 'include':
                includes.append(cfg['file'])
            elif cfg['typ'] == 'hotkey':
                userCfg = self.db.get(cfg['name'], self.name)
                if not self.getCfgValue(cfg, userCfg, 'enabled'):
                    continue
                
                key = self.getCfgValue(cfg, userCfg, 'key')
                scope = self.getCfgValue(cfg, userCfg, 'scope')
                scopeMode = self.getCfgValue(cfg, userCfg, 'scopeMode')
                function = cfg[['functionCode', 'functionURL', 'functionSend'][cfg['functionMode']]]
                if scopeMode not in hotkeys:
                    hotkeys[scopeMode] = []
                # save a global if global scope set or all-but AND scope is empty
                if scopeMode == 0 or scopeMode == 2 and scope == '':
                    hotkeys[0].append([key, function])
                else:
                    hotkeys[scopeMode].append([scope, key, function])
        
        self.db.set('includes', includes, self.name)
        self.db.set('hotkeys', hotkeys, self.name)
        self.main.settingsChanged()

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
        with open(self.configFile, 'w') as fileObj:
            fileObj.write('')
        if main:
            main.modSelect(True)

    def createScript(self):
        scriptName, ok = QtGui.QInputDialog.getText(self.main, 'new script',
            'give a name for the new script file:', QtGui.QLineEdit.Normal,
            'awesomeScript')

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

    def setUserCfg(self, subCfg, attrName, setValue):
        """
        Helps to keep the user config as small as possible. For instance if there is a value
        'enabled' True by default only setting it to False will be saved. User setting it to True
        would delete it from user settings, so it's taking the default again.
        
        user sets True AND default is True:
            delete from userCfg
        user sets True AND default it False:
            set to userCfg
        """
        userCfg = self.db.get(subCfg['name'], self.name) or {}
        if attrName in userCfg:
            # value to set equals CURRENT value: done
            if setValue == userCfg[attrName]:
                return
            # in any other case: delete to make changes
            userCfg.pop(attrName)

        # value to set equals CONFIG value: done. otherwise: save it:
        if setValue != subCfg[attrName]:
            userCfg[attrName] = setValue
        self.db.set(subCfg['name'], userCfg, self.name)

    def getCfgValue(self, subCfg, userCfg, attrName):
        """
        unified call to get a value no matter if its set by user already
        or still default from the module config.
        """
#         print('getCfgValue: %s' % attrName)
#         print('subCfg: %s' % subCfg)
#         print('userCfg: %s' % userCfg)
        if userCfg is not None and attrName in userCfg:
            return userCfg[attrName]
        elif attrName in subCfg:
            return subCfg[attrName]
        else:
            return None
