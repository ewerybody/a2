from functools import partial
from a2qt import QtGui, QtCore, QtWidgets

import a2mod
import a2uic
import a2ctrl
import a2core

log = a2core.get_logger(__name__)
_CFG_PREFIX = 'modlist_'
SHOW_ENABLED = 'show_enabled_only'
ARRANG_PACKG = 'arrange_by_package'
SORT_BY_PAKG = 'sort_by_package'
PKG_COLLAPSD = 'package_collapsed'


class A2ModuleList(QtWidgets.QWidget):
    selection_changed = QtCore.Signal(list)
    enable_request = QtCore.Signal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.a2 = a2core.A2Obj.inst()
        self._setup_ui()
        self.selection = None

        self._filtered = False
        self._filter_tags = []
        # self.icon_label = a2ctrl.Icons.label
        self._brush_default = None
        self._brush_tinted = None
        # to avoid adding variables to external objects
        self._module_map = {}

    def _on_selection_change(self, items):
        modules = [item.data(0, QtCore.Qt.UserRole) for item in items]
        selection = [m for m in modules if m is not None]
        if selection != self.selection:
            self.selection = selection
            self.selection_changed.emit(self.selection)

    def select(self, modules=None):
        self.ui.a2module_list_widget.blockSignals(True)
        self.ui.a2module_list_widget.clear_selection()

        selection, last_item = self._select(modules)

        if last_item is not None:
            self.ui.a2module_list_widget.setCurrentItem(last_item)

        self.ui.a2module_list_widget.blockSignals(False)
        if selection != self.selection:
            self.selection = selection
            self.selection_changed.emit(self.selection)

    def _select(self, modules):
        selection = []
        last_item = None
        if not modules:
            return selection, last_item

        if isinstance(modules, str):
            modules = [modules]

        for item in modules:
            if isinstance(item, a2mod.Mod):
                selection.append(item)
                list_item = self._module_map.get(item.key)

            elif isinstance(item, str):
                list_item = self._module_map.get(item)
                try:
                    srcname, modname = item.split('|', 1)
                    mod = self.a2.module_sources[srcname].mods[modname]
                    selection.append(mod)
                except (KeyError, AttributeError):
                    continue
            else:
                continue

            if list_item is not None:
                list_item.setSelected(True)
                last_item = list_item

        return selection, last_item

    def draw_modules(self, select_mods=None):
        """
        Call to refill the module list with items.
        ... to match filtering, module deletion or enabling of module sources.
        """
        if not select_mods:
            if not self._filtered and not self._filter_tags and not self.cfg(SHOW_ENABLED):
                select_mods = self.selection or []
            else:
                select_mods = []

        self.ui.a2module_list_widget.blockSignals(True)
        self.ui.a2module_list_widget.clear()
        self._module_map.clear()

        arrange = self.cfg(ARRANG_PACKG, True)
        collapsed = self.cfg(PKG_COLLAPSD, [])
        show_enabled = self.cfg(SHOW_ENABLED)

        if arrange:
            self.ui.a2module_list_widget.itemCollapsed.connect(self._on_root_toggle)
            self.ui.a2module_list_widget.itemExpanded.connect(self._on_root_toggle)
        self.ui.a2module_list_widget.setIndentation(10 if arrange else 0)

        shown_mods = []
        for source in self.a2.module_sources.values():
            shown_mods.clear()
            for mod in source.mods.values():
                if mod not in select_mods:
                    if self.is_filtered(mod):
                        continue
                    if show_enabled and not mod.enabled:
                        continue
                shown_mods.append(mod)

            if show_enabled and not shown_mods or arrange and not shown_mods:
                continue

            if arrange:
                root_item = QtWidgets.QTreeWidgetItem(self.ui.a2module_list_widget, [source.name])
                root_item.setIcon(0, source.icon)
                if source.name not in collapsed:
                    root_item.setExpanded(True)
            else:
                root_item = self.ui.a2module_list_widget

            for mod in shown_mods:
                item = QtWidgets.QTreeWidgetItem(root_item)
                item.setText(0, mod.display_name)
                item.setData(0, QtCore.Qt.UserRole, mod)
                self._module_map[mod.key] = item
                self._set_item_state(item, mod)

        if not self.cfg(SORT_BY_PAKG):
            self.ui.a2module_list_widget.sortItems(0, QtCore.Qt.AscendingOrder)

        if select_mods:
            self.select(select_mods)
        self.ui.a2module_list_widget.blockSignals(False)

    def _on_root_toggle(self, item):
        collapsed = self.cfg(PKG_COLLAPSD, [])
        name = item.data(0, QtCore.Qt.DisplayRole)
        if self.ui.a2module_list_widget.isItemExpanded(item):
            if name in collapsed:
                collapsed.remove(name)
        elif name not in collapsed:
            collapsed.append(name)
        self.set_cfg(PKG_COLLAPSD, collapsed)

    def is_filtered(self, mod):
        """
        Gets you True/False to see if the module should be filtered away.
        """
        if self._filtered and self._filter_phrase not in mod.name.lower():
            return True
        if self._filter_tags:
            for tag in self._filter_tags:
                if mod.has_tag(tag):
                    return False
            return True
        return False

    def _setup_ui(self):
        from a2widget import a2module_list_ui

        a2uic.check_module(a2module_list_ui)
        self.ui = a2module_list_ui.Ui_ModuleList()
        self.ui.setupUi(self)

        self.ui.a2search_x_button.setIcon(a2ctrl.Icons.clear)
        self.ui.a2search_x_button.setVisible(False)
        self.ui.search_field.textChanged.connect(self.update_filter)
        self.ui.a2search_x_button.clicked.connect(self.reset_filter)
        self.ui.filter_menu_button.menu_called.connect(self.build_filter_menu)
        self.setLayout(self.ui.module_list_layout)

        self.ui.a2module_list_widget.items_selected.connect(self._on_selection_change)
        self.ui.a2module_list_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.a2module_list_widget.customContextMenuRequested.connect(self._build_context_menu)

    def update_filter(self, phrase=''):
        self._filter_phrase = phrase
        self._filtered = phrase != ''
        self.ui.a2search_x_button.setVisible(self._filtered)
        self.draw_modules()

    def reset_filter(self):
        self.ui.search_field.setText('')

    def build_filter_menu(self, menu: QtWidgets.QMenu):
        self._add_cfg_action(menu, SHOW_ENABLED, 'Only Enabled', self.toggle_cfg)
        self._add_cfg_action(menu, ARRANG_PACKG, 'Arrange under package', self.toggle_cfg)
        self._add_cfg_action(menu, SORT_BY_PAKG, 'Sort by package', self.toggle_cfg)
        menu.addSeparator()

        if self._filter_tags:
            menu.addAction(a2ctrl.Icons.clear, 'Clear Tags', self.clear_filter_tags)

        for tag in a2core.tags():
            action = menu.addAction(a2ctrl.Icons.label, tag, self.do_filter_tags)
            action.setCheckable(True)
            action.setChecked(tag in self._filter_tags)

    def _add_cfg_action(self, menu: QtWidgets.QMenu, name, label, func):
        action = menu.addAction(label, func)
        action.setData(name)
        action.setCheckable(True)
        action.setChecked(self.cfg(name, False))
        return action

    def clear_filter_tags(self):
        self._filter_tags = []
        self.draw_modules()

    def do_filter_tags(self):
        tag_name = self.sender().text()
        if tag_name in self._filter_tags:
            self._filter_tags.remove(tag_name)
        else:
            self._filter_tags.append(tag_name)
        self.draw_modules()

    def toggle_cfg(self):
        action = self.sender()
        self.set_cfg(action.data(), action.isChecked())
        self.draw_modules()

    def set_item_state(self, module):
        item = self._module_map.get(module.key)
        if item is None:
            log.error('Could not get item from module: %s' % module.key)
        else:
            self._set_item_state(item, module)

    def _set_item_state(self, item, module):
        if module.enabled:
            icon, brush = module.icon, self._brush_default
        else:
            icon, brush = module.icon.tinted, self._brush_tinted
        item.setIcon(0, icon)
        item.setForeground(0, brush)

    def set_item_states(self, modules):
        for mod in modules:
            self.set_item_state(mod)

    def set_item_colors(self, default, tinted):
        self._brush_default = QtGui.QBrush(QtGui.QColor(default))
        self._brush_tinted = QtGui.QBrush(QtGui.QColor(tinted))

    def _build_context_menu(self, pos):
        if not self.selection:
            return

        menu = QtWidgets.QMenu(self)
        if len(self.selection) == 1:
            module = self.selection[0]
            menu.addAction(a2ctrl.Icons.folder, 'Explore to module folder', self._explore_module)
            name = f'"{module.display_name}"'
            label = 'Disable' if module.enabled else 'Enable'
            _add_action(menu, label, name, partial(self.enable_request.emit, not module.enabled))

        else:
            num_enabled = sum(m.enabled for m in self.selection)
            name = 'Selected Modules'
            if len(self.selection) != num_enabled:
                _add_action(menu, 'Enable', name, partial(self.enable_request.emit, True))
            if num_enabled:
                _add_action(menu, 'Disable', name, partial(self.enable_request.emit, False))

        if not menu.isEmpty():
            menu.popup(QtGui.QCursor.pos())

    def _explore_module(self):
        if not self.selection:
            return
        import a2util

        a2util.explore(self.selection[0].path)

    def cfg(self, name, default=None):
        """Lookup Module List settings from db."""
        value = self.a2.db.get(f'{_CFG_PREFIX}{name}')
        if value is None:
            return default
        return value

    def set_cfg(self, name, value):
        """Set Module List settings to db."""
        self.a2.db.set(f'{_CFG_PREFIX}{name}', value)


def _add_action(menu, label, name, signal):
    menu.addAction(a2ctrl.Icons.check, f'{label} {name}', signal)
