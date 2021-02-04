"""
All about a2 modules.
Modules in a2 always come in packages aka "module sources".
These are collections of 1 or more modules.
"""
import os
import sys
import shutil

import a2ahk
import a2path
import a2core
import a2ctrl
import a2ctrl.icons
import a2util


log = a2core.get_logger(__name__)
CONFIG_FILENAME = 'a2module.json'
USER_CFG_KEY = 'user_cfg'


class Mod(object):
    """
    The ui creates such a Mod instance when dealing with it
    from this it gets all information that it displays (hotkey interface,
    buttons, sliders, checkboxes, text, and the language for that)

    also holds the requirements of the module such as local (in the module folder)
    or global (in the a2/libs folder) libs.
    stores the available parts of the module that can be enabled in the ui.
    also the according variables, hotkeys, defaults, inits
    encapsulates the background functions for enabling/disabling a part

    config is None at first and filled as soon as the mod is selected in the UI.
    If there is no config_file yet it will be emptied instead of None.
    """
    def __init__(self, source, modname):
        # gather files from module path in local list
        self.source = source
        self.name = modname
        self.a2 = a2core.A2Obj.inst()
        self.path = os.path.join(self.source.path, modname)
        self._data_path = None
        self._backup_path = None
        self._config = None
        self.config_file = os.path.join(self.path, CONFIG_FILENAME)
        self.ui = None
        self._icon = None

        # the compound modulesource|modulename identifier
        self.key = self.source.name + '|' + self.name

    @property
    def has_config_file(self):
        return os.path.isfile(self.config_file)

    @property
    def config(self):
        if self._config is None:
            self.get_config()
        return self._config

    @config.setter
    def config(self, cfg_dict):
        self._config = cfg_dict
        self.backup_config()
        try:
            a2util.json_write(self.config_file, self._config)
        except PermissionError:
            a2util.write_enable(self.config_file)
            a2util.json_write(self.config_file, self._config)

    def get_config(self):
        if self.has_config_file:
            try:
                self._config = a2util.json_read(self.config_file)
                return self._config
            except Exception as error:
                log.error('config exists but could not be loaded!: '
                          '%s\nerror: %s' % (self.config_file, error))
        self._config = []
        return self._config

    def backup_config(self):
        """
        Backups the current config_file.
        """
        if not self.has_config_file:
            return

        if not os.path.isdir(self.backup_path):
            os.makedirs(self.backup_path)

        config_backups = [f for f in os.listdir(self.backup_path)
                          if f.startswith('%s.' % CONFIG_FILENAME)]
        if config_backups:
            config_backups.sort()
            # split and increase appended version index
            backup_index = int(config_backups[-1].rsplit('.', 1)[1]) + 1
        else:
            backup_index = 1

        path = os.path.join(self.backup_path, '%s.%i' % (CONFIG_FILENAME, backup_index))
        shutil.copyfile(self.config_file, path)

    def change(self):
        """
        Sets the mods own db entries.
        TODO: remove empty entries!
        """
        db_dict = {'variables': {}, 'hotkeys': {}, 'includes': [], 'init_calls': []}
        a2ctrl.assemble_settings(self.key, self.config[1:], db_dict, self.path)
        for typ, data in db_dict.items():
            if data:
                self.a2.db.set(typ, data, self.key)
            else:
                self.a2.db.pop(typ, self.key)

    @property
    def scripts(self):
        return [f for f in self.files if f.lower().endswith(a2ahk.EXTENSION)]

    @property
    def files(self):
        """never shale, always browses path for files"""
        return a2path.get_file_names(self.path)

    @property
    def enabled(self):
        return self.name in self.source.enabled_mods

    @enabled.setter
    def enabled(self, state):
        current = self.a2.enabled
        source_state, enabled_mods = current.get(self.source.name, [False, []])
        if state and self.name not in enabled_mods:
            enabled_mods.append(self.name)
            current[self.source.name] = [source_state, enabled_mods]
            self.a2.enabled = current
        elif self.name in enabled_mods:
            enabled_mods.remove(self.name)
            current[self.source.name] = [source_state, enabled_mods]
            self.a2.enabled = current
        self.change()

    def create_script(self, script_name, author_name):
        script_name = script_name.strip()
        if not script_name:
            return
        if script_name != a2ahk.ensure_ahk_ext(script_name):
            raise NameError('The script needs to have an "%s" extension!!' % a2ahk.EXTENSION)

        script_path = os.path.join(self.path, script_name)
        if not os.path.isfile(script_path):
            with open(script_path, 'w') as file_obj:
                content = '; %s - %s\n' % (self.name, script_name)
                content += '; author: %s\n' % author_name
                content += '; created: %s\n\n' % a2util.get_date()
                file_obj.write(content)
        return script_name

    def check_create_script(self, name):
        name = os.path.splitext(name.lower())[0]
        black_list = [os.path.splitext(s)[0].lower() for s in self.scripts]
        return a2util.standard_name_check(
            name, black_list, 'Module has already a script named "%s"!')

    def set_user_cfg(self, element_cfg, value, attr_name=None):
        """
        Sets an elements user value.

        Helps to keep the user config as small as possible.
        For instance if there is a value 'enabled' True by default
        only setting it to False will be saved. User setting it to True
        would delete it from user settings, so it's taking the default again.

        user sets True AND default is True:
            delete from user_cfg
        user sets True AND default it False:
            set to user_cfg

        :param dict element_cfg: The modules original config for the element.
        :param any value: Variable value o
        :param str attr_name: If given sets the value to the name inside a dict.
            Otherwise the value is regarded as a whole.
        """
        cfg_name = a2util.get_cfg_default_name(element_cfg)
        module_user_cfg = self.get_user_cfg()

        if attr_name is None:
            current_cfg = module_user_cfg.get(cfg_name)
            if value == current_cfg:
                return
            current_cfg = value

        else:
            current_cfg = module_user_cfg.get(cfg_name, {})
            if attr_name in current_cfg:
                # value to set equals CURRENT value: done
                if value == current_cfg.get(attr_name):
                    return
                # in any other case: delete to make changes
                current_cfg.pop(attr_name)

            # value to set equals CONFIG value: done. otherwise: save it:
            if value != element_cfg.get(attr_name):
                current_cfg[attr_name] = value

        # delete the value from module_user_cfg if needed
        if current_cfg is None:
            try:
                del module_user_cfg[cfg_name]
            except KeyError:
                pass
        else:
            module_user_cfg[cfg_name] = current_cfg

        # delete module_user_cfg alltogether if needed
        if module_user_cfg:
            self.a2.db.set(USER_CFG_KEY, module_user_cfg, self.key)
        else:
            self.clear_user_cfg()

    def get_user_cfg(self):
        return self.a2.db.get(USER_CFG_KEY, self.key) or {}

    def clear_user_cfg(self):
        self.a2.db.pop(USER_CFG_KEY, self.key)
        self.change()

    def clear_user_cfg_name(self, cfg_name):
        module_user_cfg = self.get_user_cfg()
        try:
            del module_user_cfg[cfg_name]
        except KeyError:
            pass

        # delete module_user_cfg alltogether if needed
        if module_user_cfg:
            self.a2.db.set(USER_CFG_KEY, module_user_cfg, self.key)
        else:
            self.clear_user_cfg()
        self.change()

    def is_in_user_cfg(self, name):
        """
        Tells you if an element has user data saved.
        :param str name: Name of the element
        :rtype: bool
        """
        return name in self.get_user_cfg()

    def help(self):
        try:
            a2util.surf_to(self.config[0].get('url'))
        except Exception as error:
            log.error('Error calling help() on module: %s\n:%s' % (self.name, error))

    def __repr__(self):
        return '<a2mod.Mod %s at %s>' % (self.name, hex(id(self)))

    @property
    def icon(self):
        self._icon = a2ctrl.icons.get(self._icon, self.path, self.source.icon)
        return self._icon

    def has_tag(self, tagname):
        """
        Checks if the given tag is among the modules tags
        :param str tagname: Tag name to look for
        :rtype: bool
        """
        if self.config and tagname in self.config[0].get('tags', []):
            return True
        return False

    @property
    def data_path(self):
        if self._data_path is None:
            self._data_path = os.path.join(
                self.a2.paths.data, 'module_data', self.source.name, self.name)
        return self._data_path

    @property
    def backup_path(self):
        if self._backup_path is None:
            self._backup_path = os.path.join(
                self.a2.paths.temp, self.source.name, 'config_backups', self.name)
        return self._backup_path

    def get_config_backups(self):
        times_and_files = []
        for item in a2path.iter_files(self.backup_path):
            if not item.name[-1].isdigit():
                continue
            times_and_files.append((os.path.getmtime(item.path), item.name))
        times_and_files.sort()
        return times_and_files

    def clear_backups(self):
        a2path.remove_dir(self.backup_path)

    def rollback(self, backup_file_name):
        backup_file_path = os.path.join(self.backup_path, backup_file_name)
        self.backup_config()
        os.remove(self.config_file)
        shutil.copyfile(backup_file_path, self.config_file)
        self.get_config()
        self.change()

    def call_ahk_script(self, script_name, *args):
        import a2ahk
        script_name = a2ahk.ensure_ahk_ext(script_name)
        script_path = os.path.join(self.path, script_name)
        return a2ahk.call_cmd(script_path, cwd=self.path, *args)

    def call_python_script(self, script_name):
        if not script_name:
            return

        path = os.path.join(self.path, script_name)
        if not os.path.isfile(path):
            return

        import traceback
        from importlib import import_module

        if self.path not in sys.path:
            sys.path.append(self.path)

        base, _ = os.path.splitext(script_name)
        # make sure that script changes make it to runtime
        if base in sys.modules:
            del sys.modules[base]

        try:
            script_module = import_module(base)
        except ImportError:
            log.error(traceback.format_exc().strip())
            log.error('Could not import local script_module! "%s"', script_name)

        try:
            script_module.main(self.a2, self)
        except Exception:
            tb = traceback.format_exc().strip()

            if base in sys.modules:
                log.info('unloading module "%s" ...', base)
                del sys.modules[base]

            log.error('\n  Error executing main() of script_module "%s"\n'
                      '%s\n  path: %s', script_name, tb, path)

        if self.path in sys.path:
            sys.path.remove(self.path)
