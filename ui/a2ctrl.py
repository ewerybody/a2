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
import logging
from functools import partial
import subprocess
from os.path import join
from hotkey_edit_ui import Ui_hotkey_edit
import inspect
logging.basicConfig()
log = logging.getLogger('a2ctrl')
log.setLevel(logging.DEBUG)
margin = 5
labelW = 100

def draw(element):
    """
    mapper that returns display control objects
    according to the 'typ' of a config element
    """
    if element['typ'] == 'nfo':
        return DrawNfo(element)
    elif element['typ'] == 'check':
        return DrawCheck(element)
    elif element['typ'] == 'hotkey':
        return DrawHotkey(element)


class DrawWelcome(QtGui.QWidget):
    'Hello user! Welcome to a2! This is a template introduction Text. So far there is not much to say. I just wanted this to fill up more than one line properly. Voila!'

class DrawNfo(QtGui.QWidget):
    def __init__(self, data):
        super(DrawNfo, self).__init__()
        
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.label = QtGui.QLabel(self)
        self.label.setText(data.get('description') or '')
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)


class DrawCheck(QtGui.QWidget):
    def __init__(self, data):
        super(DrawCheck, self).__init__()
        self.layout = QtGui.QVBoxLayout(self)


class DrawHotkey(QtGui.QWidget):
    """
    User ui for a Hotkey control.
    shows: label, checkbox if disablable, shortcut(s), controls to add, remove
        additional shortcuts, controls to change scope if that's enabled...
    
    cfg['label'] == 'Hotkeytest with a MsgBox'
    cfg['typ'] == 'hotkey':
    cfg['name'] == 'modnameHotkey1'
    cfg['enabled'] = True
    cfg['disablable'] = True
    cfg['key'] = 'Win+G'
    cfg['keyChange'] = True
    cfg['multiple'] = True
    cfg['scope'] = ''
    cfg['scopeChange'] = True
    # mode can be: ahk, file, key: to execute code, open up sth, send keystroke
    cfg['mode'] = 'ahk'
    """
    def __init__(self, data):
        super(DrawHotkey, self).__init__()
        self.ctrllayout = QtGui.QHBoxLayout(self)
        self.labelBoxLayout = QtGui.QVBoxLayout()
        self.labelBoxLayout.setContentsMargins(0, 10, 0, 0)
        self.labelLayout = QtGui.QHBoxLayout()
        if data['disablable']:
            self.check = QtGui.QCheckBox(self)
            self.check.setChecked(data['enabled'])
            self.labelLayout.addWidget(self.check)
        self.label = QtGui.QLabel(data.get('label') or '', self)
        self.labelLayout.addWidget(self.label)
        self.labelBoxLayout.addLayout(self.labelLayout)
        self.labelBoxLayout.addItem(QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum,
                                                      QtGui.QSizePolicy.Expanding))
        self.ctrllayout.addLayout(self.labelBoxLayout)
        
        self.hotkeyListLayout = QtGui.QVBoxLayout()
        self.hotkeyLayout = QtGui.QHBoxLayout()
        self.hotkeyButton = QtGui.QPushButton(data.get('key') or '')
        self.hotkeyButton.setMinimumSize(QtCore.QSize(300, 40))
        self.hotkeyLayout.addWidget(self.hotkeyButton)
        self.hotkeyLayout.addItem(QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding,
                                                    QtGui.QSizePolicy.Minimum))
        self.hotkeyListLayout.addLayout(self.hotkeyLayout)
        self.hotkeyListLayout.addItem(QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum,
                                                        QtGui.QSizePolicy.Expanding))
        self.ctrllayout.addLayout(self.hotkeyListLayout)
        

def edit(element, mod, main):
    if element['typ'] == 'nfo':
        return EditNfo(element)
    elif element['typ'] == 'include':
        return EditInclude(element, mod, main)
    elif element['typ'] == 'hotkey':
        return EditHotkey(element, mod, main)


