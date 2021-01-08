# -*- coding: utf-8 -*-
"""
a2ctrl - basic functionality for all the a2element building blocks
"""
import os
import sys
import traceback
from importlib import reload, import_module

import a2core
from a2ctrl.icons import Ico, Icons


log = a2core.get_logger(__name__)
UI_FILE_SUFFIX = '_ui'
NO_DRAW_TYPES = ['include', 'init']
ELEMENTS_PACKAGE = 'a2element'
LOCAL_ELEMENT_ID = 'a2_local_element'
_element_map = {}


def check_ui_module(module, force=False):
    """
    Recompile a ui xml file to Python if out-of-date.

    :param module module: Module object to check.
    """
    if not a2core.is_dev_mode():
        return

    if getattr(sys, 'frozen', False):
        # log.info('frozen! no need to compile %s' % module)
        return

    pyfile = module.__file__
    folder, pybase = os.path.split(pyfile)
    uiname = os.path.splitext(pybase)[0]
    uibase = None

    if uiname.endswith(UI_FILE_SUFFIX):
        uibase = uiname[: -len(UI_FILE_SUFFIX)] + '.ui'
    else:
        uibase = _get_ui_basename_from_header(pyfile)

    if uibase is None:
        raise RuntimeError(
            'Could not get source ui file from module:\n %s\n  ' 'Not a ui file module??!' % module
        )

    uifile = os.path.join(folder, uibase)
    if not uibase or not os.path.isfile(uifile):
        return

    diff = os.path.getmtime(pyfile) - os.path.getmtime(uifile)
    if not force and os.path.getsize(pyfile) and diff > 0:
        return

    log.debug('%s needs compile! (age: %is)', uibase, diff)

    # Make paths in compiled files project related, not from current user.
    parent_path = os.path.abspath(os.path.join(a2core.__file__, '..', '..', '..'))

    # Newer uic seems to just put the basename in the header... however.
    ui_relative = os.path.relpath(uifile, parent_path)
    curr_cwd = os.getcwd()
    os.chdir(parent_path)

    import subprocess
    import a2qt

    uic_path = os.path.join(a2qt.__path__[0], 'uic.exe')
    subprocess.call([uic_path, '-g', 'python', ui_relative, '-o', pyfile])

    os.chdir(curr_cwd)

    _patch_main_ui(uiname, pyfile)

    reload(module)


def _patch_main_ui(uiname, pyfile):
    """
    Patch compiled main ui file to have resizing handled by settings.
    Could be useful for ANY compiled UI:
        main sizes are usually related to parent arrangement!?
    """
    if uiname == 'a2design_ui':
        with open(pyfile) as pyfobj:
            lines = pyfobj.readlines()

        skip_lines = 12
        for i, line in enumerate(lines[12:]):
            if line.startswith('        a2MainWindow.resize('):
                with open(pyfile, 'w') as pyfobj:
                    pyfobj.write(
                        ''.join(lines[: i + skip_lines]) + ''.join(lines[i + skip_lines + 1 :])
                    )
                    break


def _get_ui_basename_from_header(py_ui_path):
    """TODO: This is kinda ugly I don't think we need it."""
    uibase = None
    with open(py_ui_path) as fobj:
        line = fobj.readline()
        while line and uibase is not None:
            line = line.strip()
            if line.startswith('# Form implementation '):
                uibase = line[line.rfind("'", 0, -1) + 1 : -1]
                uibase = os.path.basename(uibase.strip())
                log.error('checkUiModule from read: %s', uibase)
                break
            line = fobj.readline()
    return uibase


def draw(main, element_cfg, mod, user_cfg):
    """
    Find Draw class according to the 'typ' of a config element.
    """
    element_typ = element_cfg.get('typ')
    if element_typ in NO_DRAW_TYPES:
        return None

    if element_typ == LOCAL_ELEMENT_ID:
        element_path = os.path.join(mod.path, '%s_%s.py' % (LOCAL_ELEMENT_ID, element_cfg['name']))
        element_module = get_local_element(element_path)
    else:
        element_module = get_a2element_module(element_typ)

    try:
        return element_module.Draw(main, element_cfg, mod, user_cfg)
    except Exception:
        mod_path = None if mod is None else mod.path
        element_draw_class = get_a2element_object('Draw', element_cfg, mod_path)

        if element_draw_class is not None:
            try:
                return element_draw_class(main, element_cfg, mod, user_cfg)
            except Exception:
                log.error(traceback.format_exc().strip())
        log.error('Draw type "%s" not supported (yet)! Module: %s', element_typ, mod)


def edit(element_cfg, main, parent_cfg):
    """
    Find Edit class according to the 'typ' of a config element.
    """
    this_type = element_cfg.get('typ')
    if this_type != LOCAL_ELEMENT_ID:
        element_module = get_a2element_module(element_cfg.get('typ'))
        try:
            return element_module.Edit(element_cfg, main, parent_cfg)
        except Exception:
            pass

    mod_path = None if main.mod is None else main.mod.path
    element_edit_class = get_a2element_object('Edit', element_cfg, mod_path)
    if element_edit_class is not None:
        try:
            return element_edit_class(element_cfg, main, parent_cfg)
        except Exception:
            log.error(traceback.format_exc().strip())
            log.error(
                'Error getting Edit class for type "%s"!' ' Type not supported (yet)?!',
                element_cfg.get('typ'),
            )
    return None


