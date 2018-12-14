"""
a2core - Foundation module to host basic info and functionality

Everything thats needed by but itself has no constrains to the user interface.
Such as paths and os tweaks. Mainly this is to thin out the ui module but also
to make functionality available without passing the main ui object.

@created: 15.03.2016
@author: eric
"""
import os
import sys
import logging

# only spot where this is set! Use a2core.get_logger() anywhere else!
LOG_LEVEL = logging.INFO
log = logging.getLogger(__name__)
log.setLevel(LOG_LEVEL)

a2ahk, a2db, a2mod = None, None, None

A2DEFAULT_HOTKEY = 'Win+Shift+A'
A2TAGS = {'file': 'File system',
          'window': 'Window handling',
          'text': 'Text manipulation',
          'code': 'Programming',
          'lookup': 'Searching things',
          'web': 'Internet related',
          'wip': 'Experimental'}
_IS_DEV = None


class A2Obj(object):
    _instance = None

    @classmethod
    def inst(cls):
        """
        Returns the singleton instance of A2Obj.

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
        global a2ahk, a2db, a2mod
        import a2ahk, a2db, a2mod
        self.app = None
        self.win = None
        self.module_sources = {}

        self.paths = Paths()
        self.urls = URLs(self.paths.a2_urls)

        self.db = a2db.A2db(self.paths.db)
        self._enabled = None
        log.info('A2Obj initialised!')

    def start_up(self):
        self.fetch_modules()

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
        a2mod.get_module_sources(self, self.paths.modules, self.module_sources)

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


class URLs(object):
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


class Paths(object):
    """
    Aquires and hosts common paths around a2.
    """
    def __init__(self):
        self.ui = os.path.dirname(os.path.abspath(__file__))
        self.a2 = os.path.dirname(self.ui)
        self.widgets = os.path.join(self.ui, 'a2widget')
        self.elements = os.path.join(self.ui, 'a2element')

        self.lib = os.path.join(self.a2, 'lib')
        self.defaults = os.path.join(self.lib, '_defaults')
        self.a2_script = os.path.join(self.lib, 'a2.ahk')
        self.a2_urls = os.path.join(self.lib, 'a2_urls.ahk')
        self.a2_config = os.path.join(self.lib, 'a2_config.ahk')
        self.autohotkey = os.path.join(self.lib, 'Autohotkey', 'Autohotkey.exe')
        self.python = sys.executable

        # get data dir from config override or the default appdata dir.
        _data = os.path.join(os.getenv('LOCALAPPDATA'), 'a2', 'data')
        try:
            self.data = a2ahk.get_variables(
                os.path.join(_data, 'a2_data_path.ahk')).get('a2data')
        except FileNotFoundError:
            self.data = _data
        self.modules = os.path.join(self.data, 'modules')
        self.module_data = os.path.join(self.data, 'module_data')
        self.includes = os.path.join(self.data, 'includes')
        self.temp = os.path.join(self.data, 'temp')
        self.db = os.path.join(self.data, 'a2.db')

        # test if all necessary directories are present:
        main_items = [self.a2_script, self.lib, self.ui]
        missing = [p for p in main_items if not os.path.exists(p)]
        if missing:
            raise RuntimeError('a2ui start interrupted! %s not found in main dir!'
                               % missing)
        if os.path.isdir(self.data) and not os.access(self.data, os.W_OK):
            raise RuntimeError('a2ui start interrupted! %s inaccessable!'
                               % self.data)


def _dbCleanup():
    a2 = A2Obj.inst()
    for table in a2.db.tables():
        if table == 'a2':
            a2.db.pop('aValue')
            enabled = a2.db.get('enabled', asjson=False) or ''
            if not enabled.startswith('{'):
                a2.db.set('enabled', {})
            else:
                enabled = a2.db.get('enabled')
                write = False
                for name, data in enabled.items():
                    if not isinstance(data, list) or not data:
                        log.error('Bad data: %s: "%s"' % (name, data))
                        enabled[name] = [False, []]
                        write = True
                    if not isinstance(data[0], bool):
                        enabled[name] = [False] + data[1:]
                        write = True
                    if not isinstance(data[1], list):
                        enabled[name] = data[0] + [[]]
                        write = True
                    if len(data) > 2:
                        log.error('Too much data: %s: "%s"' % (name, data))
                        enabled[name] = data[:2]
                        write = True
                if write:
                    a2.db.set('enabled', enabled)
            continue

        includes = a2.db.get('includes', table, asjson=False)
        include = a2.db.get('include', table, asjson=False)

        # turn string separated entries into lists
        if includes is None and include is not None:
            includes = include.split('|')
        elif includes is not None and not includes.startswith('['):
            includes = includes.split('|')
        elif includes == '[""]':
            includes = []

        if isinstance(includes, list):
            a2.db.set('includes', includes, table)

        if include is not None:
            a2.db.pop('include', table)


def get_logger(name):
    newlog = logging.getLogger(name)
    newlog.setLevel(LOG_LEVEL)
    return newlog


def set_loglevel(debug=False):
    level = [logging.INFO, logging.DEBUG][debug]
    for name, logger in log.manager.loggerDict.items():
        if name.startswith('a2'):
            try:
                logger.setLevel(level)
                log.debug(f'"{name}" Log level DEBUG: active')
                log.info(f'"{name}" Log level INFO: active')
            except AttributeError as error:
                if not isinstance(logger, logging.PlaceHolder):
                    log.info('Could not set log level on logger object "%s": %s' % (name, str(logger)))
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
