"""
Created on Apr 30, 2016

@author: eRiC
"""
import a2ahk
import a2util
import a2ctrl.qlist
import a2core
from PySide import QtGui, QtCore
from functools import partial
from a2widget import a2scope_dialog_ui


log = a2core.get_logger(__name__)


class HotkeyScopeWidget(QtGui.QWidget):
    changed = QtCore.Signal(dict)

    def __init__(self, main):
        super(HotkeyScopeWidget, self).__init__()
        self.main = main
        a2ctrl.check_ui_module(a2scope_widget_ui)
        self.ui = a2scope_widget_ui.Ui_ScopeWidget()
        self.ui.setupUi(self)
        # self.ui = main.ui
        self.ui.cfg_scopeMode.currentIndexChanged.connect(self.scope_mode_change)
        self.scope_mode_change()

        self.ui.scope_add.clicked.connect(self.show_dialog)
        self.ui.scope_delete.clicked.connect(self.delete_scope)
        # self.ui.cfg_scope.mouseDoubleClickEvent = partial(self.scopePopup, change=True)
        # self.ui.cfg_scope.mouseDoubleCli
        # self.scope_update()
        self._dialog = None

    def scope_mode_change(self, index=None):
        if index is None:
            index = self.ui.cfg_scopeMode.currentIndex()
        state = index != 0
        self.ui.cfg_scope.setVisible(state)
        self.ui.scope_add.setVisible(state)
        self.ui.scope_delete.setVisible(state)

    def show_dialog(self):
        # to create new and change scope items from the list
        selItem = None
        text = ''
        if change:
            selItem = self.ui.cfg_scope.selectedItems()
            if not selItem:
                return
            text = selItem[0].text()

        self._dialog = ScopeDialog(text, self.main)
        self._dialog.okayed.connect(self.dialog_okayed)
        self._dialog.show()

    def dialog_okayed(self, scope_text):
        if self.scopePop.edit:
            item = self.ui.cfg_scope.selectedItems()[0]
            item.setText(scope_text)
        else:
            item = QtGui.QListWidgetItem(scope_text)
            self.ui.cfg_scope.addItem(item)
            item.setSelected(True)
        self.scope_update()

    def delete_scope(self):
        selected_idxs = self.ui.cfg_scope.selectedIndexes()
        if selected_idxs:
            this_row = [mi.row() for mi in selected_idxs][0]
            self.ui.cfg_scope.takeItem(this_row)
            self.scope_update()

    def scope_update(self):
        allItems = a2ctrl.qlist.get_items_as_text(self.ui.cfg_scope)
        # p = a2ctrl.fontL.pointSize()
        # h = ((max(1, len(allItems)) * p * a2ctrl.uiScale) + 20) * a2ctrl.uiScale
        # self.ui.cfg_scope.setMinimumHeight(h)
        self.main.cfg['scope'] = allItems


class HotkeyScopeWidget(object):
    def __init__(self, main):
        self.main = main
        self.ui = main.ui

        self.ui.cfg_scopeMode.currentIndexChanged.connect(self.scope_mode_changed)
        self.scope_mode_changed()

        self.ui.scopePlus.mousePressEvent = self.scope_popup
        self.ui.scopeMinus.clicked.connect(self.scope_delete)
        self.ui.cfg_scope.mouseDoubleClickEvent = partial(self.scope_popup, change=True)
        self.scope_update()

    def scope_mode_changed(self, index=None):
        if index is None:
            index = self.ui.cfg_scopeMode.currentIndex()
        state = index != 0
        self.ui.cfg_scope.setVisible(state)
        self.ui.scopePlus.setVisible(state)
        self.ui.scopeMinus.setVisible(state)

    def scope_popup(self, event, change=False):
        # to create new and change scope items from the list
        selItem = None
        text = ''
        if change:
            selItem = self.ui.cfg_scope.selectedItems()
            if not selItem:
                return
            text = selItem[0].text()

        self.scopePop = ScopeDialog(text, event.globalX(), event.globalY(),
                                    self.main, self.scope_pop_ok)
        self.scopePop.show()

    def scope_pop_ok(self):
        text = self.scopePop.ui.scopeText.text()
        if self.scopePop.edit:
            selItem = self.ui.cfg_scope.selectedItems()[0]
            selItem.setText(text)
        else:
            item = QtGui.QListWidgetItem(text)
            self.ui.cfg_scope.addItem(item)
            item.setSelected(True)
        self.scopePop.close()
        self.scope_update()

    def scope_delete(self):
        selectedIndexes = self.ui.cfg_scope.selectedIndexes()
        if selectedIndexes:
            selIndex = [mi.row() for mi in selectedIndexes][0]
            self.ui.cfg_scope.takeItem(selIndex)
            self.scope_update()

    def scope_update(self):
        allItems = a2ctrl.qlist.get_items_as_text(self.ui.cfg_scope)
        # p = a2ctrl.fontL.pointSize()
        # h = ((max(1, len(allItems)) * p * a2ctrl.uiScale) + 20) * a2ctrl.uiScale
        # self.ui.cfg_scope.setMinimumHeight(h)
        self.main.cfg['scope'] = allItems


class ScopeDialog(QtGui.QDialog):
    def __init__(self, text, x, y, parent, ok_func, *args):
        super(ScopeDialog, self).__init__(parent)
        self.ui = a2scope_dialog_ui.Ui_ScopeDialog()
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
        pos = self.pos()
        pos.setX(x - (self.width() / 2))
        pos.setY(y - (self.height() / 2))
        self.move(pos)
        self.ui.a2ok_button.clicked.connect(self.ok_func)
        self.ui.a2cancel_button.clicked.connect(self.close)
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
            action = QtGui.QAction(title, menu, triggered=partial(a2util.surf_to, url))
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
        scope_nfo = a2ahk.call_lib_cmd('get_scope_nfo')
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
