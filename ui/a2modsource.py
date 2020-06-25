"""
All about a2 module sources aka packages.
So, a module always comes with a package. These can come from arbitrary locations.
Basically just locally or from an FTP, github, another URL, network location ...
They can be enabled/disabled individually affecting all their child modules.
"""
import os
import time
import shutil

from PySide2 import QtCore

import a2path
import a2core
import a2util
import a2ctrl.icons


CONFIG_FILENAME = 'a2modsource.json'
STALE_CONFIG_TIMEOUT = 0.5
MSG_NO_UPDATE_URL = 'No update-URL given!'
MSG_NO_CFG_FILE = 'The Package has no config file!'
MSG_UPDATE_URL_INVALID = 'Update URL Invalid (%s)'
MSG_DOWNLOAD = 'Downloading %s - %s (%s)'
MSG_UNPACK = 'Unpacking %s - %s'
MSG_BACKUP = 'Backing up %s'
MSG_BACKUP_ERROR = 'Error Backing up %s'
MSG_NOT_EMPTY_ERROR = 'Error preparing folder: Not empty but no previous version found!'
MSG_INSTALL = 'Installing %s'
log = a2core.get_logger(__name__)


def get(main, modules_path):
    """
    Browse a a2 data module folder for sources and assemble modsource_dict with
    ModSource objects. Skip folders that have no CONFIG_FILENAME inside.
    Call all module sources to update their modules.
    """
    modsource_dict = {}
    for item in a2path.iter_dirs(modules_path):
        if not os.path.isfile(item.join(CONFIG_FILENAME)):
            continue
        this_source = ModSource(main, item.name)
        this_source.fetch_modules()
        modsource_dict[item.name.lower()] = this_source

    log.info('Gathered %i sources with %i modules in total. (%s)',
             len(modsource_dict), sum(s.mod_count for s in modsource_dict.values()), modules_path)
    return modsource_dict


class ModSource(object):
    def __init__(self, a2, name):
        self.a2 = a2
        self.name = name
        self.path = os.path.join(a2.paths.modules, name)
        self.config_file = os.path.join(self.path, CONFIG_FILENAME)
        self.backup_path = os.path.join(a2.paths.temp, name, 'versions')
        self.mods = {}
        self.mod_count = 0

        self._icon = None
        self._cfg_fetched = None
        self._last_config = {}
        self._config_load_error = None

    def fetch_modules(self, state=None):
        self._cfg_fetched = None
        mods_in_path = a2path.get_dirs(self.path)
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

        import a2mod
        # add new one
        for mod_name in mods_in_path:
            if mod_name not in self.mods:
                self.mods[mod_name] = a2mod.Mod(self, mod_name)

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
        self._icon = a2ctrl.icons.get(self._icon, self.path)
        return self._icon

    def get_update_checker(self, parent, url=None):
        """
        Provides a thread object for the according Module Source instance.

        :rtype: ModSourceCheckThread
        """
        return ModSourceCheckThread(parent, self, url)

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
        return a2path.get_dirs(self.backup_path)

    def __repr__(self):
        return '<a2mod.ModSource %s at %s>' % (self.name, hex(id(self)))

    def move_to_temp_backup(self):
        this_version = self.config.get('version')
        if this_version is None:
            return False

        version_tmpath = os.path.join(self.backup_path, this_version)

        # not yet backed up: move current version to temp
        if not os.path.isdir(version_tmpath):
            log.info('backing up %s %s', self.name, this_version)
            os.makedirs(self.backup_path, exist_ok=True)
            os.rename(self.path, version_tmpath)

        # if backed up: remove the current package
        else:
            log.info('backed up already!\n'
                     '    removing: %s %s', self.name, this_version)
            self.remove()

        return not os.path.isdir(self.path)

    def remove(self):
        """
        Deletes the package from the modules storage
        """
        a2path.remove_dir(self.path)

    def remove_backups(self):
        a2path.remove_dir(self.backup_path)

    @property
    def has_problem(self):
        if self._config_load_error:
            return True
        return False

    def get_problem_msg(self):
        return str(self._config_load_error)

    def is_git(self):
        return os.path.isdir(os.path.join(self.path, '.git'))


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
            remote_data = _get_remote_data(update_url, self.mod_source.config.get('main_branch'))
        except FileNotFoundError:
            self._error(MSG_UPDATE_URL_INVALID % update_url)
            return
        except Exception as error:
            self._error(str(error))
            return

        self.data_fetched.emit(remote_data)


def _get_remote_data(url, main_branch=None):
    url = url.lower().strip()
    if url.startswith('http') or 'github.com/' in url:
        import a2download
        if 'github.com/' in url:
            owner, repo = a2download.get_github_owner_repo(url)
            download_url = '/'.join(
                [a2download.GITHUB_RAW_URL, owner, repo, main_branch or a2download.DEFAULT_MAIN_BRANCH])
        else:
            download_url = url

        if not download_url.endswith(CONFIG_FILENAME):
            download_url = a2path.add_slash(download_url)
            download_url += CONFIG_FILENAME

        remote_data = a2download.get_remote_data(download_url)

    else:
        if os.path.exists(url):
            _, base = os.path.split(url)
            if base.lower() != CONFIG_FILENAME:
                url = os.path.join(url, CONFIG_FILENAME)
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
            if not os.path.isfile(os.path.join(temp_new_version, CONFIG_FILENAME)):
                new_version_dir = None
                for this_path, _dirs, this_files in os.walk(temp_new_version):
                    if CONFIG_FILENAME in this_files:
                        new_version_dir = this_path
                        break
                if new_version_dir is None:
                    self._error('Could not find %s in new package!' % CONFIG_FILENAME)
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
            log.debug(MSG_BACKUP, old_version)
            try:
                self.mod_source.move_to_temp_backup()
            except Exception as error:
                log.error(MSG_BACKUP_ERROR % old_version + '(%s)' % self.mod_source.path)
                log.error(error)
                self._error(MSG_BACKUP_ERROR % old_version)
                return False
        return True

    def _handle_url_download(self, update_url, pack_basename, temp_packpath):
        import a2download
        import traceback
        if 'github.com/' in update_url:
            owner, repo = a2download.get_github_owner_repo(update_url)
            update_url = '/'.join(['https://github.com', owner, repo, 'archive'])
        update_url = a2path.add_slash(update_url)
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
            print('os.path.exists: %s %s', (update_url, False))
            self._error(MSG_UPDATE_URL_INVALID % update_url)
            return False

        try:
            remote_path = os.path.join(update_url, pack_basename)
            shutil.copy2(remote_path, temp_packpath)
        except Exception as error:
            self._error('Error copying from path...\n' + str(error))
            return False
        return True


def create_dir(name):
    a2 = a2core.A2Obj.inst()
    source_path = os.path.join(a2.paths.modules, name)
    os.makedirs(source_path, exist_ok=True)
    return source_path


def get_default_package_cfg():
    a2 = a2core.A2Obj.inst()
    cfg = a2util.json_read(os.path.join(a2.paths.defaults, 'default_package.json'))
    return cfg


def create(name, author_name, author_url):
    path = create_dir(name)
    # write empty cfg json so its found by the package lister
    cfg = get_default_package_cfg()
    cfg['name'] = name
    cfg['maintainer'] = author_name
    cfg['url'] = author_url
    a2util.json_write(os.path.join(path, CONFIG_FILENAME), cfg)
