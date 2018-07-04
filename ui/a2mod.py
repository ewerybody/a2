"""
All about a2 modules.
Modules in a2 always come in packages aka "module sources".
These are collections of 1 or more modules.

A module always comes with a package. These can come from arbitrary locations.
Basically just locally or from an FTP, github, another URL, network location ...
They can be enabled/disabled individually affecting all their child modules.

@created Jul 9, 2015
@author: eRiC
"""
import os
import json
import time
import uuid

import a2core
import a2ctrl
import a2util
import shutil
from PySide2 import QtCore
import traceback


log = a2core.get_logger(__name__)
CONFIG_FILENAME = 'a2module.json'
MOD_SOURCE_NAME = 'a2modsource.json'
ICON_FILENAME = 'a2icon'
ICON_FORMATS = ['.svg', '.png', '.ico']
ICON_TYPES = [ICON_FILENAME + ext for ext in ICON_FORMATS]
STALE_CONFIG_TIMEOUT = 0.5

MSG_NO_UPDATE_URL = 'No update-URL given!'
MSG_DOWNLOAD = 'Downloading %s - %s (%i%s)'
MSG_UNPACK = 'Unpacking %s'
MSG_BACKUP = 'Backing up %s'
MSG_BACKUP_ERROR = 'Error Backing up %s'
MSG_NOT_EMPTY_ERROR = 'Error preparing folder: Not empty but no previous version found!'
MSG_INSTALL = 'Installing %s'
MSG_UPDATE_URL_INVALID = 'Update URL Invalid'
MSG_NO_CFG_FILE = 'The Package has no config file!'


def get_module_sources(main, path, modsource_dict):
    """
    Browses the a2 module folder for module sources and updates given
    modsource_dict with new ModSource objects if found or deletes vanished ones.
    Skips folders that have CONFIG_FILENAME inside.
    Calls all module sources to update their modules.
    """
    modsources = get_folders(path)

    # get rid of inexistent module sources
    # getting list avoids "dictionary changed size during iteration"-error
    for source_name in list(modsource_dict):
        if source_name not in modsources:
            modsource_dict.pop(source_name)

    # add new ones
    for name in modsources:
        if not os.path.exists(os.path.join(path, name, MOD_SOURCE_NAME)):
            continue
        modsource_dict.setdefault(name.lower(), ModSource(main, name)).fetch_modules()


