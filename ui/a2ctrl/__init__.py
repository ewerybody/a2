'''
Created on Mar 6, 2015

@author: eRiC

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
'''
from PySide import QtGui, QtCore
from pysideuic import compileUi
from os.path import join, getmtime, dirname, basename, exists, splitext
from copy import deepcopy
from functools import partial
import subprocess
import inspect
import importlib
import time
import threading
from a2ctrl import inputDialog_ui
import ahk
import logging


logging.basicConfig()
log = logging.getLogger(__name__)
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
    print('dpi: %s' % dpi)
    if dpi >= 144:
        global labelW, lenM, lenL, fontL, fontXL, uiScale
        lenM *= 1.5
        lenL *= 1.5
        uiScale *= 1.6
        fontL.setPointSize(9)
        fontXL.setPointSize(13)
        labelW *= 1.6


def checkUiModule(module):
    pyfile = module.__file__
    pybase = basename(pyfile)
    uiname = splitext(pybase)[0]
    pypath = dirname(pyfile)
    uibase = None
    
    if uiname.endswith(UI_FILE_SUFFIX):
        uibase = uiname[:-len(UI_FILE_SUFFIX)] + '.ui'
    else:
        with open(pyfile, 'r') as fobj:
            line = fobj.readline()
            while line or uibase is not None:
                line = line.strip()
                if line.startswith('# Form implementation '):
                    uibase = line[line.rfind("'", 0, -1) + 1:-1]
                    uibase = basename(uibase)
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
    return


def draw(cfg, mod):
    """
    mapper that returns display control objects
    according to the 'typ' of a config element
    """
    if cfg['typ'] == 'nfo':
        return DrawNfo(cfg)
    elif cfg['typ'] == 'checkBox':
        return a2ctrl.check.Draw(cfg, mod)
    elif cfg['typ'] == 'hotkey':
        return a2ctrl.hotkey.Draw(cfg, mod)
    elif cfg['typ'] == 'groupBox':
        return a2ctrl.group.Draw(cfg, mod)


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


def edit(cfg, mod, main):
    if cfg['typ'] == 'nfo':
        return EditNfo(cfg)
    elif cfg['typ'] == 'include':
        return EditInclude(cfg, mod, main)
    elif cfg['typ'] == 'hotkey':
        return a2ctrl.hotkey.Edit(cfg, main)
    elif cfg['typ'] == 'checkBox':
        return a2ctrl.check.Edit(cfg, main)
    elif cfg['typ'] == 'groupBox':
        return a2ctrl.group.Edit(cfg, main)


class EditNfo(QtGui.QGroupBox):
    def __init__(self, data):
        super(EditNfo, self).__init__()
        self.data = data
        self.typ = data['typ']
        self.setTitle('module information:')
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                             QtGui.QSizePolicy.Maximum))
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(5, 5, 5, 10)
        self.description = EditText('description', data.get('description'), self.layout, self.getCfg)
        self.author = EditLine('author', data.get('author'), self.layout, self.getCfg)
        self.version = EditLine('version', data.get('version'), self.layout, self.getCfg)
        self.date = EditLine('date', data.get('date'), self.layout, self.getCfg)
        self.url = EditLine('url', data.get('url') or '', self.layout, self.getCfg)

    def getCfg(self):
        self.data['description'] = self.description.value
        self.data['author'] = self.author.value
        self.data['version'] = self.version.value
        self.data['date'] = self.date.value
        self.data['url'] = self.url.value
        return self.data


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
    
    def __init__(self, cfg, main, addLayout=True):
        super(EditCtrl, self).__init__()
        self.cfg = cfg
        self.main = main
        self._setupUi(addLayout)
        self._getCfgList = []
        self.helpUrl = self.main.urls.helpEditCtrl
    
    def delete(self):
        if self.cfg in self.main.tempConfig:
            self.main.tempConfig.remove(self.cfg)
            self.main.editMod()
    
    def move(self, value, *args):
        index = self.main.tempConfig.index(self.cfg)
        maxIndex = len(self.main.tempConfig) - 1
        if isinstance(value, bool):
            if value:
                newindex = 1
                #self.main.ui.scrollArea.scrollToTop()
                #self.main.ui.scrollArea
            else:
                newindex = maxIndex
                #self.main.ui.scrollArea.scrollToBottom()
        else:
            newindex = index + value
        # hop out if already at start or end
        if index == newindex or newindex < 1 or newindex > maxIndex:
            #print('returning from move! curr/new/max: %s/%s/%s' % (index, newindex, maxIndex))
            return
        
        #cfg = self.main.tempConfig.pop(index)
        self.main.tempConfig.pop(index)
        self.main.tempConfig.insert(newindex, self.cfg)
        self.main.editMod()

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
        self._ctrlButton.setMenu(self._ctrlMenu)

        for item in [('up', partial(self.move, -1)),
                     ('down', partial(self.move, 1)),
                     ('to top', partial(self.move, True)),
                     ('to bottom', partial(self.move, False)),
                     ('delete', self.delete),
                     ('duplicate', self.duplicate),
                     ('help on %s' % self.ctrlType, self.help)]:
            action = QtGui.QAction(self._ctrlMenu)
            action.setText(item[0])
            action.triggered.connect(item[1])
            self._ctrlMenu.addAction(action)
    
    def getCtrlData(self):
        for ctrl in self._getCfgList:
            self.cfg[ctrl[0]] = ctrl[1]()
    
    def getCfg(self):
        self.getCtrlData()
        return self.cfg

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

    def duplicate(self):
        self._scrollValB4 = self.main.ui.scrollBar.value()
        self._scrollMaxB4 = self.main.ui.scrollBar.maximum()
        newCfg = deepcopy(self.cfg)
        self.main.tempConfig.append(newCfg)
        self.main.editMod()

        threading.Thread(target=self.scrolltobottom).start()
    
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
        
    def help(self):
        self.main.surfTo(self.helpUrl)


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
    def __init__(self, mod, tempConfig, rebuildFunc):
        super(EditAddElem, self).__init__()
        self.tempConfig = tempConfig
        self.rebuildFunc = rebuildFunc
        self.mod = mod
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
        self.menu_include = BrowseScriptsMenu(self.tempConfig, self.mod, self.addCtrl)
        self.menu.addMenu(self.menu_include)

        for ctrl in ('checkBox hotkey groupBox textField floatField intField '
                     'fileField text button comboBox').split():
            action = QtGui.QAction(self.menu)
            action.setText(ctrl)
            action.triggered.connect(partial(self.addCtrl, ctrl))
            self.menu.addAction(action)
    
    def addCtrl(self, typ, name=''):
        """Just adds a new dict with the accodting typ value to the tempConfig.
        Only if it's an include we already enter the file selected.
        Every other default value will be handled by the very control element.
        """
        cfg = {'typ': typ}
        if typ == 'include':
            cfg['file'] = name
        
        self.tempConfig.append(cfg)
        self.rebuildFunc()


