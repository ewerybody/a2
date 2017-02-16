"""
a2widget.a2item_editor

@created: Sep 26, 2016
@author: eRiC
"""
import a2ctrl.qlist
from PySide import QtGui, QtCore
from a2widget import a2item_editor_ui


class A2ItemEditor(QtGui.QWidget):
    selected_name_changed = QtCore.Signal(str)
    selection_changed = QtCore.Signal(list)
    item_changed = QtCore.Signal(tuple)
    item_deleted = QtCore.Signal(str)

    def __init__(self, *args, **kwargs):
        super(A2ItemEditor, self).__init__(*args, **kwargs)
        a2ctrl.check_ui_module(a2item_editor_ui)
        self.ui = a2item_editor_ui.Ui_A2ItemEditor()
        self.ui.setupUi(self)

        self._selected_name = None

        self.ui.item_list.itemChanged.connect(self.check_item_change)
        self.ui.item_list.keyPressEvent = self.item_list_keyPressEvent
        self.ui.add_entry_button.clicked.connect(self.add_item)
        self.ui.del_entry_button.clicked.connect(self.delete_item)

        self.ui.item_list.itemSelectionChanged.connect(self.selection_change)
        # self.ui.item_list.currentTextChanged.connect(self.selection_change)

    def check_item_change(self, item):
        new_name = item.text()
        old_name = self._selected_name
        if new_name != old_name:
            self._selected_name = new_name
            self.item_changed.emit((old_name, new_name, item))

    @property
    def item_names(self):
        return a2ctrl.qlist.get_items_as_text(self.ui.item_list)

    def fill_items(self, item_list):
        for item_name in item_list:
            self._add_and_setup_item(item_name)

    @property
    def selected_name(self):
        return self._selected_name

    def selection_change(self):
        item_objs = self.ui.item_list.selectedItems()
        self.selection_changed.emit(item_objs)

        text = item_objs[0].text() if item_objs else ''
        if text != self._selected_name:
            self._selected_name = text
            self.selected_name_changed.emit(text)

        self.ui.config_widget.setEnabled(item_objs != [])
        self.ui.del_entry_button.setEnabled(item_objs != [])

    def item_list_keyPressEvent(self, event):
        """
        Capture delete key to remove entries
        """
        if event.key() == QtCore.Qt.Key_Delete:
            self.delete_item()
        return QtGui.QListWidget.keyPressEvent(self.ui.item_list, event)

    def _add_and_setup_item(self, name):
        item = QtGui.QListWidgetItem(name)
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable |
                      QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled)
        self.ui.item_list.addItem(item)
        return item

    def add_item(self):
        new_item_name = ''
        item = self._add_and_setup_item(new_item_name)
        self.ui.item_list.editItem(item)
        a2ctrl.qlist.select_items(self.ui.item_list, item)

    def delete_item(self):
        item_objs = self.ui.item_list.selectedItems()
        for item in item_objs:
            item_row = self.ui.item_list.row(item)
            self.ui.item_list.takeItem(item_row)
        item_name = item_objs[0].text()
        self.item_deleted.emit(item_name)
