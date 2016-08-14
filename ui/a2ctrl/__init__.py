"""
# create header edit controls
def editctrl(nfoDict, keyName, typ, parent, editCtrls):
    if keyName not in nfoDict:
        return

    label = QtGui.QLabel('%s:' % keyName)
    parent.addWidget(label)
    if typ == 'text':
        inputctrl = QtGui.QPlainTextEdit()
        inputctrl.setPlainText(nfoDict.get(keyName) or '')
        inputctrl.setTabChangesFocus(True)
    else:
        inputctrl = QtGui.QLineEdit()
        inputctrl.setText(nfoDict.get(keyName) or '')
    parent.addWidget(inputctrl)
    editCtrls[keyName] = inputctrl

nfo item is always the 0th entry in the configuration. it just draws and holds all
the author, name, version, description info

@created: Mar 6, 2015
@author: eRiC
"""
import sys
import time
import logging
import inspect
import threading
import importlib
import subprocess
import collections
from copy import deepcopy
from functools import partial
from pysideuic import compileUi
from os.path import join, getmtime, dirname, basename, exists, splitext
from PySide import QtGui, QtCore, QtSvg

import ahk
import a2core
from a2ctrl import inputDialog_ui
from a2ctrl.path_field import PathField
from a2ctrl.base import EditCtrl, Ico, Icons, connect_cfg_controls


logging.basicConfig()
log = logging.getLogger('a2ctrl')
log.setLevel(logging.DEBUG)


uipath = dirname(__file__)
margin = 5
labelW = 100
lenM = 35
lenL = 61  # alright for 3 rows of text fontL
fontL = QtGui.QFont()
fontL.setFamily("Segoe UI")
fontL.setPointSize(10)
fontXL = QtGui.QFont()
fontXL.setFamily("Segoe UI")
fontXL.setPointSize(13)
uiScale = 1
UI_FILE_SUFFIX = '_ui'



class UIValues(object):
    spacing = 5


def adjustSizes(app):
    desk = app.desktop()
    dpi = desk.physicalDpiX()
    #print('dpi: %s' % dpi)
    if dpi >= 144:
        global labelW, lenM, lenL, fontL, fontXL, uiScale
        lenM *= 1.5
        lenL *= 1.5
        uiScale *= 1.6
        fontL.setPointSize(9)
        fontXL.setPointSize(13)
        labelW *= 1.6


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

    uifile = join(folder, uibase)
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
        importlib.reload(module)


def draw(main, cfg, mod):
    """
    mapper that returns display control objects
    according to the 'typ' of a config element
    """
    if cfg.get('typ') in draw_classes:
        return draw_classes[cfg['typ']](main, cfg, mod)
    # invisible types
    elif cfg.get('typ') in ['include']:
        return
    else:
        log.error('Draw type "%s" not supported (yet)! Module: %s' % (cfg.get('typ'), mod.name))


class DrawCtrl(QtGui.QWidget):
    def __init__(self, main, cfg, mod, _init_ctrl=True):
        if _init_ctrl:
            super(DrawCtrl, self).__init__()
        self.a2 = a2core.A2Obj.inst()
        self.main = main
        self.cfg = cfg
        self.mod = mod
        self.check_delay = 150
        self.userCfg = self.a2.db.get(self.cfg['name'], self.mod.name)

    def get_user_value(self, typ, name='value', default=None):
        """
        Get a user value.
        Name is 'value' by default so you can just get the default value by stating the type. Voila!
        """
        return get_cfg_value(self.cfg, self.userCfg, name, typ, default)

    def set_user_value(self, this, name='value'):
        """
        Set a user value.
        Name is 'value' by default so you can just set the default value by ... well:
        passing the value. Voila!
        """
        self.mod.set_user_cfg(self.cfg, name, this)

    def change(self, specific=None):
        self.mod.change()
        if self.mod.enabled:
            self.main.settings_changed(specific)

    def delayed_check(self, *args):
        QtCore.QTimer().singleShot(self.check_delay, partial(self.check, *args))

    def check(self, *args):
        pass


class DrawNfo(QtGui.QWidget):
    def __init__(self, main, cfg, mod):
        super(DrawNfo, self).__init__()
        global lenM, fontL
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, lenM / 2)
        self.label = QtGui.QLabel(self)
        self.label.setText(cfg.get('description') or '')
        self.label.setFont(fontL)
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)


def edit(cfg, main, parent_cfg):
    if cfg['typ'] in edit_classes:
        return edit_classes[cfg['typ']](cfg, main, parent_cfg)
    else:
        log.error('Edit type "%s" not supported (yet)!' % cfg['typ'])


