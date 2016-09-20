'''
Created on Jul 9, 2015

@author: eRiC
'''
import os
import a2core
import a2ctrl
from os.path import exists, splitext, isdir, isfile
from shutil import copy2
from PySide import QtGui


log = a2core.get_logger(__name__)
CONFIG_FILENAME = 'a2module.json'
MOD_SOURCE_NAME = 'a2modsource.json'
ICON_FILENAME = 'a2icon'
ICON_FORMATS = ['.svg', '.png']


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
        self._icon = None

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
        if state is None:
            state = not self.enabled
        self.enabled = state

    @property
    def icon(self):
        self._icon = get_icon(self._icon, self.path, a2ctrl.Icons.inst().a2)
        return self._icon

    def __repr__(self):
        return '<a2mod.ModSource %s at %s>' % (self.name, hex(id(self)))


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
        self._icon = None

    @property
    def has_config_file(self):
        return exists(self.config_file)

    @property
    def config(self):
        if self._config is None:
            self.get_config()
        return self._config

    @config.setter
    def config(self, cfg_dict):
        self._config = cfg_dict
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
        db_dict = {'variables': {}, 'hotkeys': [], 'includes': []}
        a2ctrl.assemble_settings(self.key, self.config[1:], db_dict)
        for typ, data in db_dict.items():
            self.a2.db.set(typ, data, self.key)

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

    def create_script(self, script_name, author_name):
        if not script_name:
            return
        # make sure there is lowercase .ahk as extension
        script_name = '%s.ahk' % splitext(script_name)[0]
        script_name = script_name.strip()

        with open(os.path.join(self.path, script_name), 'w') as fObj:
            content = '; %s - %s\n' % (self.name, script_name)
            content += '; author: %s\n' % author_name
            content += '; created: %s\n\n' % a2core.get_date()
            fObj.write(content)
        return script_name

    def check_create_script(self, name):
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

    def __repr__(self):
        return '<a2mod.Mod %s at %s>' % (self.name, hex(id(self)))

    @property
    def icon(self):
        self._icon = get_icon(self._icon, self.path, self.source.icon)
        return self._icon


def get_files(path):
    return [f for f in os.listdir(path) if isfile(os.path.join(path, f))]


def get_folders(path):
    return [f for f in os.listdir(path) if isdir(os.path.join(path, f))]


icon_types = [ICON_FILENAME + ext for ext in ICON_FORMATS]


def get_icon(current_icon, folder, fallback):
    if current_icon is None or not exists(current_icon.path):
        icon_path = ''
        for item in get_files(folder):
            if item in icon_types:
                icon_path = os.path.join(folder, item)

                break
        if icon_path:
            if item.endswith('.svg'):
                current_icon = a2ctrl.Ico(icon_path)
            else:
                current_icon = QtGui.QIcon(icon_path)
                current_icon.path = icon_path
        else:
            current_icon = fallback

    return current_icon


if __name__ == '__main__':
    import a2app
    a2app.main()
