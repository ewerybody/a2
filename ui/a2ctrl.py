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

TODO: maybe make the nfo item just always the 0th entry in the config.json
Then its an nfo-type element that just draws and holds all the author, name,
version, description info
'''

from PySide import QtGui, QtCore
import logging
logging.basicConfig()
log = logging.getLogger('a2ctrl')
log.setLevel(logging.DEBUG)
margin = 5
labelW = 100

def draw(element):
    """
    mapper that returns display controls
    according to the typ keys of a config element
    """
    if element['typ'] == 'nfo':
        return DrawNfo(element)
    elif element['typ'] == 'check':
        return DrawCheck(element)


class DrawNfo(QtGui.QWidget):
    def __init__(self, data):
        super(DrawNfo, self).__init__()
        
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.label = QtGui.QLabel(self)
        self.label.setText(data.get('description') or '')
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)


def edit(element):
    if element['typ'] == 'nfo':
        return EditNfo(element)


class EditNfo(QtGui.QGroupBox):
    def __init__(self, data):
        super(EditNfo, self).__init__()
        log.info('Building EditNfo...')
        self.typ = data['typ']
        #self.box = QtGui.QGroupBox(self)
        self.setTitle('module information:')
        self.boxLayout = QtGui.QVBoxLayout(self)
        self.boxLayout.setSpacing(5)
        self.boxLayout.setContentsMargins(5, 5, 5, 5)
        #EditText('description', nfo, nfoBoxLayout, nfoCtrls)
        self.description = EditText('description', data.get('description'), self.boxLayout)
        self.author = EditLine('author', data.get('author'), self.boxLayout)
        self.version = EditLine('version', data.get('version'), self.boxLayout)
        self.date = EditLine('date', data.get('date'), self.boxLayout)

    def getcfg(self):
        cfg = {'typ': self.typ,
               'description': self.description.value,
               'author': self.author.value,
               'version': self.version.value,
               'date': self.date.value
               }
        return cfg


class EditLine(QtGui.QWidget):
    def __init__(self, name, text, parent=None):
        super(EditLine, self).__init__()
        self.name = name
        self.parent = parent
        self.baselayout = QtGui.QHBoxLayout(self)
        self.baselayout.setSpacing(5)
        self.baselayout.setContentsMargins(margin, margin, margin, margin)
        self.labelCtrl = QtGui.QLabel('%s:' % name)
        #self.labelCtrl.setMaximumSize(QtCore.QSize(16777215, labelW))
        self.labelCtrl.setMinimumSize(QtCore.QSize(labelW, 0))
        self.baselayout.addWidget(self.labelCtrl)
        self.inputCtrl = QtGui.QLineEdit()
        self.baselayout.addWidget(self.inputCtrl)
        self.inputCtrl.setText(str(text))
        if parent:
            parent.addWidget(self)
    
    @property
    def value(self):
        return self.inputCtrl.text()


class EditText(QtGui.QWidget):
    def __init__(self, name, text, parent=None):
        super(EditText, self).__init__()
        self.name = name
        self.parent = parent
        self.baselayout = QtGui.QVBoxLayout(self)
        self.baselayout.setSpacing(5)
        self.baselayout.setContentsMargins(margin, margin, margin, margin)
        self.labelCtrl = QtGui.QLabel('%s:' % name)
        self.baselayout.addWidget(self.labelCtrl)
        self.inputCtrl = QtGui.QPlainTextEdit()
        self.inputCtrl.setPlainText(str(text))
        self.inputCtrl.setTabChangesFocus(True)
        self.inputCtrl.setMaximumSize(QtCore.QSize(16777215, 100))
        self.baselayout.addWidget(self.inputCtrl)
        if parent:
            parent.addWidget(self)
    
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
    def __init__(self, mod, parent):
        super(EditAddElem, self).__init__()
        self.parent = parent
        self.mod = mod
        self.baselayout = QtGui.QHBoxLayout(self)
        self.baselayout.setSpacing(5)
        self.baselayout.setContentsMargins(margin, margin, margin, margin)
        
        self.line = QtGui.QFrame(self)
        self.line.setMinimumSize(QtCore.QSize(0, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setLineWidth(3)
        self.parent.addWidget(self.line)
        
        self.labelCtrl = QtGui.QLabel('add element:')
        #self.labelCtrl.setMaximumSize(QtCore.QSize(16777215, labelW))
        self.labelCtrl.setMinimumSize(QtCore.QSize(labelW, 0))
        self.baselayout.addWidget(self.labelCtrl)
        
        self.comboBox = QtGui.QComboBox(self)
        self.comboBox.addItems('include checkBox hotkey groupBox textField floatField intField fileField text button comboBox'.split())
        self.comboBox.setMaximumSize(QtCore.QSize(150, 50))
        self.baselayout.addWidget(self.comboBox)
        
        self.button = QtGui.QPushButton('Add')
        self.baselayout.addWidget(self.button)
        
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.baselayout.addItem(spacerItem)
        #self.parent.addWidget(self)
        self.button.clicked.connect(self.addCtrl)
        
    def addCtrl(self):
        typ = self.comboBox.currentText()
        log.debug('adding "%s" to %s' % (typ, self.parent))
        
        if typ == 'include':
            i = Include(self.mod, self.parent, self.parent.count() - 1)


class Include(QtGui.QWidget):
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
    def __init__(self, mod, parent, cfg=None, index=-1):
        super(Include, self).__init__()

        if cfg is None:
            self.cfg = {'typ': 'include',
                        'file': ''}
        
        self.parent = parent
        self.widget = QtGui.QWidget()
        self.baselayout = QtGui.QHBoxLayout(self.widget)
        self.baselayout.setSpacing(5)
        self.baselayout.setContentsMargins(margin, margin, margin, margin)
        self.labelCtrl = QtGui.QLabel('include script:')
        #self.labelCtrl.setMaximumSize(QtCore.QSize(16777215, labelW))
        self.labelCtrl.setMinimumSize(QtCore.QSize(labelW, 0))
        self.baselayout.addWidget(self.labelCtrl)
        self.comboBox = QtGui.QComboBox(self)
        self.comboBox.addItems(mod.scripts)
        self.baselayout.addWidget(self.comboBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.baselayout.addItem(spacerItem)
        
        parent.insertWidget(index, self.widget)
        #ctrldict[name] = self
    
    @property
    def value(self):
        return self.comboBox.currentText()

class EditView(QtGui.QWidget):
    """
    TODO: self contained object that displays editable controls for the
    different parameters of a module
    """
    def __init__(self):
        pass