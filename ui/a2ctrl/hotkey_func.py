"""
Created on Apr 30, 2016

@author: eRiC
"""
import a2core
import subprocess
from PySide import QtGui
from functools import partial


class Hotkey_Function_Handler(object):
    def __init__(self, main):
        self.main = main
        self.ui = main.ui

        self.functions = ['functionCode', 'functionURL', 'functionSend']
        self.ui.cfg_functionMode.currentIndexChanged.connect(self.functionSetText)
        self.functionMenu = QtGui.QMenu(self.ui.functionButton)
        self.functionMenu.aboutToShow.connect(self.functionMenuBuild)
        self.ui.functionButton.setMenu(self.functionMenu)
        self.functionSetText()
        self.ui.functionText.textChanged.connect(self.functionChanged)
    
    def functionMenuBuild(self):
        self.functionMenu.clear()
        index = self.ui.cfg_functionMode.currentIndex()
        if index == 0:
            fsubmenu1 = self.functionMenu.addMenu('local functions')
            _fsubmenu2 = self.functionMenu.addMenu('built-in functions')
        elif index == 1:
            for x in [('browse...', self.functionBrowse),
                      ('explore to...', self.functionExplore)]:
                action = QtGui.QAction(self.functionMenu)
                action.setText(x[0])
                action.triggered.connect(x[1])
                self.functionMenu.addAction(action)
        else:
            fsubmenu1 = self.functionMenu.addMenu('Send Mode')
            for x in ['Send', 'SendInput', 'SendRaw']:
                action = QtGui.QAction(fsubmenu1)
                action.setText(x)
                action.triggered.connect(partial(self.functionSendMode, x))
                fsubmenu1.addAction(action)
            #fsubmenu2 = self.functionMenu.addMenu('built-in variables')
            for x in [('Help on Send', self.functionSendHelp)]:
                action = QtGui.QAction(self.functionMenu)
                action.setText(x[0])
                action.triggered.connect(x[1])
                self.functionMenu.addAction(action)
    
    def functionSendMode(self, mode):
        self.main.cfg['sendmode'] = mode
    
    def functionBrowse(self):
        """TODO"""
        
        self.functionSetText(1, 'C:\asasasdf\asdfasdf')

    def functionExplore(self):
        """TODO: verify"""
        text = self.ui.functionText.text()
        subprocess.Popen(['explorer.exe', text])
    
    def functionSendHelp(self):
        a2core.surfTo(self.a2.urls.ahksend)
    
    def functionChanged(self, text=None):
        #text = self.ui.functionText.text()
        index = self.ui.cfg_functionMode.currentIndex()
        self.main.cfg[self.functions[index]] = text
    
    def functionSetText(self, index=None, text=None):
        if index is None:
            index = self.ui.cfg_functionMode.currentIndex()
        if text is None:
            text = self.main.cfg.get(self.functions[index]) or ''
        self.ui.functionText.setText(text)
        # show include thingy
        #self.ui.scopePlus.setVisible(index == 0)
