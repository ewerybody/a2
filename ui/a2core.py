"""
a2core - Foundation module to host basic info and functionality.

Everything thats needed by but itself has no constrains to the user interface.
Such as paths and os tweaks. Mainly this is to thin out the ui module but also
to make functionality available without passing the main ui object.
"""
import os
import sys
import time
import logging

import a2path

# Only spot where this is set! Use a2core.get_logger() anywhere else!
LOG_LEVEL = logging.INFO
log = logging.getLogger(__name__)
log.setLevel(LOG_LEVEL)

A2DEFAULT_HOTKEY = 'Win+Shift+A'
_A2TAGS = {}
_IS_DEV = None
NAME = 'a2'
ENTRYPOINT_FILENAME = 'a2_entry.ahk'
ENTRYPOINT_TEMPLATE_NAME = 'a2_entry.template.ahk'
CUSTOM_DATA_FILENAME = 'a2_user_data.pth'
EDIT_DISCLAIMER = "; a2 {} - Don't bother editing! - File is generated automatically!\n{}"
SQL_DLL = 'sqlite3.dll'
SQL_INI = 'SQLiteDB.ini'
PACKAGE_CFG = 'pyproject.toml'


class A2Obj:
    """Non-Ui a2 backend object."""

    _instance = None

    @classmethod
    def inst(cls):
        """
        Return the singleton instance of A2Obj.

        :rtype: A2Obj
        """
        if A2Obj._instance is None:
            A2Obj._instance = A2Obj()
        return A2Obj._instance

    def __init__(self):
        if A2Obj._instance is not None:
            raise RuntimeError('A2Obj has already been initialized!\n  Use a2core.get() to get it!')

        import a2output

        self.app = None
        self.win = None
        self.module_sources = {}  # type: dict[str, a2modsource.ModSource]
        self._modules_fetched = 0.0
        self._enabled = None

        self.paths: Paths = Paths()
        self.urls = URLs(self.paths.a2_urls)
        self.log = a2output.get_logwriter()
        self._db = None
        self._version = None
        self._updates = {}
        log.info('A2Obj initialized!')

    def start_up(self):
        import a2db

        self.log.set_data_path(self.paths.data)
        self._db = a2db.A2db(self.paths.db)
        self._enabled = None
        self.fetch_modules()
        self.setup_proxy()
        log.info('A2Obj loaded with data path: "%s"', self.paths.data)

    def fetch_modules_if_stale(self):
        if time.time() - self._modules_fetched > 0.5:
            self.fetch_modules()
            self._modules_fetched = time.time()

    def fetch_modules(self):
        """
        Gets/Updates all module sources with their modules into
        self.module_sources. It looks like:

            {   'module_source1': a2Mod.ModSource,
                'module_source2': a2Mod.ModSource, ...}

        Then on a module source object:

            ModSource.mods = {'module1': a2Mod.Mod,
                              'module2': a2Mod.Mod, ...}
        """
        import a2modsource

        self.module_sources.clear()
        self.module_sources.update(a2modsource.get(self, self.paths.modules))
        self._modules_fetched = time.time()

    def get_module_obj(self, source_name: str, module_name: str):
        source = self.module_sources.get(source_name)
        if source is None:
            raise RuntimeError(f'No module source named "{source_name}"!')
        module = source.mods.get(module_name)
        if module is None:
            raise RuntimeError(f'Module source "{source_name}" has no module "{module_name}"!')
        return module

    @property
    def enabled(self):
        if self._enabled is None:
            self._enabled = self.db.get('enabled') or {}
        return self._enabled

    @enabled.setter
    def enabled(self, these):
        self._enabled = these
        self.db.set('enabled', these)

    @property
    def dev_mode(self):
        """Tell True/False if user dev-mode is enabled."""
        global _IS_DEV
        if _IS_DEV is None:
            _IS_DEV = self.db.get('dev_mode') or False
        return _IS_DEV

    def set_dev_mode(self, state):
        global _IS_DEV
        _IS_DEV = state
        self.db.set('dev_mode', state)

    def setup_proxy(self):
        """
        Look up a2.db "proxy_enabled" and "proxy_settings".
        Configure urllib.request accordingly.

        If set a2.db.get('proxy_settings') will give a dictionary::

            {'http': 'http', # or 'https'
            'user': 'username',
            'pass': 'p4$$w0Rd',
            'server': 'server.address.com',
            'port': 1337
            }

        Where 'user', 'pass' and 'port' might be optional!
        """
        if not (self.db.get('proxy_enabled') or False) and 'urllib.request' in sys.modules:
            from urllib import request

            log.info('disabling proxy ...')
            request.install_opener(None)  # ty:ignore[invalid-argument-type]
            return

        settings = self.db.get('proxy_settings') or {}
        server = settings.get('server')
        if not server:
            return

        from urllib import request

        http_mode = settings.get('http', '')
        proxy_str = http_mode + '://'

        usr, pwd = settings.get('user'), settings.get('pass')
        if usr and pwd:
            proxy_str += usr + ':' + pwd + '@'

        proxy_str += server

        port = settings.get('port')
        if port is not None:
            proxy_str += ':' + port

        log.info('setting up proxy: %s', proxy_str)
        proxy_handler = request.ProxyHandler({http_mode: proxy_str})
        opener = request.build_opener(proxy_handler)
        request.install_opener(opener)

    @property
    def db(self):
        """Return the database instance. Make sure to start up if None yet."""
        if self._db is None:
            self.start_up()
        assert self._db is not None
        return self._db

    def check_update(self):
        import a2download

        owner, repo = a2download.get_github_owner_repo(self.urls.a2)
        url = a2download.GITHUB_LATEST.format(owner=owner, repo=repo)
        data = a2download.get_remote_data(url)
        remote_version = data.get('tag_name')
        if remote_version != self.version:
            return remote_version
        return ''

    @property
    def version(self):
        if self._version is None:
            import tomllib

            with open(self.paths.package_cfg, 'rb') as file_obj:
                self._version = tomllib.load(file_obj)['project']['version']
        return self._version

    def check_all_updates(self):
        self._updates.update(
            {
                'core': {NAME: [self.version]},
                'sources': {s: [] for s in self.module_sources},
                'current': 0,
                'total': 1 + len(self.module_sources),
                'checked': time.time(),
            }
        )

        if self.is_git():
            self._updates['total'] += 3

        yield self._updates

        if self.is_git():
            log.info("Skipping a2 update check as we're in dev.")
        else:
            log.info('Checking for a2 updates ...')
            try:
                new_version = self.check_update()
                if new_version:
                    self._updates['core'][NAME].append(new_version)
                    yield self._updates
            except Exception:
                log.exception('Error checking for a2 update!')

        self._updates['current'] += 1
        yield self._updates

        log.info('Checking module package updates ...')
        for source_name, source in self.module_sources.items():
            self._updates['sources'][source_name].append(source.config.get('version'))
            if not source.is_git():
                try:
                    data = source.check_update()
                    if source.has_update:
                        version = data.get('version', '')
                        log.info('New "%s" %s module source package!', source_name, version)
                        self._updates['sources'][source_name].append(version)

                except FileNotFoundError:
                    pass
                except RuntimeError as error:
                    log.error('Checking "%s" resulted in: %s', source_name, error)

            self._updates['current'] += 1
            yield self._updates

        if self.is_git():
            import a2dev

            for name, current, latest in a2dev.check_dev_updates():
                self._updates['core'][name] = [current]
                if latest is not None:
                    self._updates['core'][name].append(latest)
                self._updates['current'] += 1
                yield self._updates
        return self._updates

    @property
    def updates(self):
        if not self._updates:
            self.check_all_updates()
        return self._updates

    def is_git(self):
        return os.path.isdir(self.paths.git)


