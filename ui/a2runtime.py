"""
Functionality all around managing the Autohotkey runtime of a2.
"""
import os
import time
import subprocess

import a2ahk
import a2core
import a2util

EDIT_DISCLAIMER = "; a2 %s.ahk - Don't bother editing! - File is generated automatically!"
a2default_hotkey = 'Win+Shift+A'
log = a2core.get_logger(__name__)


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

                if mod.key not in mod_settings:
                    mod.change()

                for collection in self.all_collections:
                    if collection is None:
                        continue
                    collection.gather(mod)

    def write(self):
        for collection in self.all_collections:
            if collection is None:
                continue
            collection.write()

    @property
    def all_collections(self):
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
        a2util.write_utf8(path, self._final_content())

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
        self.var_list = []

    def gather(self, mod):
        for var_name, value in (self.a2.db.get('variables', mod.key) or {}).items():
            self.var_list.append('%s := %s' % (var_name, a2ahk.py_value_to_ahk_string(value)))

    def get_content(self):
        return '\n'.join(self.var_list)


class HotkeysCollection(_Collection):
    def __init__(self, a2obj_instance):
        super(HotkeysCollection, self).__init__(a2obj_instance)
        self.name = 'hotkeys'
        self.hk_mode = {'1': '#IfWinActive,', '2': '#IfWinNotActive,'}
        self.hd_dict = {}

    def gather(self, mod):

        a2_hotkey = a2ahk.translate_hotkey(self.a2.db.get('a2_hotkey') or a2default_hotkey)
        self.hd_dict = {self.hk_mode['1']: [a2_hotkey + '::a2UI()']}

        hotkeys = self.a2.db.get('hotkeys', mod.key) or {}
        for typ in hotkeys:
            for hk in hotkeys.get(typ) or []:
                # type 0 is global, append under the #IfWinActive label
                if typ == '0':
                    hk_string = a2ahk.translate_hotkey(hk[0]) + '::' + hk[1]
                    self.hd_dict[self.hk_mode['1']].append(hk_string)
                # assemble type 1 and 2 in hotkeys_ahk keys with the hotkey strings listed
                else:
                    hk_string = a2ahk.translate_hotkey(hk[1]) + '::' + hk[2]
                    for scope_string in hk[0]:
                        scope_key = '%s %s' % (self.hk_mode[typ], scope_string)
                        self.hd_dict.setdefault(scope_key, []).append(hk_string)

    def get_content(self):
        content = ''
        for key in sorted(self.hk_dict.keys()):
            content += '\n'.join([key] + self.hk_dict[key]) + '\n\n'
        return content


class HotkeyManager(object):
    def __init__(self):
        pass


def kill_a2_process():
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


if __name__ == '__main__':
    idc = IncludeDataCollector()
    idc.get_vars()
    idc.collect()
    idc.write()
