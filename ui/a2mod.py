'''
Created on Jul 9, 2015

@author: eRiC
'''
import os
import a2core
import a2ctrl
from os.path import exists, splitext, isdir, isfile
from shutil import copy2


log = a2core.get_logger(__name__)
CONFIG_FILENAME = 'a2module.json'
MOD_SOURCE_NAME = 'a2modsource.json'
VALUE_MAP = {'check': {'typ': bool, 'default': False},
             'number': {'typ': (int, float), 'default': 0.0},
             'string': {'typ': str, 'default': ''},
             'combo': {'typ': str, 'default': ''},
             'path': {'typ': str, 'default': ''}}


def get_module_sources(main, path, modsource_dict):
    """
    Browses the a2 module folder for module sources and updates given
    modsource_dict with new ModSource objects if found or deletes vanished ones.
    Skips folders that have CONFIG_FILENAME inside.
    Calls all module sources to update their modules.
    """
    modsources = get_folders(path)
    # get rid of inexistent module sources
    [modsource_dict.pop(m) for m in list(modsource_dict) if m not in modsources]

    for name in modsources:
        if not exists(os.path.join(path, name, MOD_SOURCE_NAME)):
            continue
#        if name not in modsource_dict:
#            modsource_dict[name] = ModSource(main, name)
#        modsource_dict[name].fetch_modules()
        modsource_dict.setdefault(name, ModSource(main, name)).fetch_modules()


class ModSource(object):
    def __init__(self, a2, name):
        self.a2 = a2
        self.name = name
        self.path = os.path.join(a2.paths.modules, name)
        self.config_file = os.path.join(self.path, MOD_SOURCE_NAME)
        self.mods = {}

    def fetch_modules(self, state=None):
        mods_in_path = get_folders(self.path)
        if not mods_in_path:
            log.debug('No modules in module source: %s' % self.path)
        self.mod_count = len(mods_in_path)

        if state is None:
            state = self.enabled
        if not state:
            self.mods = {}
            return

        # pop inexistent modules
        [self.mods.pop(m) for m in list(self.mods) if m not in mods_in_path]

        # add new ones
        for modname in mods_in_path:
            if modname not in ['.git'] and modname not in self.mods:
                self.mods[modname] = Mod(self, modname)

    @property
    def config(self):
        try:
            return a2core.json_read(self.config_file)
        except Exception:
            return {}

    @config.setter
    def config(self, data):
        a2core.json_write(self.config_file, data)

    @property
    def enabled(self):
        state, enabled_mods = self.a2.enabled.get(self.name, (False, []))
        self.enabled_count = len(enabled_mods)
        return state

    @enabled.setter
    def enabled(self, state):
        current = self.a2.enabled
        current_state, enabled_mods = current.get(self.name, (False, []))
        if current_state != state:
            if not state and enabled_mods == [] and self.name in current:
                current.pop(self.name)
            else:
                current[self.name] = (state, enabled_mods)
            self.a2.enabled = current
            self.fetch_modules(state)

    def toggle(self, state=None):
        print('state: %s' % state)
        if state is None:
            state = not self.enabled
        self.enabled = state


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
    def __init__(self, source, modname):
        # gather files from module path in local list
        self.source = source
        self.name = modname
        self.a2 = a2core.A2Obj.inst()
        self.path = os.path.join(self.source.path, modname)
        self._config = None
        self.config_file = os.path.join(self.path, CONFIG_FILENAME)
        self.ui = None
        # the compound modulesource|modulename identifier
        self.key = self.source.name + '|' + self.name
        # to itentify the module in the module list widget e.g. for selection
        self._item = None

    @property
    def has_config_file(self):
        return exists(self.config_file)

    @property
    def config(self):
        if self._config is None:
            self.get_config()
        return self._config

    @config.setter
    def config(self, cfgdict):
        self._config = cfgdict
        # backup current config_file
        backup_path = os.path.join(self.path, '_config_backups')
        if not exists(backup_path):
            os.mkdir(backup_path)
        _config_backups = [f for f in os.listdir(backup_path) if f.startswith('%s.' % CONFIG_FILENAME)]
        if _config_backups:
            _config_backups.sort()
            backup_index = int(_config_backups[-1].rsplit('.', 1)[1]) + 1
        else:
            backup_index = 1
        if self.has_config_file:
            copy2(self.config_file, os.path.join(backup_path, '%s.%i' % (CONFIG_FILENAME, backup_index)))

        # overwrite config_file
        a2core.json_write(self.config_file, self._config)

    def get_config(self):
        if self.has_config_file:
            try:
                self._config = a2core.json_read(self.config_file)
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
            self.a2.db.set(typ, data[typ], self.key)

    def loop_cfg(self, cfgDict, data):
        for cfg in cfgDict:

            if cfg['typ'] == 'include':
                data['includes'].append(cfg['file'])

            elif 'name' in cfg:
                userCfg = self.a2.db.get(cfg['name'], self.key)
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
        return get_files(self.path)

    @property
    def enabled(self):
        current = self.a2.enabled
        _, enabled_mods = current.get(self.source.name, [False, []])
        return self.name in enabled_mods

    @enabled.setter
    def enabled(self, state):
        current = self.a2.enabled
        source_state, enabled_mods = current.get(self.source.name, [False, []])
        if state and self.name not in enabled_mods:
            enabled_mods.append(self.name)
            current[self.source.name] = [source_state, enabled_mods]
            self.a2.enabled = current
        elif self.name in enabled_mods:
            enabled_mods.remove(self.name)
            current[self.source.name] = [source_state, enabled_mods]
            self.a2.enabled = current
        self.change()

    def createScript(self, scriptName=None):
        if not scriptName:
            return
        # make sure there is lowercase .ahk as extension
        scriptName = '%s.ahk' % splitext(scriptName)[0]
        scriptName = scriptName.strip()

        with open(os.path.join(self.path, scriptName), 'w') as fObj:
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
        user_cfg = self.a2.db.get(sub_cfg['name'], self.key) or {}
        print('user_cfg: %s' % user_cfg)
        print('sub_cfg: %s' % sub_cfg)
        print('attr_name: %s: %s' % (attr_name, value))
        if attr_name in user_cfg:
            # value to set equals CURRENT value: done
            if value == user_cfg.get(attr_name):
                return
            # in any other case: delete to make changes
            user_cfg.pop(attr_name)

        # value to set equals CONFIG value: done. otherwise: save it:
        if value != sub_cfg.get(attr_name):
            user_cfg[attr_name] = value
        self.a2.db.set(sub_cfg['name'], user_cfg, self.key)

    def help(self):
        try:
            a2core.surfTo(self.config[0].get('url'))
        except Exception as error:
            log.error('Error calling help() on module: %s\n:%s' % (self.name, error))


