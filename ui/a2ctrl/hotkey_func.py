"""
Created on Apr 30, 2016

@author: eRiC
"""
import a2core
import subprocess
from PySide import QtGui
from functools import partial
from os.path import normpath


class Hotkey_Function_Handler(object):
    def __init__(self, main):
        self.main = main
        self.ui = main.ui

        self.functions = ['functionCode', 'functionURL', 'functionSend']
        
        self.ui.cfg_functionMode.currentIndexChanged.connect(self.set_text)
        self.menu = QtGui.QMenu(self.ui.functionButton)
        self.menu.aboutToShow.connect(self.menu_build)
        self.ui.functionButton.setMenu(self.menu)
        self.set_text()
        self.ui.functionText.textChanged.connect(self.changed)
    
    def menu_build(self):
        self.menu.clear()
        index = self.ui.cfg_functionMode.currentIndex()
        if index == 0:
            fsubmenu1 = self.menu.addMenu('local functions')
            _fsubmenu2 = self.menu.addMenu('built-in functions')
        elif index == 1:
            for label, func in [('browse directory...', self.browse_dir),
                                ('browse file...', self.browse_file),
                                ('explore to...', self.explore)]:
                action = QtGui.QAction(label, self.menu, triggered=func)
                self.menu.addAction(action)
        else:
            fsubmenu1 = self.menu.addMenu('Send Mode')
            for mode in ['Send', 'SendInput', 'SendRaw']:
                action = QtGui.QAction(mode, fsubmenu1, triggered=partial(self.set_sendmode, mode))
                fsubmenu1.addAction(action)
            fsubmenu2 = self.menu.addMenu('built-in variables')
            action = QtGui.QAction('Help on Send', self.menu, triggered=self.help_on_send)
            self.menu.addAction(action)
    
    def set_sendmode(self, mode):
        self.main.cfg['sendmode'] = mode
    
    def browse_file(self):
        options = QtGui.QFileDialog.Options() | QtGui.QFileDialog.DontConfirmOverwrite
        fileName, _filter = QtGui.QFileDialog.getSaveFileName(
            self.main, "Browsing for a file ...", options=options)
        if fileName:
            self.set_text(1, normpath(fileName))
    
    def browse_dir(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self.main, "Browsing for a directory ...")
        if directory:
            self.set_text(1, directory)

    def explore(self):
        """TODO: verify"""
        text = self.ui.functionText.text()
        subprocess.Popen(['explorer.exe', text])
    
    def help_on_send(self):
        a2core.surfTo(self.a2.urls.ahksend)
    
    def changed(self, text=None):
        #text = self.ui.functionText.text()
        index = self.ui.cfg_functionMode.currentIndex()
        self.main.cfg[self.functions[index]] = text
    
    def set_text(self, index=None, text=None):
        if index is None:
            index = self.ui.cfg_functionMode.currentIndex()
        if text is None:
            text = self.main.cfg.get(self.functions[index]) or ''
        self.ui.functionText.insert(text)
        # show include thingy
        #self.ui.scopePlus.setVisible(index == 0)
