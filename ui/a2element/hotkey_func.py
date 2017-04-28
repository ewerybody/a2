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

        self._functions = ['functionCode', 'functionURL', 'functionSend']
        self._send_modes = ['sendraw', 'sendinput', 'sendplay', 'sendevent', 'send']

        self.ui.cfg_functionMode.currentIndexChanged.connect(self.set_text)
        self.menu = QtGui.QMenu(self.ui.functionButton)
        self.menu.aboutToShow.connect(self.menu_build)
        self.ui.functionButton.setMenu(self.menu)
        self.set_text()
        self.ui.functionText.textChanged.connect(self.changed)
        self.ui.function_send_mode.currentIndexChanged.connect(partial(self.changed, None))

    def menu_build(self):
        self.menu.clear()
        index = self.ui.cfg_functionMode.currentIndex()
        if index == 0:
            # fsubmenu1 = self.menu.addMenu('local functions')
            # fsubmenu2 = self.menu.addMenu('built-in functions')
            action = QtGui.QAction('Help on Autohotkey commands', self.menu,
                                   triggered=partial(a2util.surf_to, self.main.a2.urls.ahk_commands))
            self.menu.addAction(action)

        elif index == 1:
            for label, func in [('browse directory...', self.browse_dir),
                                ('browse file...', self.browse_file),
                                ('explore to...', self.explore),
                                ('Help on Autohotkey "Run"',
                                 partial(a2util.surf_to, self.main.a2.urls.ahk_run))]:
                action = QtGui.QAction(label, self.menu, triggered=func)
                self.menu.addAction(action)

        else:
            fsubmenu1 = self.menu.addMenu('Insert modifier key')
            for label, key in [('! - Alt', '!'), ('^ - Control', '^'),
                               ('+ - Shift', '+'), ('# - Win', '#')]:
                action = QtGui.QAction(label, fsubmenu1, triggered=partial(self.ui.functionText.insert, key))
                fsubmenu1.addAction(action)
#             fsubmenu2 = self.menu.addMenu('built-in variables')
#             for var in []:
#                 action = QtGui.QAction(var, fsubmenu2, triggered=partial(self.set_sendmode, var))
#                 fsubmenu2.addAction(action)
            for label, func in [('Help on Autohotkey "Send"',
                                 partial(a2util.surf_to, self.main.a2.urls.ahksend)),
                                ('Help on Autohotkey Built-in Variables',
                                 partial(a2util.surf_to, self.main.a2.urls.ahk_builtin_vars))]:
                action = QtGui.QAction(label, self.menu, triggered=func)
                self.menu.addAction(action)

    def browse_file(self):
        options = QtGui.QFileDialog.Options() | QtGui.QFileDialog.DontConfirmOverwrite
        fileName, _filter = QtGui.QFileDialog.getSaveFileName(
            self.main, "Browsing for a file ...", options=options)
        if fileName:
            self.ui.functionText.insert(normpath(fileName))

    def browse_dir(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self.main, "Browsing for a directory ...")
        if directory:
            self.ui.functionText.insert(directory)

    def explore(self):
        """TODO: verify"""
        text = self.ui.functionText.text()
        subprocess.Popen(['explorer.exe', text])

    def changed(self, text=None, *args):
        if text is None:
            text = self.ui.functionText.text()
        index = self.ui.cfg_functionMode.currentIndex()
        if index == 1:
            text = 'Run, ' + text
        elif index == 2:
            send_mode = self.ui.function_send_mode.currentText()
            text = '%s, %s' % (send_mode, text)
        self.main.cfg[self._functions[index]] = text

    def set_text(self, index=None):
        if index is None:
            index = self.ui.cfg_functionMode.currentIndex()
        self.ui.run_label.setVisible(index == 1)
        self.ui.function_send_mode.setVisible(index == 2)

        text = self.main.cfg.get(self._functions[index]) or ''
        text = self._strip_mode(text, index)
        self.ui.functionText.setText(text)

    def _strip_mode(self, text, index):
        """removes Run, or Send* to put it into the input field"""
        modes = [None, ['run'], self._send_modes]
        if index in [1, 2]:
            for mode in modes[index]:
                if text.lower().startswith(mode):
                    text = text[len(mode):]
                    if text.startswith(','):
                        text = text[1:]
                    text = text.strip()
                    break
            # set the send mode combobox
            if index == 2:
                for i in range(self.ui.function_send_mode.count()):
                    if self.ui.function_send_mode.itemText(i).lower() == mode:
                        self.ui.function_send_mode.setCurrentIndex(i)
                        break
        return text
