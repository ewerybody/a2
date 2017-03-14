# -*- coding: utf-8 -*-
"""
a2ctrl - basic functionality for all the a2element building blocks

@created: Mar 6, 2015
@author: eRiC
"""
import os
import sys
import traceback
import collections
from functools import partial
from pysideuic import compileUi
from importlib import reload, import_module
from os.path import getmtime, dirname, basename, exists, splitext

from PySide import QtGui

import a2core
from a2ctrl.base import Ico, Icons


log = a2core.get_logger(__name__)
UI_FILE_SUFFIX = '_ui'
NO_DRAW_TYPES = ['include', 'init']
ELEMENTS_PACKAGE = 'a2element'
_element_map = {}


def check_ui_module(module):
    if getattr(sys, 'frozen', False):
        log.info('frozen! no need to compile %s' % module)
        return

    pyfile = module.__file__
    pybase = basename(pyfile)
    uiname = splitext(pybase)[0]
    folder = dirname(pyfile)
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
                    uibase = basename(uibase.strip())
                    log.debug('checkUiModule from read: %s' % uibase)
                line = fobj.readline()

    uifile = os.path.join(folder, uibase)
    if not uibase or not exists(uifile):
        log.error('Ui-file not found: %s' % pybase)
        return

    pyTime = getmtime(pyfile)
    uiTime = getmtime(uifile)
    diff = pyTime - uiTime
    if diff < 0:
        log.debug('%s needs compile! (age: %is)' % (pybase, diff))
        with open(pyfile, 'w') as pyfobj:
            compileUi(uifile, pyfobj)
        reload(module)


def draw(main, cfg, mod):
    """
    mapper that returns display control objects
    according to the 'typ' of a config element
    """
    if cfg.get('typ') in NO_DRAW_TYPES:
        return

    import a2element

    mod_path = None if mod is None else mod.path
    ElementDrawClass = get_a2element_object('Draw', cfg.get('typ'), mod_path)

    if ElementDrawClass is not None:
        try:
            return ElementDrawClass(main, cfg, mod)
        except Exception:
            log.error(traceback.format_exc().strip())
    log.error('Draw type "%s" not supported (yet)! Module: %s' % (cfg.get('typ'), mod))


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
    element_mod = get_a2element(element_type)
    if element_mod is not None:
        return getattr(element_mod, obj_name)
    elif module_path:
        element_objects = get_local_element(os.path.join(module_path, element_type + '.py'))
        if obj_name not in element_objects:
            raise RuntimeError('Local Element "%s" has no object "%s"!!' % (element_type, obj_name))
        return element_objects[obj_name]
    else:
        log.error('Could not get object "%s" from element_type "%s"' % (obj_name, element_type))


def get_a2element(element_type):
    """
    From the "typ" tries to import the according module from a2element
    """
    try:
        return _element_map[element_type]
    except KeyError:
        try:
            element_mod_name = ELEMENTS_PACKAGE + '.' + element_type
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


