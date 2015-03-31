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

'''
from PySide import QtGui, QtCore
import logging
logging.basicConfig()
log = logging.getLogger('a2ctrl')
log.setLevel(logging.DEBUG)
margin = 5
labelW = 100

class EditLine(object):
    def __init__(self, name, dictionary, parent, ctrldict):
        self.name = name
        self.parent = parent
        self.widget = QtGui.QWidget()
        self.layout = QtGui.QHBoxLayout(self.widget)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(margin, margin, margin, margin)
        self.labelCtrl = QtGui.QLabel('%s:' % name)
        #self.labelCtrl.setMaximumSize(QtCore.QSize(16777215, labelW))
        self.labelCtrl.setMinimumSize(QtCore.QSize(labelW, 0))
        self.layout.addWidget(self.labelCtrl)
        self.inputCtrl = QtGui.QLineEdit()
        self.layout.addWidget(self.inputCtrl)
        self.inputCtrl.setText(dictionary.get(name or ''))
        parent.addWidget(self.widget)
        ctrldict[name] = self
    
    @property
    def value(self):
        return self.inputCtrl.text()


class EditText(object):
    def __init__(self, name, dictionary, parent, ctrldict):
        self.name = name
        self.parent = parent
        self.widget = QtGui.QWidget()
        self.layout = QtGui.QVBoxLayout(self.widget)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(margin, margin, margin, margin)
        self.labelCtrl = QtGui.QLabel('%s:' % name)
        self.layout.addWidget(self.labelCtrl)
        self.inputCtrl = QtGui.QPlainTextEdit()
        self.inputCtrl.setPlainText(dictionary.get(name) or '')
        self.inputCtrl.setTabChangesFocus(True)
        self.inputCtrl.setMaximumSize(QtCore.QSize(16777215, 100))
        self.layout.addWidget(self.inputCtrl)
        parent.addWidget(self.widget)
        ctrldict[name] = self
    
    @property
    def value(self):
        return self.inputCtrl.toPlainText()


class EditAddCtrl(QtGui.QWidget):
    """
    to add a control to a module setup. This will probably go into some popup
    later. This way its a little too clunky I think.
    
    til: if you don't make this a widget and just a object Qt will forget about
    any connections you make!
    """
    def __init__(self, parent):
        super(EditAddCtrl, self).__init__()
        self.parent = parent
        #self.widget = QtGui.QWidget()
        self.layout = QtGui.QHBoxLayout(self)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(margin, margin, margin, margin)
        
        self.line = QtGui.QFrame(self)
        self.line.setMinimumSize(QtCore.QSize(0, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setLineWidth(3)
        self.parent.addWidget(self.line)
        
        self.labelCtrl = QtGui.QLabel('add control:')
        #self.labelCtrl.setMaximumSize(QtCore.QSize(16777215, labelW))
        self.labelCtrl.setMinimumSize(QtCore.QSize(labelW, 0))
        self.layout.addWidget(self.labelCtrl)
        
        self.comboBox = QtGui.QComboBox(self)
        self.comboBox.addItems('include checkBox hotkey groupBox textField floatField intField fileField text button comboBox'.split())
        self.comboBox.setMaximumSize(QtCore.QSize(150, 50))
        self.layout.addWidget(self.comboBox)
        
        self.button = QtGui.QPushButton('Add')
        self.layout.addWidget(self.button)
        
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.layout.addItem(spacerItem)
        
        self.parent.addWidget(self)
        self.button.clicked.connect(self.addCtrl)
            
    def addCtrl(self):
        x = self.comboBox.currentText()
        log.debug('adding "%s" to %s' % (x, self.parent))
        