class NewModuleSourceTool(object):
    def __init__(self, main):
        self.a2 = a2core.A2Obj.inst()
        self.main = main
        self.source_names = [m.lower() for m in self.a2.module_sources]
        a2ctrl.InputDialog(self.main, 'New Module Source', self.create_source, self.check_name,
                           msg='Name the new module source:', text='my_module_source')

    def check_name(self, NAME):
        """
        Run on keystroke when creating new module, to give way to okaying the module creation
        """
        name = NAME.lower()
        if NAME == '':
            return 'Name cannot be empty!'
        if name == 'a2':
            return 'You just cannot name your module "a2"! Ok?'
        if name in self.source_names:
            return 'Module source name "%s" is in use!' % name
        if any([(l in a2core.string.whitespace) for l in name]):
            return 'Name cannot have whitespace! Use _ or - insead!'
        if not all([(l in a2core.ALLOWED_CHARS) for l in name]):
            return 'Name can only have letters, digits, _ and -'
        if name in a2core.ILLEGAL_NAMES:
            return 'Name cannot be reserved Windows device name!'
        if not any([(l in a2core.string.ascii_letters) for l in name]):
            return 'Come one have at least 1 letter in the name!'
        return True

    def create_source(self, name):
        if not self.check_name(name):
            return
        if not os.access(self.a2.paths.modules, os.W_OK):
            log.error('A2 module directory not writable! %s' % self.a2.paths.modules)
            return

        source_path = os.path.join(self.a2.paths.modules, name)
        source_cfg = os.path.join(source_path, MOD_SOURCE_NAME)
        os.mkdir(source_path)
        a2core.json_write(source_cfg, {})
        self.a2.fetch_modules()
        self.main.ui.module_view.draw_mod()


def get_files(path):
    return [f for f in os.listdir(path) if isfile(os.path.join(path, f))]


def get_folders(path):
    return [f for f in os.listdir(path) if isdir(os.path.join(path, f))]


if __name__ == '__main__':
    import a2app
    a2app.main()
