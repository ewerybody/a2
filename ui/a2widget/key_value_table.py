from a2qt import QtWidgets, QtCore
from a2widget.tools import BlockSignalContext


class KeyValueTable(QtWidgets.QTableWidget):
    """Custom Table widget to handle simple key, value dictionaries."""

    changed = QtCore.Signal()

    def __init__(self, parent):
        super(KeyValueTable, self).__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        # Drag & Drop and sorting would be nice if we had a solution to
        # keep the connected data consistent... so far we better disable it.
        self.setSortingEnabled(False)
        self.setDragEnabled(False)
        self.setAcceptDrops(False)
        # self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setAlternatingRowColors(True)

        self.setColumnCount(2)
        self.setRowCount(1)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        item = QtWidgets.QTableWidgetItem('Keys')
        self.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem('Values')
        self.setHorizontalHeaderItem(1, item)

        self.itemChanged.connect(self._on_change)

    def _on_change(self, item=None):
        """Make checks on item change."""
        self._check_item()
        self.changed.emit()

    def _check_item(self, item=None):
        """
        * Always have a last empty row to add lines.
        * Alert on empty key items.
        * Alert on double key items.
        """
        if item is None:
            is_last_row = True
            row = self.rowCount() - 1
        else:
            row = item.row()
            is_last_row = row == self.rowCount() - 1

        if is_last_row:
            # look at last row
            items = [self.item(row, i) for i in range(self.columnCount())]
            is_empty = all(i.text() == '' for i in items if i is not None)
            if not is_empty:
                self.setRowCount(self.rowCount() + 1)

        if item is not None:
            keyitems = [self.item(i, 0) for i in range(self.rowCount())]
            keys = [i.text() for i in keyitems if i is not None and i is not item]
            if item.text() in keys:
                QtCore.QTimer(self).singleShot(50, self._edit_item)

    def _edit_item(self):
        items = self.selectedItems()
        if len(items) == 1:
            self.editItem(items[0])

    def get_data(self):
        """From rows & columns assemble key: value dictionary."""
        data = {}
        for row in range(self.rowCount()):
            kitem = self.item(row, 0)
            if kitem is None:
                continue
            key = kitem.text()
            if not key:
                continue
            if key in data:
                raise KeyError('Key already lsited! %s' % key)

            vitem = self.item(row, 1)
            val = '' if vitem is None else vitem.text()
            data[key] = val
        return data

    def set_data(self, data):
        """From a key:value dictionary set rows & columns of the table.
        and trigger change"""
        self.set_silent(data)
        self.changed.emit()

    def set_silent(self, data):
        if not isinstance(data, dict):
            raise TypeError(
                'Cannot set data of type "%s" to %s' % (type(data), self.__class__.__name__)
            )

        with BlockSignalContext(self):
            self.clearContents()
            self.setRowCount(max(1, len(data)))
            for i, (key, value) in enumerate(data.items()):
                item = QtWidgets.QTableWidgetItem(str(key))
                self.setItem(i, 0, item)
                item = QtWidgets.QTableWidgetItem(str(value))
                self.setItem(i, 1, item)
        self._check_item()


if __name__ == '__main__':
    from a2widget.demo import key_value_table_demo

    key_value_table_demo.show()
