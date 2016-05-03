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
import time
import logging
import webbrowser
from os.path import exists, join, dirname

import ahk
import a2db
import a2mod


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


edit_disclaimer = ("; a2 %s.ahk - Don't bother editing! - File is generated automatically!")
a2default_hotkey = 'Win+Shift+A'
reload_modules = [ahk, a2db, a2mod]


class A2Obj(object):
    __instance = None
    
    @classmethod
    def inst(cls):
        if A2Obj.__instance is None:
            A2Obj.__instance = A2Obj()
        return A2Obj.__instance
    
    def __init__(self):
        self.app = None
        self.win = None
        self.modules = {}
        self.urls = URLs()
        self.paths = Paths()
        self.db = a2db.A2db(self.paths.db)

    def start_up(self):
        self.fetch_modules()
        self.get_used_scopes()
        self.get_used_hotkeys()

    def fetch_modules(self):
        moddirs = os.listdir(self.paths.modules)
        # get rid of modules gone
        [self.modules.pop(m) for m in self.modules if m not in moddirs]
        # register new modules
        for modname in os.listdir(self.paths.modules):
            if modname not in self.modules:
                self.modules[modname] = a2mod.Mod(modname)
        return self.modules

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
        return self.db.get('enabled') or []

    @enabled.setter
    def enabled(self, these):
        self.db.set('enabled', these)


class URLs(object):
    def __init__(self):
        """
        Common a2 & ahk related web links.
        """
        self.a2 = 'https://github.com/ewerybody/a2'
        self.help = self.a2 + '#description'
        self.helpEditCtrl = self.a2 + '/wiki/EditCtrls'
        self.helpHotkey = self.a2 + '/wiki/Edit-Hotkey-Control'
        self.helpCheckbox = self.a2 + '/wiki/Edit-Checkbox-Control'
        self.helpScopes = self.a2 + '/wiki/Edit-Scopes'
        self.help_string = self.a2 + '/wiki/Edit-String'
        self.help_number = self.a2 + '/wiki/Edit-Number'

        self.ahk = 'https://autohotkey.com'
        self.ahk_commands = self.ahk + '/docs/commands'
        self.ahk_run = self.ahk_commands + '/Run.htm'
        self.ahksend = self.ahk_commands + '/Send.htm'
        self.ahkWinActive = self.ahk_commands + '/WinActive.htm'
        self.ahk_builtin_vars = self.ahk + '/docs/Variables.htm#BuiltIn'
        self.ahkWinTitle = self.ahk + '/docs/misc/WinTitle.htm'


class Paths(object):
    """
    Hosts common paths around a2.
    """
    def __init__(self):
        self.ui = dirname(__file__)
        
        if not self.ui:
            cwd = os.getcwd()
            if exists(join(cwd, 'a2ui.py')):
                self.ui = cwd
                log.info('fetched a2ui dir from cwd... %s' % cwd)
            else:
                raise Exception('a2ui start interrupted! '
                                'Could not get main Ui dir!')

        self.a2 = dirname(self.ui)
        self.lib = join(self.a2, 'lib')
        self.starter_exe = join(self.a2, 'a2Starter.exe')
        self.a2_script = join(self.a2, 'a2.ahk')
        self.settings = get_settings_path()
        self.modules = join(self.a2, 'modules')
        
        # test if all necessary directories are present:
        main_items = [self.a2_script, self.starter_exe, self.lib,
                      self.modules, self.settings, self.ui]
        missing = [p for p in main_items if not exists(p)]
        if missing:
            raise Exception('a2ui start interrupted! %s not found in main dir!'
                            % missing)
        if not os.access(self.settings, os.W_OK):
            raise Exception('a2ui start interrupted! %s inaccessable!'
                            % self.settings)
    
        # by default the Autohotkey.exe in the lib should be uses
        # but we need an option for that a user can put it to whatever he wants
        self.autohotkey = join(self.lib, 'AutoHotkey', 'AutoHotkey.exe')
        self.db = join(self.settings, 'a2.db')


