"""
Created on Apr 30, 2016

@author: eRiC
"""
import ahk
import a2ctrl
import a2ctrl.list
import a2core
import logging
from PySide import QtGui
from functools import partial
from a2ctrl import scopeDialog_ui


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Hotkey_Scope_Handler(object):
    def __init__(self, main):
        self.main = main
        self.ui = main.ui

        self.ui.cfg_scopeMode.currentIndexChanged.connect(self.scopeModeChanged)
        self.scopeModeChanged()
        
        self.ui.scopePlus.mousePressEvent = self.scopePopup
        self.ui.scopeMinus.clicked.connect(self.scopeDelete)
        self.ui.cfg_scope.mouseDoubleClickEvent = partial(self.scopePopup, change=True)
        self.ui.cfg_scope.setFont(a2ctrl.fontL)
        self.scopeUpdate()

    def scopeModeChanged(self, index=None):
        if index is None:
            index = self.ui.cfg_scopeMode.currentIndex()
        state = index != 0
        self.ui.cfg_scope.setVisible(state)
        self.ui.scopePlus.setVisible(state)
        self.ui.scopeMinus.setVisible(state)
        
    def scopePopup(self, event, change=False):
        # to create new and change scope items from the list
        selItem = None
        text = ''
        if change:
            selItem = self.ui.cfg_scope.selectedItems()
            if not selItem:
                return
            text = selItem[0].text()

        self.scopePop = ScopeDialog(text, event.globalX(), event.globalY(),
                                    self.main, self.scopePopOK)
        self.scopePop.show()

    def scopePopOK(self):
        text = self.scopePop.ui.scopeText.text()
        if self.scopePop.edit:
            selItem = self.ui.cfg_scope.selectedItems()[0]
            selItem.setText(text)
        else:
            item = QtGui.QListWidgetItem(text)
            self.ui.cfg_scope.addItem(item)
            item.setSelected(True)
        self.scopePop.close()
        self.scopeUpdate()

    def scopeDelete(self):
        selectedIndexes = self.ui.cfg_scope.selectedIndexes()
        if selectedIndexes:
            selIndex = [mi.row() for mi in selectedIndexes][0]
            self.ui.cfg_scope.takeItem(selIndex)
            self.scopeUpdate()

    def scopeUpdate(self):
        allItems = a2ctrl.list.get_items_as_text(self.ui.cfg_scope)
        p = a2ctrl.fontL.pointSize()
        h = ((max(1, len(allItems)) * p * a2ctrl.uiScale) + 20) * a2ctrl.uiScale
        self.ui.cfg_scope.setMinimumHeight(h)
        self.main.cfg['scope'] = allItems


class ScopeDialog(QtGui.QDialog):
    def __init__(self, text, x, y, parent, ok_func, *args):
        super(ScopeDialog, self).__init__(parent)
        self.ui = scopeDialog_ui.Ui_ScopeDialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.ok_func = ok_func
        self.setWindowTitle('setup scope')
        self.a2 = a2core.A2Obj.inst()
        self.edit = text != ''

        self.get_scope_nfo()
        self.setupUi(x, y)
        self.setScopeText(text)

    def setupUi(self, x, y):
        self.resize(self.width() * a2ctrl.uiScale, self.minimumSizeHint().height())
        pos = self.pos()
        pos.setX(x - (self.width() / 2))
        pos.setY(y - (self.height() / 2))
        self.move(pos)
        self.ui.scopeText.setStyleSheet('* {background-color:#E0E0E0}')
        for ui in [self.ui.scopeText, self.ui.okButton, self.ui.cancelButton]:
            ui.setFont(a2ctrl.fontXL)
        #for ui in [self.ui.helpButton, self.ui.titleButton, self.ui.classButton, self.ui.exeButton]:
        #    ui.setMinimumWidth(labelW)
        self.ui.okButton.clicked.connect(self.ok_func)
        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.scopeTitle.setFocus()

        for ctrl in [self.ui.scopeTitle, self.ui.scopeClass, self.ui.scopeExe]:
            ctrl.textChanged.connect(self.textChange)
        # put menus to the different buttons
        for i, lst, ctrl in [(1, self.titles, self.ui.titleButton),
                             (2, self.classes, self.ui.classButton),
                             (3, self.processes, self.ui.exeButton),
                             (None, None, self.ui.helpButton)]:
            if lst:
                menu = QtGui.QMenu(self)
                usedmenu = QtGui.QMenu(menu)
                usedmenu.setTitle('all in use...')
                submenu = QtGui.QMenu(menu)
                submenu.setTitle('all available...')
                menu.addMenu(submenu)
                for item in sorted(lst, key=lambda s: s.lower()):
                    action = QtGui.QAction(item, submenu, triggered=partial(self.setScope, i, item))
                    submenu.addAction(action)
                ctrl.setMenu(menu)
            ctrl.setMinimumWidth(a2ctrl.labelW)

        menu = QtGui.QMenu(self)
        submenu = QtGui.QMenu(menu)
        submenu.setTitle('all in use...')
        for scope in sorted(self.a2.get_used_scopes(), key=lambda s: s.lower()):
            action = QtGui.QAction(scope, submenu, triggered=partial(self.setScopeText, scope))
            submenu.addAction(action)
        menu.addMenu(submenu)
        for title, url in [('Help on Scope Setup', self.a2.urls.helpScopes),
                           ('Help on AHK WinActive', self.a2.urls.ahkWinActive),
                           ('Help on AHK WinTitle', self.a2.urls.ahkWinTitle)]:
            action = QtGui.QAction(title, menu, triggered=partial(a2core.surfTo, url))
            menu.addAction(action)
        self.ui.helpButton.setMenu(menu)

    def setScopeText(self, text, *args):
        self.ui.scopeText.setText(text)
        # from given text fill the line edits already
        if text:
            for typ, ctrl in [('ahk_exe', self.ui.scopeExe), ('ahk_class', self.ui.scopeClass)]:
                found = text.find(typ)
                if found != -1:
                    ctrl.setText(text[found + len(typ):].strip())
                    text = text[:found]
            self.ui.scopeTitle.setText(text.strip())

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
        ctrls = [self.ui.scopeText, self.ui.scopeTitle, self.ui.scopeClass, self.ui.scopeExe]
        ctrls[index].setText(text)

    def get_scope_nfo(self):
        # call AHK script to get all window classes, titles and executables
        scope_nfo = ahk.call_cmd('get_scope_nfo')
        scope_nfo = scope_nfo.split('\\n')
        if not scope_nfo:
            log.error('Error getting scope_nfo!! scope_nfo: %s' % scope_nfo)
            return
        
        self.titles = set()
        self.classes = set()
        self.processes = set()
        num_items = len(scope_nfo)
        num_items = num_items - (num_items % 3)
        for i in range(0, num_items, 3):
            if scope_nfo[i]:
                self.titles.add(scope_nfo[i])
            if scope_nfo[i + 1]:
                self.classes.add(scope_nfo[i + 1])
            if scope_nfo[i + 2]:
                self.processes.add(scope_nfo[i + 2])