class EditNfo(QtGui.QGroupBox):
    def __init__(self, cfg, main, parent_cfg):
        super(EditNfo, self).__init__()
        self.cfg = cfg
        self.typ = cfg['typ']
        self.setTitle('module information:')
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                             QtGui.QSizePolicy.Maximum))
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(5, 5, 5, 10)
        self.description = EditText('description', cfg.get('description'), self.layout, self.getCfg)
        self.author = EditLine('author', cfg.get('author'), self.layout, self.getCfg)
        self.version = EditLine('version', cfg.get('version'), self.layout, self.getCfg)
        self.date = EditLine('date', cfg.get('date'), self.layout, self.getCfg)
        self.url = EditLine('url', cfg.get('url') or '', self.layout, self.getCfg)

    def getCfg(self):
        self.cfg['description'] = self.description.value
        self.cfg['author'] = self.author.value
        self.cfg['version'] = self.version.value
        self.cfg['date'] = self.date.value
        self.cfg['url'] = self.url.value
        return self.cfg





class EditLine(QtGui.QWidget):
    def __init__(self, name, text, parentLayout=None, updatefunc=None):
        super(EditLine, self).__init__()
        global labelW
        self.name = name
        self.updatefunc = updatefunc
        self.parentLayout = parentLayout
        self.layout = QtGui.QHBoxLayout(self)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(margin, 0, margin, 0)
        self.labelCtrl = QtGui.QLabel('%s:' % name)
        self.labelCtrl.setMinimumWidth(labelW)
        self.labelCtrl.setAlignment(QtCore.Qt.AlignRight)
        self.layout.addWidget(self.labelCtrl)
        self.inputCtrl = QtGui.QLineEdit()
        self.inputCtrl.setText(str(text))
        self.inputCtrl.textChanged.connect(self.update)
        self.layout.addWidget(self.inputCtrl)
        if parentLayout:
            parentLayout.addWidget(self)

    def update(self):
        if self.updatefunc:
            self.updatefunc()

    @property
    def value(self):
        return self.inputCtrl.text()


class EditText(QtGui.QWidget):
    def __init__(self, name, text, parent=None, updatefunc=None):
        super(EditText, self).__init__()
        global labelW, lenL
        self.name = name
        self.parent = parent
        self.updatefunc = updatefunc
        self.baselayout = QtGui.QVBoxLayout(self)
        self.baselayout.setSpacing(5)
        self.baselayout.setContentsMargins(margin, 0, margin, 0)
        #self.labelCtrl = QtGui.QLabel('%s:' % name)
        #self.baselayout.addWidget(self.labelCtrl)
        self.inputCtrl = QtGui.QPlainTextEdit()
        self.inputCtrl.setPlainText(str(text))
        self.inputCtrl.setTabChangesFocus(True)
        self.inputCtrl.setMinimumSize(QtCore.QSize(16777215, lenL))
        self.inputCtrl.setMaximumSize(QtCore.QSize(16777215, lenL))
        self.inputCtrl.textChanged.connect(self.update)
        self.baselayout.addWidget(self.inputCtrl)
        if parent:
            parent.addWidget(self)

    def update(self):
        if self.updatefunc:
            self.updatefunc()

    @property
    def value(self):
        return self.inputCtrl.toPlainText()


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
        self.baselayout.setContentsMargins(margin, margin, margin, margin)

        self.addButton = QtGui.QPushButton('add ...')
        self.addButton.setStyleSheet('QPushButton {background-color:#37ED95}')
        self.addButton.setFont(fontXL)
        self.addButton.setMinimumSize(QtCore.QSize(lenL * 2, lenM))
        self.addButton.setMaximumHeight(lenM)
        self.baselayout.addWidget(self.addButton)

        self.menu = QtGui.QMenu(self)
        self.menu.aboutToShow.connect(self.populateMenu)
        self.addButton.setMenu(self.menu)
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
        self.main.editMod()


class EditInclude(EditCtrl):
    """
    User-invisible control that you only see in edit-mode
    """
    def __init__(self, cfg, main, parentCfg):
        self.ctrlType = 'Include'
        super(EditInclude, self).__init__(cfg, main, parentCfg, addLayout=False)
        self.main = main
        #self.layout = QtGui.QHBoxLayout(self.ctrlui.layout)
        self.layout = QtGui.QHBoxLayout()
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(10, margin, margin, margin)
        self.labelCtrl = QtGui.QLabel('script file:')
        self.labelCtrl.setMinimumWidth(labelW)
        self.labelCtrl.setAlignment(QtCore.Qt.AlignRight)
        self.layout.addWidget(self.labelCtrl)
        self.button = QtGui.QPushButton(self.cfg['file'])
        self.buttonMenu = BrowseScriptsMenu(self.main, self.setScript)
        self.button.setMenu(self.buttonMenu)
        self.layout.addWidget(self.button)

        self.editButton = QtGui.QPushButton('edit script')
        self.editButton.pressed.connect(self.editScript)
        self.layout.addWidget(self.editButton)

        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.layout.addItem(spacerItem)
        self.mainWidget.setLayout(self.layout)

    def setScript(self, typ, name):
        self.cfg['file'] = name
        self.button.setText(name)

    def editScript(self):
        subprocess.Popen([self.main.scriptEditor, join(self.main.mod.path, self.cfg['file'])])


