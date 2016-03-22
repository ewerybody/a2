'''
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

nfo item is always the 0th entry in the config.json it just draws and holds all
the author, name, version, description info

@created: Mar 6, 2015
@author: eRiC
'''
import sys
import ahk
import time
import a2core
import logging
import inspect
import threading
import importlib
import subprocess
from copy import deepcopy
from functools import partial
from pysideuic import compileUi
from PySide import QtGui, QtCore
from a2ctrl import inputDialog_ui
from os.path import join, getmtime, dirname, basename, exists, splitext


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
    pypath = dirname(pyfile)
    uibase = None
    
    if uiname.endswith(UI_FILE_SUFFIX):
        uibase = uiname[:-len(UI_FILE_SUFFIX)] + '.ui'
        log.debug('checkUiModule from name: %s' % uibase)
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
    
    uifile = join(pypath, uibase)
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
    if cfg['typ'] == 'nfo':
        return DrawNfo(cfg)
    else:
        for typ, ctrl_class in [('checkBox', a2ctrl.check.Draw),
                                ('hotkey', a2ctrl.hotkey.Draw),
                                ('groupBox', a2ctrl.group.Draw),
                                ('string', a2ctrl.string.Draw)]:
            if cfg['typ'] == typ:
                return ctrl_class(main, cfg, mod)


class DrawCtrl(QtGui.QWidget):
    def __init__(self, main, cfg, mod, _init_ctrl=True):
        if _init_ctrl:
            super(DrawCtrl, self).__init__()
        self.a2 = a2core.a2
        self.main = main
        self.cfg = cfg
        self.mod = mod
        self.userCfg = self.a2.db.get(self.cfg['name'], self.mod.name)

    def change(self, specific=None):
        self.mod.change()
        if self.mod.enabled:
            self.main.settings_changed(specific)


class DrawWelcome(QtGui.QWidget):
    'Hello user! Welcome to a2! This is a template introduction Text. So far there is not much to say. I just wanted this to fill up more than one line properly. Voila!'


class DrawNfo(QtGui.QWidget):
    def __init__(self, cfg):
        super(DrawNfo, self).__init__()
        global lenM, fontL
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, lenM / 2)
        self.label = QtGui.QLabel(self)
        self.label.setText(cfg.get('description') or '')
        self.label.setFont(fontL)
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)


def edit(cfg, main, parentCfg):
    if cfg['typ'] == 'nfo':
        return EditNfo(cfg)
    elif cfg['typ'] == 'include':
        return EditInclude(cfg, main, parentCfg)
    elif cfg['typ'] == 'hotkey':
        return a2ctrl.hotkey.Edit(cfg, main, parentCfg)
    elif cfg['typ'] == 'checkBox':
        return a2ctrl.check.Edit(cfg, main, parentCfg)
    elif cfg['typ'] == 'groupBox':
        return a2ctrl.group.Edit(cfg, main, parentCfg)
    elif cfg['typ'] == 'string':
        return a2ctrl.string.Edit(cfg, main, parentCfg)


class EditNfo(QtGui.QGroupBox):
    def __init__(self, cfg):
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


