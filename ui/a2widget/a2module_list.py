from a2qt import QtGui, QtCore, QtWidgets

import a2mod
import a2uic
import a2ctrl
import a2core

log = a2core.get_logger(__name__)


class A2ModuleList(QtWidgets.QWidget):
    selection_changed = QtCore.Signal(list)
    enable_requested = QtCore.Signal()
    disable_requested = QtCore.Signal()

    def __init__(self, parent):
        super(A2ModuleList, self).__init__(parent)
        self.a2 = a2core.A2Obj.inst()
        self.setup_ui()
        self.selection = None

        self._filtered = False
        self._filter_tags = []
        self._show_enabled_only = self.a2.db.get('modlist_show_enabled_only') or False
        self.icon_label = a2ctrl.Icons.inst().label
        self._font_color = None
        self._font_color_tinted = None
        self.brush_default = None
        self.brush_tinted = None
        # to avoid adding variables to external objects
        self._item_map = {}
        self._module_map = {}

    def _on_selection_change(self, items):
        modules = [self._item_map.get(id(item)) for item in items]
        self.selection = [m for m in modules if m is not None]
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
            if not self._filtered and not self._filter_tags and not self._show_enabled_only:
                select_mods = self.selection or []
            else:
                select_mods = []

        self.ui.a2module_list_widget.blockSignals(True)
        self.ui.a2module_list_widget.clear()
        self._item_map, self._module_map = {}, {}

        for source in self.a2.module_sources.values():
            for mod in source.mods.values():
                if mod not in select_mods:
                    if self.is_filtered(mod):
                        continue
                    if self._show_enabled_only and not mod.enabled:
                        continue

                item = QtWidgets.QListWidgetItem(mod.display_name)
                self._item_map[id(item)] = mod
                self._module_map[mod.key] = item
                self._set_item_state(item, mod)
                self.ui.a2module_list_widget.addItem(item)

        if select_mods:
            self.select(select_mods)
        self.ui.a2module_list_widget.blockSignals(False)

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

    def setup_ui(self):
        from a2widget import a2module_list_ui

        a2uic.check_module(a2module_list_ui)
        self.ui = a2module_list_ui.Ui_ModuleList()
        self.ui.setupUi(self)

        self.ui.a2search_x_button.setIcon(a2ctrl.Icons.inst().clear)
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

    def build_filter_menu(self, menu):
        action = menu.addAction('Only Enabled', self.toggle_show_enabled)
        action.setCheckable(True)
        action.setChecked(self._show_enabled_only)

        menu.addSeparator()

        icons = a2ctrl.Icons.inst()
        if self._filter_tags:
            menu.addAction(icons.clear, 'Clear Tags', self.clear_filter_tags)

        for tag in a2core.A2TAGS:
            action = menu.addAction(icons.label, tag, self.do_filter_tags)
            action.setCheckable(True)
            action.setChecked(tag in self._filter_tags)

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

    def toggle_show_enabled(self):
        state = self.sender().isChecked()
        self._show_enabled_only = state
        self.a2.db.set('modlist_show_enabled_only', state)
        self.draw_modules()

    def set_item_state(self, module):
        item = self._module_map.get(module.key)
        if item is None:
            log.error('Could not get item from module: %s' % module.key)
        else:
            self._set_item_state(item, module)

    def _set_item_state(self, item, module):
        if module.enabled:
            item.setIcon(module.icon)
            item.setForeground(self.brush_default)
        else:
            item.setIcon(module.icon.tinted)
            item.setForeground(self.brush_tinted)

    def set_item_states(self, modules):
        for mod in modules:
            self.set_item_state(mod)

    def set_item_colors(self, default, tinted):
        self._font_color = default
        self._font_color_tinted = tinted
        self.brush_default = QtGui.QBrush(QtGui.QColor(self._font_color))
        self.brush_tinted = QtGui.QBrush(QtGui.QColor(self._font_color_tinted))

    def _build_context_menu(self, pos):
        if not self.selection:
            return

        menu = QtWidgets.QMenu(self)
        if len(self.selection) == 1:
            module = self.selection[0]
            menu.addAction(
                a2ctrl.Icons.inst().folder,
                f'Explore to module folder',
                self._explore_module,
            )
            name = f'"{module.display_name}"'
            if module.enabled:
                _add_action(menu, 'Disable', name, self.disable_requested)
            else:
                _add_action(menu, 'Enable', name, self.enable_requested)

        else:
            num_enabled = sum(m.enabled for m in self.selection)
            name = 'Selected Modules'
            if len(self.selection) != num_enabled:
                _add_action(menu, 'Enable', name, self.enable_requested)
            if num_enabled:
                _add_action(menu, 'Disable', name, self.disable_requested)

        if not menu.isEmpty():
            menu.popup(QtGui.QCursor.pos())

    def _explore_module(self):
        if not self.selection:
            return
        import a2util

        a2util.explore(self.selection[0].path)


def _add_action(menu, label, name, signal):
    menu.addAction(a2ctrl.Icons.inst().check, f'{label} {name}', signal.emit)
