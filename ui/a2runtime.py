"""
Functionality all around managing the Autohotkey runtime of a2.
"""
import os
import enum
import subprocess

import a2ahk
import a2core
import a2path
import a2util

log = a2core.get_logger(__name__)

A2_DATA = '%a2data%'
PACKAGE_LIB = '.lib'
EDIT_DISCLAIMER = a2core.EDIT_DISCLAIMER
ERROR_DUP_VALUE = 'Value name already collected!!\n  module: %s\n  value name: %s'
ERROR_EMPTYNAME = 'Empty variable name!!\n  module: %s\n  value name: %s'


class Scope:
    glob = '0'
    incl = '1'
    excl = '2'


class IncludeType(enum.Enum):
    variables = 0
    includes = 2
    hotkeys = 3
    init = 4
    source_libs = 5
    exit = 6


class IncludeDataCollector(object):
    def __init__(self):
        self.a2 = a2core.A2Obj.inst()
        self.a2.fetch_modules()

        self.variables = None
        self.includes = None
        self.hotkeys = None
        self.init = None
        self.source_libs = None
        self.exit = None

    def collect(self):
        mod_settings = self.a2.db.tables()

        for source_name, (source_enabled, enabled_modules) in self.a2.enabled.items():
            if not source_enabled:
                continue

            source = self.a2.module_sources.get(source_name.lower())
            if source is None:
                log.debug('Source: "%s" is enabled but missing!' % source_name)
                continue

            if self.source_libs:
                self.source_libs.gather(source)

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
        os.makedirs(self.a2.paths.includes, exist_ok=True)
        for collection in self.collections:
            if collection is not None:
                collection.write()
        if self.source_libs:
            self.source_libs.write()
        self.a2.paths.set_data_path(self.a2.paths.data)

    @property
    def collections(self):
        # type: () -> list[None | _Collection]
        """
        Collections per module.
        A property to be dynamically fillable.
        """
        return [self.variables, self.includes, self.hotkeys, self.init, self.exit]

    def get_vars(self):
        self.variables = VariablesCollection(self.a2)

    def get_includes(self):
        self.includes = IncludesCollection(self.a2)

    def get_hotkeys(self):
        self.hotkeys = HotkeysCollection(self.a2)

    def get_init(self):
        self.init = InitCollection(self.a2)

    def get_source_libs(self):
        self.source_libs = SourceLibsCollection(self.a2)

    def get_exit(self):
        self.exit = ExitCollection(self.a2)

    def get_all_collections(self):
        self.get_vars()
        self.get_includes()
        self.get_hotkeys()
        self.get_init()
        self.get_source_libs()
        self.get_exit()


class _Collection(object):
    def __init__(self, a2_instance=None):
        if a2_instance is None:
            self.a2 = a2core.A2Obj.inst()
        else:
            self.a2 = a2_instance
        self.name = ''

    def write(self):
        path = os.path.join(self.a2.paths.includes, self.name + a2ahk.EXTENSION)
        a2util.write_utf8(path, self._get_final_content())

    def gather(self, mod):
        """To collect the needed data from a module."""
        raise NotImplementedError

    def get_content(self):
        """Creates the AHK code out of the collected data."""
        raise NotImplementedError

    @property
    def has_content(self):
        """To return if there is anything to write before assembling at all"""
        raise NotImplementedError

    def _get_final_content(self):
        return EDIT_DISCLAIMER % self.name + self.get_content()


class VariablesCollection(_Collection):
    def __init__(self, a2obj_instance=None):
        super(VariablesCollection, self).__init__(a2obj_instance)
        self.name = 'variables'
        self._data = {}

    def gather(self, mod):
        for var_name, value in (self.a2.db.get('variables', mod.key) or {}).items():
            if var_name in self._data:
                log.error(ERROR_DUP_VALUE, mod.name, var_name)
                continue
            if not var_name:
                log.error(ERROR_EMPTYNAME, mod.name, var_name)
                continue
            self._data[var_name] = (value, mod.key)

    @property
    def data(self):
        flat_data = {}
        for var_name, (value, _) in self._data.items():
            flat_data[var_name] = value
        return flat_data

    def iter_mod_variables(self):
        """Loop over all gathered variables, yield tuple of source module key,
        variable name and value."""
        for var_name, (value, mod_key) in self._data.items():
            yield mod_key, var_name, value

    def get_content(self):
        content = ''
        for var_name, value in sorted(self.data.items(), key=lambda k: k[0].lower()):
            content += 'global %s := %s\n' % (var_name, a2ahk.py_value_to_ahk_string(value))
        return content

    @property
    def has_content(self):
        return self._data != {}


