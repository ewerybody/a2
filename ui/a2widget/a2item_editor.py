"""
a2widget.a2item_editor

@created: Sep 26, 2016
@author: eRiC
"""
import a2ctrl.qlist
from PySide import QtGui, QtCore
from a2widget import a2item_editor_ui


class A2ItemEditor(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(A2ItemEditor, self).__init__(*args, **kwargs)
        a2ctrl.check_ui_module(a2item_editor_ui)
        self.ui = a2item_editor_ui.Ui_A2ItemEditor()
        self.ui.setupUi(self)

        self.ui.item_list.itemChanged.connect(self.update_items)
        self.ui.item_list.keyPressEvent = self.item_list_keyPressEvent
        self.ui.add_entry_button.clicked.connect(self.add_item)
        self.ui.del_entry_button.clicked.connect(self.delete_item)

    def item_list_keyPressEvent(self, event):
        """
        Capture delete key to remove entries
        """
        if event.key() == QtCore.Qt.Key_Delete:
            self.delete_item()
        return QtGui.QListWidget.keyPressEvent(self.ui.item_list, event)

    def add_item(self):
        current_items = a2ctrl.qlist.get_items_as_text(self.ui.item_list)
        new_item_name = ''
        item = QtGui.QListWidgetItem(new_item_name)
        current_items.append(new_item_name)
        self.update_items(items=current_items)
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable |
                      QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled)
        self.ui.item_list.addItem(item)
        self.ui.item_list.editItem(item)

    def delete_item(self):
        item_objs = self.ui.item_list.selectedItems()
        sel_items = [i.text() for i in item_objs]
        all_items = a2ctrl.qlist.get_items_as_text(self.ui.item_list)
        new_items = [i for i in all_items if i not in sel_items]
        self.update_items(items=new_items)
        for item in item_objs:
            # doesnt doanything :(
            # self.ui.cfg_items.removeItemWidget(item)
            item_row = self.ui.item_list.row(item)
            self.ui.item_list.takeItem(item_row)

    def update_items(self, item=None, items=None):
        if item is not None:
            a2ctrl.qlist.select_items(self.ui.item_list, item)
            # item.setSelected(True)
        if items is None:
            items = a2ctrl.qlist.get_items_as_text(self.ui.item_list)