def get() -> A2Obj:
    """Pass the core A2Obj instance."""
    return A2Obj.inst()


class URLs:
    """Internet addresses for various things."""

    def __init__(self, a2_urls_ahk):
        """
        Common a2 & ahk related web links.
        """
        import a2ahk

        variables_dict = a2ahk.get_variables(a2_urls_ahk)
        self.a2 = variables_dict.get('a2_url', 'https://github.com/ewerybody/a2')
        self.help = variables_dict.get('a2_help', (self.a2 + '#a2---'))
        self.wiki = self.a2 + '/wiki/'
        self.helpEditCtrl = self.wiki + 'EditCtrls'
        self.helpHotkey = self.wiki + 'Edit-Hotkey-Control'
        self.helpCheckbox = self.wiki + 'Edit-Checkbox-Control'
        self.help_scopes = self.wiki + 'Edit-Scopes'
        self.help_string = self.wiki + 'Edit-String'
        self.help_number = self.wiki + 'Edit-Number'
        self.help_path = self.wiki + 'Edit-Path'
        self.report_bug = self.a2 + '/issues/new/?labels=bug'
        self.report_suggestion = self.a2 + '/issues/new/?labels=improvement'
        self.gitter = 'https://gitter.im/ewerybody/a2'
        self.telegram = 'https://t.me/a2script_de'
        self.security = variables_dict.get('a2_security', '')
        self.latest_release = self.a2 + '/releases/latest'

        self.ahk = 'https://autohotkey.com'
        self.ahk_commands = self.ahk + '/docs/commands'
        self.ahk_run = self.ahk_commands + '/Run.htm'
        self.ahk_send = self.ahk_commands + '/Send.htm'
        self.ahkWinActive = self.ahk_commands + '/WinActive.htm'
        self.ahk_builtin_vars = self.ahk + '/docs/Variables.htm#BuiltIn'
        self.ahkWinTitle = self.ahk + '/docs/misc/WinTitle.htm'


