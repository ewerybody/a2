from PySide2 import QtWidgets, QtCore


class KeyValueTable(QtWidgets.QTableWidget):
    changed = QtCore.Signal()

    def __init__(self, parent):
        super(KeyValueTable, self).__init__(parent)
        self.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self._items = []
        self._setup_ui()

    def _setup_ui(self):
        self.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked
            # QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.DoubleClicked|
            # QtWidgets.QAbstractItemView.EditKeyPressed
            )
        self.setColumnCount(2)
        self.setRowCount(1)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        item = QtWidgets.QTableWidgetItem('Keys')
        self.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem('Values')
        self.setHorizontalHeaderItem(1, item)

        self.itemChanged.connect(self._on_cell_change)

    # def mouseDoubleClickEvent(self, event):
    #     print(event)
    #     event.accept()
    #     return event

    def _on_cell_change(self, item):
        row = item.row()
        if len(self._items) <= row:
            if not item.text():
                return
            self._items.append(['', ''])
            self.setRowCount(self.rowCount() + 1)
        self._items[item.row()][item.column()] = item.text()

    def get_data(self):
        data = {}
        for key, value in self._items:
            if key and value:
                data[key] = value
        return data

    def set_data(self, data):
        self.clear()
        self._items.clear()
        for key, value in data.items():
            self.add_row(key, value)
            self._items.append([key, value])

    def add_row(self, key='', value=''):
        count = self.rowCount()
        self.setRowCount(count + 1)
        item = QtWidgets.QTableWidgetItem(key)
        self.setItem(count - 1, 0, item)
        item = QtWidgets.QTableWidgetItem(value)
        self.setItem(count - 1, 1, item)


if __name__ == '__main__':
    from a2widget.demo import key_value_table_demo
    key_value_table_demo.show()
