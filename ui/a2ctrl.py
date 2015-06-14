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
from ctrl_ui import Ui_EditCtrl
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
        self.layout = QtGui.QVBoxLayout(self)
        
         

def edit(element, mod, main):
    if element['typ'] == 'nfo':
        return EditNfo(element)
    elif element['typ'] == 'include':
        return EditInclude(element, mod, main)


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
    def __init__(self, element, main):
        super(EditCtrl, self).__init__()
        self.element = element
        self.main = main
        self.ui = Ui_EditCtrl()
        self.ui.setupUi(self)
        self.ui.menu = QtGui.QMenu(self)
        self.ui.ctrlButton.setMenu(self.ui.menu)
        
        for item in [('up', partial(self.move, -1)), ('down', partial(self.move, 1)),
                 ('delete', self.delete)]:
            action = QtGui.QAction(self.ui.menu)
            action.setText(item[0])
            action.triggered.connect(item[1])
            self.ui.menu.addAction(action)
    
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
        super(EditInclude, self).__init__(element, main)
        self.typ = element['typ']
        self.file = element['file']
        self.mod = mod

        self.layout = QtGui.QHBoxLayout(self)
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
        self.ui.layout.addLayout(self.layout)
    
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
        cfg['mode'] = 'ahk'

    """
    def __init__(self, element, mod, main):
        super(EditHotkey, self).__init__(element, main)
        




class EditView(QtGui.QWidget):
    """
    TODO: self contained object that displays editable controls for the
    different parameters of a module
    """
    def __init__(self):
        pass
