# -*- coding: utf-8 -*-
"""
a2ctrl - basic functionality for all the a2element building blocks
"""
import os
import sys
import traceback
from pyside2uic import compileUi
from importlib import reload, import_module

import a2core
import a2util
from a2ctrl import connect
from a2ctrl.icons import Ico, Icons


log = a2core.get_logger(__name__)
UI_FILE_SUFFIX = '_ui'
NO_DRAW_TYPES = ['include', 'init']
ELEMENTS_PACKAGE = 'a2element'
_element_map = {}


def check_ui_module(module):
    if not a2core.is_dev_mode():
        return

    if getattr(sys, 'frozen', False):
        log.info('frozen! no need to compile %s' % module)
        return

    pyfile = module.__file__
    folder, pybase = os.path.split(pyfile)
    uiname = os.path.splitext(pybase)[0]
    uibase = None

    if uiname.endswith(UI_FILE_SUFFIX):
        uibase = uiname[:-len(UI_FILE_SUFFIX)] + '.ui'
    else:
        with open(pyfile, 'r') as fobj:
            line = fobj.readline()
            while line and uibase is not None:
                line = line.strip()
                if line.startswith('# Form implementation '):
                    uibase = line[line.rfind("'", 0, -1) + 1:-1]
                    uibase = os.path.basename(uibase.strip())
                    log.debug('checkUiModule from read: %s' % uibase)
                line = fobj.readline()

    if uibase is None:
        raise RuntimeError('Could not get source ui file from module:\n %s\n  '
                           'Not a ui file module??!' % module)

    uifile = os.path.join(folder, uibase)
    if not uibase or not os.path.isfile(uifile):
        # Nothing to test against. That's alright!
        # log.debug('Ui-file not found: %s' % pybase)
        return

    py_time = os.path.getmtime(pyfile)
    ui_time = os.path.getmtime(uifile)
    diff = py_time - ui_time
    if diff < 0:
        log.debug('%s needs compile! (age: %is)' % (pybase, diff))
        with open(pyfile, 'w') as pyfobj:
            compileUi(uifile, pyfobj)
        reload(module)


def draw(main, cfg, mod):
    """
    Mapper that returns display control objects
    according to the 'typ' of a config element.
    """
    typ = cfg.get('typ')
    if typ in NO_DRAW_TYPES:
        return

    mod_path = None if mod is None else mod.path
    ElementDrawClass = get_a2element_object('Draw', typ, mod_path)

    if ElementDrawClass is not None:
        try:
            return ElementDrawClass(main, cfg, mod)
        except Exception:
            log.error(traceback.format_exc().strip())
    log.error('Draw type "%s" not supported (yet)! Module: %s' % (typ, mod))


def edit(cfg, main, parent_cfg):
    mod_path = None if main.mod is None else main.mod.path
    ElementEditClass = get_a2element_object('Edit', cfg.get('typ'), mod_path)
    if ElementEditClass is not None:
        try:
            return ElementEditClass(cfg, main, parent_cfg)
        except Exception:
            log.error(traceback.format_exc().strip())
    log.error('Error getting Edit class for type "%s"!'
              ' Type not supported (yet)?!' % cfg.get('typ'))


def get_a2element_object(obj_name, element_type, module_path=None):
    """
    :param str obj_name:
    :param element_type:
    :param module_path:
    :rtype: class
    """
    element_mod = get_a2element(element_type)
    if element_mod is not None:
        return getattr(element_mod, obj_name)

    elif module_path:
        element_objects = get_local_element(os.path.join(module_path, element_type + '.py'))
        if obj_name not in element_objects:
            raise RuntimeError('Local Element "%s" has no object "%s"!!' % (element_type, obj_name))
        return element_objects[obj_name]


def get_a2element(element_type):
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

        # import error is expected if the element is local only
        except ImportError:
            pass
        except Exception:
            log.error(traceback.format_exc().strip())
            log.error('Could not import element type "%s"!' % element_type)


def get_local_element(itempath):
    if os.path.isfile(itempath):
        with open(itempath) as fobj:
            element_content = fobj.read()

        element_objects = {}
        try:
            exec(element_content, element_objects)
            # element_objects.pop('__builtins__')

        except Exception:
            log.error(traceback.format_exc().strip())
            log.error('Could not exec code from "%s"' % itempath)
        return element_objects
    else:
        raise RuntimeError('Cannot load local element! File does not exist! (%s)' % itempath)


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
                log.error('Fetched wrong type for attr_name %s: %s' % (attr_name, value))
                value = default

    return value


def assemble_settings(module_key, cfg_dict, db_dict, module_path=None):
    a2obj = a2core.A2Obj.inst()
    for cfg in cfg_dict:
        # get configs named db entry of module or None
        cfg_name = a2util.get_cfg_default_name(cfg)
        user_cfg = a2obj.db.get(cfg_name, module_key)
        # pass if there is an 'enabled' entry and it's False
        if not get_cfg_value(cfg, user_cfg, 'enabled', default=True):
            continue

        element_get_settings_func = get_a2element_object('get_settings', cfg['typ'], module_path)

        # no result try again with getting the module path:
        if element_get_settings_func is None and module_path is None:
            source_name, mod_name = module_key.split('|')
            module_path = a2obj.module_sources[source_name].mods[mod_name].path
            element_get_settings_func = get_a2element_object('get_settings', cfg['typ'], module_path)

        if element_get_settings_func is not None:
            try:
                element_get_settings_func(module_key, cfg, db_dict, user_cfg)
            except Exception:
                log.error(traceback.format_exc().strip())
                log.error('Error calling get_settings function for module: "%s"' % module_key)


if __name__ == '__main__':
    import a2app
    a2app.main()
