"""
All about a2 modules.
Modules in a2 always come in packages aka module sources.
These are collections of 1 or more modules.
A module always comes with a module source.

The module sources can come from arbitrary locations. Basically just locally or
from an FTP, github project, another URL, network location ...
They can be enabled/disabled individually affecting all their child modules.

@created Jul 9, 2015
@author: eRiC
"""
import os
import time
import uuid

import a2core
import a2ctrl
import a2util
import shutil
from PySide import QtCore


log = a2core.get_logger(__name__)
CONFIG_FILENAME = 'a2module.json'
MOD_SOURCE_NAME = 'a2modsource.json'
ICON_FILENAME = 'a2icon'
ICON_FORMATS = ['.svg', '.png', '.ico']
ICON_TYPES = [ICON_FILENAME + ext for ext in ICON_FORMATS]
EXCLUDE_FOLDERS = ['.git']
STALE_CONFIG_TIMEOUT = 0.5

MSG_NO_UPDATE_URL = 'No update-URL given!'
MSG_DOWNLOAD = 'Downloading %s'
MSG_UNPACK = 'Unpacking %s'
MSG_BACKUP = 'Backing up %s'
MSG_BACKUP_ERROR = 'Error Backing up %s'
MSG_INSTALL = 'Installing %s'
MSG_UPDATE_URL_INVALID = 'Update URL Invalid'


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
        if not os.path.exists(os.path.join(path, name, MOD_SOURCE_NAME)):
            continue
        modsource_dict.setdefault(name, ModSource(main, name)).fetch_modules()


class ModSource(object):
    def __init__(self, a2, name):
        self.a2 = a2
        self.name = name
        self.path = os.path.join(a2.paths.modules, name)
        self.config_file = os.path.join(self.path, MOD_SOURCE_NAME)
        self.backup_path = os.path.join(a2.paths.a2_temp, name)
        self.mods = {}
        self.mod_count = 0

        self._icon = None
        self._cfg_fetched = None
        self._last_config = None

    def fetch_modules(self, state=None):
        self._cfg_fetched = None
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
            if modname not in self.mods:
                self.mods[modname] = Mod(self, modname)

    @property
    def config(self):
        try:
            now = time.time()
            if not self._cfg_fetched or now - self._cfg_fetched > STALE_CONFIG_TIMEOUT:
                self._cfg_fetched = now
                self._last_config = a2util.json_read(self.config_file)
            return self._last_config
        except Exception as error:
            log.error('Error loading config file for "%s" (%s)\n'
                      '  %s' % (self.name, self.config_file, error))
            return {}

    @config.setter
    def config(self, data):
        a2util.json_write(self.config_file, data)

    @property
    def enabled(self):
        state, _ = self.a2.enabled.get(self.name, (False, []))
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

    @property
    def enabled_mods(self):
        _state, enabled_mods = self.a2.enabled.get(self.name, (False, []))
        return enabled_mods

    @property
    def enabled_count(self):
        return len(self.enabled_mods)

    def toggle(self, state=None):
        if state is None:
            state = not self.enabled
        self.enabled = state

    @property
    def icon(self):
        self._icon = get_icon(self._icon, self.path, a2ctrl.Icons.inst().a2)
        return self._icon

    def get_update_checker(self, parent):
        """
        Provides a thread object for the according Module Source instance.

        :rtype: _ModSourceUpdateCheckThread
        """
        return _ModSourceUpdateCheckThread(self, parent)

    def get_updater(self, version, parent):
        """
        Provides a thread object for the according Module Source instance.

        :rtype: _ModSourceUpdateThread
        """
        return _ModSourceUpdateThread(self, version, parent)

    def get_backup_versions(self):
        """
        Looks up a2s temp storage for versions of the package
        to roll back to if wanted.

        :return: List of strings of stored versions.
        :rtype: list
        """
        return get_folders(self.backup_path)

    def __repr__(self):
        return '<a2mod.ModSource %s at %s>' % (self.name, hex(id(self)))

    def _move_to_temp_backup(self):
        this_version = self.config.get('version')
        version_tmpath = os.path.join(self.backup_path, this_version)

        # not yet backed up: move current version to temp
        if not os.path.isdir(self.backup_path):
            log.info('backing up %s %s' % (self.name, this_version))
            os.makedirs(self.backup_path, exist_ok=True)
            os.rename(self.path, version_tmpath)
            return not os.path.isdir(self.path)

        # if backed up: move current to temp then delete
        else:
            log.info('backed up already!\n'
                     '    removing: %s %s' % (self.name, this_version))
            trash_path = os.path.join(os.getenv('TEMP'), str(uuid.uuid4()))
            os.rename(self.path, trash_path)
            shutil.rmtree(trash_path)
            return not os.path.isdir(self.path) and not os.path.isdir(trash_path)