class IncludesCollection(_Collection):
    """
    Collects the ahk-File paths to be listed in the includes.ahk.
    These can be from modules directly or generated by modules and written to
    the 'module data' directory.
    """

    def __init__(self, a2obj_instance=None):
        super(IncludesCollection, self).__init__(a2obj_instance)
        self.name = 'includes'
        self.include_paths = []

    def gather(self, mod):
        """
        Creates the module specific paths and assembles the include files.
        :param mod: Current Module object.
        """
        paths = [
            ('includes', os.path.join('modules', mod.source.name, mod.name)),
            ('data_includes', os.path.join('module_data', mod.source.name, mod.name)),
        ]

        for include_type, include_dir in paths:
            includes = self.a2.db.get(include_type, mod.key) or []
            if not isinstance(includes, list):
                log.warning('%s: includes "%s" not a list: %s' % (mod.key, include_type, includes))
                includes = [includes]

            for include in includes:
                self.include_paths.append(os.path.join(include_dir, include))

    def get_content(self):
        return '#include ..\n' + '\n'.join(['#include %s' % p for p in self.include_paths])

    @property
    def has_content(self):
        return self.include_paths != []


class HotkeysCollection(_Collection):
    def __init__(self, a2obj_instance=None):
        super(HotkeysCollection, self).__init__(a2obj_instance)
        self.name = 'hotkeys'

        self.hotkeys_global = {}
        self.hotkeys_scope_incl = {}
        self.hotkeys_scope_excl = {}
        self._scope_types = {
            Scope.incl: self.hotkeys_scope_incl,
            Scope.excl: self.hotkeys_scope_excl,
        }

        # add a2 standard hotkey
        a2_standard_hotkey = self.a2.db.get('a2_hotkey') or a2core.A2DEFAULT_HOTKEY
        for key in iter_str_or_list(a2_standard_hotkey):
            self.hotkeys_global.setdefault(key, []).append(('a2UI()', None))

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
                        self.hotkeys_global.setdefault(key, []).append((command, mod))

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
                            self._scope_types[scope_type][scope_string].setdefault(key, []).append(
                                (command, mod)
                            )

    def get_content(self):
        scope_modes = {Scope.incl: '#IfWinActive', Scope.excl: '#IfWinNotActive'}

        # write global hotkey text
        content = scope_modes[Scope.incl] + ',\n'
        content += self._create_hotkey_code(self.hotkeys_global)
        # write the scoped stuff
        for mode, scope_dict in self._scope_types.items():
            for scope, hotkey_data in scope_dict.items():
                content += '\n%s, %s\n' % (scope_modes[mode], scope)
                content += self._create_hotkey_code(hotkey_data)

        return content

    @property
    def has_content(self):
        return any(
            [
                d != {}
                for d in [self.hotkeys_global, self.hotkeys_scope_incl, self.hotkeys_scope_excl]
            ]
        )

    @staticmethod
    def _create_hotkey_code(hotkey_data):
        code = ''
        for hotkey, commands in hotkey_data.items():
            code += a2ahk.translate_hotkey(hotkey) + '::'

            command_code = '\n\t'.join(cmd for cmd, _ in commands)
            # to gather more than 1 command in a code block
            if '\n' in command_code:
                code += '{\n ' + command_code.replace('\n', '\n ') + '\n}\n'
            # or just inline
            else:
                code += command_code + '\n'
        return code


class InitCollection(_Collection):
    def __init__(self, a2obj_instance=None):
        super(InitCollection, self).__init__(a2obj_instance)
        self.name = 'init'
        self.init_code = ''

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
        return 'a2_init_calls() {\n' + self.init_code + '}\n'

    @property
    def has_content(self):
        return self.init_code != ''


