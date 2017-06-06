"""
a2core - Foundation module to host basic info and functionality

Everything thats needed by but itself has no constrains to the user interface.
Such as paths and os tweaks. Mainly this is to thin out the ui module but also
to make functionality available without passing the main ui object.

@created: 15.03.2016
@author: eric
"""
import os
import logging
from os.path import exists, join, dirname, abspath, relpath
import codecs

# only spot where this is set! Use a2core.get_logger() anywhere else!
LOG_LEVEL = logging.INFO
log = logging.getLogger(__name__)
log.setLevel(LOG_LEVEL)

a2ahk, a2db, a2mod = None, None, None

edit_disclaimer = "; a2 %s.ahk - Don't bother editing! - File is generated automatically!"
a2default_hotkey = 'Win+Shift+A'

a2tags = {'file': 'File system',
          'window': 'Window handling',
          'text': 'Text manipulation',
          'code': 'Programming',
          'lookup': 'Searching things',
          'web': 'Internet related',
          'wip': 'Experimental'}


class A2Obj(object):
    _instance = None

    @classmethod
    def inst(cls):
        if A2Obj._instance is None:
            A2Obj._instance = A2Obj()
        return A2Obj._instance

    def __init__(self):
        # lazy import so importing a2core does not depend on other a2 module
        global a2ahk, a2db, a2mod
        import a2ahk
        import a2db
        import a2mod
        self.app = None
        self.win = None
        self.module_sources = {}

        self.paths = Paths()
        self.urls = URLs(self.paths.urls_ahk)

        self.db = a2db.A2db(self.paths.db)
        self._enabled = None

    def start_up(self):
        self.fetch_modules()
        self.get_used_scopes()
        self.get_used_hotkeys()

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

    def get_used_scopes(self):
        """
        browses the hotkey setups of enabled modules for scope strings
        TODO: this type of lookup can also be used to get hold of used hotkeys...
        """
        self.scopes = {}
        for modname in self.enabled:
            hotkeys = self.db.get('hotkeys', modname)
            if not hotkeys:
                continue
            for i in ['1', '2']:
                for hksetup in hotkeys.get(i) or []:
                    for scope in hksetup[0]:
                        if scope not in self.scopes:
                            self.scopes[scope] = set([modname])
                        else:
                            self.scopes[scope].add(modname)
        return self.scopes

    def get_used_hotkeys(self):
        """
        wip - for a proper hotkey list we might need more than a list. You'd also wanna
        know what the hotkey does... shouldn't our data structure care for this right away?
        """
        self.hotkeys = set()
        for modname in self.enabled:
            hotkeys = self.db.get('hotkeys', modname)
            if not hotkeys:
                continue
            for i in ['1', '2']:
                for hksetup in hotkeys.get(i) or []:
                    self.hotkeys.add(hksetup[1])
            for hksetup in hotkeys.get('0') or []:
                self.hotkeys.add(hksetup[0])
        return self.hotkeys

    @property
    def enabled(self):
        if self._enabled is None:
            self._enabled = self.db.get('enabled') or {}
        return self._enabled

    @enabled.setter
    def enabled(self, these):
        self._enabled = these
        self.db.set('enabled', these)


class URLs(object):
    def __init__(self, a2_urls_ahk):
        """
        Common a2 & ahk related web links.
        """
        variables_dict = a2ahk.get_variables(a2_urls_ahk)
        self.a2 = variables_dict.get('a2_url', 'https://github.com/ewerybody/a2')
        self.help = variables_dict.get('a2_help', (self.a2 + '#a2-'))
        self.helpEditCtrl = self.a2 + '/wiki/EditCtrls'
        self.helpHotkey = self.a2 + '/wiki/Edit-Hotkey-Control'
        self.helpCheckbox = self.a2 + '/wiki/Edit-Checkbox-Control'
        self.helpScopes = self.a2 + '/wiki/Edit-Scopes'
        self.help_string = self.a2 + '/wiki/Edit-String'
        self.help_number = self.a2 + '/wiki/Edit-Number'
        self.help_path = self.a2 + '/wiki/Edit-Path'
        self.help_report_issue = self.a2 + '/issues/new'

        self.ahk = 'https://autohotkey.com'
        self.ahk_commands = self.ahk + '/docs/commands'
        self.ahk_run = self.ahk_commands + '/Run.htm'
        self.ahksend = self.ahk_commands + '/Send.htm'
        self.ahkWinActive = self.ahk_commands + '/WinActive.htm'
        self.ahk_builtin_vars = self.ahk + '/docs/Variables.htm#BuiltIn'
        self.ahkWinTitle = self.ahk + '/docs/misc/WinTitle.htm'


