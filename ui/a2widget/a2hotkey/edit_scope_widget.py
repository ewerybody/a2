import a2ahk
import a2util
import a2ctrl.qlist
import a2core
from PySide import QtGui, QtCore
from functools import partial
from a2widget.a2hotkey import edit_scope_widget_ui, scope_dialog
#from a2widget.a2hotkey.scope_dialog import ScopeDialog


log = a2core.get_logger(__name__)


class ScopeWidget(QtGui.QWidget):
    changed = QtCore.Signal(dict)

    def __init__(self, parent):
        super(ScopeWidget, self).__init__(parent)
        self.main = parent
        a2ctrl.check_ui_module(edit_scope_widget_ui)
        self.ui = edit_scope_widget_ui.Ui_ScopeWidget()
        self.ui.setupUi(self)
        # self.ui = main.ui
        self.ui.cfg_scopeMode.currentIndexChanged.connect(self.scope_mode_change)
        self.scope_mode_change()

        self.ui.scope_add.clicked.connect(self.show_add_dialog)
        self.ui.scope_delete.clicked.connect(self.delete_scope)
        # self.ui.cfg_scope.mouseDoubleClickEvent = partial(self.scopePopup, change=True)
        # self.ui.cfg_scope.mouseDoubleCli
        #self.scope_update()
        self._dialog = None

    def scope_mode_change(self, index=None):
        if index is None:
            index = self.ui.cfg_scopeMode.currentIndex()
        state = index != 0
        self.ui.cfg_scope.setVisible(state)
        self.ui.scope_add.setVisible(state)
        self.ui.scope_delete.setVisible(state)

    def show_add_dialog(self):
        self._dialog = scope_dialog.ScopeDialog(self)
        self._dialog.okayed.connect(self.dialog_okayed)
        self._dialog.show()

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


if __name__ == '__main__':
    import a2widget.demo.scope_demo
    a2widget.demo.scope_demo.show()