class ExitCollection(_Collection):
    def __init__(self, a2obj_instance=None):
        super(ExitCollection, self).__init__(a2obj_instance)
        self.name = 'exit'
        self.exit_code = ''

    def gather(self, mod):
        exit_calls = self.a2.db.get('exit_calls', mod.key) or []
        if exit_calls:
            self.exit_code += '    ; %s\n' % mod.key
            for call in exit_calls:
                call = '    ' + call.replace('\n', '\n    ')
                if not call.endswith('\n'):
                    call += '\n'
                self.exit_code += call

    def get_content(self):
        return 'a2_exit_calls() {\n' + self.exit_code + '}\n'

    @property
    def has_content(self):
        return self.exit_code != ''


class SourceLibsCollection(_Collection):
    """
    For script libraries that may come with a module source package.

    So a package is no longer dependent on the built-in lib to have certain
    libraries shipped and its modules don't need to care for dedicated includes
    as well.
    """

    def __init__(self, a2obj_instance=None):
        super(SourceLibsCollection, self).__init__(a2obj_instance)
        self.name = 'source_libs'
        self.includes = []

    def gather(self, source):
        lib_path = os.path.join(source.path, PACKAGE_LIB)
        if not os.path.isdir(lib_path):
            return
        names = [i.name for i in a2path.iter_types(lib_path, a2ahk.EXTENSION)]
        if not names:
            return
        # point the includes into the lib dir of this package
        self.includes.append(lib_path)
        # then add the names for relative include
        self.includes.extend(names)

    def get_content(self):
        return '\n'.join(['#include %s' % p for p in self.includes])

    @property
    def has_content(self):
        return self.includes != []


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
        elif specific is IncludeType.includes:
            collector.get_includes()
        elif specific is IncludeType.hotkeys:
            collector.get_hotkeys()
        elif specific is IncludeType.init:
            collector.get_init()
        elif specific is IncludeType.exit:
            collector.get_exit()

    collector.collect()
    return collector


def write_includes(specific=None):
    collector = collect_includes(specific)
    collector.write()


def collect_hotkeys():
    # type: () -> tuple[dict, dict, dict] | tuple
    """
    Kick of Hotkeys collection and return all dictionaries.

    :return: Tuple with 3 collections: global, include, exclude
    """
    collector = collect_includes(IncludeType.hotkeys)
    if collector.hotkeys is None:
        return ()

    data = (
        collector.hotkeys.hotkeys_global,
        collector.hotkeys.hotkeys_scope_incl,
        collector.hotkeys.hotkeys_scope_excl,
    )
    return data


def collect_variables():
    """Kick of Variables collection and return collection object."""
    collector = collect_includes(IncludeType.variables)
    if collector.variables is None:
        raise RuntimeError('Variables was not collected!')

    return collector.variables


def _get_hidden_process_startup_nfo():
    startup_nfo = subprocess.STARTUPINFO()
    startup_nfo.wShowWindow = subprocess.SW_HIDE
    startup_nfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return startup_nfo


def kill_a2_process():
    """
    Deprecated. Keping for emergency reasons.
    a2 runtime can now deal with a "--shutdown" argument!

    Find and kill Autohotkey processes that run a2.ahk.
    Takes a moment. So start it in a thread!

    note there is also:
    ctypes.windll.kernel32.TerminateProcess(handle, 0)

    :return: Process Id of found and terminated a2 runtime.
    :rtype: str
    """
    pid = get_a2_runtime_pid()

    if pid:
        args = ['/f', '/pid', pid]
        a2util.start_process_detached('taskkill.exe', args)
        return pid


def get_a2_runtime_pid():
    """
    Uses WMIC to get the PID and commandline arguments from
    any Autohotkey processes to find a running a2 instance.

    :return: PID string of an Autohotkey process running a2.
    :rtype: str
    """
    wmicout = subprocess.check_output(
        f'wmic process where name="{a2ahk.EXECUTABLE_NAME}" ' 'get ProcessID,CommandLine',
        startupinfo=_get_hidden_process_startup_nfo(),
        stderr=subprocess.STDOUT,
    )
    wmicout = str(wmicout).split('\\r\\r\\n')

    for line in wmicout[1:-1]:
        if a2ahk.EXECUTABLE_NAME in line.lower():
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
    # pid = get_a2_runtime_pid()
    # print('pid: %s' % pid)
    # print('is_runtime_live(): %s' % is_runtime_live())
    idc = IncludeDataCollector()
    idc.get_hotkeys()
    idc.collect()
    print('idc.hotkeys: %s' % idc.hotkeys)
    # glob, incl, excl = collect_hotkeys()
    # idc.write()
