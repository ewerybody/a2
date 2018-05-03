import a2ctrl.qlist
import a2core
from PySide import QtGui, QtCore
from a2widget.a2hotkey import edit_scope_widget_ui, scope_dialog


log = a2core.get_logger(__name__)


class ScopeWidget(QtGui.QWidget):
    changed = QtCore.Signal()

    def __init__(self, parent):
        super(ScopeWidget, self).__init__(parent)
        # self.main = main

        a2ctrl.check_ui_module(edit_scope_widget_ui)
        self.ui = edit_scope_widget_ui.Ui_ScopeWidget()
        self.ui.setupUi(self)

        self.ui.cfg_scopeMode.currentIndexChanged.connect(self.set_scope_mode)
        self._init_scope_mode()

        self.ui.scope_add.clicked.connect(self.show_add_dialog)
        self.ui.scope_delete.clicked.connect(self.delete_scope)

        self.ui.cfg_scope.itemDoubleClicked.connect(self.show_edit_dialog)

    def set_config(self, config_dict):
        self.config_dict = config_dict

    def _init_scope_mode(self):
        index = self.ui.cfg_scopeMode.currentIndex()
        self._set_scope_mode(index)

    def set_scope_mode(self, index):
        self._set_scope_mode(index)
        self.changed.emit()

    def _set_scope_mode(self, index):
        state = index != 0
        self.ui.cfg_scope.setVisible(state)
        self.ui.scope_add.setVisible(state)
        self.ui.scope_delete.setVisible(state)

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

    def scope_update(self):
        all_items = a2ctrl.qlist.get_items_as_text(self.ui.cfg_scope)
        self.config_dict['scope'] = all_items
        try:
            p = self.main.css_values
            #h = ((max(1, len(all_items)) * p * a2ctrl.uiScale) + 20) * a2ctrl.uiScale
            #self.ui.cfg_scope.setMinimumHeight(h)
        except Exception as error:
            print('error: %s' % error)

        self.changed.emit()


if __name__ == '__main__':
    import a2widget.demo.scope_demo
    a2widget.demo.scope_demo.show()
