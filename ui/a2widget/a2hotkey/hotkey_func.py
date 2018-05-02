"""
Created on Apr 30, 2016

@author: eRiC
"""
import os
import enum
from functools import partial
from PySide import QtGui

import a2util


class _HelpLabel(enum.Enum):
    cmds = 'Help on Autohotkey commands'
    run = 'Help on Autohotkey "Run"'
    send = 'Help on Autohotkey "Send"'
    vars = 'Help on Autohotkey Built-in Variables'


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

        urls = self.main.a2.urls
        self.help_map = {_HelpLabel.cmds.value: urls.ahk_commands,
                         _HelpLabel.run.value: urls.ahk_run,
                         _HelpLabel.send.value: urls.ahk_send,
                         _HelpLabel.vars.value: urls.ahk_builtin_vars}

    def menu_build(self):
        self.menu.clear()
        index = self.ui.cfg_functionMode.currentIndex()
        if index == 0:
            self.menu.addAction(_HelpLabel.cmds.value, self.surf_to_help)

        elif index == 1:
            for label, func in [('browse directory...', self.browse_dir),
                                ('browse file...', self.browse_file),
                                ('explore to...', self.explore),
                                (_HelpLabel.run.value, self.surf_to_help)]:
                self.menu.addAction(label, func)

        else:
            fsubmenu1 = self.menu.addMenu('Insert modifier key')
            for label, key in [('! - Alt', '!'), ('^ - Control', '^'),
                               ('+ - Shift', '+'), ('# - Win', '#')]:
                fsubmenu1.addAction(label, partial(self.ui.functionText.insert, key))

#             fsubmenu2 = self.menu.addMenu('built-in variables')
#             for var in []:
#                 action = QtGui.QAction(var, fsubmenu2, triggered=partial(self.set_sendmode, var))
#                 fsubmenu2.addAction(action)

            for label, func in [(_HelpLabel.send.value, self.surf_to_help),
                                (_HelpLabel.vars.value, self.surf_to_help)]:
                self.menu.addAction(label, func)

    def browse_file(self):
        options = QtGui.QFileDialog.Options() | QtGui.QFileDialog.DontConfirmOverwrite
        fileName, _filter = QtGui.QFileDialog.getSaveFileName(
            self.main, "Browsing for a file ...", options=options)
        if fileName:
            self.ui.functionText.insert(os.path.normpath(fileName))

    def browse_dir(self):
        directory = QtGui.QFileDialog.getExistingDirectory(
            self.main, "Browsing for a directory ...")
        if directory:
            self.ui.functionText.insert(directory)

    def explore(self):
        text = self.ui.functionText.text()
        a2util.explore(text)

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

    def surf_to_help(self):
        a2util.surf_to(self.help_map[self.ui.functionButton.sender().text()])
