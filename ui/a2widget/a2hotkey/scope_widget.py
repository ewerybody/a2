import a2core
import a2ctrl.qlist
import a2ctrl.connect
from PySide import QtGui, QtCore
from a2widget.a2hotkey import scope_widget_ui
from pprint import pprint
import a2ahk
from collections import OrderedDict
from functools import partial


log = a2core.get_logger(__name__)
MAX_NON_SCROLL_ITEMS = 5
LIST_LINE_HEIGHT = None
SCOPE_ITEMS = ['titles', 'classes', 'processes']


class ScopeWidget(QtGui.QWidget):
    changed = QtCore.Signal()
    _scope_mode_changed = QtCore.Signal(bool)

    def __init__(self, parent, config=None):
        super(ScopeWidget, self).__init__(parent)
        # self.main = main
        self._cfg = config
        self._line_height_set = False

        self._setup_ui()
        self.get_scope_data()
        self.set_config()

    def on_text_change(self):
        scope_string = self.get_scope_string(
            self.ui.scope_title.text(), self.ui.scope_class.text(), self.ui.scope_exe.text())
        self.set_scope_string(scope_string)

    def set_scope_string(self, scope_string):
        selected_idxs = self.ui.cfg_scope.selectedIndexes()
        if len(selected_idxs) == 1:
            item = self.ui.cfg_scope.itemFromIndex(selected_idxs[0])
            item.setText(scope_string)

    def get_scope_string(self, title, class_name, process):
        items = [title]
        if class_name:
            items.append('ahk_class ' + class_name)
        if process:
            items.append('ahk_exe ' + process)
        scope_string = ' '.join(items).strip()
        return scope_string

    def set_config(self, config_dict=None):
        if config_dict is not None:
            self._cfg = config_dict

        if self._cfg is None:
            return

        a2ctrl.connect.control_list([self.ui.scopeMode_1, self.ui.scopeMode_2],
                                    self._cfg, self._scope_mode_changed)

    def on_selection_change(self):
        items = a2ctrl.qlist.get_selected_as_text(self.ui.cfg_scope)
        print('items: %s' % items)
        if len(items) == 1:
            scope_string = items[0]
            for typ, ctrl in [('ahk_exe', self.ui.scope_exe),
                              ('ahk_class', self.ui.scope_class)]:
                found = scope_string.find(typ)
                if found != -1:
                    ctrl.setText(scope_string[found + len(typ):].strip())
                    scope_string = scope_string[:found]
            self.ui.scope_title.setText(scope_string.strip())

    def on_scope_mode_change(self):
        scope_mode = self._cfg.get('scopeMode')
        print('scope_mode: %s' % scope_mode)

    def set_scope_mode(self):
        self._set_scope_mode()
        self.changed.emit()

    def _set_scope_mode(self, index):
        show_ctrls = index != 0
        self.ui.cfg_scope.setVisible(show_ctrls)
        self.ui.scope_add.setVisible(show_ctrls)
        self.ui.scope_delete.setVisible(show_ctrls)
        if not self._line_height_set:
            self._set_list_line_height()
        return show_ctrls

    def add_scope(self, scope_string=''):
        item = QtGui.QListWidgetItem(scope_string)
        self.ui.cfg_scope.addItem(item)
        item.setSelected(True)
        self.scope_update()

    def delete_scope(self):
        selected_idxs = self.ui.cfg_scope.selectedIndexes()
        if selected_idxs:
            this_row = [mi.row() for mi in selected_idxs][0]
            self.ui.cfg_scope.takeItem(this_row)
            self.scope_update()

    def showEvent(self, *args, **kwargs):
        if self._cfg is None:
            log.error('Showing ScopeWidget whild config is not set yet!')
        self._set_list_line_height()

        return QtGui.QWidget.showEvent(self, *args, **kwargs)

    def _init_line_height(self):
        # figure out list_widget row height
        global LIST_LINE_HEIGHT
        if LIST_LINE_HEIGHT is None:
            item = self.ui.cfg_scope.item(0)
            dummy_create = item is None
            if dummy_create:
                item = QtGui.QListWidgetItem('')
                self.ui.cfg_scope.addItem(item)
            LIST_LINE_HEIGHT = self.ui.cfg_scope.visualItemRect(item).height()
            if dummy_create:
                self.ui.cfg_scope.takeItem(0)
        return LIST_LINE_HEIGHT

    def _set_list_line_height(self, num_items=None):
        self._init_line_height()
        if num_items is None:
            num_items = self.ui.cfg_scope.count()
        h = LIST_LINE_HEIGHT * min(max(num_items, 1), MAX_NON_SCROLL_ITEMS)
        h += LIST_LINE_HEIGHT / 3
        self.ui.cfg_scope.setMinimumHeight(h)
        self.ui.cfg_scope.setMaximumHeight(h)
        self._line_height_set = True

    def scope_update(self):
        all_items = a2ctrl.qlist.get_items_as_text(self.ui.cfg_scope)
        if self._cfg is not None:
            self._cfg['scope'] = all_items
        self._set_list_line_height(len(all_items))
        self.changed.emit()

    def build_list_context_menu(self, pos):
        if self.ui.cfg_scope.selectedItems():
            self.context_menu.popup(self.ui.cfg_scope.mapToGlobal(pos))

    def build_button_field_menu(self, index, menu):
        menu.clear()
        name = SCOPE_ITEMS[index]
        # usedmenu = menu.addMenu('%s in use' % name.title())
        submenu = menu.addMenu('Available %s' % name.title())
        for item in sorted(self.system_scope_data[name], key=lambda s: s.lower()):
            # action = QtGui.QAction(item, submenu, triggered=partial(self.set_scope, i, item))
            action = submenu.addAction(item, self._set_button_field)
            action.setData(name)

    def _set_button_field(self):
        sender = self.sender()
        self.scope_ctrls[sender.data()].setText(sender.text())

    def build_all_scopes_menu(self):
        self.scopes_submenu.clear()

        import a2runtime
        collector = a2runtime.collect_includes(a2runtime.IncludeType.hotkeys)
        scopes = list(collector.hotkeys.hotkeys_scope_incl.keys())
        scopes.extend(collector.hotkeys.hotkeys_scope_excl.keys())

        for scope in sorted(scopes, key=lambda s: s.lower()):
            self.scopes_submenu.addAction(scope, self._add_scope_from_action)

    def _add_scope_from_action(self):
        scope_string = self.sender().text()
        self.add_scope(scope_string)

    def pick_scope_info(self):
        #a2 = a2core.A2Obj.inst()
        #text = a2ahk.call_lib_cmd('pick_scope_nfo', cwd=a2.paths.a2)
        scope_nfo_string = a2ahk.call_lib_cmd('pick_scope_nfo')
        try:
            title, class_name, process = scope_nfo_string.split('\\n')
            for name, value in zip(SCOPE_ITEMS, [title, class_name, process]):
                self.scope_ctrls[name].setText(value)

        except ValueError:
            pass

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

    def _setup_ui(self):
        # update check done in parent widget for proper order
        self.ui = scope_widget_ui.Ui_ScopeWidget()
        self.ui.setupUi(self)

        self.scope_ctrls = OrderedDict()
        for name, ctrl in zip(SCOPE_ITEMS, [self.ui.scope_title,
                              self.ui.scope_class, self.ui.scope_exe]):
            self.scope_ctrls[name] = ctrl

        icons = a2ctrl.Icons.inst()
        self.ui.scope_add.clicked.connect(self.add_scope)
        self.ui.scope_add.setIcon(icons.list_add)
        self.ui.scope_delete.clicked.connect(self.delete_scope)
        self.ui.scope_delete.setIcon(icons.delete)
        self.ui.scope_pick.clicked.connect(self.pick_scope_info)
        self.ui.scope_pick.setIcon(icons.locate)

        self.ui.cfg_scope.itemSelectionChanged.connect(self.on_selection_change)

        self.ui.cfg_scope.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.cfg_scope.customContextMenuRequested.connect(self.build_list_context_menu)
        self.context_menu = QtGui.QMenu(self)
        self.context_menu.addAction(icons.delete, 'Delete scope item', self.delete_scope)

        shortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete),
                                   self.ui.cfg_scope, self.delete_scope)
        shortcut.setContext(QtCore.Qt.WidgetShortcut)
        self._scope_mode_changed.connect(self.on_scope_mode_change)

        for i, ctrl in enumerate(self.scope_ctrls.values()):
            ctrl.textChanged.connect(self.on_text_change)
            ctrl.menu_about_to_show.connect(partial(self.build_button_field_menu, i))

        self.add_menu = QtGui.QMenu(self)
#        submenu = QtGui.QMenu(self.add_menu)
#        submenu.setTitle('all in use...')
#        for scope in sorted(self.a2.get_used_scopes(), key=lambda s: s.lower()):
#            action = QtGui.QAction(scope, submenu, triggered=partial(self.set_scope_string, scope))
#            submenu.addAction(action)
#        menu.addMenu(submenu)

        self.scopes_submenu = self.add_menu.addMenu('All Scopes in use')
        self.scopes_submenu.aboutToShow.connect(self.build_all_scopes_menu)
#        self.ui.scope_string.menu.addSeparator()
#        for title in self.help_map:
#            self.ui.scope_string.add_action(title, self.surf_to_help)


if __name__ == '__main__':
    import a2widget.demo.scope_demo
    a2widget.demo.scope_demo.show()