class Paths(object):
    """
    Aquires and hosts common paths around a2.
    """
    def __init__(self):
        self.ui = dirname(abspath(__file__))
        self.elements = join(self.ui, 'a2element')
        self.widgets = join(self.ui, 'a2widget')
        self.a2 = dirname(self.ui)
        self.lib = join(self.a2, 'lib')
        self.settings_ahk = os.path.join(self.a2, 'settings', 'a2_settings.ahk')
        self._defaults = join(self.lib, '_defaults')
        self.urls_ahk = os.path.join(self._defaults, 'a2_urls.ahk')
        self.a2_script = join(self.lib, 'a2.ahk')

        path_vars = self._fetch_a2_setting_paths()
        self.settings = path_vars['settings']
        self.modules = path_vars['modules']
        self.autohotkey = path_vars['ahk']
        self.python = path_vars['python']

        # test if all necessary directories are present:
        main_items = [self.a2_script, self.lib, self.modules, self.settings, self.ui]
        missing = [p for p in main_items if not exists(p)]
        if missing:
            raise Exception('a2ui start interrupted! %s not found in main dir!'
                            % missing)
        if not os.access(self.settings, os.W_OK):
            raise Exception('a2ui start interrupted! %s inaccessable!'
                            % self.settings)

        self.db = join(self.settings, 'a2.db')

    def _get_settings_ahk(self):
        if not exists(self.settings_ahk):
            return os.path.join(self._defaults, 'a2_settings.ahk')
        return self.settings_ahk

    def _fetch_a2_setting_paths(self):
        keys = ['settings', 'modules']
        prefix = 'a2_'
        result = {}
        settings_dict = a2ahk.get_variables(self._get_settings_ahk())
        for key, value in settings_dict.items():
            key = key[len(prefix):]
            if key in keys:
                if os.path.isabs(value):
                    result[key] = value
                else:
                    result[key] = os.path.abspath(os.path.join(self.a2, value))
        result['ahk'] = settings_dict.get('a2_ahk') or os.path.join(self.lib, 'Autohotkey', 'Autohotkey.exe')
        # Python path can be relative! So we take anything here.
        result['python'] = settings_dict.get('a2_python')
        return result


class IncludeDataCollector(object):
    def __init__(self):
        self.a2 = A2Obj.inst()
        self.a2.fetch_modules()

        self.variables = None
        self.libs = None
        self.includes = None
        self.hotkeys = None
        self.init = None
        self.all_collections = [self.variables, self.libs, self.includes, self.hotkeys, self.init]

    def init_all_collections(self):
        self.variables = VariablesCollection(self.a2)
        self.libs = LibsCollection(self.a2)
        self.includes = IncludesCollection(self.a2)
        self.hotkeys = HotkeysCollection(self.a2)
        self.init = InitCollection(self.a2)



    def collect(self):
        mod_settings = self.a2.db.tables()

        for source_name, data in self.a2.enabled.items():
            source_enabled, enabled_modules = data
            if not source_enabled:
                continue

            source = self.a2.module_sources.get(source_name)
            if source is None:
                log.debug('Source: "%s" is enabled but missing!' % source_name)
                continue

            for modname in enabled_modules:
                if modname not in source.mods:
                    continue

                mod = source.mods[modname]
                if mod.key not in mod_settings:
                    mod.change()

                for collection in self.all_collections:
                    if collection is None:
                        continue
                    collection.gather(mod)


class _Collection(object):
    def __init__(self, a2obj_instance):
        self.a2 = a2obj_instance
        self.name = None
        self.content = ''

    def write(self):
        path = os.path.join(self.a2.paths.settings, self.name + '.ahk')
        with codecs.open(path, 'w', encoding='utf-8-sig') as fobj:
            fobj.write(self.content)


class VariablesCollection(_Collection):
    def __init__(self, a2obj_instance):
        super(VariablesCollection, self).__init__(a2obj_instance)
        self.name = 'variables'


