"""
Functionality all around managing the Autohotkey runtime of a2.
"""
import os
import enum
import subprocess

import a2ahk
import a2core
import a2util

EDIT_DISCLAIMER = "; a2 %s.ahk - Don't bother editing! - File is generated automatically!"
log = a2core.get_logger(__name__)

TODO_DEFAULT_LIBS = ['a2', 'tt', 'func_file', 'func_string', 'functions', 'Explorer_Get',
                     'ahk_functions', 'ObjectTools', 'RichObject', 'Array', 'uri_encode',
                     'HTTPRequest', 'base64']


class Scope:
    glob = '0'
    incl = '1'
    excl = '2'


class IncludeType(enum.Enum):
    variables = 0
    libs = 1
    includes = 2
    hotkeys = 3
    init = 4


class IncludeDataCollector(object):
    def __init__(self):
        self.a2 = a2core.A2Obj.inst()
        self.a2.fetch_modules()

        self.variables = None
        self.libs = None
        self.includes = None
        self.hotkeys = None
        self.init = None

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
                mod = source.mods.get(modname)
                if mod is None:
                    continue

                # ensure settings have been written once at least
                if mod.key not in mod_settings:
                    mod.change()

                for collection in self.collections:
                    if collection is not None:
                        collection.gather(mod)

    def write(self):
        for collection in self.collections:
            if collection is None:
                continue
            collection.write()

    @property
    def collections(self):
        """property to be dynamically fillable"""
        return [self.variables, self.libs, self.includes, self.hotkeys, self.init]

    def get_vars(self):
        self.variables = VariablesCollection(self.a2)

    def get_libs(self):
        self.libs = LibsCollection(self.a2)

    def get_includes(self):
        self.includes = IncludesCollection(self.a2)

    def get_hotkeys(self):
        self.hotkeys = HotkeysCollection(self.a2)

    def get_init(self):
        self.init = InitCollection(self.a2)

    def get_all_collections(self):
        self.get_vars()
        self.get_libs()
        self.get_includes()
        self.get_hotkeys()
        self.get_init()


class _Collection(object):
    def __init__(self, a2_instance):
        self.a2 = a2_instance
        self.name = None

    def write(self):
        path = os.path.join(self.a2.paths.settings, self.name + '.ahk')
        a2util.write_utf8(path, self._final_content)

    def gather(self, mod):
        raise NotImplementedError

    def get_content(self):
        raise NotImplementedError

    @property
    def _final_content(self):
        content = EDIT_DISCLAIMER % self.name
        return '%s\n%s' % (content, self.get_content())


class VariablesCollection(_Collection):
    def __init__(self, a2obj_instance):
        super(VariablesCollection, self).__init__(a2obj_instance)
        self.name = 'variables'
        self.data = {}

    def gather(self, mod):
        for var_name, value in (self.a2.db.get('variables', mod.key) or {}).items():
            if var_name in self.data:
                log.error('Value name already collected!!\n'
                          '  module: %s\n'
                          '  value name: %s' % (mod.name, var_name))
                continue

            self.data[var_name] = value

    def get_content(self):
        content = ''
        for var_name, value in sorted(self.data.items(), key=lambda k: k[0].lower()):
            content += '%s := %s\n' % (var_name, a2ahk.py_value_to_ahk_string(value))
        return content


class LibsCollection(_Collection):
    def __init__(self, a2obj_instance):
        super(LibsCollection, self).__init__(a2obj_instance)
        self.name = 'libs'
        # TODO: we might use a set thats filled with the used libs
        # that are gathered when browsing the modules ...
        # self.libs = set()

    def gather(self, mod):
        # TODO: Used Libraries also need to be collected
        # from all the active modules!
        pass

    def get_content(self):
        # TODO: currently this just packs a list of commonly used default libraries.
        libs_ahk = ['#include lib/ahklib/%s.ahk' % lib for lib in TODO_DEFAULT_LIBS]
        return '\n'.join(libs_ahk)