class EditNfo(QtGui.QGroupBox):
    def __init__(self, data):
        super(EditNfo, self).__init__()
        log.info('Building EditNfo...')
        self.data = data
        self.typ = data['typ']
        self.setTitle('module information:')
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                             QtGui.QSizePolicy.Maximum))
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.description = EditText('description', data.get('description'), self.layout, self.getCfg)
        self.author = EditLine('author', data.get('author'), self.layout, self.getCfg)
        self.version = EditLine('version', data.get('version'), self.layout, self.getCfg)
        self.date = EditLine('date', data.get('date'), self.layout, self.getCfg)

    def getCfg(self):
        self.data['description'] = self.description.value
        self.data['author'] = self.author.value
        self.data['version'] = self.version.value
        self.data['date'] = self.date.value
        return self.data


class EditCtrl(QtGui.QWidget):
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
    def __init__(self, element, main, addLayout=True):
        super(EditCtrl, self).__init__()
        self.element = element
        self.main = main
        self._setupUi(addLayout)
        self._getCfgList = []
    
    def delete(self):
        if self.element in self.main.tempConfig:
            self.main.tempConfig.remove(self.element)
            self.main.editMod()
    
    def move(self, value):
        index = self.main.tempConfig.index(self.element)
        newindex = index + value
        if newindex < 1 or newindex >= len(self.main.tempConfig):
            return

        element = self.main.tempConfig.pop(index)
        self.main.tempConfig.insert(newindex, element)
        self.main.editMod()

    def _setupUi(self, addLayout):
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self._ctrlLayout = QtGui.QHBoxLayout(self)
        self._ctrlLayout.setSpacing(0)
        self._ctrlLayout.setContentsMargins(5, 5, 5, 5)
        self.mainWidget = QtGui.QWidget(self)
        if addLayout:
            self.mainLayout = QtGui.QVBoxLayout()
            self.mainLayout.setContentsMargins(5, 5, 5, 5)
            self.mainWidget.setLayout(self.mainLayout)
        self._ctrlLayout.addWidget(self.mainWidget)
        
        self._ctrlButtonLayout = QtGui.QVBoxLayout()
        self._ctrlButtonLayout.setSpacing(0)
        self._ctrlButtonLayout.setContentsMargins(5, 0, 0, 0)
        self._ctrlButtonLayout.setObjectName("ctrlButtonLayout")
        
        self._ctrlButton = QtGui.QPushButton(self)
        self._ctrlButton.setMaximumSize(QtCore.QSize(50, 50))
        self._ctrlButton.setText("...")
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
                     ('delete', self.delete)]:
            action = QtGui.QAction(self._ctrlMenu)
            action.setText(item[0])
            action.triggered.connect(item[1])
            self._ctrlMenu.addAction(action)
    
    def getCtrlData(self):
        for ctrl in self._getCfgList:
            self.element[ctrl[0]] = ctrl[1]()
    
    def getCfg(self):
        self.getCtrlData()
        return self.element

    def enlistCfgCtrls(self, uiclass):
        """
        already deprecated. You'd have to connect the widgets to the getCfg method
        anyways and then fetch them there in again...
        
        just for historic reasons...
        browses a given widget class members and according to their type adds
        them to the _getCfgList which is then looped by getCfg on change.
        To have a widget listed its name MUST start with 'cfg_'
        The string after that will be the name of the data piece in the element
        dictionary. So
            self.ui.cfg_bananas = QtGui.QCheckBox()
        will end up as ('bananas', self.ui.cfg_bananas.isChecked) in the list so
        it can be called to get the value and set in the dict.
        just if like you wrote
            self.element['bananas'] = self.ui.cfg_bananas.isChecked()
        """
        self._getCfgList = []
        for ctrl in inspect.getmembers(uiclass):
            if ctrl[0].startswith('cfg_'):
                name = ctrl[0][4:]
                #log.info('ctrl: %s' % str(ctrl))
                if isinstance(ctrl[1], QtGui.QCheckBox):
                    self._getCfgList.append((name, ctrl[1].isChecked))
                    if name in self.element:
                        ctrl[1].setChecked(self.element[name])
            #log.info('e.__name__: %s' % e.__name__)
    
    def connectCfgCtrls(self, uiclass):
        for ctrl in inspect.getmembers(uiclass):
            if not ctrl[0].startswith('cfg_'):
                continue
            
            name = ctrl[0][4:]
            control = ctrl[1]
            
            if isinstance(control, QtGui.QCheckBox):
                control.clicked.connect(partial(self._updateCfgData,
                                                name, control.isChecked))
                # set ctrl according to config or set config from ctrl
                if name in self.element:
                    control.setChecked(self.element[name])
                else:
                    self.element[name] = control.isChecked()
            
            elif isinstance(control, QtGui.QLineEdit):
                control.textChanged.connect(partial(self._updateCfgData, name, None))
                if name in self.element:
                    control.setText(self.element[name])
                else:
                    self.element[name] = control.text()
            
            elif isinstance(control, QtGui.QComboBox):
                control.currentIndexChanged.connect(partial(self._updateCfgData, name, None))
                if name in self.element:
                    control.setCurrentIndex(self.element[name])
                else:
                    self.element[name] = control.currentIndex()            
            
            else:
                log.error('Cannot handle widget "%s"!\n  type "%s" NOT covered yet!' %
                          (ctrl[0], type(control)))
    
    def _updateCfgData(self, name, func, data=None, *args):
        #print('widget sent data: %s' % str(args))
        if data is not None:
            self.element[name] = data
        elif func is not None:
            self.element[name] = func()        


