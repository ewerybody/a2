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
import sys
import json
import time
import uuid
import shutil
import traceback

import a2core
import a2ctrl
import a2util

from PySide2 import QtCore


log = a2core.get_logger(__name__)
CONFIG_FILENAME = 'a2module.json'
MOD_SOURCE_NAME = 'a2modsource.json'
ICON_FILENAME = 'a2icon'
ICON_FORMATS = ['.svg', '.png', '.ico']
ICON_TYPES = [ICON_FILENAME + ext for ext in ICON_FORMATS]
STALE_CONFIG_TIMEOUT = 0.5
USER_CFG_KEY = 'user_cfg'

MSG_NO_UPDATE_URL = 'No update-URL given!'
MSG_DOWNLOAD = 'Downloading %s - %s (%s)'
MSG_UNPACK = 'Unpacking %s - %s'
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
        if not os.path.isfile(os.path.join(path, name, MOD_SOURCE_NAME)):
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
        self.backup_path = os.path.join(a2.paths.temp, name, 'versions')
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

    def get_updater(self, parent, version, remote_data):
        """
        Provides a thread object for the according Module Source instance.

        :rtype: ModSourceFetchThread
        """
        return ModSourceFetchThread(self, parent, version, remote_data)

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

    def __init__(self, mod_source, parent, version, remote_data=None, url=None):
        super(ModSourceFetchThread, self).__init__(parent)
        self.mod_source = mod_source
        self.version = version
        self.url = url
        self.remote_data = remote_data
        self._downloaded_blocks = 0
        self._download_size = None

    def _error(self, msg):
        self.failed.emit(str(msg))
        self.quit()

    def _download_status(self, blocknum, blocksize, fullsize):
        """Used as 'reporthook' callback for url request"""
        if not blocknum:
            return

        self._downloaded_blocks += blocksize

        if not self._download_size:
            # not all headers contain a "content-length"
            if fullsize != -1:
                self._download_size = fullsize
            elif self.remote_data is not None and 'zip_size' in self.remote_data:
                self._download_size = self.remote_data.get('zip_size')

        if self._download_size:
            percentage = 100 * float(self._downloaded_blocks) / self._download_size
            msg = MSG_DOWNLOAD % (self.mod_source.name, self.version,
                                  '%i%%' % min(100, percentage))
        else:
            msg = MSG_DOWNLOAD % (self.mod_source.name, self.version,
                                  '%i kb' % (self._downloaded_blocks * 1024))
        log.info(msg)
        self.status.emit(msg)

    def run(self):
        # exit if there is no URL to actually use
        update_url = self.url or self.mod_source.config.get('update_url')
        if not update_url:
            self._error(MSG_NO_UPDATE_URL)
            return

        old_version = self.mod_source.config.get('version')

        # exit if given version is current version
        if old_version is not None and old_version == self.version:
            self.fetched.emit()
            return

        if not self._handle_old_version(old_version):
            return

        pack_basename = self.version + '.zip'
        temp_packpath = os.path.join(self.mod_source.backup_path, pack_basename)
        temp_new_version = os.path.join(self.mod_source.backup_path, self.version)

        if not os.path.isdir(temp_new_version):
            self.status.emit(MSG_DOWNLOAD % (self.mod_source.name, self.version, 0))
            os.makedirs(self.mod_source.backup_path, exist_ok=True)

            if update_url.startswith('http') or 'github.com/' in update_url:
                if not self._handle_url_download(update_url, pack_basename, temp_packpath):
                    return
            else:
                if not self._handle_file_copy(update_url, pack_basename, temp_packpath):
                    return

            self.status.emit(MSG_UNPACK % (self.mod_source.name, self.version))
            import zipfile
            with zipfile.ZipFile(temp_packpath) as tmp_zip:
                for filename in tmp_zip.namelist():
                    tmp_zip.extract(filename, temp_new_version)
            os.remove(temp_packpath)

            new_version_dir = temp_new_version
            # if mod_source_config not directly under path search for it
            if MOD_SOURCE_NAME not in get_files(temp_new_version):
                new_version_dir = None
                for this_path, _dirs, this_files in os.walk(temp_new_version):
                    if MOD_SOURCE_NAME in this_files:
                        new_version_dir = this_path
                        break
                if new_version_dir is None:
                    self._error('Could not find %s in new package!' % MOD_SOURCE_NAME)
                    return

        # cleanup
        self.status.emit(MSG_INSTALL % self.version)
        os.rename(new_version_dir, self.mod_source.path)
        if os.path.isdir(temp_new_version):
            shutil.rmtree(temp_new_version)

        self.fetched.emit()

    def _handle_old_version(self, old_version):
        if old_version is None:
            files = os.listdir(self.mod_source.path)
            if files:
                self._error(MSG_NOT_EMPTY_ERROR)
                return False
            try:
                self.mod_source.remove()
            except Exception as error:
                self._error(MSG_NOT_EMPTY_ERROR)
                return False
        else:
            self.status.emit(MSG_BACKUP % old_version)
            log.debug(MSG_BACKUP % old_version)
            try:
                self.mod_source._move_to_temp_backup()
            except Exception as error:
                log.error(MSG_BACKUP_ERROR % old_version + '(%s)' % self.mod_source.path)
                log.error(error)
                self._error(MSG_BACKUP_ERROR % old_version)
                return False
        return True

    def _handle_url_download(self, update_url, pack_basename, temp_packpath):
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
            return False
        return True

    def _handle_file_copy(self, update_url, pack_basename, temp_packpath):
        if not os.path.exists(update_url):
            self._error(MSG_UPDATE_URL_INVALID)
            return False

        try:
            remote_path = os.path.join(update_url, pack_basename)
            shutil.copy2(remote_path, temp_packpath)
        except Exception as error:
            self._error('Error copying from path...\n' + str(error))
            return False
        return True


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
        self._data_path = None
        self._backup_path = None
        self._config = None
        self.config_file = os.path.join(self.path, CONFIG_FILENAME)
        self.ui = None
        self._icon = None

        # the compound modulesource|modulename identifier
        self.key = self.source.name + '|' + self.name

    @property
    def has_config_file(self):
        return os.path.isfile(self.config_file)

    @property
    def config(self):
        if self._config is None:
            self.get_config()
        return self._config

    @config.setter
    def config(self, cfg_dict):
        self._config = cfg_dict
        self.backup_config()
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

    def backup_config(self):
        """
        Backups the current config_file.
        """
        if not self.has_config_file:
            return

        if not os.path.isdir(self.backup_path):
            os.makedirs(self.backup_path)

        config_backups = [f for f in os.listdir(self.backup_path)
                          if f.startswith('%s.' % CONFIG_FILENAME)]
        if config_backups:
            config_backups.sort()
            # split and increase appended version index
            backup_index = int(config_backups[-1].rsplit('.', 1)[1]) + 1
        else:
            backup_index = 1

        path = os.path.join(self.backup_path, '%s.%i' % (CONFIG_FILENAME, backup_index))
        shutil.copy2(self.config_file, path)

    def change(self):
        """
        Sets the mods own db entries.
        TODO: remove empty entries!
        """
        db_dict = {'variables': {}, 'hotkeys': {}, 'includes': [], 'init_calls': []}
        a2ctrl.assemble_settings(self.key, self.config[1:], db_dict, self.path)
        for typ, data in db_dict.items():
            if data:
                self.a2.db.set(typ, data, self.key)
            else:
                self.a2.db.pop(typ, self.key)

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
        name = os.path.splitext(name.lower())[0]
        black_list = [os.path.splitext(s)[0].lower() for s in self.scripts]
        return a2util.standard_name_check(
            name, black_list, 'Module has already a script named "%s"!')

    def set_user_cfg(self, element_cfg, value, attr_name=None):
        """
        Sets an elements user value.

        Helps to keep the user config as small as possible.
        For instance if there is a value 'enabled' True by default
        only setting it to False will be saved. User setting it to True
        would delete it from user settings, so it's taking the default again.

        user sets True AND default is True:
            delete from user_cfg
        user sets True AND default it False:
            set to user_cfg

        :param dict element_cfg: The modules original config for the element.
        :param any value: Variable value o
        :param str attr_name: If given sets the value to the name inside a dict.
            Otherwise the value is regarded as a whole.
        """
        cfg_name = a2util.get_cfg_default_name(element_cfg)
        module_user_cfg = self.get_user_cfg()

        if attr_name is None:
            current_cfg = module_user_cfg.get(cfg_name)
            if value == current_cfg:
                return
            current_cfg = value

        else:
            current_cfg = module_user_cfg.get(cfg_name, {})
            if attr_name in current_cfg:
                # value to set equals CURRENT value: done
                if value == current_cfg.get(attr_name):
                    return
                # in any other case: delete to make changes
                current_cfg.pop(attr_name)

            # value to set equals CONFIG value: done. otherwise: save it:
            if value != element_cfg.get(attr_name):
                current_cfg[attr_name] = value

        # delete the value from module_user_cfg if needed
        if current_cfg is None:
            try:
                del module_user_cfg[cfg_name]
            except KeyError:
                pass
        else:
            module_user_cfg[cfg_name] = current_cfg

        # delete module_user_cfg alltogether if needed
        if module_user_cfg:
            self.a2.db.set(USER_CFG_KEY, module_user_cfg, self.key)
        else:
            self.clear_user_cfg()

    def get_user_cfg(self):
        return self.a2.db.get(USER_CFG_KEY, self.key) or {}

    def clear_user_cfg(self):
        self.a2.db.pop(USER_CFG_KEY, self.key)
        self.change()

    def clear_user_cfg_name(self, cfg_name):
        module_user_cfg = self.get_user_cfg()
        try:
            del module_user_cfg[cfg_name]
        except KeyError:
            pass

        # delete module_user_cfg alltogether if needed
        if module_user_cfg:
            self.a2.db.set(USER_CFG_KEY, module_user_cfg, self.key)
        else:
            self.clear_user_cfg()
        self.change()

    def is_in_user_cfg(self, name):
        """
        Tells you if an element has user data saved.
        :param str name: Name of the element
        :rtype: bool
        """
        return name in self.get_user_cfg()

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

    @property
    def data_path(self):
        if self._data_path is None:
            self._data_path = os.path.join(
                self.a2.paths.data, 'module_data', self.source.name, self.name)
        return self._data_path

    @property
    def backup_path(self):
        if self._backup_path is None:
            self._backup_path = os.path.join(
                self.a2.paths.temp, self.source.name, 'config_backups', self.name)
        return self._backup_path

    def get_config_backups(self):
        times_and_files = []
        for file_path, file_name in iter_file_paths(self.backup_path):
            if not file_name[-1].isdigit():
                continue
            times_and_files.append((os.path.getmtime(file_path), file_name))
        times_and_files.sort()
        return times_and_files

    def clear_backups(self):
        for file_path, _ in iter_file_paths(self.backup_path):
            os.remove(file_path)
        os.rmdir(self.backup_path)

    def rollback(self, backup_file_name):
        backup_file_path = os.path.join(self.backup_path, backup_file_name)
        self.backup_config()
        os.remove(self.config_file)
        shutil.copy(backup_file_path, self.config_file)
        self.get_config()
        self.change()

    def call_ahk_script(self, script_name, *args):
        import a2ahk
        script_name = a2ahk.ensure_ahk_ext(script_name)
        script_path = os.path.join(self.path, script_name)
        return a2ahk.call_cmd(script_path, cwd=self.path, *args)

    def call_python_script(self, script_name):
        if not script_name:
            return

        path = os.path.join(self.path, script_name)
        if not os.path.isfile(path):
            return

        from importlib import import_module

        if self.path not in sys.path:
            sys.path.append(self.path)

        base, _ = os.path.splitext(script_name)
        # make sure that script changes make it to runtime
        if base in sys.modules:
            del sys.modules[base]

        try:
            script_module = import_module(base)
        except ImportError:
            log.error(traceback.format_exc().strip())
            log.error('Could not import local script_module! "%s"' % script_name)

        try:
            script_module.main(self.a2, self)
        except Exception:
            tb = traceback.format_exc().strip()

            if base in sys.modules:
                log.info('unloading module "%s" ...' % base)
                del sys.modules[base]

            log.error('\n  Error executing main() of script_module "%s"\n'
                      '%s\n  path: %s' % (script_name, tb, path))

        if self.path in sys.path:
            sys.path.remove(self.path)


def get_files(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def iter_file_paths(path):
    if os.path.isdir(path):
        for item in os.scandir(path):
            if item.is_file():
                yield item.path, item.name


def get_file_paths(path):
    files = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            files.append(item_path)
    return files


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