class InputDialog(QtGui.QDialog):
    def __init__(self, parent, title, okFunc=None, checkFunk=None,
                 text='', msg='', size=None, *args):
        super(InputDialog, self).__init__(parent)
        self.ui = inputDialog_ui.Ui_InputDialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.okFunc = okFunc
        self.checkFunk = checkFunk
        self.setWindowTitle(title)
        self.output = None

        if self.checkFunk is not None:
            self.ui.textField.textChanged.connect(self.check)

        self.ui.okButton.setFont(fontXL)
        self.ui.okButton.clicked.connect(self.okay)
        self.ui.cancelButton.setFont(fontXL)
        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.label.setFont(fontL)
        self.ui.label.setText(msg)
        self.ui.textField.setFont(fontL)
        self.ui.textField.setText(text)
        self.ui.textField.setFocus()

        if size:
            self.resize(size[0], size[1])

        self.show()

    def check(self, name):
        if self.checkFunk is not None:
            answer = self.checkFunk(name)
            if answer is True:
                self.ui.okButton.setEnabled(True)
                self.ui.okButton.setToolTip(None)
            else:
                self.ui.okButton.setEnabled(False)
                self.ui.okButton.setToolTip(answer)

    def okay(self):
        txt = self.ui.textField.text()
        self.output = txt
        self.close()
        if self.okFunc is not None:
            self.okFunc(txt)


class Popup(QtGui.QWidget):
    """QtCore.Qt.Window
    | QtCore.Qt.CustomizeWindowHint
    """
    def __init__(self, x, y, closeOnLeave=True, parent=None):
        super(Popup, self).__init__(parent=parent)
        self.setpos = (x, y)
        self.closeOnLeave = closeOnLeave
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape),
                        self, self.close)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)

    def placeAtCursor(self):
        x, y = self.setpos
        pos = self.pos()
        pos.setX(x - (self.width() / 2))
        pos.setY(y - (self.height() / 2))
        self.move(pos)

    def leaveEvent(self, event):
        if self.closeOnLeave:
            self.close()

    def focusOutEvent(self, event):
        self.close()
        #self.focusOutEvent()


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
            InputDialog(self.main, 'New Script', partial(self.setScript, create=True),
                        self.main.mod.checkCreateScript, text='awesomeScript',
                        msg='Give a name for the new script file:', size=(400, 50))
            return
        if create:
            name = self.main.mod.createScript(name)
        self.func('include', name)





def get_cfg_value(subCfg, userCfg, attrName, typ=None, default=None):
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


# deferred import of sub controls because they might use any part of this module
import a2ctrl.check, a2ctrl.hotkey, a2ctrl.group, a2ctrl.string, a2ctrl.a2settings, a2ctrl.number
import a2ctrl.combo, a2ctrl.path, a2ctrl.hotkey_func, a2ctrl.hotkey_scope, a2ctrl.a2module_list
import a2ctrl.a2module_view

# import first, then add here for reload coverage
reload_modules = [
    a2ctrl.check,
    a2ctrl.hotkey,
    a2ctrl.hotkey_func,
    a2ctrl.hotkey_scope,
    a2ctrl.a2settings,
    a2ctrl.group,
    a2ctrl.string,
    a2ctrl.number,
    a2ctrl.combo,
    a2ctrl.path]

ui_modules = [
    inputDialog_ui,
    a2ctrl.check.check_edit_ui,
    a2ctrl.hotkey.hotkey_edit_ui,
    a2ctrl.hotkey_scope.scopeDialog_ui,
    a2ctrl.group.group_edit_ui,
    a2ctrl.string.string_edit_ui,
    a2ctrl.a2settings.a2settings_ui,
    a2ctrl.a2module_list.a2module_list_ui,
    a2ctrl.a2module_view.a2module_view_ui,
    a2ctrl.number.number_edit_ui,
    a2ctrl.combo.combo_edit_ui,
    a2ctrl.path.path_edit_ui]

draw_classes = {'nfo': DrawNfo,
                'hotkey': a2ctrl.hotkey.Draw,
                'check': a2ctrl.check.Draw,
                'group': a2ctrl.group.Draw,
                'string': a2ctrl.string.Draw,
                'number': a2ctrl.number.Draw,
                'combo': a2ctrl.combo.Draw,
                'path': a2ctrl.path.Draw}

edit_classes = {'nfo': EditNfo,
                'include': EditInclude,
                'hotkey': a2ctrl.hotkey.Edit,
                'check': a2ctrl.check.Edit,
                'group': a2ctrl.group.Edit,
                'string': a2ctrl.string.Edit,
                'number': a2ctrl.number.Edit,
                'combo': a2ctrl.combo.Edit,
                'path': a2ctrl.path.Edit}


def check_all_ui():
    for uimod in ui_modules:
        check_ui_module(uimod)


if __name__ == '__main__':
    import a2app
    a2app.main()
