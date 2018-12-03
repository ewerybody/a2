from PySide2 import QtGui, QtCore, QtWidgets


class A2List(QtWidgets.QListWidget):
    """
    A simple list widget.
    """
    names_selected = QtCore.Signal(list)
    items_selected = QtCore.Signal(list)
    single_name_selected = QtCore.Signal(str)
    single_item_selected = QtCore.Signal(QtWidgets.QListWidgetItem)
    selection_cleared = QtCore.Signal()

    name_double_clicked = QtCore.Signal(str)
    item_double_clicked = QtCore.Signal(QtWidgets.QListWidgetItem)
    changed = QtCore.Signal()
    items_removed = QtCore.Signal(list)
    context_menu_requested = QtCore.Signal(QtWidgets.QMenu)

    def __init__(self, parent=None, names=None):
        """

        """
        super(A2List, self).__init__(parent)
        self._unique = True
        self._menu = None

        if names:
            self.blockSignals(True)
            self.add(names)
            self.blockSignals(False)

        self.itemSelectionChanged.connect(self._on_selection_change)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete),
                                       self, self.remove_selected)
        shortcut.setContext(QtCore.Qt.WidgetShortcut)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_context_menu_requested)

    def add(self, names):
        current = self.get_names_lower()
        added_something = False

        item = None
        for NAME in ensure_list(names):
            name = NAME.lower()
            if self._unique:
                if name in current:
                    continue
                current.append(name)

            item = QtWidgets.QListWidgetItem(NAME)
            self.addItem(item)

            added_something = True

        if added_something:
            item.setSelected(True)
            self.changed.emit()

        return item

    def set_names(self, names):
        self.clear()
        self.add(names)

    def iter_items(self):
        for i in range(self.count()):
            yield self.item(i)

    def get_items(self):
        return [self.item(i) for i in range(self.count())]

    def get_items_from_names(self, names):
        items = []
        names = [n.lower() for n in ensure_list(names)]
        for item in self.iter_items():
            if item.text().lower() in names:
                items.append(item)
        return items

    def get_names(self):
        return [self.item(i).text() for i in range(self.count())]

    def get_names_lower(self):
        return [self.item(i).text().lower() for i in range(self.count())]

    def contains(self, names):
        current = self.get_names_lower()
        for name in ensure_list(names):
            if name.lower() not in current:
                return False
        return True

    @property
    def unique(self):
        return self._unique

    def set_unique(self, state):
        self._unique = state

    def get_selected_names(self):
        return [i.text() for i in self.selectedItems()]

    def get_selected_items(self):
        return self.selectedItems()

    def set_item_name(self, new_name, item=None):
        if item is None:
            selected = self.get_selected_items()
            if len(selected) != 1:
                raise RuntimeError('Cannot set name! No single selection '
                                   'and No item given!')
            item = selected[0]

        item.setText(new_name)

    def select_names(self, names=None):
        items = self.get_items_from_names(names)
        self.select_items(items)

    def select_items(self, items):
        """
        WTF!?: there is an error when checking if a QListWidgetItem is  in a list
        of QListWidgetItems via "item in item_list":
            NotImplementedError: operator not implemented.
        This uses a workaround getting the objects id()s.
        """
        if not items:
            self.clear_selection()
            return

        item_ids = [id(i) for i in items]

        last_item = None
        for item in self.iter_items():
            if id(item) in item_ids:
                item.setSelected(True)
                last_item = item
            else:
                item.setSelected(False)

        if last_item is not None:
            self.setCurrentItem(last_item)

    def clear_selection(self):
        for item in self.selectedItems():
            item.setSelected(False)

    def _on_selection_change(self):
        items = self.get_selected_items()
        names = self.get_selected_names()
        self.items_selected.emit(items)
        self.names_selected.emit(names)
        if len(items) == 1:
            self.single_item_selected.emit(items[0])
            self.single_name_selected.emit(names[0])
        if len(items) == 0:
            self.selection_cleared.emit()

    def remove_selected(self):
        self.remove_items(self.selectedItems())

    def remove_names(self, names):
        items = self.get_items_from_names(names)
        self.remove_items(items)

    def remove_items(self, items):
        for item in items:
            idx = self.indexFromItem(item)
            self.takeItem(idx.row())
        self.items_removed.emit(items)
        self.changed.emit()

    def _on_context_menu_requested(self, pos):
        if self._menu is None:
            self._menu = QtWidgets.QMenu(self)

        self.context_menu_requested.emit(self._menu)

        if not self._menu.isEmpty():
            self._menu.popup(self.mapToGlobal(pos))

    def set_context_menu(self, menu):
        self._menu = menu


class A2ListCompact(A2List):
    def __init__(self, parent=None, names=None):
        super(A2ListCompact, self).__init__(parent, names)
        self._shown = False
        self.changed.connect(self._set_list_line_height)
        self._max_lines_visible = 5
        self._list_line_height = None
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    @property
    def max_lines_visible(self):
        return self._max_lines_visible

    def set_max_lines_visible(self, num_lines):
        self._max_lines_visible = num_lines
        self._set_list_line_height()

    def showEvent(self, *args, **kwargs):
        self._shown = True
        self._set_list_line_height()
        return QtWidgets.QListWidget.showEvent(self, *args, **kwargs)

    def _init_line_height(self):
        # figure out list_widget row height
        if self._list_line_height is None:
            item = self.item(0)
            dummy_create = item is None
            if dummy_create:
                item = QtWidgets.QListWidgetItem('')
                self.addItem(item)
            self._list_line_height = self.visualItemRect(item).height()
            if dummy_create:
                self.takeItem(0)
        return self._list_line_height

    def _set_list_line_height(self):
        if not self._shown:
            return

        self._init_line_height()
        num_items = self.count()
        h = self._list_line_height * min(max(num_items, 1), self._max_lines_visible)
        h += self._list_line_height / 3
        self.setMinimumHeight(h)
        self.setMaximumHeight(h)
        self._line_height_set = True


def ensure_list(strings):
    if strings is None:
        return []

    if not isinstance(strings, (str, list, tuple, set)):
        raise TypeError('Please provide a string, list, tuple or set')

    if isinstance(strings, str):
        strings = [strings]

    return strings


if __name__ == '__main__':
    import a2widget.demo.a2list_demo
    a2widget.demo.a2list_demo.show()
