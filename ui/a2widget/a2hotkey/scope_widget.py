from functools import partial
from collections import OrderedDict

from PySide2 import QtGui, QtCore, QtWidgets

import a2ahk
import a2util
import a2core
import a2ctrl.connect
from a2widget.a2hotkey import scope_widget_ui
from a2widget.a2hotkey.hotkey_widget import Vars

log = a2core.get_logger(__name__)
SCOPE_ITEMS = ['titles', 'classes', 'processes']
AHK_TYPES = ['ahk_class', 'ahk_exe']
MAX_LABEL_LEN = 80


class ScopeWidget(QtWidgets.QWidget):
    changed = QtCore.Signal()
    _scope_mode_changed = QtCore.Signal(str)
    _scope_text_changed = QtCore.Signal(str)

    def __init__(self, parent):
        super(ScopeWidget, self).__init__(parent)
        self._cfg = None
        self.help_map = None
        self.help_menu = None
        self._setup_ui()
        self.system_scope_data = {}
        self.get_scope_data()

    def on_text_change(self):
        scope_string = get_scope_string(*[f.text() for f in self.input_fields.values()])
        if self.ui.cfg_scope.count():
            self.ui.cfg_scope.set_item_name(scope_string)
        else:
            self.add_scope(scope_string)
        self.scope_update()

    def set_config(self, config_dict=None):
        if config_dict is not None:
            self._cfg = config_dict

        if self._cfg is None:
            return

        a2ctrl.connect.control_list([self.ui.scopeMode_0, self.ui.scopeMode_1, self.ui.scopeMode_2],
                                    self._cfg, self._scope_mode_changed)
        self.ui.cfg_scope.add(self._cfg.get(Vars.scope, []))

        if not self._cfg.get(Vars.scope_change, False):
            for widget in [self.ui.type_radio_widget, self.ui.fields_widget,
                           self.ui.tool_buttons_widget, self.ui.cfg_scope]:
                widget.setEnabled(False)
        else:
            self.on_scope_mode_change()

    def get_config(self):
        return self._cfg

    def on_selection_change(self, scope_string):
        self.blockSignals(True)
        texts = ['', '', '']
        for i, typ in [(2, AHK_TYPES[1]), (1, AHK_TYPES[0])]:
            found = scope_string.find(typ)
            if found != -1:
                texts[i] = (scope_string[found + len(typ):].strip())
                scope_string = scope_string[:found]
        texts[0] = scope_string.strip()
        for i, ctrl in enumerate(self.input_fields.values()):
            ctrl.setText(texts[i])
        self.blockSignals(False)

    def on_scope_mode_change(self):
        scope_mode = self._cfg.get(Vars.scope_mode) != 0
        for wgt in [self.ui.fields_widget, self.ui.tool_buttons_widget, self.ui.cfg_scope]:
            wgt.setEnabled(scope_mode)
        self.changed.emit()

    def add_scope(self, scope_string=''):
        self.ui.cfg_scope.add(scope_string)
        self.ui.scope_title.setFocus()

    def scope_update(self):
        if self._cfg is not None:
            self._cfg['scope'] = self.ui.cfg_scope.get_names()
        self.changed.emit()

    def build_list_context_menu(self, pos):
        if self.ui.cfg_scope.selectedItems():
            self.context_menu.popup(self.ui.cfg_scope.mapToGlobal(pos))

    def build_button_field_menu(self, index, menu):
        name = SCOPE_ITEMS[index]
        # usedmenu = menu.addMenu('%s in use' % name.title())
        submenu = menu.addMenu('Available %s' % name.title())
        for item in sorted(self.system_scope_data[name], key=lambda s: s.lower()):
            # action = QtGui.QAction(item, submenu, triggered=partial(self.set_scope, i, item))
            action = submenu.addAction(item, self._set_button_field)
            action.setData(name)

    def _set_button_field(self):
        sender = self.sender()
        self.input_fields[sender.data()].setText(sender.text())

    def build_add_scope_menu(self):
        if self.add_menu is None:
            self.add_menu = QtWidgets.QMenu(self)

            icons = a2ctrl.Icons.inst()
            self.add_menu.addAction(icons.list_add, 'Add New Empty', self.add_scope)
            self.add_menu.addAction(icons.locate, 'Pick from Window', self.pick_scope_info)

            submenu = QtWidgets.QMenu(self.add_menu)
            submenu.setTitle('All in use...')
            submenu.aboutToShow.connect(self._build_in_use_menu)
            self.add_menu.addMenu(submenu)

            submenu = QtWidgets.QMenu(self.add_menu)
            submenu.setTitle('All available ...')
            submenu.aboutToShow.connect(self._build_available_menu)
            self.add_menu.addMenu(submenu)

            self.add_menu.addSeparator()

            help_menu = self.build_help_menu()
            help_menu.setTitle('Help ...')
            help_menu.setIcon(icons.help)
            self.add_menu.addMenu(help_menu)

        self.add_menu.popup(QtGui.QCursor.pos())

    def _build_available_menu(self):
        menu = self.sender()
        menu.clear()
        for title, class_name, process in self.system_scope_data['__all']:
            scope_string = get_scope_string(title, class_name, process)
            action = menu.addAction(scope_string[:MAX_LABEL_LEN], self._add_scope_from_action)
            action.setData(scope_string)

    def _build_in_use_menu(self):
        menu = self.sender()
        menu.clear()
        import a2runtime
        collector = a2runtime.collect_includes(a2runtime.IncludeType.hotkeys)
        scopes = list(collector.hotkeys.hotkeys_scope_incl.keys())
        scopes.extend(collector.hotkeys.hotkeys_scope_excl.keys())

        for scope in sorted(scopes, key=lambda s: s.lower()):
            action = menu.addAction(scope[:MAX_LABEL_LEN], self._add_scope_from_action)
            action.setData(scope)

    def _add_scope_from_action(self):
        scope_string = self.sender().data()
        self.add_scope(scope_string)

    def pick_scope_info(self):
        scope_nfo_string = a2ahk.call_lib_cmd('pick_scope_nfo')
        try:
            title, class_name, process = scope_nfo_string.split('\\n')
            scope_string = get_scope_string(title, class_name, process)
            self.add_scope(scope_string)

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
        self.system_scope_data['__all'] = set()
        num_items = len(scope_nfo)
        num_items -= num_items % 3
        for i in range(0, num_items, 3):
            self.system_scope_data['__all'].add((scope_nfo[i], scope_nfo[i + 1], scope_nfo[i + 2]))
            for j in range(3):
                this_value = scope_nfo[i + j]
                if this_value:
                    self.system_scope_data[SCOPE_ITEMS[j]].add(this_value)

    def _setup_ui(self):
        # update check done in parent widget for proper order
        self.ui = scope_widget_ui.Ui_ScopeWidget()
        self.ui.setupUi(self)

        self.input_fields = OrderedDict()
        i = 0
        for name, ctrl in zip(SCOPE_ITEMS, [self.ui.scope_title, self.ui.scope_class, self.ui.scope_exe]):
            self.input_fields[name] = ctrl
            ctrl.textChanged.connect(self._scope_text_changed.emit)
            ctrl.menu_called.connect(partial(self.build_button_field_menu, i))
            i += 1

        icons = a2ctrl.Icons.inst()
        self.ui.scope_add.setIcon(icons.list_add)
        self.ui.scope_delete.clicked.connect(self.ui.cfg_scope.remove_selected)
        self.ui.scope_delete.setIcon(icons.delete)
        self.ui.scope_pick.clicked.connect(self.pick_scope_info)
        self.ui.scope_pick.setIcon(icons.locate)

        self.ui.cfg_scope.single_name_selected.connect(self.on_selection_change)
        self.ui.cfg_scope.selection_cleared.connect(self.on_selection_clear)

        self.ui.cfg_scope.changed.connect(self.scope_update)
        self.ui.cfg_scope.context_menu_requested.connect(self.build_list_context_menu)

        self.context_menu = QtWidgets.QMenu(self)
        self.context_menu.addAction(icons.delete, 'Delete scope item',
                                    self.ui.cfg_scope.remove_selected)

        self._scope_mode_changed.connect(self.on_scope_mode_change)
        self._scope_text_changed.connect(self.on_text_change)

        self.add_menu = None
        self.ui.scope_add.clicked.connect(self.build_add_scope_menu)

        self.ui.scope_help.setIcon(icons.help)
        self.ui.scope_help.clicked.connect(self.popup_help_menu)

    def build_help_menu(self):
        if not self.help_map:
            self.help_menu = QtWidgets.QMenu(self)
            a2 = a2core.A2Obj.inst()
            icons = a2ctrl.Icons.inst()
            self.help_map = {'Help on Scope Setup': a2.urls.help_scopes,
                             'Help on AHK WinActive': a2.urls.ahkWinActive,
                             'Help on AHK WinTitle': a2.urls.ahkWinTitle}
            for title in self.help_map:
                self.help_menu.addAction(icons.help, title, self.goto_help)

        return self.help_menu

    def popup_help_menu(self):
        menu = self.build_help_menu()
        menu.popup(QtGui.QCursor.pos())

    def goto_help(self):
        a2util.surf_to(self.help_map[self.sender().text()])

    def on_selection_clear(self):
        self.blockSignals(True)
        for f in self.input_fields.values():
            f.setText('')
        self.blockSignals(False)

    def hide_global_button(self):
        self.ui.scopeMode_0.setVisible(False)
        self.ui.scopeMode_1.setChecked(True)
        self.on_scope_mode_change()


def get_scope_string(title, class_name, process):
    items = [title]
    if class_name:
        items.append(AHK_TYPES[0] + ' ' + class_name)
    if process:
        items.append(AHK_TYPES[1] + ' ' + process)
    scope_string = ' '.join(items).strip()
    return scope_string


if __name__ == '__main__':
    import a2widget.demo.hotkey_demo
    a2widget.demo.hotkey_demo.show()
