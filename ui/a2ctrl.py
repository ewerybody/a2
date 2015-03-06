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