def create_module_source_dir(name):
    a2 = a2core.A2Obj.inst()
    source_path = os.path.join(a2.paths.modules, name)
    os.makedirs(source_path, exist_ok=True)
    return source_path


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
        self._last_config = {}
        self._config_load_error = None

    def fetch_modules(self, state=None):
        self._cfg_fetched = None
        mods_in_path = get_folders(self.path)
        self.mod_count = len(mods_in_path)
        if self.mod_count == 0:
            log.debug('No modules in module source: %s' % self.path)

        if state is None:
            state = self.enabled
        if not state:
            self.mods = {}
            return

        # pop inexistent modules
        # getting list avoids "dictionary changed size during iteration"-error
        for mod_name in list(self.mods):
            if mod_name not in mods_in_path:
                self.mods.pop(mod_name)

        # add new one
        for mod_name in mods_in_path:
            if mod_name not in self.mods:
                self.mods[mod_name] = Mod(self, mod_name)

    @property
    def config(self):
        try:
            # to serve from memory most of the times, only from disk after timeout
            now = time.time()
            if self._cfg_fetched is None or now - self._cfg_fetched > STALE_CONFIG_TIMEOUT:
                self._cfg_fetched = now
                self._last_config = a2util.json_read(self.config_file)
                self._config_load_error = None
            return self._last_config

        except FileNotFoundError:
            self._config_load_error = MSG_NO_CFG_FILE

        except Exception as error:
            msg = ('Error loading config file for "%s" (%s)\n'
                   '  %s' % (self.name, self.config_file, error))
            self._config_load_error = msg
            log.error(msg)
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
        enabled_mods = [m for m in enabled_mods if m in self.mods]
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

        :rtype: ModSourceCheckThread
        """
        return ModSourceCheckThread(parent, self)

    def get_updater(self, parent, version):
        """
        Provides a thread object for the according Module Source instance.

        :rtype: ModSourceFetchThread
        """
        return ModSourceFetchThread(self, parent, version)

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
        if this_version is None:
            return

        version_tmpath = os.path.join(self.backup_path, this_version)

        # not yet backed up: move current version to temp
        if not os.path.isdir(version_tmpath):
            log.info('backing up %s %s' % (self.name, this_version))
            os.makedirs(self.backup_path, exist_ok=True)
            os.rename(self.path, version_tmpath)
            return not os.path.isdir(self.path)

        # if backed up: remove the current package
        else:
            log.info('backed up already!\n'
                     '    removing: %s %s' % (self.name, this_version))
            return self.remove()

    def remove(self):
        """
        Deletes the package from the modules storage
        """
        remove_folder(self.path)

    def remove_backups(self):
        remove_folder(self.backup_path)

    @property
    def has_problem(self):
        if self._config_load_error:
            return True
        return False

    def get_problem_msg(self):
        return str(self._config_load_error)


class ModSourceCheckThread(QtCore.QThread):
    """
    To check for a remote module source dictionary.
    Connect to its Signals:

     - data_fetched(dict) - Remote data as dictionary.
     - update_error(str) - Error message as string.

    and kick it off by .start()-ing it.
    """
    data_fetched = QtCore.Signal(dict)
    update_error = QtCore.Signal(str)

    def __init__(self, parent, mod_source=None, check_url=None):
        super(ModSourceCheckThread, self).__init__(parent)
        self.mod_source = mod_source
        self.check_url = check_url

    def _error(self, msg):
        self.update_error.emit(str(msg))
        self.quit()

    def run(self):
        if self.mod_source is not None:
            update_url = self.mod_source.config.get('update_url', '')
        elif self.check_url is not None:
            update_url = self.check_url

        if not update_url:
            self._error(MSG_NO_UPDATE_URL)
            return

        try:
            remote_data = _get_remote_data(update_url)
        except FileNotFoundError:
            self._error(MSG_UPDATE_URL_INVALID)
            return
        except Exception as error:
            self._error(str(error))
            return

        self.data_fetched.emit(remote_data)


def _get_remote_data(url):
    url = url.lower().strip()
    if url.startswith('http') or 'github.com/' in url:
        if 'github.com/' in url:
            owner, repo = _get_github_owner_repo(url)
            download_url = '/'.join(['https://raw.githubusercontent.com', owner, repo, 'master'])
        else:
            download_url = url

        if not download_url.endswith(MOD_SOURCE_NAME):
            download_url = _add_slash(download_url)
            download_url += MOD_SOURCE_NAME

        from urllib import request
        try:
            data = request.urlopen(download_url).read()
        except request.HTTPError as error:
            raise RuntimeError('Could not find a2 package data at given address!\n%s' % error)

        try:
            data = data.decode(encoding='utf-8-sig')
        except Exception as error:
            log.error(error)
            raise RuntimeError('Error decoding data from given address!:\n%s' % error)

        try:
            remote_data = json.loads(data)
        except Exception as error:
            log.error(error)
            raise RuntimeError('Error loading JSON from given address!:\n%s' % error)

    else:
        if os.path.exists(url):
            _, base = os.path.split(url)
            if base.lower() != MOD_SOURCE_NAME:
                url = os.path.join(url, MOD_SOURCE_NAME)
            remote_data = a2util.json_read(url)
        else:
            raise FileNotFoundError()
    return remote_data


class ModSourceFetchThread(QtCore.QThread):
    """
    To get or change the version of a package (aka updating from remote
    location OR rolling back to a backed up version).

    First it will back up the installed version if not done already.
    The passed version will then be checked against the backed up versions.
    If found:
        copy the backup in place.
    else:
        download the version from the remote location.

    Connect to its Signals:

     - fetched() - no args
     - failed(str) - Error message as string.
     - status(str) - current status like download percentage

    and kick it off by .start()-ing it.
    """
    fetched = QtCore.Signal()
    failed = QtCore.Signal(str)
    status = QtCore.Signal(str)

    def __init__(self, mod_source, parent, version, url=None):
        super(ModSourceFetchThread, self).__init__(parent)
        self.mod_source = mod_source
        self.version = version
        self.url = url
        self._downloaded_blocks = 0

    def _error(self, msg):
        self.failed.emit(str(msg))
        self.quit()

    def _download_status(self, blocknum, blocksize, fullsize):
        if not blocknum:
            return
        self._downloaded_blocks += blocksize
        percentage = min(100, (100 * float(self._downloaded_blocks) / fullsize))
        self.status.emit(MSG_DOWNLOAD % (self.mod_source.name,
                                         self.version, percentage, '%'))

    def run(self):
        old_version = self.mod_source.config.get('version')
        if old_version is not None and old_version == self.version:
            self.fetched.emit()
            return

        update_url = self.url or self.mod_source.config.get('update_url')
        if not update_url:
            self._error(MSG_NO_UPDATE_URL)
            return

        if old_version is None:
            files = os.listdir(self.mod_source.path)
            if files:
                self._error(MSG_NOT_EMPTY_ERROR)
                return
            try:
                self.mod_source.remove()
            except Exception as error:
                self._error(MSG_NOT_EMPTY_ERROR)
                return
        else:
            self.status.emit(MSG_BACKUP % old_version)
            log.debug(MSG_BACKUP % old_version)
            try:
                self.mod_source._move_to_temp_backup()
            except Exception as error:
                log.error(MSG_BACKUP_ERROR % old_version + '(%s)' % self.mod_source.path)
                log.error(error)
                self._error(MSG_BACKUP_ERROR % old_version)
                return

        pack_basename = self.version + '.zip'
        temp_packpath = os.path.join(self.mod_source.backup_path, pack_basename)
        temp_new_version = os.path.join(self.mod_source.backup_path, self.version)
        new_version_dir = temp_new_version

        if not os.path.isdir(temp_new_version):
            self.status.emit(MSG_DOWNLOAD % (self.mod_source.name, self.version, 0, '%'))
            os.makedirs(self.mod_source.backup_path, exist_ok=True)

            if update_url.startswith('http') or 'github.com/' in update_url:
                if 'github.com/' in update_url:
                    owner, repo = _get_github_owner_repo(update_url)
                    update_url = '/'.join(['https://github.com', owner, repo, 'archive'])
                update_url = _add_slash(update_url)
                update_url += pack_basename

                from urllib import request
                try:
                    request.FancyURLopener().retrieve(
                        update_url, temp_packpath, self._download_status)
                except Exception as error:
                    log.error(traceback.format_exc().strip())
                    self._error('Error retrieving package...\n' + str(error))
                    return

            else:
                if not os.path.exists(update_url):
                    self._error(MSG_UPDATE_URL_INVALID)
                    return

                try:
                    remote_path = os.path.join(update_url, pack_basename)
                    shutil.copy2(remote_path, temp_packpath)
                except Exception as error:
                    self._error('Error copying from path...\n' + str(error))
                    return

            import zipfile
            with zipfile.ZipFile(temp_packpath) as tmp_zip:
                for filename in tmp_zip.namelist():
                    tmp_zip.extract(filename, temp_new_version)
            os.remove(temp_packpath)

            # if mod_source_config not directly under path search for it
            if MOD_SOURCE_NAME not in get_files(temp_new_version):
                new_version_dir = None
                for _this_path, _dirs, _this_files in os.walk(temp_new_version):
                    if MOD_SOURCE_NAME in _this_files:
                        new_version_dir = _this_path
                        break
                if new_version_dir is None:
                    self._error('Could not find %s in new package!' % MOD_SOURCE_NAME)
                    return

        self.status.emit(MSG_INSTALL % self.version)
        os.rename(new_version_dir, self.mod_source.path)
        if os.path.isdir(temp_new_version):
            shutil.rmtree(temp_new_version)

        self.fetched.emit()


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
                return self._config
            except Exception as error:
                log.error('config exists but could not be loaded!: '
                          '%s\nerror: %s' % (self.config_file, error))
        self._config = []
        return self._config

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

    def has_tag(self, tagname):
        """
        Checks if the given tag is among the modules tags
        :param str tagname: Tag name to look for
        :rtype: bool
        """
        if self.config and tagname in self.config[0].get('tags', []):
            return True
        return False


def get_files(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def get_folders(path):
    """
    From a given path fetches all the folders.
    Excluding ones starting with a dot! like ".git" ect.
    """
    if not os.path.isdir(path):
        return []

    return [f for f in os.listdir(path) if not f.startswith('.') and
            os.path.isdir(os.path.join(path, f))]


def remove_folder(path):
    """
    Moves the path to temp with random name then deletes it.
    Instead of deleting the single items directly this will already
    correctly fail moving to temp if ANY of the containing items is locked.
    So there is no other safeguard needed.
    """
    trash_path = os.path.join(os.getenv('TEMP'), str(uuid.uuid4()))
    os.rename(path, trash_path)
    shutil.rmtree(trash_path)


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


def _get_github_owner_repo(url):
    parts = url.split('/')
    i = parts.index('github.com')
    owner, repo = parts[i + 1: i + 3]
    return owner, repo


def _add_slash(url):
    if not url.endswith('/'):
        url += '/'
    return url


def get_default_package_cfg():
    a2 = a2core.A2Obj.inst()
    cfg = a2util.json_read(os.path.join(a2.paths.defaults, 'default_package.json'))
    return cfg


if __name__ == '__main__':
    import a2app
    a2app.main()
