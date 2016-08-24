"""
a2ctrl.qlist

@created: Apr 30, 2016
@author: eRiC
"""
from PySide import QtGui

import a2core


log = a2core.get_logger(__name__)


def get_all_items(list_ctrl):
    return [list_ctrl.item(i)for i in range(list_ctrl.count())]


def get_items_as_text(list_ctrl):
    return [list_ctrl.item(i).text() for i in range(list_ctrl.count())]


def select_items(list_ctrl, items):
    if items is None:
        list_ctrl.clearSelection()
        return

    if not isinstance(items, list):
        items = [items]

    if all([isinstance(i, str) for i in items]):
        text_check = True
    elif all([isinstance(i, QtGui.QListWidgetItem) for i in items]):
        text_check = False
        item_ids = [id(i) for i in items]
    else:
        log.error('select_items: All given elements must either be strings or QListWidgetItems!')
        return

    lastitem = None
    for i in range(list_ctrl.count()):
        this = list_ctrl.item(i)
        if text_check and this.text() in items:
            this.setSelected(True)
            lastitem = this
        # WTF!?: there is an error when checking if a QListWidgetItem is
        # in a list of QListWidgetItems via "item in item_list"
        # NotImplementedError: operator not implemented.
        # this is a workaround:
        elif not text_check and id(this) in item_ids:
            this.setSelected(True)
            lastitem = this
        else:
            this.setSelected(False)
    if lastitem is not None:
        list_ctrl.setCurrentItem(lastitem)


def get_selected_as_text(list_ctrl):
    return [i.text() for i in list_ctrl.selectedItems()]


def deselect_all(list_ctrl):
    [i.setSelected(False) for i in list_ctrl.selectedItems()]