class EditCtrl(QtGui.QGroupBox):
    """
    frame widget for an edit control which enables basic arrangement of the
    control up & down as well as deleting the control.
    
    It's made to work with handwritten and compiled Uis right away.
    To embedd a compiled ui tell it so addLayout=False in the super()-statement:
        super(MyNewCtrl, self).__init__(addLayout=False)
    state the mainWidget in setupUi:
        self.ui.setupUi(self.mainWidget)
    and then set the self.mainWidget-layout to your top layout in the compiled ui:
        self.mainWidget.setLayout(self.ui.mytoplayout)
    
    TODO: currently this is embedded as menuitems on a button which is pretty shitty.
        I'd like to have some actual up/down buttons and an x to indicate delete
        functionality
    """
    ctrlType = 'EditCtrl'
    
    def __init__(self, cfg, main, parentCfg, addLayout=True):
        super(EditCtrl, self).__init__()
        self.a2 = a2core.a2
        self.cfg = cfg
        self.main = main
        self.parentCfg = parentCfg
        self._setupUi(addLayout)
        self.helpUrl = self.a2.urls.helpEditCtrl
    
    def move(self, value, *args):
        if self.parentCfg and self.parentCfg[0].get('typ', '') == 'nfo':
            top_index = 1
        else:
            top_index = 0
        
        index = self.parentCfg.index(self.cfg)
        maxIndex = len(self.parentCfg) - 1
        if isinstance(value, bool):
            if value:
                newindex = top_index
                #self.main.ui.scrollArea.scrollToTop()
                #self.main.ui.scrollArea
            else:
                newindex = maxIndex
                self.scrolltobottom()
        else:
            newindex = index + value
        # hop out if already at start or end
        if index == newindex or newindex < top_index or newindex > maxIndex:
            #print('returning from move! curr/new/max: %s/%s/%s' % (index, newindex, maxIndex))
            return
        
        #cfg = self.parentCfg.pop(index)
        self.parentCfg.pop(index)
        self.parentCfg.insert(newindex, self.cfg)
        self.main.editMod()
    
    def delete(self):
        if self.cfg in self.parentCfg:
            self.parentCfg.remove(self.cfg)
            self.main.editMod()

    def duplicate(self):
        self._scrollValB4 = self.main.ui.scrollBar.value()
        self._scrollMaxB4 = self.main.ui.scrollBar.maximum()
        newCfg = deepcopy(self.cfg)
        self.parentCfg.append(newCfg)
        self.main.editMod()

        threading.Thread(target=self.scrolltobottom).start()
    
    def cut(self):
        self.main.edit_clipboard.append(deepcopy(self.cfg))
        self.delete()
    
    def help(self):
        self.main.surfTo(self.helpUrl)

    def _setupUi(self, addLayout):
        self.setTitle(self.cfg['typ'])
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self._ctrlLayout = QtGui.QHBoxLayout(self)
        self._ctrlLayout.setSpacing(0)
        self._ctrlLayout.setContentsMargins(0, 0, 0, 0)
        self.mainWidget = QtGui.QWidget(self)
        if addLayout:
            self.mainLayout = QtGui.QVBoxLayout()
            self.mainLayout.setContentsMargins(5, 5, 5, 5)
            self.mainWidget.setLayout(self.mainLayout)
        self._ctrlLayout.addWidget(self.mainWidget)
        
        self._ctrlButtonLayout = QtGui.QVBoxLayout()
        self._ctrlButtonLayout.setSpacing(0)
        self._ctrlButtonLayout.setContentsMargins(5, 0, 5, 5)
        self._ctrlButtonLayout.setObjectName("ctrlButtonLayout")
        
        self._ctrlButton = QtGui.QPushButton(self)
        self._ctrlButton.setMinimumSize(QtCore.QSize(40, 40))
        self._ctrlButton.setMaximumSize(QtCore.QSize(40, 40))
        self._ctrlButton.setText("...")
        self._ctrlButton.setFlat(True)
        self._ctrlButton.setObjectName("ctrlButton")
        self._ctrlButtonLayout.addWidget(self._ctrlButton)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum,
                                       QtGui.QSizePolicy.Expanding)
        self._ctrlButtonLayout.addItem(spacerItem)
        self._ctrlLayout.addLayout(self._ctrlButtonLayout)
        self._ctrlLayout.setStretch(0, 1)
        
        self._ctrlMenu = QtGui.QMenu(self)
        self._ctrlMenu.aboutToShow.connect(self.buildMenu)
        self._ctrlButton.setMenu(self._ctrlMenu)

    def buildMenu(self):
        self._ctrlMenu.clear()
        menu_items = [('Up', partial(self.move, -1)),
                      ('Down', partial(self.move, 1)),
                      ('To Top', partial(self.move, True)),
                      ('To Bottom', partial(self.move, False)),
                      ('Delete', self.delete),
                      ('Duplicate', self.duplicate),
                      ('Help on %s' % self.ctrlType, self.help)]
        
        clipboard_count = ''
        if self.main.edit_clipboard:
            clipboard_count = ' (%i)' % len(self.main.edit_clipboard)
        
        if self.ctrlType == 'Groupbox':
            menu_items.insert(-1, ('Paste' + clipboard_count, self.paste))
        else:
            menu_items.insert(-1, ('Cut' + clipboard_count, self.cut))

        for item in menu_items:
            action = QtGui.QAction(self._ctrlMenu)
            action.setText(item[0])
            action.triggered.connect(item[1])
            self._ctrlMenu.addAction(action)

    def connectCfgCtrls(self, uiclass):
        """
        browses all members of the ui object to connect ones named 'cfg_'
        with the EditCtrls current cfg and fill it with current value.
        """
        for ctrl in inspect.getmembers(uiclass):
            if not ctrl[0].startswith('cfg_'):
                continue
            
            name = ctrl[0][4:]
            control = ctrl[1]
            
            if isinstance(control, QtGui.QCheckBox):
                # checkBox.clicked doesn't send state, so we put the func to check
                # checkBox.stateChanged does! But sends int: 0, 1, 2 for off, tri, on
                # solution: control.clicked[bool] sends the state already!
                control.clicked[bool].connect(partial(self._updateCfgData, name))
                # set ctrl according to config or set config from ctrl
                if name in self.cfg:
                    control.setChecked(self.cfg[name])
                else:
                    self.cfg[name] = control.isChecked()
            
            elif isinstance(control, QtGui.QLineEdit):
                control.textChanged.connect(partial(self._updateCfgData, name))
                if name in self.cfg:
                    control.setText(self.cfg[name])
                else:
                    self.cfg[name] = control.text()
            
            elif isinstance(control, QtGui.QComboBox):
                control.currentIndexChanged.connect(partial(self._updateCfgData, name))
                if name in self.cfg:
                    control.setCurrentIndex(self.cfg[name])
                else:
                    self.cfg[name] = control.currentIndex()

            elif isinstance(control, QtGui.QListWidget):
                # so far only to fill the control
                if name in self.cfg:
                    control.insertItems(0, self.cfg[name])
                else:
                    items = [control.item(i).text() for i in range(control.count())]
                    self.cfg[name] = items

            else:
                log.error('Cannot handle widget "%s"!\n  type "%s" NOT covered yet!' %
                          (ctrl[0], type(control)))
    
    def _updateCfgData(self, name, data=None, func=None):
        """
        issued from a control change function this sets an according item in config dict
        """
        if data is not None:
            self.cfg[name] = data
        elif func is not None:
            self.cfg[name] = func()

    def scrolltobottom(self, *args):
        print('scrollValB4: %s' % self._scrollValB4)
        time.sleep(0.1)
        tmax = 0.3
        curve = QtCore.QEasingCurve(QtCore.QEasingCurve.OutQuad)
        res = 0.01
        steps = tmax / res
        tsteps = 1 / steps
        t = 0.0
        #this = self.main.ui.scrollBar.value()
        scrollEnd = self.main.ui.scrollBar.maximum()
        print('scrollEnd: %s' % scrollEnd)
        if not scrollEnd:
            scrollEnd = self._scrollMaxB4 + 100
        r = scrollEnd - self._scrollValB4
        self.main.ui.scrollBar.setValue(self._scrollValB4)
        while t <= 1.0:
            time.sleep(res)
            t += tsteps
            v = curve.valueForProgress(t)
            scrollval = self._scrollValB4 + (v * r)
            self.main.ui.scrollBar.setValue(scrollval)


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
        
        self.menu = QtGui.QMenu(self.addButton)
        self.menu.aboutToShow.connect(self.populateMenu)
        self.addButton.setMenu(self.menu)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.baselayout.addItem(spacerItem)

    def populateMenu(self):
        self.menu.clear()
        self.menu_include = BrowseScriptsMenu(self.main, self.addCtrl)
        self.menu.addMenu(self.menu_include)

        for typ in ('checkBox hotkey groupBox string textField floatField intField '
                    'fileField text button comboBox').split():
            action = QtGui.QAction(self.menu)
            action.setText(typ)
            action.triggered.connect(partial(self.addCtrl, typ))
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
        self.setTitle('include')
        self.aboutToShow.connect(self.buildMenu)
        self.tempConfig = self.main.tempConfig

    def buildMenu(self):
        self.clear()
        scriptsInUse = set()
        for cfg in self.tempConfig:
            if cfg['typ'] == 'include':
                scriptsInUse.add(cfg['file'])
        
        scriptsUnused = set(self.main.mod.scripts) - scriptsInUse
        
        for scriptName in scriptsUnused:
            action = QtGui.QAction(self)
            action.setText(scriptName)
            action.triggered.connect(partial(self.setScript, scriptName))
            self.addAction(action)

        newIncludeAction = QtGui.QAction(self)
        newIncludeAction.setText('create new')
        newIncludeAction.triggered.connect(self.setScript)
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