class Paths:
    """Acquires and hosts common paths around a2."""

    def __init__(self):
        join = os.path.join
        self.ui = os.path.dirname(os.path.abspath(__file__))
        self.a2 = os.path.dirname(self.ui)
        self.a2exe = join(self.a2, 'a2.exe')
        self.a2uiexe = join(self.a2, 'a2ui.exe')
        self.widgets = join(self.ui, 'a2widget')
        self.elements = join(self.ui, 'a2element')

        self.lib: str = join(self.a2, 'lib')
        self.defaults: str = join(self.lib, 'defaults')
        self.a2_script: str = join(self.lib, 'a2.ahk')
        self.a2_urls: str = join(self.lib, 'a2_urls.ahk')
        self.a2_config: str = join(self.lib, 'a2_config.ahk')
        self.autohotkey: str = join(self.lib, 'Autohotkey', 'Autohotkey.exe')
        self.python: str = sys.executable
        self.git: str = join(self.a2, '.git')
        self.uninstaller: str = join(self.a2, 'Uninstall a2.exe')
        self.package_cfg: str = join(self.a2, PACKAGE_CFG)

        # get data dir from user include file in a2 root
        self.portable_data: str = join(self.a2, 'data')
        self.local_user_data: str = join(os.getenv('LOCALAPPDATA', ''), NAME, 'data')
        self.custom_path_cfg: str = join(self.local_user_data, CUSTOM_DATA_FILENAME)
        self.data = ''
        self._build_data_paths()
        self._test_dirs()

    def _build_data_paths(self):
        try:
            self.data = self.get_data_path()
        except FileNotFoundError:
            self.data = self.portable_data
        os.makedirs(self.data, exist_ok=True)

        join = os.path.join
        self.modules = join(self.data, 'modules')
        self.module_data = join(self.data, 'module_data')
        self.includes = join(self.data, 'includes')
        self.temp = join(self.data, 'temp')
        self.db = join(self.data, NAME + '.db')
        self.user_cfg = join(self.data, NAME + '.cfg')

    def _test_dirs(self):
        # test if all necessary directories are present:
        main_items = [self.a2_script, self.lib, self.ui]
        missing = [p for p in main_items if not os.path.exists(p)]
        if missing:
            raise RuntimeError('a2ui start interrupted! %s Not found in main dir!' % missing)
        if os.path.isdir(self.data) and not os.access(self.data, os.W_OK):
            raise RuntimeError('a2ui start interrupted! %s inaccessible!' % self.data)

    def set_data_path(self, path: str = '') -> None:
        """
        Make sure currently set user data path can be included by runtime and
        some standard files are available.
        """
        self.data = self.local_user_data if not path else path
        self._write_entrypoint()
        self._build_data_paths()

        if os.path.isfile(self.user_cfg):
            return
        with open(os.path.join(self.defaults, NAME + '.cfg')) as src_file_obj:
            with open(self.user_cfg, 'w') as dst_file_obj:
                dst_file_obj.write(src_file_obj.read())

    def get_data_path(self) -> str:
        """
        Establish user data path.
        * If there is a portable entry point file: We're portable!
        * If there is a custom path file in {LOCALAPPDATA}\\a2\\data
            * read the file, return path
        * Otherwise its {LOCALAPPDATA}\\a2\\data
        """
        portable_entry = os.path.join(self.portable_data, ENTRYPOINT_FILENAME)
        if os.path.isfile(portable_entry):
            return self.portable_data

        if not self.has_data_override():
            return self.local_user_data

        with open(self.custom_path_cfg) as file_obj:
            custom_path = file_obj.read()
            if os.path.isdir(custom_path):
                return custom_path
        return self.local_user_data

    def has_data_override(self):
        return os.path.isfile(self.custom_path_cfg)

    def _write_entrypoint(self):
        """Write Autohotkey entry file to point to the right data path.

        * `self.data` was just set
        * if its outside of app_dir
            * remove entry file from {app_dir}\\data
            * write entry file to {LOCALAPPDATA}\\a2\\data
              No matter where it data should point!
        * else if in app_dir (portable mode)
            * remove entry file from {LOCALAPPDATA}\\a2\\data
            * write entry file to {app_dir}\\data
        """
        try:
            data_path = os.path.relpath(self.data, self.a2)
            if data_path.startswith('.'):
                data_path = self.data
        except ValueError:
            data_path = self.data

        portable_entry = os.path.join(self.portable_data, ENTRYPOINT_FILENAME)
        installed_entry = os.path.join(self.local_user_data, ENTRYPOINT_FILENAME)

        is_portable = a2path.is_same(self.data, self.portable_data)
        if is_portable:
            target, cleanup = portable_entry, [installed_entry, self.custom_path_cfg]
        else:
            target, cleanup = installed_entry, [portable_entry]
            if a2path.is_same(data_path, self.local_user_data):
                cleanup.append(self.custom_path_cfg)
            else:
                with open(self.custom_path_cfg, 'w', encoding='utf8') as file_obj:
                    file_obj.write(self.data)

        template_path = os.path.join(self.defaults, ENTRYPOINT_TEMPLATE_NAME)
        with open(template_path) as file_obj:
            template = EDIT_DISCLAIMER.format(ENTRYPOINT_FILENAME, file_obj.read())

        write_if_changed(target, template.format(data_path=data_path, lib_path=self.lib))

        for cleanup_path in cleanup:
            if not os.path.isfile(cleanup_path):
                continue
            os.unlink(cleanup_path)