class EditInclude(EditCtrl):
    """
    TODO: An EditInclude only needs to know the mod object to be able to open the file,
    but that can also be handled by the main obj! lets get rid of this. All the ctrsl
    need to be module agnostic!
    """
    def __init__(self, cfg, mod, main):
        self.ctrlType = 'Include'
        super(EditInclude, self).__init__(cfg, main, addLayout=False)
        self.typ = cfg['typ']
        self.file = cfg['file']
        self.mod = mod

        #self.layout = QtGui.QHBoxLayout(self.ctrlui.layout)
        self.layout = QtGui.QHBoxLayout()
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(10, margin, margin, margin)
        self.labelCtrl = QtGui.QLabel('script file:')
        self.labelCtrl.setMinimumWidth(labelW)
        self.labelCtrl.setAlignment(QtCore.Qt.AlignRight)
        self.layout.addWidget(self.labelCtrl)
        self.button = QtGui.QPushButton(self.file)
        self.buttonMenu = BrowseScriptsMenu(main.tempConfig, mod, self.setScript)
        self.button.setMenu(self.buttonMenu)
        self.layout.addWidget(self.button)
        
        self.editButton = QtGui.QPushButton('edit script')
        self.editButton.pressed.connect(self.editScript)
        self.layout.addWidget(self.editButton)
        
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.layout.addItem(spacerItem)
        self.mainWidget.setLayout(self.layout)
    
    def getCfg(self):
        cfg = {'typ': self.typ,
               'file': self.file}
        return cfg
    
    def setScript(self, typ, name):
        self.file = name
        self.cfg['file'] = name
        self.button.setText(name)
    
    def editScript(self):
        subprocess.Popen([self.main.scriptEditor, join(self.mod.path, self.file)])


class InputDialog(QtGui.QDialog):
    def __init__(self, title, main, okFunc, checkFunk, text='', msg='', *args):
        super(InputDialog, self).__init__(main)
        self.ui = inputDialog_ui.Ui_InputDialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.okFunc = okFunc
        self.checkFunk = checkFunk
        self.setWindowTitle(title)
        self.main = main

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
        if self.okFunc is not None:
            txt = self.ui.textField.text()
            self.okFunc(txt)
            self.close()


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
    def __init__(self, tempConfig, mod, func):
        super(BrowseScriptsMenu, self).__init__()
        self.func = func
        self.mod = mod
        self.setTitle('include')
        self.aboutToShow.connect(self.buildMenu)
        self.tempConfig = tempConfig

    def buildMenu(self):
        self.clear()
        scriptsInUse = set()
        for cfg in self.tempConfig:
            if cfg['typ'] == 'include':
                scriptsInUse.add(cfg['file'])
        
        scriptsUnused = set(self.mod.scripts) - scriptsInUse
        
        for scriptName in scriptsUnused:
            action = QtGui.QAction(self)
            action.setText(scriptName)
            action.triggered.connect(partial(self.setScript, scriptName))
            self.addAction(action)

        newIncludeAction = QtGui.QAction(self)
        newIncludeAction.setText('create new')
        newIncludeAction.triggered.connect(self.setScript)
        self.addAction(newIncludeAction)
    
    def setScript(self, name=''):
        if not name:
            name = self.mod.createScript()
            if not name:
                return
        self.func('include', name)


def list_getAllItems_asText(listCtrl):
    return [listCtrl.item(i).text() for i in range(listCtrl.count())]


def list_selectItems(listCtrl, text):
    if isinstance(text, str):
        text = [text]
    
    lastitem = None
    for i in range(listCtrl.count()):
        this = listCtrl.item(i)
        if this.text() in text:
            this.setSelected(True)
            lastitem = this
        else:
            this.setSelected(False)
    if lastitem is not None:
        listCtrl.setCurrentItem(lastitem)


# deferred import of sub controls because they might use any part of this module
import a2ctrl.check, a2ctrl.hotkey, a2ctrl.group
reModules = [a2ctrl.check, a2ctrl.hotkey, a2ctrl.group]
uiModules = [inputDialog_ui, a2ctrl.check.checkbox_edit_ui, a2ctrl.hotkey.hotkey_edit_ui,
             a2ctrl.hotkey.scopeDialog_ui]
for uimod in uiModules:
    checkUiModule(uimod)