def write_includes(specific=None):
    """
    For each enabled module writes available data to the
    hotkey, include, variables or libs .ahk include files
    """
    a2 = A2Obj.inst()
    a2.fetch_modules()

    hkmode = {'1': '#IfWinActive,', '2': '#IfWinNotActive,'}

    include_ahk = [edit_disclaimer % 'includes']
    a2_hotkey = a2ahk.translate_hotkey(a2.db.get('a2_hotkey') or a2default_hotkey)
    hotkeys_ahk = {hkmode['1']: [a2_hotkey + '::a2UI()']}
    variables_ahk = [edit_disclaimer % 'variables']
    # TODO: this needs to be implemented dynamically
    libs_ahk = [edit_disclaimer % 'libs']
    libs_ahk += ['#include lib/ahklib/%s.ahk' % lib for lib in
                 ['a2', 'tt', 'functions', 'Explorer_Get', 'ahk_functions', 'ObjectTools',
                  'RichObject', 'Array', 'uri_encode', 'HTTPRequest', 'base64']]
    init_ahk = edit_disclaimer % 'init' + '\na2_init_calls() {\n'

    # browse the enabled modules to collect the include data
    mod_settings = a2.db.tables()
    mod_path = relpath(a2.paths.modules, a2.paths.a2)
    settings_path = relpath(a2.paths.settings, a2.paths.a2)

    for source_name, data in a2.enabled.items():
        source_enabled, enabled_modules = data
        if not source_enabled:
            continue

        source = a2.module_sources.get(source_name)
        if source is None:
            log.debug('Source: "%s" is enabled but missing!' % source_name)
            continue

        for modname in enabled_modules:
            if modname not in source.mods:
                continue

            module = source.mods[modname]
            if module.key not in mod_settings:
                module.change()

            for include_type, include_dir in [('includes', os.path.join(mod_path, source.name, modname)),
                                              ('settings_includes', settings_path)]:
                includes = a2.db.get(include_type, module.key) or []
                if not isinstance(includes, list):
                    log.warn('%s not a list: %s' % (include_type, includes))
                    includes = [includes]

                for include in includes:
                    include_path = os.path.join(include_dir, include)
                    include_ahk += ['#include %s' % include_path]

            hotkeys = a2.db.get('hotkeys', module.key) or {}
            for typ in hotkeys:
                for hk in hotkeys.get(typ) or []:
                    # type 0 is global, append under the #IfWinActive label
                    if typ == '0':
                        hkstring = a2ahk.translate_hotkey(hk[0]) + '::' + hk[1]
                        hotkeys_ahk[hkmode['1']].append(hkstring)
                    # assemble type 1 and 2 in hotkeysAhks keys with the hotkey strings listed
                    else:
                        hkstring = a2ahk.translate_hotkey(hk[1]) + '::' + hk[2]
                        for scopeStr in hk[0]:
                            scopeKey = '%s %s' % (hkmode[typ], scopeStr)
                            if scopeKey not in hotkeys_ahk:
                                hotkeys_ahk[scopeKey] = []
                            hotkeys_ahk[scopeKey].append(hkstring)

            for var_name, value in (a2.db.get('variables', module.key) or {}).items():
                variables_ahk.append('%s := %s' % (var_name, a2ahk.py_value_to_ahk_string(value)))

            init_calls = a2.db.get('init_calls', module.key) or []
            if init_calls:
                init_ahk += '    ; %s\n' % module.key
                for call in init_calls:
                    call = '    ' + call.replace('\n', '\n    ')
                    if not call.endswith('\n'):
                        call += '\n'
                    init_ahk += call

    # write all the include files
    import a2util
    a2util.write_utf8(os.path.join(a2.paths.settings, 'variables.ahk'), '\n'.join(variables_ahk))

    a2util.write_utf8(os.path.join(a2.paths.settings, 'libs.ahk'), '\n'.join(libs_ahk))

    a2util.write_utf8(os.path.join(a2.paths.settings, 'includes.ahk'), '\n'.join(include_ahk))

    content = edit_disclaimer % 'hotkeys' + '\n'
    for key in sorted(hotkeys_ahk.keys()):
        content += '\n'.join([key] + hotkeys_ahk[key]) + '\n\n'
    a2util.write_utf8(os.path.join(a2.paths.settings, 'hotkeys.ahk'), content)

    a2util.write_utf8(os.path.join(a2.paths.settings, 'init.ahk'), init_ahk + '}\n')


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
            except AttributeError as error:
                if not isinstance(logger, logging.PlaceHolder):
                    log.info('Could not set log level on logger object "%s": %s' % (name, str(logger)))
                    log.error(error)


if __name__ == '__main__':
    import a2app
    a2app.main()