def write_includes(specific=None):
    a2 = A2Obj.inst()
    a2.fetch_modules()
    
    hkmode = {'1': '#IfWinActive,', '2': '#IfWinNotActive,'}
    
    includeAhk = [edit_disclaimer % 'includes']
    a2_hotkey = ahk.translateHotkey(a2.db.get('a2_hotkey') or a2default_hotkey)
    hotkeysAhk = {hkmode['1']: [a2_hotkey + '::a2UI()']}
    variablesAhk = [edit_disclaimer % 'variables']
    # TODO: this needs to be implemented dynamically
    libsAhk = [edit_disclaimer % 'libs'] + ['#include lib/%s.ahk' % lib for lib in
                                            ['tt', 'functions', 'Explorer_Get']]
    
    # browse the enabled modules to collect the include data
    modSettings = a2.db.tables()
    for modname in a2.db.get('enabled') or []:
        if modname not in modSettings:
            a2.modules[modname].change()
        
        includes = a2.db.get('includes', modname)
        
        if not isinstance(includes, list):
            log.warn('includes not a list: %s' % includes)
            includes = [includes]
        
        includeAhk += ['#include modules\%s\%s'
                       % (modname, i) for i in includes]
        
        hotkeys = a2.db.get('hotkeys', modname)
        for typ in hotkeys:
            for hk in hotkeys.get(typ) or []:
                # type 0 is global, append under the #IfWinActive label
                if typ == '0':
                    hkstring = ahk.translateHotkey(hk[0]) + '::' + hk[1]
                    hotkeysAhk[hkmode['1']].append(hkstring)
                # assemble type 1 and 2 in hotkeysAhks keys with the hotkey strings listed
                else:
                    hkstring = ahk.translateHotkey(hk[1]) + '::' + hk[2]
                    for scopeStr in hk[0]:
                        scopeKey = '%s %s' % (hkmode[typ], scopeStr)
                        if scopeKey not in hotkeysAhk:
                            hotkeysAhk[scopeKey] = []
                        hotkeysAhk[scopeKey].append(hkstring)
    
        for var_name, value in (a2.db.get('variables', modname) or {}).items():
            if isinstance(value, bool):
                variablesAhk.append('%s := %s' % (var_name, str(value).lower()))
            elif isinstance(value, str):
                variablesAhk.append('%s := "%s"' % (var_name, value))
            elif isinstance(value, float):
                variablesAhk.append('%s := %f' % (var_name, value))
            elif isinstance(value, int):
                variablesAhk.append('%s := %i' % (var_name, value))
            else:
                log.error('Please check handling variable type "%s" (%s: %s)'
                          % (type(value), var_name, str(value)))
                variablesAhk.append('%s := %s' % (var_name, str(value)))
    
    # write all the include files
    with open(join(a2.paths.settings, 'variables.ahk'), 'w') as fobj:
        fobj.write('\n'.join(variablesAhk))
    
    with open(join(a2.paths.settings, 'libs.ahk'), 'w') as fobj:
        fobj.write('\n'.join(libsAhk))
    
    with open(join(a2.paths.settings, 'includes.ahk'), 'w') as fobj:
        fobj.write('\n'.join(includeAhk))
    
    with open(join(a2.paths.settings, 'hotkeys.ahk'), 'w') as fobj:
        fobj.write(edit_disclaimer % 'hotkeys' + '\n')
        for key in sorted(hotkeysAhk.keys()):
            fobj.write('\n'.join([key] + hotkeysAhk[key]) + '\n\n')
    
    with open(join(a2.paths.settings, 'init.ahk'), 'w') as fobj:
        fobj.write(edit_disclaimer % 'init' + '\n')


def get_settings_path():
    """
    Location of regulary written settings db and import modules.
    TODO: same shit: make it changable
    """
    return join(dirname(dirname(__file__)), 'settings')


def get_author():
    return A2Obj.inst().db.get('devAuthor') or os.getenv('USERNAME')


def get_date():
    now = time.localtime()
    return '%i %i %i' % (now.tm_year, now.tm_mon, now.tm_mday)


def set_windows_startup(state=True):
    """
    might be doable via python but this is just too easy with AHKs A_Startup
    """
    ahk.call_cmd('set_windows_startup', A2Obj.inst().paths.a2, int(state))


def surfTo(url):
    if url:
        webbrowser.get().open(url)


def _dbCleanup():
    a2 = A2Obj.inst()
    for table in a2.db.tables():
        if table == 'a2':
            a2.db.pop('aValue')
            enabled = a2.db.get('enabled', asjson=False)
            if not enabled.startswith('["'):
                enabled = enabled.split('|')
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


if __name__ == '__main__':
    import a2app
    a2app.main()
