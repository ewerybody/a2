from a2qt import QtCore, QtWidgets


class A2ModList(QtWidgets.QTreeWidget):
    items_selected = QtCore.Signal(list)

    def __init__(self, parent=None, names=None):
        super(A2ModList, self).__init__(parent)
        self.itemSelectionChanged.connect(self._on_selection_change)

    def _on_selection_change(self):
        self.items_selected.emit(self.selectedItems())

    def clear_selection(self):
        for item in self.selectedItems():
            item.setSelected(False)