class _ModSourceUpdateCheckThread(QtCore.QThread):
    """
    To check for newer versions via its configs update_url.
    Connect to its Signals:

     - update_error(str) - Error message as string.
     - is_uptodate() - no args
     - update_available(str) - Remote version as string.

    and kick it off by .start()-ing it.
    """
    is_uptodate = QtCore.Signal()
    update_available = QtCore.Signal(str)
    update_error = QtCore.Signal(str)

    def __init__(self, mod_source, parent):
        super(_ModSourceUpdateCheckThread, self).__init__(parent)
        self.mod_source = mod_source

    def _error(self, msg):
        self.update_error.emit(str(msg))
        self.quit()

    def run(self):
        update_url = self.mod_source.config.get('update_url', '')
        if not update_url:
            self._error(MSG_NO_UPDATE_URL)

        if update_url.startswith('http') or 'github.com/' in update_url:
            # TODO: web update check
            pass
        else:
            if os.path.exists(update_url):
                try:
                    _, base = os.path.split(update_url)
                    if base.lower() != MOD_SOURCE_NAME:
                        update_url = os.path.join(update_url, MOD_SOURCE_NAME)
                    remote_data = a2util.json_read(update_url)
                    remote_version = remote_data.get('version')
                    if remote_data['version'] == self.mod_source.config.get('version'):
                        self.is_uptodate.emit()
                    else:
                        self.update_available.emit(remote_version)
                except Exception as error:
                    self._error(str(error))
            else:
                self._error(MSG_UPDATE_URL_INVALID)