class IncludesCollection(_Collection):
    def __init__(self, a2obj_instance):
        super(IncludesCollection, self).__init__(a2obj_instance)
        self.name = 'includes'
        self.modules_path = os.path.relpath(self.a2.paths.modules, self.a2.paths.a2)
        self.settings_path = os.path.relpath(self.a2.paths.settings, self.a2.paths.a2)
        self.include_paths = []

    def gather(self, mod):
        this_include_path = os.path.join(self.modules_path, mod.source.name, mod.name)

        for include_type, include_dir in [('includes', this_include_path),
                                          ('settings_includes', self.settings_path)]:
            includes = self.a2.db.get(include_type, mod.key) or []
            if not isinstance(includes, list):
                log.warning('%s not a list: %s' % (include_type, includes))
                includes = [includes]

            for include in includes:
                self.include_paths.append(os.path.join(include_dir, include))

    def get_content(self):
        return '\n'.join(['#include %s' % p for p in self.include_paths])


class HotkeysCollection(_Collection):
    def __init__(self, a2obj_instance):
        super(HotkeysCollection, self).__init__(a2obj_instance)
        self.name = 'hotkeys'

        self.hotkeys_global = {}
        self.hotkeys_scope_incl = {}
        self.hotkeys_scope_excl = {}
        self._scope_types = {Scope.incl: self.hotkeys_scope_incl,
                             Scope.excl: self.hotkeys_scope_excl}

        # add a2 standard hotkey
        a2_standard_hotkey = self.a2.db.get('a2_hotkey') or a2core.A2DEFAULT_HOTKEY
        for key in iter_str_or_list(a2_standard_hotkey):
            self.hotkeys_global.setdefault(key, []).append('a2UI()')

    def gather(self, mod):
        mod_hotkey_data = self.a2.db.get('hotkeys', mod.key) or {}

        for scope_type, hotkey_list in mod_hotkey_data.items():
            for hotkey_data in hotkey_list:
                # type 0 is global, gather hotkeys (0) and commands (1) in tuples
                if scope_type is Scope.glob:
                    hotkeys, command = hotkey_data
                    if not command:
                        continue
                    for key in iter_str_or_list(hotkeys):
                        if not key:
                            continue
                        self.hotkeys_global.setdefault(key, []).append(command)

                # '1' & '2' are include/exclude scopes
                # gather per type (0) hotkeys (1) and commands (2)
                else:
                    scopes, hotkeys, command = hotkey_data
                    if not command:
                        continue
                    for scope_string in scopes:
                        # make sure there is a hotkey dict for this scope
                        self._scope_types[scope_type].setdefault(scope_string, {})
                        # now append the command under hotkeys
                        for key in iter_str_or_list(hotkeys):
                            if not key:
                                continue
                            self._scope_types[scope_type][scope_string].setdefault(
                                key, []).append(command)

    def get_content(self):
        scope_modes = {Scope.incl: '#IfWinActive',
                       Scope.excl: '#IfWinNotActive'}

        def create_hotkey_code(hotkey_data):
            code = ''
            for hotkey, commands in hotkey_data.items():
                code += a2ahk.translate_hotkey(hotkey) + '::'

                command_code = '\n\t'.join(commands)
                if '\n' in command_code:
                    code += '\n\t' + command_code + '\nreturn\n'
                else:
                    code += command_code + '\n'
            return code

        # write global hotkey text
        content = scope_modes[Scope.incl] + ',\n'
        content += create_hotkey_code(self.hotkeys_global)
        # write the scoped stuff
        for mode, scope_dict in self._scope_types.items():
            for scope, hotkey_data in scope_dict.items():
                content += '\n%s, %s\n' % (scope_modes[mode], scope)
                content += create_hotkey_code(hotkey_data)

        return content


class HotkeyManager(object):
    def __init__(self):
        pass