class EditLine(QtGui.QWidget):
    def __init__(self, name, text, parentLayout=None, updatefunc=None):
        super(EditLine, self).__init__()
        self.name = name
        self.updatefunc = updatefunc
        self.parentLayout = parentLayout
        self.layout = QtGui.QHBoxLayout(self)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(margin, margin, margin, margin)
        self.labelCtrl = QtGui.QLabel('%s:' % name)
        self.labelCtrl.setMinimumSize(QtCore.QSize(labelW, 0))
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
        self.name = name
        self.parent = parent
        self.updatefunc = updatefunc
        self.baselayout = QtGui.QVBoxLayout(self)
        self.baselayout.setSpacing(5)
        self.baselayout.setContentsMargins(margin, margin, margin, margin)
        self.labelCtrl = QtGui.QLabel('%s:' % name)
        self.baselayout.addWidget(self.labelCtrl)
        self.inputCtrl = QtGui.QPlainTextEdit()
        self.inputCtrl.setPlainText(str(text))
        self.inputCtrl.setTabChangesFocus(True)
        self.inputCtrl.setMaximumSize(QtCore.QSize(16777215, 100))
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
        
        self.addButton = QtGui.QPushButton('add')
        self.baselayout.addWidget(self.addButton)
        
        self.menu = QtGui.QMenu(self.addButton)
        self.menu.aboutToShow.connect(self.populateMenu)
        self.addButton.setMenu(self.menu)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.baselayout.addItem(spacerItem)

    def populateMenu(self):
        self.menu.clear()
        self.menu_include = self.menu.addMenu('include')
        scriptsInUse = set()
        for element in self.tempConfig:
            if element['typ'] == 'include':
                scriptsInUse.add(element['file'])
        scriptsUnused = set(self.mod.scripts) - scriptsInUse
        for scriptName in scriptsUnused:
            action = QtGui.QAction(self.menu_include)
            action.setText(scriptName)
            action.triggered.connect(partial(self.newInclude, scriptName))
            self.menu_include.addAction(action)
        
        newIncludeAction = QtGui.QAction(self.menu_include)
        newIncludeAction.setText('create new')
        newIncludeAction.triggered.connect(self.newInclude)
        self.menu_include.addAction(newIncludeAction)
        
        for el in 'checkBox hotkey groupBox textField floatField intField '\
                  'fileField text button comboBox'.split():
            action = QtGui.QAction(self.menu)
            action.setText(el)
            action.triggered.connect(partial(self.addCtrl, el))
            self.menu.addAction(action)
    
    def newInclude(self, name=''):
        if not name:
            name = self.mod.createScript()
            if not name:
                return
        log.info('including: %s' % name)
        self.addCtrl('include', name)
    
    def addCtrl(self, typ, name=''):
        """
        TODO: I guess we should put the configuration of the element rather to the
        very class that builds it instead of writing it all in this wrapper thingy
        here. Maybe there could be a class method that adds to the tempConfig...
        """
        cfg = {'typ': typ}
        if cfg['typ'] == 'include':
            cfg['file'] = name
        elif cfg['typ'] == 'hotkey':
            cfg['enabled'] = True
            cfg['disablable'] = True
            cfg['key'] = 'Win+G'
            cfg['keyChange'] = True
            cfg['multiple'] = True
            cfg['scope'] = ''
            cfg['scopeChange'] = True
            # mode can be: ahk, file, key
            # to execute code, open up sth, send keystroke
            cfg['mode'] = 'ahk'
        
        self.tempConfig.append(cfg)
        self.rebuildFunc()


