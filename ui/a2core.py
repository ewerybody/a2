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

# Only spot where this is set! Use a2core.get_logger() anywhere else!
LOG_LEVEL = logging.INFO
log = logging.getLogger(__name__)
log.setLevel(LOG_LEVEL)

A2DEFAULT_HOTKEY = 'Win+Shift+A'
_A2TAGS = {}
_IS_DEV = None
NAME = 'a2'
ENTRYPOINT_FILENAME = 'user_data_include'
USER_INCLUDES_NAME = 'a2_user_includes.ahk'
EDIT_DISCLAIMER = "; a2 %s - Don't bother editing! - File is generated automatically!\n"
DATA_PATTERN = '{a2data}'
SQLDLL = 'sqlite3.dll'
SQLINI = 'SQLiteDB.ini'
PACKAGE_CFG = 'package.json'


def get():
    """Pass the core A2Obj instance."""
    return A2Obj.inst()


# pylint: disable=too-many-instance-attributes
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
            raise RuntimeError(
                'Singleton A2Obj has already been initialized!\n'
                '  Use A2Obj.inst() to get the instance!'
            )

        import a2output

        self.app = None
        self.win = None
        self.module_sources = {}
        self._modules_fetched = 0.0
        self._enabled = None

        self.paths = Paths()
        self.urls = URLs(self.paths.a2_urls)
        self.log = a2output.get_logwriter()
        self._db = None
        log.info('A2Obj initialised!')

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
        if self.db.get('proxy_enabled') or False:
            settins = self.db.get('proxy_settings') or {}
            server = settins.get('server')
            if server:
                from urllib import request

                http_mode = settins.get('http', '')
                proxy_str = http_mode + '://'

                usr, pwd = settins.get('user'), settins.get('pass')
                if usr and pwd:
                    proxy_str += usr + ':' + pwd + '@'

                proxy_str += server

                port = settins.get('port')
                if port is not None:
                    proxy_str += ':' + port

                log.info('setting up proxy: %s', proxy_str)
                proxy_handler = request.ProxyHandler({http_mode: proxy_str})
                opener = request.build_opener(proxy_handler)
                request.install_opener(opener)
                return

        if 'urllib.request' in sys.modules:
            from urllib import request

            log.info('disabling proxy ...')
            request.install_opener(None)

    @property
    def db(self):
        """Return the database instance. Make sure to start up if None yet."""
        if self._db is None:
            self.start_up()
        assert self._db is not None
        return self._db

    def check_update(self):
        import a2util
        import a2download

        owner, repo = a2download.get_github_owner_repo(self.urls.a2)
        url = a2download.GITHUB_LATEST.format(owner=owner, repo=repo)
        data = a2download.get_remote_data(url)
        remote_version = data.get('tag_name')
        current = a2util.json_read(self.paths.package_cfg).get('version')
        if remote_version != current:
            return remote_version
        return ''


class URLs:
    """Internet adresses for various things."""

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
        self.report_sugg = self.a2 + '/issues/new/?labels=improvement'
        self.gitter = 'https://gitter.im/ewerybody/a2'
        self.telegram = 'https://t.me/a2script_de'
        self.security = variables_dict.get('a2_security', '')

        self.ahk = 'https://autohotkey.com'
        self.ahk_commands = self.ahk + '/docs/commands'
        self.ahk_run = self.ahk_commands + '/Run.htm'
        self.ahk_send = self.ahk_commands + '/Send.htm'
        self.ahkWinActive = self.ahk_commands + '/WinActive.htm'
        self.ahk_builtin_vars = self.ahk + '/docs/Variables.htm#BuiltIn'
        self.ahkWinTitle = self.ahk + '/docs/misc/WinTitle.htm'


