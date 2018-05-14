import a2ahk
import a2core
import a2ctrl
import a2util
from collections import OrderedDict
from PySide import QtGui, QtCore

from . import scope_dialog_ui
from functools import partial


log = a2core.get_logger(__name__)
SCOPE_ITEMS = ['titles', 'classes', 'processes']


class ScopeDialog(QtGui.QDialog):
    okayed = QtCore.Signal(str)

    def __init__(self, parent, config=None):
        super(ScopeDialog, self).__init__(parent)
        self._cfg = config
        a2ctrl.check_ui_module(scope_dialog_ui)
        self.ui = scope_dialog_ui.Ui_ScopeDialog()

        self.ui.setupUi(self)
        self.setModal(True)
        self.setWindowTitle('Setup Scope')

        self.system_scope_data = {}
        self.get_scope_data()

        self.a2 = a2core.A2Obj.inst()
        self.help_map = OrderedDict()
        self.help_map['Help on Scope Setup'] = self.a2.urls.helpScopes
        self.help_map['Help on AHK WinActive'] = self.a2.urls.ahkWinActive
        self.help_map['Help on AHK WinTitle'] = self.a2.urls.ahkWinTitle

        self.setup_ui()
        self.set_scope_string()

    def setup_ui(self):
        pos = self.pos()
        cursor_pos = QtGui.QCursor.pos()
        pos.setX(cursor_pos.x() - (self.width() / 2))
        pos.setY(cursor_pos.y() - (self.height() / 2))
        self.move(pos)
        self.ui.a2ok_button.clicked.connect(self.ok)
        self.ui.a2cancel_button.clicked.connect(self.reject)
        self.ui.scope_title.setFocus()

        self.scope_ctrls = OrderedDict()
        for name, ctrl in zip(SCOPE_ITEMS, [self.ui.scope_title, self.ui.scope_class,
                                            self.ui.scope_exe]):
            self.scope_ctrls[name] = ctrl

        for i, ctrl in enumerate(self.scope_ctrls.values()):
            ctrl.textChanged.connect(self.text_change)
            ctrl.menu_about_to_show.connect(partial(self.build_button_menu, i))

#        menu = QtGui.QMenu(self)
#        submenu = QtGui.QMenu(menu)
#        submenu.setTitle('all in use...')
#        for scope in sorted(self.a2.get_used_scopes(), key=lambda s: s.lower()):
#            action = QtGui.QAction(scope, submenu, triggered=partial(self.set_scope_string, scope))
#            submenu.addAction(action)
#        menu.addMenu(submenu)

#        self.scopes_submenu = self.ui.scope_string.menu.addMenu('All Scopes in use')
#        self.scopes_submenu.aboutToShow.connect(self.build_all_scopes_menu)
        # self.ui.scope_string.menu.addSeparator()
#        for title in self.help_map:
#            self.ui.scope_string.add_action(title, self.surf_to_help)

    def build_all_scopes_menu(self):
        self.scopes_submenu.clear()

        import a2runtime
        collector = a2runtime.collect_includes(a2runtime.IncludeType.hotkeys)
        scopes = list(collector.hotkeys.hotkeys_scope_incl.keys())
        scopes.extend(collector.hotkeys.hotkeys_scope_excl.keys())

        for scope in sorted(scopes, key=lambda s: s.lower()):
            print('scope: %s' % scope)
#            action = QtGui.QAction(scope, submenu, triggered=partial(self.set_scope_string, scope))
            self.scopes_submenu.addAction(scope, self.set_scope_string)

    def build_button_menu(self, index, menu):
        menu.clear()
        name = SCOPE_ITEMS[index]
        # usedmenu = menu.addMenu('%s in use' % name.title())
        submenu = menu.addMenu('Available %s' % name.title())
        for item in sorted(self.system_scope_data[name], key=lambda s: s.lower()):
            # action = QtGui.QAction(item, submenu, triggered=partial(self.set_scope, i, item))
            action = submenu.addAction(item, self.set_menu_item)
            action.setData(name)

    def set_menu_item(self):
        sender = self.sender()
        self.scope_ctrls[sender.data()].setText(sender.text())

    def surf_to_help(self):
        url = self.help_map[self.sender().text()]
        a2util.surf_to(url)

    def set_scope_config(self, config=None):
        if config is None:
            scope_string = self.sender().text()
        self.ui.scope_string.setText(scope_string)

        # from given text fill the line edits
        if scope_string:
            for typ, ctrl in [('ahk_exe', self.ui.scope_exe),
                              ('ahk_class', self.ui.scope_class)]:
                found = scope_string.find(typ)
                if found != -1:
                    ctrl.setText(scope_string[found + len(typ):].strip())
                    scope_string = scope_string[:found]
            self.ui.scope_title.setText(scope_string.strip())

    def text_change(self):
        texts = [self.ui.scope_title.text()]
        winclass = self.ui.scope_class.text()
        if winclass:
            texts.append('ahk_class ' + winclass)
        winexe = self.ui.scope_exe.text()
        if winexe:
            texts.append('ahk_exe ' + winexe)
        self.scope_string = ' '.join(texts).strip()
        self.ui.scope_string.setText(self.scope_string)

    def set_scope(self, index, text):
        ctrls = [self.ui.scope_string, self.ui.scope_title, self.ui.scope_class, self.ui.scope_exe]
        ctrls[index].setText(text)

    def get_scope_data(self):
        # call AHK script to get all window classes, titles and executables
        scope_nfo = a2ahk.call_lib_cmd('get_scope_nfo')
        scope_nfo = scope_nfo.split('\\n')
        if not scope_nfo:
            log.error('Error getting scope_nfo!! scope_nfo: %s' % scope_nfo)
            return

        self.system_scope_data = dict([(n, set()) for n in SCOPE_ITEMS])
        num_items = len(scope_nfo)
        num_items -= num_items % 3
        for i in range(0, num_items, 3):
            for j in range(3):
                this_value = scope_nfo[i + j]
                if this_value:
                    self.system_scope_data[SCOPE_ITEMS[j]].add(this_value)

    def ok(self):
        self.okayed.emit(self.scope_string)
        self.accept()