def get_logger(name: str):
    # make sure logging is initialized
    if not logging.root.handlers:
        logging.basicConfig()

    # make bend name == __main__-runs to actual module name
    if name == '__main__':
        try:
            frame = sys._getframe(1)
            print('frame.f_code.co_filename: %s' % frame.f_code.co_filename)
            dirpath, base = os.path.split(frame.f_code.co_filename)
            name = os.path.splitext(base)[0]
            if name == '__init__':
                name = os.path.basename(dirpath)
        except AttributeError:
            pass

    new_log = logging.getLogger(name)
    new_log.setLevel(LOG_LEVEL)
    return new_log


def set_loglevel(debug: bool = False):
    level = [logging.INFO, logging.DEBUG][debug]
    for name, logger in log.manager.loggerDict.items():
        if name.startswith(NAME) and isinstance(logger, logging.Logger):
            try:
                logger.setLevel(level)
                log.debug('"%s" Log level DEBUG: active', name)
                log.info('"%s" Log level INFO: active', name)
            except AttributeError as error:
                if not isinstance(logger, logging.PlaceHolder):
                    log.info(
                        'Could not set log level on logger object "%s": %s',
                        name,
                        str(logger),
                    )
                    log.error(error)


def is_dev_mode():
    """
    Check for developer mode flag without the ui or a2 obj.
    :rtype: bool
    """
    global _IS_DEV
    if _IS_DEV is None:
        a2 = A2Obj.inst()
        return a2.dev_mode
    return _IS_DEV


def set_dev_mode(state):
    """
    Sets developer mode flag without the ui or a2 obj.
    :param bool state: True/False developer mode flag on/off.
    """
    a2 = A2Obj.inst()
    a2.set_dev_mode(state)


def is_debugging():
    """Tell if there is a debugger attached."""
    gettrace = getattr(sys, 'gettrace', None)
    return gettrace is not None and gettrace() is not None


def write_if_changed(path: str, content: str):
    """Write file at given `path` when needed.
    That is: file does not exist or file has different `content`."""
    if os.path.isfile(path):
        with open(path) as file_obj:
            if file_obj.read() == content:
                return False
        log.debug('Updating "%s"', os.path.basename(path))
    else:
        log.debug('Creating "%s"', os.path.basename(path))

    with open(path, 'w') as file_obj:
        file_obj.write(content)

    return True


def tags():
    if not _A2TAGS:
        import a2util

        a2 = A2Obj.inst()
        _A2TAGS.update(a2util.json_read(os.path.join(a2.paths.defaults, 'tags.json')))
    return _A2TAGS