class Paths:
    """Aquires and hosts common paths around a2."""

    def __init__(self):
        join = os.path.join
        self.ui = os.path.dirname(os.path.abspath(__file__))
        self.a2 = os.path.dirname(self.ui)
        self.a2exe = join(self.a2, 'a2.exe')
        self.a2uiexe = join(self.a2, 'a2ui.exe')
        self.widgets = join(self.ui, 'a2widget')
        self.elements = join(self.ui, 'a2element')

        self.lib = join(self.a2, 'lib')
        self.defaults = join(self.lib, 'defaults')
        self.a2_script = join(self.lib, 'a2.ahk')
        self.a2_urls = join(self.lib, 'a2_urls.ahk')
        self.a2_config = join(self.lib, 'a2_config.ahk')
        self.autohotkey = join(self.lib, 'Autohotkey', 'Autohotkey.exe')
        self.python = sys.executable
        self.git = join(self.a2, '.git')
        self.uninstaller = join(self.a2, 'Uninstall a2.exe')
        self.package_cfg = join(self.a2, PACKAGE_CFG)

        # get data dir from user include file in a2 root
        self.default_data = join(self.a2, 'data')
        self.local_user_data = join(os.getenv('LOCALAPPDATA', ''), NAME, 'data')
        self.user_includes = join(self.a2, '_ user_data_include')
        self.data = ''
        self._build_data_paths()
        self._test_dirs()

    def _build_data_paths(self):
        try:
            self.data = self.get_data_path()
        except FileNotFoundError:
            self.data = self.default_data
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
            raise RuntimeError('a2ui start interrupted! %s inaccessable!' % self.data)

    def set_data_path(self, path: str = ''):
        """
        Make sure currently set user data path can be included by runtime and
        some standard files are available.
        """
        self.data = self.default_data if not path else path
        self._write_entrypoint()
        self._build_data_paths()

        if not os.path.isfile(self.user_cfg):
            with open(os.path.join(self.defaults, NAME + '.cfg')) as src_file_obj:
                with open(self.user_cfg, 'w') as dst_file_obj:
                    dst_file_obj.write(src_file_obj.read())
        self.write_user_include()

    def write_user_include(self):
        with open(os.path.join(self.defaults, USER_INCLUDES_NAME)) as src_file_obj:
            write_if_changed(
                os.path.join(self.data, USER_INCLUDES_NAME),
                src_file_obj.read().format(a2data=self.data),
            )

    def get_data_path(self):
        if os.path.isfile(self.user_includes):
            include_key = '#include '
            with open(self.user_includes) as file_obj:
                line = file_obj.readline().strip()
                while line and not line.startswith(include_key):
                    line = file_obj.readline().strip()
            if not line.startswith(include_key):
                return self.default_data

            path = line[len(include_key) :]
            if os.path.isabs(path):
                return path

            return os.path.abspath(os.path.join(self.a2, path))

        return self.default_data

    def has_data_override(self):
        return self.data != self.default_data

    def _write_entrypoint(self):
        """Write `_ user_data_include` file to point to the right data path.
        Write SQLiteDB.ini with path to its needed .dll file."""
        try:
            data_path = os.path.relpath(self.data, self.a2)
            if data_path.startswith('.'):
                data_path = self.data
        except ValueError:
            data_path = self.data

        tmpl8_path = os.path.join(self.defaults, ENTRYPOINT_FILENAME + '.template')
        with open(tmpl8_path) as file_obj:
            tmpl8 = EDIT_DISCLAIMER % ENTRYPOINT_FILENAME + file_obj.read()
        write_if_changed(
            os.path.join(self.a2, '_ ' + ENTRYPOINT_FILENAME), tmpl8.format(data_path=data_path)
        )

        dll_path = os.path.join(self.ui, SQLDLL)
        if not os.path.isfile(dll_path):
            dll_path = os.path.join(os.path.dirname(self.python), 'DLLs', SQLDLL)
        assert os.path.isfile(dll_path)
        write_if_changed(os.path.join(self.lib, SQLINI), f'[Main]\nDllPath={dll_path}')


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

    newlog = logging.getLogger(name)
    newlog.setLevel(LOG_LEVEL)
    return newlog


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
                    log.info('Could not set log level on logger object "%s": %s', name, str(logger))
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



def check_for_updates():
    a2 = A2Obj.inst()

    # Only check for new a2 release when not dev/no .git present:
    if not os.path.isdir(a2.paths.git):
        new_version = a2.check_update()
        if new_version:
            yield 'core', {'a2': new_version}

    log.info('Checking module package updates ...')
    for source_name, source in a2.module_sources.items():
        try:
            data = source.check_update()
            if source.has_update:
                version = data.get('version', '')
                log.info('New "%s" %s module source package', source_name, version)
                yield 'sources', {source_name: version}
            else:
                yield 'sources', None
        except FileNotFoundError:
            continue

    if a2.dev_mode and os.path.isdir(a2.paths.git):
        import a2dev

        for name, version in a2dev.check_dev_updates():
            yield 'core', {name: version}
