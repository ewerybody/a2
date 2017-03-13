"""
a2ctrl.module_list
"""
from PySide import QtGui, QtCore

import a2mod
import a2ctrl
import a2ctrl.qlist
import a2core
from a2ctrl.base import Ico
from a2widget import a2module_list_ui


DISABLED_GREY = 160
_DISABLED_BRUSH = QtGui.QBrush(QtGui.QColor(DISABLED_GREY, DISABLED_GREY, DISABLED_GREY))
log = a2core.get_logger(__name__)


class A2ModuleList(QtGui.QWidget):
    selection_changed = QtCore.Signal(list)

    def __init__(self, parent):
        super(A2ModuleList, self).__init__(parent)
        self.a2 = a2core.A2Obj.inst()
        self.setup_ui()
        self.selection = None
        self.ui.a2module_list_widget.itemSelectionChanged.connect(self.selection_change)
        self._filtered = False
        self._show_enabled_only = self.a2.db.get('modlist_show_enabled_only') or False
        self.update_filter()
        self._draw_phase = False

    def selection_change(self):
        if not self._draw_phase:
            self.selection = [item._module for item in self.ui.a2module_list_widget.selectedItems()]
            self.selection_changed.emit(self.selection)

    def select(self, modules=None):
        self._draw_phase = True
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
                    except Exception:
                        pass

                elif isinstance(item, str):
                    srcname, modname = item.split('|', 1)
                    mod = self.a2.module_sources.get(srcname, {}).mods.get(modname, {})
                    try:
                        mod._item.setSelected(True)
                        lastitem = mod._item
                        selection.append(mod)
                    except Exception:
                        pass

        if lastitem is not None:
            self.ui.a2module_list_widget.setCurrentItem(lastitem)

        self._draw_phase = False
        if selection != self.selection:
            self.selection = selection
            self.selection_changed.emit(self.selection)

    def draw_modules(self, select_mods=None):
        """
        Call to refill the module list with items.
        ... to match filtering, module deletion or enabling of module sources.
        """
        self._draw_phase = True
        self.ui.a2module_list_widget.clear()
        for source in self.a2.module_sources.values():
            for mod in source.mods.values():
                if self._filtered and self._filter_phrase not in mod.name.lower():
                    continue
                if self._show_enabled_only and not mod.enabled:
                    continue

                item = QtGui.QListWidgetItem(mod.name)
                if mod.enabled:
                    item.setIcon(mod.icon)
                else:
                    item.setIcon(mod.icon.tinted)
                    item.setForeground(_DISABLED_BRUSH)
                item._module = mod
                mod._item = item
                self.ui.a2module_list_widget.addItem(item)

        if select_mods is None:
            select_mods = self.selection
        self.select(select_mods)

        self._draw_phase = False

    def setup_ui(self):
        a2ctrl.check_ui_module(a2module_list_ui)
        self.ui = a2module_list_ui.Ui_ModuleList()
        self.ui.setupUi(self)

        self.ui.a2search_x_button.setIcon(a2ctrl.Icons().clear)
        self.ui.search_field.textChanged.connect(self.update_filter)
        self.ui.a2search_x_button.clicked.connect(self.reset_filter)
        self.ui.filter_menu_button.clicked.connect(self.build_filter_menu)
        self.setLayout(self.ui.module_list_layout)

        self.filter_menu = QtGui.QMenu()

    def update_filter(self, phrase=''):
        self._filter_phrase = phrase
        self._filtered = phrase != ''
        self.ui.a2search_x_button.setVisible(self._filtered)
        self.draw_modules()

    def reset_filter(self):
        self.ui.search_field.setText('')

    def build_filter_menu(self):
        self.filter_menu.clear()

        action = QtGui.QAction('Only Enabled', self)
        action.setCheckable(True)
        action.setChecked(self._show_enabled_only)
        action.triggered[bool].connect(self.toggle_show_enabled)
        self.filter_menu.addAction(action)

        pos = self.ui.filter_menu_button.mapToGlobal(self.ui.filter_menu_button.pos())
        pos.setY(pos.y() - 5)
        self.filter_menu.popup(pos)

    def toggle_show_enabled(self, state):
        self._show_enabled_only = state
        self.a2.db.set('modlist_show_enabled_only', state)
        self.draw_modules()
