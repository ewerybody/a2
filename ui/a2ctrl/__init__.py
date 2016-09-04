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
from a2ctrl import connect
from a2ctrl.base import Ico, Icons
from a2widget.a2input_dialog import A2InputDialog


log = a2core.get_logger(__name__)
UI_FILE_SUFFIX = '_ui'
NO_DRAW_TYPES = ['include']
ELEMENTS_PACKAGE = 'a2element'
_element_map = {}


def check_ui_module(module):
    pyfile = module.__file__
    pybase = basename(pyfile)
    uiname = splitext(pybase)[0]
    folder = dirname(pyfile)
    uibase = None

    if uiname.endswith(UI_FILE_SUFFIX):
        uibase = uiname[:-len(UI_FILE_SUFFIX)] + '.ui'
        #log.debug('checkUiModule from name: %s' % uibase)
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

    element_mod = get_a2element(cfg.get('typ'))
    if element_mod is not None:
        try:
            return element_mod.Draw(main, cfg, mod)
        except Exception as error:
            log.error(traceback.format_exc().strip())
            print('error: %s' % error)
            log.error('Draw type "%s" not supported (yet)! Module: %s' % (cfg.get('typ'), mod.name))


def edit(cfg, main, parent_cfg):
    element_mod = get_a2element(cfg.get('typ'))
    if element_mod is not None:
        try:
            return element_mod.Edit(cfg, main, parent_cfg)
        except Exception as error:
            log.error(traceback.format_exc().strip())
            print('error: %s' % error)
            log.error('Edit type "%s" not supported (yet)!' % cfg.get('typ'))


def get_a2element(element_type):
    """
    From the "typ" tries to import the according module from a2element
    """
    try:
        return _element_map[element_type]
    except KeyError:
        try:
            element_mod_name = ELEMENTS_PACKAGE + '.' + element_type
            if element_mod_name not in sys.modules:
                element_mod = import_module(element_mod_name, ELEMENTS_PACKAGE)
            else:
                element_mod = sys.modules[element_mod_name]

            _element_map[element_type] = element_mod
            return element_mod

        except Exception as error:
            log.error(traceback.format_exc().strip())
            print('error: %s' % error)
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
        self.menu.aboutToShow.connect(self.populateMenu)
        self.a2add_button.setMenu(self.menu)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.baselayout.addItem(spacerItem)

    def populateMenu(self):
        icons = Icons.inst()
        self.menu.clear()
        self.menu_include = BrowseScriptsMenu(self.main, self.addCtrl)
        self.menu.addMenu(self.menu_include)

        menu_items = collections.OrderedDict()
        menu_items['check'] = ('CheckBox', icons.check)
        menu_items['hotkey'] = ('Hotkey', icons.hotkey)
        menu_items['group'] = ('GroupBox', icons.group)
        menu_items['string'] = ('String', icons.string)
        menu_items['number'] = ('Number', icons.number)
        menu_items['combo'] = ('ComboBox', icons.combo)
        menu_items['path'] = ('Path', icons.folder)
        #'text'] = ('TextField', None),
        #'button'] = ('Button', None)

        for typ, values in menu_items.items():
            action = QtGui.QAction(values[0], self.menu, triggered=partial(self.addCtrl, typ))
            if values[1]:
                action.setIcon(values[1])
            self.menu.addAction(action)

    def addCtrl(self, typ, name=''):
        """Just adds a new dict with the accodting typ value to the tempConfig.
        Only if it's an include we already enter the file selected.
        Every other default value will be handled by the very control element.
        """
        cfg = {'typ': typ}
        if typ == 'include':
            cfg['file'] = name

        self.config.append(cfg)
        self.main.edit_mod()


class BrowseScriptsMenu(QtGui.QMenu):
    def __init__(self, main, func):
        super(BrowseScriptsMenu, self).__init__()
        self.func = func
        self.main = main
        self.setIcon(Icons.inst().code)
        self.setTitle('Include')
        self.aboutToShow.connect(self.buildMenu)
        self.tempConfig = self.main.tempConfig

    def buildMenu(self):
        self.clear()
        scriptsInUse = set()
        for cfg in self.tempConfig:
            if cfg['typ'] == 'include':
                scriptsInUse.add(cfg['file'])

        icons = Icons.inst()
        scriptsUnused = set(self.main.mod.scripts) - scriptsInUse

        for scriptName in scriptsUnused:
            action = QtGui.QAction(icons.code, scriptName, self,
                                   triggered=partial(self.setScript, scriptName))
            self.addAction(action)
        newIncludeAction = QtGui.QAction(icons.code, 'create new', self, triggered=self.setScript)
        self.addAction(newIncludeAction)

    def setScript(self, name='', create=False):
        if not name:
            A2InputDialog(self.main, 'New Script', partial(self.setScript, create=True),
                          self.main.mod.checkCreateScript, text='awesomeScript',
                          msg='Give a name for the new script file:', size=(400, 50))
            return
        if create:
            name = self.main.mod.createScript(name)
        self.func('include', name)


def get_cfg_value(subCfg, userCfg, attrName='value', typ=None, default=None):
    """
    unified call to get a value no matter if its set by user already
    or still default from the module config.
    """
    value = None
    if userCfg is not None and attrName in userCfg:
        value = userCfg[attrName]
    elif attrName in subCfg:
        value = subCfg[attrName]

    if typ is not None:
        if not isinstance(value, typ):
            log.error('Fetched wrong type for attrName %s: %s' % (attrName, value))
            if default is None:
                value = typ()
            else:
                value = default

    return value


def assemble_settings(module_key, cfg_dict, db_dict):

    for cfg in cfg_dict:
        # get configs named db entry of module or None
        user_cfg = a2core.A2Obj.inst().db.get(cfg.get('name'), module_key)
        # pass if there is an 'enabled' entry and its False
        if not get_cfg_value(cfg, user_cfg, 'enabled', default=True):
            continue

        cfg_pymod = get_a2element(cfg['typ'])
        cfg_pymod.get_settings(module_key, cfg, db_dict, user_cfg)


if __name__ == '__main__':
    import a2app
    a2app.main()