class _ModSourceUpdateThread(QtCore.QThread):
    """
    To change the version of the package.
    Aka updating from a remote location OR rolling back to a backed up version.

    First it will back up the installed version if not done already.
    The passed version will then be checked against the backed up versions.
    If found:
        copy the backup in place.
    else:
        download the version from the remote location.

    Connect to its Signals:

     - finished() - no args
     - failed(str) - Error message as string.

    and kick it off by .start()-ing it.
    """
    finished = QtCore.Signal()
    failed = QtCore.Signal(str)
    status = QtCore.Signal(str)

    def __init__(self, mod_source, version, parent):
        super(_ModSourceUpdateThread, self).__init__(parent)
        self.version = version
        self.mod_source = mod_source

    def _error(self, msg):
        self.failed.emit(str(msg))
        self.quit()

    def run(self):
        old_version = self.mod_source.config.get('version')
        if old_version == self.version:
            self.finished.emit()
            return

        update_url = self.mod_source.config.get('update_url', '')
        if not update_url:
            self._error(MSG_NO_UPDATE_URL)
            return

        self.status.emit(MSG_BACKUP % old_version)
        try:
            self.mod_source._move_to_temp_backup()
        except Exception as error:
            log.error('Could not backup %s (%s)!' % (old_version, self.mod_source.path))
            log.error(error)
            self._error(MSG_BACKUP_ERROR % old_version)
            return

        temp_new_version = os.path.join(self.mod_source.backup_path, self.version)
        if not os.path.isdir(temp_new_version):
            self.status.emit(MSG_DOWNLOAD % self.version)
            if update_url.startswith('http') or 'github.com/' in update_url:
                # TODO: web update
                pass
            else:
                if not os.path.exists(update_url):
                    self._error(MSG_UPDATE_URL_INVALID)
                    return

                pack_basename = self.version + '.zip'
                remote_path = os.path.join(update_url, pack_basename)
                temp_packpath = os.path.join(self.mod_source.backup_path, pack_basename)
                shutil.copy2(remote_path, temp_packpath)

            try:
                import zipfile
                with zipfile.ZipFile(temp_packpath) as tmp_zip:
                    for filename in tmp_zip.namelist():
                        tmp_zip.extract(filename, temp_new_version)
                os.remove(temp_packpath)

            except Exception as error:
                self._error(str(error))
                return

        self.status.emit(MSG_INSTALL % self.version)
        shutil.copytree(temp_new_version, self.mod_source.path)

        self.finished.emit()


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
        # to identify the module in the module list widget e.g. for selection
        self._item = None
        self._icon = None

    @property
    def has_config_file(self):
        return os.path.exists(self.config_file)

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
        if not os.path.exists(backup_path):
            os.mkdir(backup_path)
        _config_backups = [f for f in os.listdir(backup_path) if f.startswith('%s.' % CONFIG_FILENAME)]
        if _config_backups:
            _config_backups.sort()
            backup_index = int(_config_backups[-1].rsplit('.', 1)[1]) + 1
        else:
            backup_index = 1
        if self.has_config_file:
            shutil.copy2(self.config_file, os.path.join(backup_path, '%s.%i' % (CONFIG_FILENAME, backup_index)))

        # overwrite config_file
        a2util.json_write(self.config_file, self._config)

    def get_config(self):
        if self.has_config_file:
            try:
                self._config = a2util.json_read(self.config_file)
                return
            except Exception as error:
                log.error('config exists but could not be loaded!: '
                          '%s\nerror: %s' % (self.config_file, error))
        self._config = []

    def change(self):
        """
        Sets the mods own db entries
        """
        db_dict = {'variables': {}, 'hotkeys': {}, 'includes': [], 'init_calls': []}
        a2ctrl.assemble_settings(self.key, self.config[1:], db_dict, self.path)
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
        return self.name in self.source.enabled_mods

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
        script_name = '%s.ahk' % os.path.splitext(script_name)[0]
        script_name = script_name.strip()

        with open(os.path.join(self.path, script_name), 'w') as fObj:
            content = '; %s - %s\n' % (self.name, script_name)
            content += '; author: %s\n' % author_name
            content += '; created: %s\n\n' % a2util.get_date()
            fObj.write(content)
        return script_name

    def check_create_script(self, name):
        if name.strip() == '':
            return 'Script name cannot be empty!'
        if os.path.splitext(name.lower())[0] in [os.path.splitext(s)[0].lower() for s in self.scripts]:
            return 'Module has already a script named "%s"!' % name
        return True

    def set_user_cfg(self, sub_cfg, value, attr_name=None):
        """
        Sets an elements user value.

        Helps to keep the user config as small as possible. For instance if there is a value
        'enabled' True by default only setting it to False will be saved. User setting it to True
        would delete it from user settings, so it's taking the default again.

        user sets True AND default is True:
            delete from user_cfg
        user sets True AND default it False:
            set to user_cfg
        """
        cfg_name = a2util.get_cfg_default_name(sub_cfg)
        current_cfg = self.a2.db.get(cfg_name, self.key) or {}
        if attr_name is None:
            if value == current_cfg:
                return
            current_cfg = value
        else:
            if attr_name in current_cfg:
                # value to set equals CURRENT value: done
                if value == current_cfg.get(attr_name):
                    return
                # in any other case: delete to make changes
                current_cfg.pop(attr_name)

            # value to set equals CONFIG value: done. otherwise: save it:
            if value != sub_cfg.get(attr_name):
                current_cfg[attr_name] = value

        self.a2.db.set(cfg_name, current_cfg, self.key)

    def help(self):
        try:
            a2util.surf_to(self.config[0].get('url'))
        except Exception as error:
            log.error('Error calling help() on module: %s\n:%s' % (self.name, error))

    def __repr__(self):
        return '<a2mod.Mod %s at %s>' % (self.name, hex(id(self)))

    @property
    def icon(self):
        self._icon = get_icon(self._icon, self.path, self.source.icon)
        return self._icon


def get_files(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def get_folders(path, exclude=None):
    if exclude is None:
        exclude = EXCLUDE_FOLDERS

    if not os.path.isdir(path):
        return []

    return [f for f in os.listdir(path)
            if os.path.isdir(os.path.join(path, f)) and f not in exclude]


def get_icon(current_icon, folder, fallback):
    if current_icon is None or not os.path.exists(current_icon.path):
        icon_path = ''
        for item in get_files(folder):
            if item in ICON_TYPES:
                icon_path = os.path.join(folder, item)

                break
        if icon_path:
            current_icon = a2ctrl.Ico(icon_path)
        else:
            current_icon = fallback

    return current_icon


if __name__ == '__main__':
    import a2app
    a2app.main()