def get_a2element_object(obj_name, element_cfg, module_path=None):
    """
    Fetch a named object from element module.

    :param str obj_name: Name of the object to get.
    :param dict element_cfg:
    :param module_path:
    :rtype: class
    """
    element_typ = element_cfg['typ']
    if element_typ == LOCAL_ELEMENT_ID:
        if module_path is None:
            raise ValueError('module_path cannot be None for local element!')

        element_path = os.path.join(
            module_path, '%s_%s.py' % (LOCAL_ELEMENT_ID, element_cfg['name'])
        )
        element_mod = get_local_element(element_path)
        try:
            return getattr(element_mod, obj_name)
        except Exception as error:
            log.error(error)
            raise RuntimeError('Local Element "%s" has no object "%s"!!' % (element_path, obj_name))
    else:
        element_mod = get_a2element_module(element_typ)
        if element_mod is not None:
            return getattr(element_mod, obj_name)
    return None


def get_a2element_module(element_type):
    """
    From the "typ" tries to import the according module from a2element
    """
    try:
        return _element_map[element_type]
    except KeyError:
        try:
            element_mod_name = ELEMENTS_PACKAGE + '.' + element_type
            if ELEMENTS_PACKAGE not in sys.modules:
                import_module(ELEMENTS_PACKAGE)

            if element_mod_name in sys.modules:
                element_mod = sys.modules[element_mod_name]
            else:
                element_mod = import_module(element_mod_name, ELEMENTS_PACKAGE)

            _element_map[element_type] = element_mod
            return element_mod

        except Exception:
            log.error(traceback.format_exc().strip())
            log.error('Could not import element type "%s"!', element_type)


def get_local_element(item_path):
    """
    Load an element module local to an a2 module.

    :param str item_path: Path to the element module.
    """
    if os.path.isfile(item_path):
        dir_path, file_name = os.path.split(item_path)
        if dir_path not in sys.path:
            sys.path.append(dir_path)

        base, _ = os.path.splitext(file_name)
        try:
            element_module = import_module(base)
        except Exception:
            log.error(traceback.format_exc().strip())
            log.error('Could not get local element module! "%s"', item_path)
            element_module = None

        sys.path.remove(dir_path)

        return element_module
    else:
        raise RuntimeError('Cannot load local element! File does not exist! (%s)' % item_path)


def get_cfg_value(element_cfg, user_cfg, attr_name=None, typ=None, default=None):
    """
    unified call to get a value no matter if its set by user already
    or still default from the module config.
    """
    if user_cfg is not None and user_cfg != {} and attr_name is None:
        value = user_cfg
    elif isinstance(user_cfg, dict) and attr_name in user_cfg:
        value = user_cfg[attr_name]
    elif attr_name is None and 'value' in element_cfg:
        value = element_cfg.get('value')
    elif attr_name in element_cfg:
        value = element_cfg[attr_name]
    else:
        value = default

    if typ is not None:
        if not isinstance(value, typ):
            if default is None:
                value = typ()
            else:
                log.error('Fetched wrong type for attr_name %s: %s', attr_name, value)
                value = default

    return value


def assemble_settings(module_key, cfg_list, db_dict, module_path=None):
    """
    Get user settings from a modules elements.
    """
    import a2util, a2mod

    a2obj = a2core.A2Obj.inst()
    module_user_cfg = a2obj.db.get(a2mod.USER_CFG_KEY, module_key) or {}
    for element_cfg in cfg_list:
        # get configs named db entry of module or None
        cfg_name = a2util.get_cfg_default_name(element_cfg)
        user_cfg = module_user_cfg.get(cfg_name, {})
        # pass if there is an 'enabled' entry and it's False
        if not get_cfg_value(element_cfg, user_cfg, 'enabled', default=True):
            continue

        if module_path is None and element_cfg['typ'] == LOCAL_ELEMENT_ID:
            module_path = _get_module_path(module_key, a2obj)

        element_get_settings_func = get_a2element_object('get_settings', element_cfg, module_path)

        # no result try again with getting the module path:
        if element_get_settings_func is None and module_path is None:
            module_path = _get_module_path(module_key, a2obj)
            element_get_settings_func = get_a2element_object(
                'get_settings', element_cfg, module_path
            )

        if element_get_settings_func is not None:
            try:
                element_get_settings_func(module_key, element_cfg, db_dict, user_cfg)
            except Exception:
                log.error(traceback.format_exc().strip())
                log.error(
                    'Error calling get_settings function ' 'for module: "%s"',
                    module_key,
                )


def _get_module_path(module_key, a2obj):
    source_name, mod_name = module_key.split('|')
    module_path = a2obj.module_sources[source_name].mods[mod_name].path
    return module_path


def iter_element_cfg_type(cfg_list, typ=None):
    """
    Loop over each element configuration in and out of groups likewise.
    """
    for element_cfg in cfg_list:
        if element_cfg['typ'] == 'group':
            yield from iter_element_cfg_type(element_cfg['children'], typ)

        if typ is None:
            yield element_cfg
        elif element_cfg['typ'] == typ:
            yield element_cfg


if __name__ == '__main__':
    import a2app

    a2app.main()
