from collections import OrderedDict

import a2ahk
import a2core
import a2ctrl
import a2util
from PySide import QtGui, QtCore

from . import scope_dialog_ui


log = a2core.get_logger(__name__)


class ScopeDialog(QtGui.QDialog):
    okayed = QtCore.Signal(str)

    def __init__(self, parent, scope_string=''):
        super(ScopeDialog, self).__init__(parent)
        self.scope_string = scope_string
        a2ctrl.check_ui_module(scope_dialog_ui)
        self.ui = scope_dialog_ui.Ui_ScopeDialog()

        self.ui.setupUi(self)
        self.setWindowTitle('Setup Scope')
        self.setModal(True)

        #self.ok_func = ok_func
        self.a2 = a2core.A2Obj.inst()
        self.titles, self.classes, self.processes = set(), set(), set()
        self.get_scope_nfo()

        self.help_map = OrderedDict({'Help on Scope Setup': self.a2.urls.helpScopes,
                                     'Help on AHK WinActive': self.a2.urls.ahkWinActive,
                                     'Help on AHK WinTitle': self.a2.urls.ahkWinTitle})

        self.setup_ui()
        self.set_scope_string(scope_string)

    def setup_ui(self):
        pos = self.pos()
        cursor_pos = QtGui.QCursor.pos()
        pos.setX(cursor_pos.x() - (self.width() / 2))
        pos.setY(cursor_pos.y() - (self.height() / 2))
        self.move(pos)
        self.ui.a2ok_button.clicked.connect(self.ok)
        self.ui.a2cancel_button.clicked.connect(self.close)
        self.ui.scope_title.setFocus()

        for ctrl in [self.ui.scope_title, self.ui.scope_class, self.ui.scope_exe]:
            ctrl.textChanged.connect(self.textChange)
        # put menus to the different buttons
        # for i, lst, ctrl in [(1, self.titles, self.ui.titleButton),
        #                      (2, self.classes, self.ui.classButton),
        #                      (3, self.processes, self.ui.exeButton),
        #                      (None, None, self.ui.helpButton)]:
        #     if lst:
        #         menu = QtGui.QMenu(self)
        #         usedmenu = QtGui.QMenu(menu)
        #         usedmenu.setTitle('all in use...')
        #         submenu = QtGui.QMenu(menu)
        #         submenu.setTitle('all available...')
        #         menu.addMenu(submenu)
        #         for item in sorted(lst, key=lambda s: s.lower()):
        #             action = QtGui.QAction(item, submenu, triggered=partial(self.setScope, i, item))
        #             submenu.addAction(action)
        #         ctrl.setMenu(menu)

        menu = QtGui.QMenu(self)
        submenu = QtGui.QMenu(menu)
        submenu.setTitle('all in use...')
        for scope in sorted(self.a2.get_used_scopes(), key=lambda s: s.lower()):
            action = QtGui.QAction(scope, submenu, triggered=partial(self.set_scope_string, scope))
            submenu.addAction(action)
        menu.addMenu(submenu)
        for title, url in self.help_map.items():
            #action = QtGui.QAction(, menu, triggered=partial(a2util.surf_to, url))
            menu.addAction(title, self.surf_to_help)
        #self.ui.helpButton.setMenu(menu)

    def surf_to_help(self):
        url = self.help_map[self.sender().text()]
        a2util.surf_to(url)

    def set_scope_string(self, scope_string=None):
        if scope_string is None:
            scope_string = self.sender().text()

        self.ui.scope_string.setText(scope_string)
        # from given text fill the line edits already
        if scope_string:
            for typ, ctrl in [('ahk_exe', self.ui.scope_exe), ('ahk_class', self.ui.scope_class)]:
                found = text.find(typ)
                if found != -1:
                    ctrl.setText(text[found + len(typ):].strip())
                    text = text[:found]
            self.ui.scope_title.setText(scope_string.strip())

    def textChange(self):
        texts = [self.ui.scopeTitle.text()]
        winclass = self.ui.scopeClass.text()
        if winclass:
            texts.append('ahk_class ' + winclass)
        winexe = self.ui.scopeExe.text()
        if winexe:
            texts.append('ahk_exe ' + winexe)
        self.ui.scopeText.setText(' '.join(texts).strip())

    def setScope(self, index, text):
        ctrls = [self.ui.scope_string, self.ui.scope_title, self.ui.scope_class, self.ui.scope_exe]
        ctrls[index].setText(text)

    def get_scope_nfo(self):
        # call AHK script to get all window classes, titles and executables
        scope_nfo = a2ahk.call_lib_cmd('get_scope_nfo')
        scope_nfo = scope_nfo.split('\\n')
        if not scope_nfo:
            log.error('Error getting scope_nfo!! scope_nfo: %s' % scope_nfo)
            return

        self.titles, self.classes, self.processes = set(), set(), set()
        num_items = len(scope_nfo)
        num_items = num_items - (num_items % 3)
        for i in range(0, num_items, 3):
            if scope_nfo[i]:
                self.titles.add(scope_nfo[i])
            if scope_nfo[i + 1]:
                self.classes.add(scope_nfo[i + 1])
            if scope_nfo[i + 2]:
                self.processes.add(scope_nfo[i + 2])

    def ok(self):
        self.okayed.emit(self.scope_string)
