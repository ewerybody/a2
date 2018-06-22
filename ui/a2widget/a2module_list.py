from PySide2 import QtGui, QtCore, QtWidgets

import a2mod
import a2ctrl.qlist
import a2core
from a2widget import a2module_list_ui


DISABLED_GREY = 160
_DISABLED_BRUSH = QtGui.QBrush(QtGui.QColor(DISABLED_GREY, DISABLED_GREY, DISABLED_GREY))
log = a2core.get_logger(__name__)


class A2ModuleList(QtWidgets.QWidget):
    selection_changed = QtCore.Signal(list)

    def __init__(self, parent):
        super(A2ModuleList, self).__init__(parent)
        self.a2 = a2core.A2Obj.inst()
        self.setup_ui()
        self.selection = None
        self.ui.a2module_list_widget.itemSelectionChanged.connect(self.selection_change)
        self._filtered = False
        self._filter_tags = []
        self._show_enabled_only = self.a2.db.get('modlist_show_enabled_only') or False
        self.update_filter()
        self.icon_label = a2ctrl.Icons.inst().label

    def selection_change(self):
        self.selection = [item._module for item in self.ui.a2module_list_widget.selectedItems()]
        self.selection_changed.emit(self.selection)

    def select(self, modules=None):
        self.ui.a2module_list_widget.blockSignals(True)
        a2ctrl.qlist.deselect_all(self.ui.a2module_list_widget)
        selection = []
        lastitem = None
        if modules is not None:
            if isinstance(modules, str):
                modules = [modules]

            for item in modules:
                if isinstance(item, a2mod.Mod):
                    selection.append(item)
                    try:
                        item._item.setSelected(True)
                        lastitem = item._item
                    except AttributeError:
                        pass

                elif isinstance(item, str):
                    srcname, modname = item.split('|', 1)
                    try:
                        mod = self.a2.module_sources[srcname].mods[modname]
                        mod._item.setSelected(True)
                        lastitem = mod._item
                        selection.append(mod)
                    except AttributeError:
                        pass

        if lastitem is not None:
            self.ui.a2module_list_widget.setCurrentItem(lastitem)

        self.ui.a2module_list_widget.blockSignals(False)
        if selection != self.selection:
            self.selection = selection
            self.selection_changed.emit(self.selection)

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
        for source in self.a2.module_sources.values():
            for mod in source.mods.values():
                if mod not in select_mods:
                    if self.is_filtered(mod):
                        continue
                    if self._show_enabled_only and not mod.enabled:
                        continue

                item = QtWidgets.QListWidgetItem(mod.name)
                if mod.enabled:
                    item.setIcon(mod.icon)
                else:
                    item.setIcon(mod.icon.tinted)
                    item.setForeground(_DISABLED_BRUSH)

                item._module = mod
                mod._item = item
                self.ui.a2module_list_widget.addItem(item)

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
        a2ctrl.check_ui_module(a2module_list_ui)
        self.ui = a2module_list_ui.Ui_ModuleList()
        self.ui.setupUi(self)

        self.ui.a2search_x_button.setIcon(a2ctrl.Icons.inst().clear)
        self.ui.search_field.textChanged.connect(self.update_filter)
        self.ui.a2search_x_button.clicked.connect(self.reset_filter)
        self.ui.filter_menu_button.menu_called.connect(self.build_filter_menu)
        self.setLayout(self.ui.module_list_layout)

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
