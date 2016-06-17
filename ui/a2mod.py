'''
Created on Jul 9, 2015

@author: eRiC
'''
import os
import json
import a2core
import a2ctrl
import logging
from os.path import join, exists, splitext
from shutil import copy2

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# maybe make this even settable in a dev options dialog?
jsonIndent = 2

CONFIG_FILENAME = 'config.json'
VALUE_MAP = {'check': {'typ': bool, 'default': False},
             'number': {'typ': (int, float), 'default': 0.0},
             'string': {'typ': str, 'default': ''},
             'combo': {'typ': str, 'default': ''},
             'path': {'typ': str, 'default': ''}}


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
    If there is no config_file yet it will be emptied instead of None.
    """
    def __init__(self, modname):
        # gather files from module path in local list
        self.name = modname
        global a2
        self.a2 = a2core.A2Obj.inst()
        self.path = join(self.a2.paths.modules, modname)
        self._config = None
        self.config_file = join(self.path, CONFIG_FILENAME)
        self.ui = None

    @property
    def config(self):
        if self._config is None:
            self.get_config()
        return self._config

    @config.setter
    def config(self, cfgdict):
        self._config = cfgdict
        # backup current config_file
        backup_path = join(self.path, '_config_backups')
        if not exists(backup_path):
            os.mkdir(backup_path)
        _config_backups = [f for f in os.listdir(backup_path) if f.startswith('%s.' % CONFIG_FILENAME)]
        if _config_backups:
            _config_backups.sort()
            backup_index = int(_config_backups[-1].rsplit('.', 1)[1]) + 1
        else:
            backup_index = 1
        if exists(self.config_file):
            copy2(self.config_file, join(backup_path, '%s.%i' % (CONFIG_FILENAME, backup_index)))

        # overwrite config_file
        with open(self.config_file, 'w') as fObj:
            json.dump(self._config, fObj, indent=jsonIndent, sort_keys=True)

    def get_config(self):
        if exists(self.config_file):
            try:
                with open(self.config_file) as fobj:
                    self._config = json.load(fobj) or []
                    return
            except Exception as error:
                log.error('config exists but could not be loaded!: '
                          '%s\nerror: %s' % (self.config_file, error))
        self._config = []

    def change(self):
        """
        Sets the mods own db entries
        """
        data = {'includes': [], 'hotkeys': {}, 'variables': {}}
        data = self.loop_cfg(self.config[1:], data)

        for typ in ['includes', 'hotkeys', 'variables']:
            self.a2.db.set(typ, data[typ], self.name)

    def loop_cfg(self, cfgDict, data):
        for cfg in cfgDict:

            if cfg['typ'] == 'include':
                data['includes'].append(cfg['file'])

            elif 'name' in cfg:
                userCfg = self.a2.db.get(cfg['name'], self.name)
                if cfg['typ'] == 'hotkey':
                    if not a2ctrl.get_cfg_value(cfg, userCfg, 'enabled'):
                        continue

                    key = a2ctrl.get_cfg_value(cfg, userCfg, 'key', str)
                    scope = a2ctrl.get_cfg_value(cfg, userCfg, 'scope', list)
                    scopeMode = a2ctrl.get_cfg_value(cfg, userCfg, 'scopeMode', int)
                    function = cfg.get(['functionCode', 'functionURL', 'functionSend'][cfg['functionMode']], '')
                    if scopeMode not in data['hotkeys']:
                        data['hotkeys'][scopeMode] = []
                    # save a global if global scope set or all-but AND scope is empty
                    if scopeMode == 0 or scopeMode == 2 and scope == '':
                        data['hotkeys'][0].append([key, function])
                    else:
                        data['hotkeys'][scopeMode].append([scope, key, function])

                elif cfg['typ'] in VALUE_MAP:
                    data['variables'][cfg['name']] = a2ctrl.get_cfg_value(
                        subCfg=cfg,
                        userCfg=userCfg,
                        attrName='value',
                        typ=VALUE_MAP[cfg['typ']]['typ'],
                        default=VALUE_MAP[cfg['typ']]['default'])

                elif cfg['typ'] == 'group':
                    #disablable
                    if not a2ctrl.get_cfg_value(cfg, userCfg, 'enabled', bool):
                        continue
                    childList = cfg.get('children', [])
                    data = self.loop_cfg(childList, data)
        return data

    @property
    def scripts(self):
        return [f for f in self.files if f.lower().endswith('.ahk')]

    @property
    def files(self):
        """never shale, always browses path for files"""
        return os.listdir(self.path)

    @property
    def enabled(self):
        return self.name in self.a2.enabled

    @enabled.setter
    def enabled(self, this):
        log.error('Cannot switch enable state here')

    def createScript(self, scriptName=None):
        if not scriptName:
            return
        # make sure there is lowercase .ahk as extension
        scriptName = '%s.ahk' % splitext(scriptName)[0]
        scriptName = scriptName.strip()

        with open(join(self.path, scriptName), 'w') as fObj:
            content = '; %s - %s\n' % (self.name, scriptName)
            content += '; author: %s\n' % a2core.get_author()
            content += '; created: %s\n\n' % a2core.get_date()
            fObj.write(content)
        return scriptName

    def checkCreateScript(self, name):
        if name.strip() == '':
            return 'Script name cannot be empty!'
        if splitext(name.lower())[0] in [splitext(s)[0].lower() for s in self.scripts]:
            return 'Module has already a script named "%s"!' % name
        return True

    def set_user_cfg(self, sub_cfg, attr_name, value):
        """
        Helps to keep the user config as small as possible. For instance if there is a value
        'enabled' True by default only setting it to False will be saved. User setting it to True
        would delete it from user settings, so it's taking the default again.

        user sets True AND default is True:
            delete from userCfg
        user sets True AND default it False:
            set to userCfg
        """
        user_cfg = self.a2.db.get(sub_cfg['name'], self.name) or {}
        if attr_name in user_cfg:
            # value to set equals CURRENT value: done
            if value == user_cfg.get(attr_name):
                return
            # in any other case: delete to make changes
            user_cfg.pop(attr_name)

        # value to set equals CONFIG value: done. otherwise: save it:
        if value != sub_cfg.get(attr_name):
            user_cfg[attr_name] = value
        self.a2.db.set(sub_cfg['name'], user_cfg, self.name)

    def help(self):
        docs_url = self.config[0].get('url')
        a2core.surfTo(docs_url)


if __name__ == '__main__':
    import a2app
    a2app.main()
