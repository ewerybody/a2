"""
a2core - Foundation module to host basic info and functionality.

Everything thats needed by but itself has no constrains to the user interface.
Such as paths and os tweaks. Mainly this is to thin out the ui module but also
to make functionality available without passing the main ui object.

@created: 15.03.2016
@author: eric
"""
import os
import sys
import time
import logging

# only spot where this is set! Use a2core.get_logger() anywhere else!
LOG_LEVEL = logging.INFO
log = logging.getLogger(__name__)
log.setLevel(LOG_LEVEL)

a2ahk, a2db, a2mod, a2modsource = None, None, None, None

A2DEFAULT_HOTKEY = 'Win+Shift+A'
A2TAGS = {
    'file': 'File system',
    'window': 'Window handling',
    'text': 'Text manipulation',
    'code': 'Programming',
    'lookup': 'Searching things',
    'web': 'Internet related',
    'wip': 'Experimental'}
_IS_DEV = None
NAME = 'a2'

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
            raise RuntimeError('Singleton A2Obj has already been initialized!\n'
                               '  Use A2Obj.inst() to get the instance!')

        # lazy import so importing a2core does not depend on other a2 module
        # pylint: disable=invalid-name,global-statement,redefined-outer-name,multiple-imports
        global a2ahk, a2db, a2mod, a2modsource
        import a2ahk, a2db, a2mod, a2modsource
        import a2output
        self.app = None
        self.win = None
        self.module_sources = {}
        self._modules_fetched = 0.0

        self.paths = Paths()
        self.urls = URLs(self.paths.a2_urls)
        self.log = a2output.get_logwriter()
        self._db = None
        log.info('A2Obj initialised!')

    def start_up(self):
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
        self.module_sources.clear()
        self.module_sources.update(a2modsource.get(self, self.paths.modules))
        self._modules_fetched = time.time()

    def get_module_obj(self, source_name, module_name):
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
        Looks up a2.db "proxy_enabled" and "proxy_settings".
        Configures urllib.request accordingly.

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

                http_mode = settins.get('http')
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
        if self._db is None:
            self.start_up()
        return self._db


class URLs:
    """Internet adresses for various things."""
    def __init__(self, a2_urls_ahk):
        """
        Common a2 & ahk related web links.
        """
        variables_dict = a2ahk.get_variables(a2_urls_ahk)
        self.a2 = variables_dict.get('a2_url', 'https://github.com/ewerybody/a2')
        self.help = variables_dict.get('a2_help', (self.a2 + '#a2--'))
        self.wiki = self.a2 + '/wiki/'
        self.helpEditCtrl = self.wiki + 'EditCtrls'
        self.helpHotkey = self.wiki + 'Edit-Hotkey-Control'
        self.helpCheckbox = self.wiki + 'Edit-Checkbox-Control'
        self.help_scopes = self.wiki + 'Edit-Scopes'
        self.help_string = self.wiki + 'Edit-String'
        self.help_number = self.wiki + 'Edit-Number'
        self.help_path = self.wiki + 'Edit-Path'
        self.help_report_issue = self.a2 + '/issues/new'
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
        self.ui = os.path.dirname(os.path.abspath(__file__))
        self.a2 = os.path.dirname(self.ui)
        self.a2exe = os.path.join(self.a2, 'a2.exe')
        self.a2uiexe = os.path.join(self.a2, 'a2ui.exe')
        self.widgets = os.path.join(self.ui, 'a2widget')
        self.elements = os.path.join(self.ui, 'a2element')

        self.lib = os.path.join(self.a2, 'lib')
        self.defaults = os.path.join(self.lib, '_defaults')
        self.a2_script = os.path.join(self.lib, 'a2.ahk')
        self.a2_urls = os.path.join(self.lib, 'a2_urls.ahk')
        self.a2_config = os.path.join(self.lib, 'a2_config.ahk')
        self.autohotkey = os.path.join(self.lib, 'Autohotkey', 'Autohotkey.exe')
        self.python = sys.executable
        self.git = os.path.join(self.a2, '.git')

        # get data dir from config override or the default appdata dir.
        self.default_data = os.path.join(os.getenv('LOCALAPPDATA'), NAME, 'data')
        self.data_override_file = os.path.join(self.default_data, 'a2_data_path.ahk')
        self.data = None
        self._build_data_paths()
        self._test_dirs()

    def _build_data_paths(self):
        try:
            self.data = self.get_data_override_path()
        except FileNotFoundError:
            self.data = self.default_data
        os.makedirs(self.data, exist_ok=True)

        self.modules = os.path.join(self.data, 'modules')
        self.module_data = os.path.join(self.data, 'module_data')
        self.includes = os.path.join(self.data, 'includes')
        self.temp = os.path.join(self.data, 'temp')
        self.db = os.path.join(self.data, 'a2.db')

    def _test_dirs(self):
        # test if all necessary directories are present:
        main_items = [self.a2_script, self.lib, self.ui]
        missing = [p for p in main_items if not os.path.exists(p)]
        if missing:
            raise RuntimeError(
                'a2ui start interrupted! %s Not found in main dir!' % missing)
        if os.path.isdir(self.data) and not os.access(self.data, os.W_OK):
            raise RuntimeError(
                'a2ui start interrupted! %s inaccessable!' % self.data)

    def set_data_override(self, path):
        if not path:
            if os.path.isfile(self.data_override_file):
                os.remove(self.data_override_file)
                self.data = self.default_data
        else:
            a2ahk.set_variable(self.data_override_file, 'a2data', path)
            self.data = path
        self._build_data_paths()

    def get_data_override_path(self):
        return a2ahk.get_variables(self.data_override_file).get('a2data')

    def has_data_override(self):
        return self.data != self.default_data


def get_logger(name):
    newlog = logging.getLogger(name)
    newlog.setLevel(LOG_LEVEL)
    return newlog


def set_loglevel(debug=False):
    level = [logging.INFO, logging.DEBUG][debug]
    for name, logger in log.manager.loggerDict.items():
        if name.startswith(NAME):
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
    Checks for developer mode flag without the ui or a2 obj.
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


if __name__ == '__main__':
    import a2app
    a2app.main()