class EditInclude(EditCtrl):
    """
    TODO: An Include control has to know what can be included. Plus a
    'create script' item. If a file was included already then a new
    Include control won't show that script file. If there are no more
    scripts to include it will only show the 'create script'.
    
    TODO: each edit control has built-in functionality to delete itself
    and/or shift it up/down in the layout. Which also shifts it up/down
    in the configuration in the background. 
    """
    #def __init__(self, parent, mod):
    def __init__(self, element, mod, main):
        super(EditInclude, self).__init__(element, main, addLayout=False)
        self.typ = element['typ']
        self.file = element['file']
        self.mod = mod

        #self.layout = QtGui.QHBoxLayout(self.ctrlui.layout)
        self.layout = QtGui.QHBoxLayout()
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(margin, margin, margin, margin)
        self.labelCtrl = QtGui.QLabel('include script:')
        self.labelCtrl.setMinimumSize(QtCore.QSize(labelW, 0))
        self.layout.addWidget(self.labelCtrl)
        self.button = QtGui.QPushButton(self.file)
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
    
    def editScript(self):
        subprocess.Popen([self.main.scriptEditor, join(self.mod.path, self.file)])


class EditHotkey(EditCtrl):
    """
    TODO: Oh boy... this has so many implications but it has to be done. Let's do it!
    First: Have the edit ctrl, then the display one, Then we need checks when a mod
    config change is about to be comitted. The change will not be able to be OKed as long
    as there are conflicts with hotkeys, or missing includes or ... 

    elif cfg['typ'] == 'hotkey':
        cfg['enabled'] = True
        cfg['disablable'] = True
        cfg['key'] = 'Win+G'
        cfg['keyChange'] = True
        cfg['multiple'] = True
        cfg['scope'] = ''
        cfg['scopeChange'] = True
        # mode can be: ahk, file, key
        # to execute code, open up sth, send keystroke
        cfg['mode'] = 'ahk',
        cfg['name'] = 'someModule_hotkey1',
        cfg['label'] = 'do awesome stuff on:'
    """
    def __init__(self, element, mod, main):
        super(EditHotkey, self).__init__(element, main, addLayout=False)
        self.main = main
        self.element = element
        self.ui = Ui_hotkey_edit()
        self.ui.setupUi(self.mainWidget)
        self.mainWidget.setLayout(self.ui.hotkeyCtrlLayout)
        
        self.ui.cfg_scopeMode.currentIndexChanged.connect(self.scopeModeChanged)
        #QtGui.QComboBox.setCurrentIndex()
        self.connectCfgCtrls(self.ui)
        self.scopeModeChanged()
    
    def scopeModeChanged(self, index=None):
        if index is None:
            index = self.ui.cfg_scopeMode.currentIndex()
        state = index != 0
        self.ui.cfg_scope.setVisible(state)
        self.ui.scopePlus.setVisible(state)
        self.ui.scopeMinus.setVisible(state)
    
    def getCfg(self):
        return self.element

    

class EditView(QtGui.QWidget):
    """
    TODO: self contained object that displays editable controls for the
    different parameters of a module
    """
    def __init__(self):
        pass
