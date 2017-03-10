"""
a2core - Foundation module to host basic info and functionality

Everything thats needed by but itself has no constrains to the user interface.
Such as paths and os tweaks. Mainly this is to thin out the ui module but also
to make functionality available without passing the main ui object.

@created: 15.03.2016
@author: eric
"""
import os
import json
import time
import string
import logging
import subprocess
import webbrowser
from os.path import exists, join, dirname, abspath, relpath
import codecs

# only spot where this is set! Use a2core.get_logger() anywhere else!
LOG_LEVEL = logging.INFO
log = logging.getLogger(__name__)
log.setLevel(LOG_LEVEL)

a2ahk, a2db, a2mod = None, None, None

edit_disclaimer = ("; a2 %s.ahk - Don't bother editing! - File is generated automatically!")
a2default_hotkey = 'Win+Shift+A'
ALLOWED_CHARS = string.ascii_letters + string.digits + '_-.'
ILLEGAL_NAMES = ('con prn aux nul com1 com2 com3 com4 com5 com6 com7 com8 com9 lpt1 lpt2 lpt3 '
                 'lpt4 lpt5 lpt6 lpt7 lpt8 lpt9'.split())
JSON_INDENT = 2


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
                 ['a2', 'tt', 'functions', 'Explorer_Get', 'ahk_functions', 'ObjectTools', 'RichObject', 'Array']]
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

        print('source_name: %s' % source_name)
        for modname in enabled_modules:
            if modname not in source.mods:
                continue

            print('  modname: %s' % modname)
            module = source.mods[modname]
            if module.key not in mod_settings:
                print('  change: %s' % modname)
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
    with codecs.open(join(a2.paths.settings, 'variables.ahk'), 'w', encoding='utf-8-sig') as fobj:
        fobj.write('\n'.join(variables_ahk))

    with codecs.open(join(a2.paths.settings, 'libs.ahk'), 'w', encoding='utf-8-sig') as fobj:
        fobj.write('\n'.join(libs_ahk))

    with codecs.open(join(a2.paths.settings, 'includes.ahk'), 'w', encoding='utf-8-sig') as fobj:
        fobj.write('\n'.join(include_ahk))

    with codecs.open(join(a2.paths.settings, 'hotkeys.ahk'), 'w', encoding='utf-8-sig') as fobj:
        content = edit_disclaimer % 'hotkeys' + '\n'
        for key in sorted(hotkeys_ahk.keys()):
            content += '\n'.join([key] + hotkeys_ahk[key]) + '\n\n'
        fobj.write(content)

    with codecs.open(join(a2.paths.settings, 'init.ahk'), 'w', encoding='utf-8-sig') as fobj:
        init_ahk += ('}\n')
        fobj.write(init_ahk)


def get_date():
    now = time.localtime()
    return '%i %i %i' % (now.tm_year, now.tm_mon, now.tm_mday)


def set_windows_startup(state=True):
    """
    might be doable via python but this is just too easy with AHKs A_Startup
    """
    a2ahk.call_lib_cmd('set_windows_startup', A2Obj.inst().paths.a2, int(state))


def surfTo(url):
    if url:
        webbrowser.get().open(url)


def json_read(path):
    with open(path) as fob:
        return json.load(fob)


def json_write(path, data):
    with open(path, 'w') as fob:
        json.dump(data, fob, indent=JSON_INDENT, sort_keys=True)


def killA2process():
    """
    finds and kills Autohotkey processes that run a2.ahk.
    takes a moment. so start it in a thread!
    TODO: make sure restart happens after this finishes?

    there is also:
    ctypes.windll.kernel32.TerminateProcess(handle, 0)
    """
    t1 = time.time()
    startup_nfo = subprocess.STARTUPINFO()
    startup_nfo.wShowWindow = subprocess.SW_HIDE
    startup_nfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    wmicall = 'wmic process where name="Autohotkey.exe" get ProcessID,CommandLine'
    wmicout = subprocess.check_output(wmicall, startupinfo=startup_nfo)
    wmicout = str(wmicout).split('\\r\\r\\n')
    for line in wmicout[1:-1]:
        if 'autohotkey.exe' in line.lower():
            cmd, pid = line.rsplit(maxsplit=1)
            if cmd.endswith('a2.ahk') or cmd.endswith('a2.ahk"'):
                taskkill_proc = subprocess.Popen('taskkill /f /pid %s' % pid, shell=True, startupinfo=startup_nfo)
                taskkill_proc.wait()
                taskkill_proc.kill()
    log.debug('killA2process took: %fs' % (time.time() - t1))


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
            logger.setLevel(level)


def standard_name_check(NAME, black_list=None, black_list_msg='Name "%s" already in use!'):
        name = NAME.lower()
        if NAME == '':
            return 'Name cannot be empty!'
        if name == 'a2':
            return 'You just cannot name it "a2"! Ok?'
        if black_list is not None and name in black_list:
            return black_list_msg % name
        if any([(l in string.whitespace) for l in name]):
            return 'Name cannot have whitespace! Use _ or - insead!'
        if not all([(l in ALLOWED_CHARS) for l in name]):
            return 'Name can only have letters, digits and "_.-"'
        if name in ILLEGAL_NAMES:
            return 'Name cannot be reserved OS device name!'
        if not any([(l in string.ascii_letters) for l in name]):
            return 'Have at least 1 letter in the name!'
        return True


def get_next_free_number(name, name_list, separator=''):
    """
    Browses a list of names to find a free new version of the given name + integer number.
    Just returns the name if its not even in the name_list. Otherwise the first next will be 2.

    Example:

        name = 'trumpet'
        name_list = ['swamp', 'noodle']
        result: 'trumpet'

        name = 'bob'
        name_list = ['bob', 'alice', 'bob 2', 'bob 4']
        result: 'bob 3'

    :param str name: Base name to look up in the list
    :param iterable name_list: List to look for instances of "name"
    :param str separator: string to put between the initial name and the integer number.
    :rtype: str
    """
    if name not in name_list:
        return name

    number = 2
    try_name = name + separator + str(number)

    while try_name in name_list:
        number += 1
        try_name = name + separator + str(number)

    return try_name


def get_cfg_default_name(cfg):
    """

    :param dict cfg: Element configuration dictionary.
    :rtype: str
    """
    cfg_name = cfg.get('name', cfg.get('typ'))
    if cfg_name is None:
        raise RuntimeError('Could not find name for config piece!\n'
                           'Make sure "name" or "typ" is given in the config dict!')
    return cfg_name


if __name__ == '__main__':
    import a2app
    a2app.main()