class EditAddElem(QtGui.QWidget):
    """
    to add a control to a module setup. This will probably go into some popup
    later. This way its a little too clunky I think.

    TODO: the popup will show all available scripts to include in a sub menu
        * include > script1.ahk
                    script2.ahk
                    create new script
        * hotkey
        * checkBox
        * ...

    til: if you don't make this a widget and just a object Qt will forget about
    any connections you make!
    """
    def __init__(self, main, config):
        super(EditAddElem, self).__init__()
        self.main = main
        self.config = config
        self.baselayout = QtGui.QHBoxLayout(self)
        self.baselayout.setSpacing(5)

        self.a2add_button = QtGui.QPushButton('Add ...')
        self.a2add_button.setObjectName('a2add_button')
        self.baselayout.addWidget(self.a2add_button)

        self.menu = QtGui.QMenu(self)
        self.menu.aboutToShow.connect(self.populate_menu)
        self.a2add_button.setMenu(self.menu)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.baselayout.addItem(spacerItem)

    def populate_menu(self):
        self.menu.clear()
        self.menu_include = BrowseScriptsMenu(self.main, self._add_element)
        self.menu.addMenu(self.menu_include)

        import a2element
        for name, display_name, icon in a2element.get_list():
            action = QtGui.QAction(display_name, self.menu, triggered=partial(self._add_element, name))
            if icon:
                action.setIcon(icon)
            self.menu.addAction(action)

        self.menu.addSeparator()
        self.menu.addAction(self.main.ui.actionCreate_New_Element)
        self._check_for_local_element_mods()

    def _add_element(self, typ, name=''):
        """Just adds a new dict with the accodting typ value to the tempConfig.
        Only if it's an include we already enter the file selected.
        Every other default value will be handled by the very control element.
        """
        cfg = {'typ': typ}
        if typ == 'include':
            cfg['file'] = name

        self.config.append(cfg)
        self.main.edit_mod()

    def _check_for_local_element_mods(self):
        if self.main.mod is None:
            return

        for item in os.listdir(self.main.mod.path):
            itempath = os.path.join(self.main.mod.path, item)
            if not os.path.isfile(itempath):
                continue
            base, ext = os.path.splitext(item)
            if ext.lower() != '.py':
                continue

            element_objects = get_local_element(itempath)
            if element_objects is not None and 'Edit' in element_objects:
                name = element_objects['Edit'].element_name()
                icon = element_objects['Edit'].element_icon()

                action = QtGui.QAction(name, self.menu, triggered=partial(self._add_element, base))
                if icon:
                    action.setIcon(icon)
                self.menu.addAction(action)


class BrowseScriptsMenu(QtGui.QMenu):
    def __init__(self, main, func):
        super(BrowseScriptsMenu, self).__init__()
        self.func = func
        self.main = main
        self.setIcon(Icons.inst().code)
        self.setTitle('Include Script')
        self.aboutToShow.connect(self.build_menu)

    def build_menu(self):
        self.clear()
        scriptsInUse = set()
        for cfg in self.main.tempConfig:
            if cfg['typ'] == 'include':
                scriptsInUse.add(cfg['file'])

        icons = Icons.inst()
        scriptsUnused = set(self.main.mod.scripts) - scriptsInUse

        for scriptName in scriptsUnused:
            self.addAction(QtGui.QAction(icons.code, scriptName, self,
                                         triggered=partial(self.set_script, scriptName)))
        if scriptsUnused:
            self.addSeparator()
        newIncludeAction = QtGui.QAction(icons.code, 'Create New Script', self, triggered=self.set_script)
        self.addAction(newIncludeAction)

    def set_script(self, name='', create=False):
        if not name:
            from a2widget.a2input_dialog import A2InputDialog
            A2InputDialog(self.main, 'New Script', partial(self.set_script, create=True),
                          self.main.mod.check_create_script, text='awesomeScript',
                          msg='Give a name for the new script file:')
            return
        if create:
            name = self.main.mod.create_script(name, self.main.devset.author_name)
        self.func('include', name)


def get_local_element(itempath):
    if os.path.exists(itempath):
        with open(itempath) as fobj:
            element_content = fobj.read()

        try:
            element_objects = {}
            exec(element_content, element_objects)

            # element_objects.pop('__builtins__')
            return element_objects

        except Exception:
            log.error(traceback.format_exc().strip())
            log.error('Could not exec code from "%s"' % itempath)
    else:
        raise RuntimeError('Cannot load local element! File does not exist! (%s)' % itempath)


def get_cfg_value(element_cfg, user_cfg, attr_name=None, typ=None, default=None):
    """
    unified call to get a value no matter if its set by user already
    or still default from the module config.
    """
    value = None
    if user_cfg is not None and attr_name is None:
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

    for cfg in cfg_dict:
        # get configs named db entry of module or None
        cfg_name = a2core.get_cfg_default_name(cfg)
        user_cfg = a2core.A2Obj.inst().db.get(cfg_name, module_key)
        # pass if there is an 'enabled' entry and it's False
        if not get_cfg_value(cfg, user_cfg, 'enabled', default=True):
            continue

        element_get_settings = get_a2element_object('get_settings', cfg['typ'], module_path)
        if element_get_settings is not None:
            element_get_settings(module_key, cfg, db_dict, user_cfg)


if __name__ == '__main__':
    import a2app
    a2app.main()
