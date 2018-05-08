import a2core
import a2ctrl.qlist
from PySide import QtGui, QtCore
from a2widget.a2hotkey import edit_scope_widget_ui, scope_dialog


log = a2core.get_logger(__name__)
MAX_NON_SCROLL_ITEMS = 5
LIST_LINE_HEIGHT = None


class ScopeWidget(QtGui.QWidget):
    changed = QtCore.Signal()

    def __init__(self, parent):
        super(ScopeWidget, self).__init__(parent)
        # self.main = main
        self._config_dict = None

        # update check done in parent widget for proper order
        self.ui = edit_scope_widget_ui.Ui_ScopeWidget()
        self.ui.setupUi(self)

        self.ui.cfg_scopeMode.currentIndexChanged.connect(self.set_scope_mode)

        self.ui.scope_add.clicked.connect(self.show_add_dialog)
        self.ui.scope_delete.clicked.connect(self.delete_scope)

        self.ui.cfg_scope.itemDoubleClicked.connect(self.show_edit_dialog)

        self.ui.cfg_scope.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.cfg_scope.customContextMenuRequested.connect(self.build_context_menu)
        self.context_menu = QtGui.QMenu(self)

        icons = a2ctrl.Icons.inst()
        self.context_menu.addAction(icons.edit, 'Edit scope item', self.show_edit_dialog)
        self.context_menu.addAction(icons.delete, 'Delete scope item', self.delete_scope)
        self._line_height_set = False

        shortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete),
                                   self.ui.cfg_scope, self.delete_scope)
        shortcut.setContext(QtCore.Qt.WidgetShortcut)

    def set_config(self, config_dict):
        self._config_dict = config_dict

    def set_scope_mode(self, index):
        self._set_scope_mode(index)
        self.changed.emit()

    def _init_scope_mode(self):
        index = self.ui.cfg_scopeMode.currentIndex()
        show_ctrls = self._set_scope_mode(index)
        return show_ctrls

    def _set_scope_mode(self, index):
        show_ctrls = index != 0
        self.ui.cfg_scope.setVisible(show_ctrls)
        self.ui.scope_add.setVisible(show_ctrls)
        self.ui.scope_delete.setVisible(show_ctrls)
        if not self._line_height_set:
            self._set_list_line_height()
        return show_ctrls

    def show_add_dialog(self):
        self._dialog = scope_dialog.ScopeDialog(self)
        self._dialog.okayed.connect(self.on_scope_add)
        self._dialog.show()

    def on_scope_add(self, scope_string):
        item = QtGui.QListWidgetItem(scope_string)
        self.ui.cfg_scope.addItem(item)
        item.setSelected(True)
        self.scope_update()

    def show_edit_dialog(self, item=None):
        if item is None:
            item = self.ui.cfg_scope.selectedItems()[0]
        scope_string = item.text()
        self._dialog = scope_dialog.ScopeDialog(self, scope_string)
        self._dialog.okayed.connect(self.on_scope_edit)
        self._dialog.show()

    def on_scope_edit(self, scope_string):
        item = self.ui.cfg_scope.selectedItems()[0]
        if scope_string != item.text():
            item.setText(scope_string)
            self.scope_update()

    def delete_scope(self):
        selected_idxs = self.ui.cfg_scope.selectedIndexes()
        if selected_idxs:
            this_row = [mi.row() for mi in selected_idxs][0]
            self.ui.cfg_scope.takeItem(this_row)
            self.scope_update()

    def showEvent(self, *args, **kwargs):
        if self._init_scope_mode():
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
        if self._config_dict is not None:
            self._config_dict['scope'] = all_items
        self._set_list_line_height(len(all_items))
        self.changed.emit()

    def build_context_menu(self, pos):
        if self.ui.cfg_scope.selectedItems():
            self.context_menu.popup(self.ui.cfg_scope.mapToGlobal(pos))


if __name__ == '__main__':
    import a2widget.demo.scope_demo
    a2widget.demo.scope_demo.show()