class InitCollection(_Collection):
    def __init__(self, a2obj_instance):
        super(InitCollection, self).__init__(a2obj_instance)
        self.name = 'init'
        self.init_code = 'a2_init_calls() {\n'

    def gather(self, mod):
        init_calls = self.a2.db.get('init_calls', mod.key) or []
        if init_calls:
            self.init_code += '    ; %s\n' % mod.key
            for call in init_calls:
                call = '    ' + call.replace('\n', '\n    ')
                if not call.endswith('\n'):
                    call += '\n'
                self.init_code += call

    def get_content(self):
        self.init_code += '}\n'
        return self.init_code


def collect_includes(specific=None):
    """
    :rtype: IncludeDataCollector
    """
    collector = IncludeDataCollector()

    if isinstance(specific, str):
        specific = IncludeType.__members__.get(specific)

    if not specific:
        collector.get_all_collections()
    elif specific in IncludeType:
        if specific is IncludeType.variables:
            collector.get_vars()
        elif specific is IncludeType.libs:
            collector.get_libs()
        elif specific is IncludeType.includes:
            collector.get_includes()
        elif specific is IncludeType.hotkeys:
            collector.get_hotkeys()
        elif specific is IncludeType.init:
            collector.get_init()

    collector.collect()
    return collector


def write_includes(specific=None):
    collector = collect_includes(specific)
    collector.write()


def collect_hotkeys():
    """
    :rtype: list
    """
    collector = collect_includes(IncludeType.hotkeys)
    data = [collector.hotkeys.hotkeys_global,
            collector.hotkeys.hotkeys_scope_incl,
            collector.hotkeys.hotkeys_scope_excl]
    return data


def kill_a2_process():
    """
    finds and kills Autohotkey processes that run a2.ahk.
    takes a moment. so start it in a thread!
    TODO: make sure restart happens after this finishes?

    note there is also:
    ctypes.windll.kernel32.TerminateProcess(handle, 0)
    """
    pid = get_a2_runtime_pid()

    if pid:
        startup_nfo = subprocess.STARTUPINFO()
        startup_nfo.wShowWindow = subprocess.SW_HIDE
        startup_nfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        taskkill_proc = subprocess.Popen('taskkill /f /pid %s' % pid,
                                         startupinfo=startup_nfo)
        taskkill_proc.wait()
        taskkill_proc.kill()
        return pid


def get_a2_runtime_pid():
    """
    Uses WMIC to get the PID and commandline arguments from any Autohotkey processes
    to find a running a2 instance.

    :return: PID string of the Autohotkey process running a2
    :rtype: str
    """
    startup_nfo = subprocess.STARTUPINFO()
    startup_nfo.wShowWindow = subprocess.SW_HIDE
    startup_nfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    wmicall = f'wmic process where name="{a2ahk.EXECUTABLE_NAME}" get ProcessID,CommandLine'
    wmicout = subprocess.check_output(wmicall, startupinfo=startup_nfo)
    wmicout = str(wmicout).split('\\r\\r\\n')
    for line in wmicout[1:-1]:
        if 'autohotkey.exe' in line.lower():
            cmd, pid = line.rsplit(maxsplit=1)
            if cmd.endswith('a2.ahk') or cmd.endswith('a2.ahk"'):
                return pid


def is_runtime_live():
    """
    :return: True/False for if there is an Autohotkey executable running our a2.ahk
    :rtype: bool
    """
    pid = get_a2_runtime_pid()
    return pid is not None


def iter_str_or_list(str_or_list):
    """
    To be used in loop to not care about an obj being list or string.
    Yields either once or for each element.

    :param (str, list) str_or_list: List or string input object.
    :rtype: str
    """
    if isinstance(str_or_list, str):
        yield str_or_list
    elif isinstance(str_or_list, list):
        for item in str_or_list:
            yield item


if __name__ == '__main__':
#    pid = get_a2_runtime_pid()
#    print('pid: %s' % pid)
#    print('is_runtime_live(): %s' % is_runtime_live())
    idc = IncludeDataCollector()
    idc.get_hotkeys()
    idc.collect()
    print('idc.hotkeys: %s' % idc.hotkeys)
    #idc.write()