def list_getAllItems_asText(listCtrl):
    return [listCtrl.item(i).text() for i in range(listCtrl.count())]


def list_selectItems(listCtrl, text):
    if isinstance(text, str):
        text = [text]
    
    lastitem = None
    for i in range(listCtrl.count()):
        this = listCtrl.item(i)
        if text is not None and this.text() in text:
            this.setSelected(True)
            lastitem = this
        else:
            this.setSelected(False)
    if lastitem is not None:
        listCtrl.setCurrentItem(lastitem)


def getCfgValue(subCfg, userCfg, attrName):
    """
    unified call to get a value no matter if its set by user already
    or still default from the module config.
    """
    if userCfg is not None and attrName in userCfg:
        return userCfg[attrName]
    elif attrName in subCfg:
        return subCfg[attrName]
    else:
        return None


# deferred import of sub controls because they might use any part of this module
import a2ctrl.check, a2ctrl.hotkey, a2ctrl.group, a2ctrl.string, a2ctrl.a2settings, a2ctrl.number

# import first, then add here for reload coverage
reload_modules = [
    a2ctrl.check,
    a2ctrl.hotkey,
    a2ctrl.a2settings,
    a2ctrl.group,
    a2ctrl.string,
    a2ctrl.number]

ui_modules = [
    inputDialog_ui,
    a2ctrl.check.checkbox_edit_ui,
    a2ctrl.hotkey.hotkey_edit_ui,
    a2ctrl.hotkey.scopeDialog_ui,
    a2ctrl.group.group_edit_ui,
    a2ctrl.string.string_edit_ui,
    a2ctrl.a2settings.a2settings_ui,
    a2ctrl.number.number_edit_ui]


def check_all_ui():
    for uimod in ui_modules:
        check_ui_module(uimod)


if __name__ == '__main__':
    import a2app
    a2app.main()
