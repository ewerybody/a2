'''
Created on Apr 1, 2016

@author: eRiC
'''
import a2ctrl
import logging
from PySide import QtGui, QtCore
from a2ctrl import combo_edit_ui
from functools import partial


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Draw(a2ctrl.DrawCtrl):
    def __init__(self, main, cfg, mod):
        super(Draw, self).__init__(main, cfg, mod)
        self.value = a2ctrl.get_cfg_value(self.cfg, self.userCfg, 'value') or ''
        self.user_edit = self.cfg.get('user_edit', False)
        self._setupUi()

    def _setupUi(self):
        self.layout = QtGui.QHBoxLayout(self)
        self.label_text = self.cfg.get('label', '')
        self.label = QtGui.QLabel(self.label_text, self)
        self.layout.addWidget(self.label)
        
        self.value_ctrl = QtGui.QComboBox()
        if self.user_edit:
            items = a2ctrl.get_cfg_value(self.cfg, self.userCfg, 'items') or []
            self.value_ctrl.setEditable(True)
            self.value_ctrl.editTextChanged.connect(self.check_user_items)
        else:
            items = self.cfg.get('items', [])
        self.value_ctrl.addItems(items)
        self.value_ctrl.currentIndexChanged[str].connect(self.delayed_check)
        self.layout.addWidget(self.value_ctrl)

        if self.value in items:
            index = items.index(self.value)
            self.value_ctrl.setCurrentIndex(index)
        else:
            log.error('Saved value "%s" not found in item list!' % self.value)

    def check(self, value=None):
        if value is None:
            value = self.value_ctrl.currentText()
        
        # prevent being called double
        if self.value == value:
            return

        if self.user_edit:
            #items = a2ctrl.list_get_all_items_as_text(self.value_ctrl)
            items = [self.value_ctrl.itemText(i) for i in range(self.value_ctrl.count())]
            print('items: %s' % items)
            self.mod.set_user_cfg(self.cfg, 'items', items)

        self.value = value
        self.mod.set_user_cfg(self.cfg, 'value', value)
        self.change('variables')

    def check_user_items(self, *args):
        pass
        

class Edit(a2ctrl.EditCtrl):
    """
    Checkbox to control boolean values for the a2 runtime.
    We might put them to the db and get and fetch from there or first: just write them into
    code directly and start with the variables include.
    """
    def __init__(self, cfg, main, parentCfg):
        self.ctrlType = 'String'
        super(Edit, self).__init__(cfg, main, parentCfg, addLayout=False)
        self.helpUrl = self.a2.urls.help_number
        
        self.ui = combo_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)

        self.ui.internalNameLabel.setMinimumWidth(a2ctrl.labelW)
        self.ui.plus_button.clicked.connect(self.add_item)
        self.ui.minus_button.clicked.connect(self.delete_item)
        self.connect_cfg_controls(self.ui)
        
        for item in a2ctrl.list_get_all_items(self.ui.cfg_items):
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
        
        self.ui.cfg_items.itemChanged.connect(self.update_items)
        self.mainWidget.setLayout(self.ui.editLayout)

    def add_item(self):
        current_items = a2ctrl.list_get_all_items_as_text(self.ui.cfg_items)
        new_item_name = 'new_item'
        item = QtGui.QListWidgetItem(new_item_name)
        current_items.append(new_item_name)
        self.update_items(items=current_items)
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
        self.ui.cfg_items.addItem(item)
        self.ui.cfg_items.editItem(item)

    def delete_item(self):
        item_objs = self.ui.cfg_items.selectedItems()
        sel_items = [i.text() for i in item_objs]
        print('sel_items: %s' % sel_items)
        new_items = [i for i in self.cfg.get('items', []) if i not in sel_items]
        print('new_items: %s' % new_items)
        self.update_items(items=new_items)
        for item in item_objs:
            # doesnt doanything :(
            #self.ui.cfg_items.removeItemWidget(item)
            item_row = self.ui.cfg_items.row(item)
            self.ui.cfg_items.takeItem(item_row)

    def update_items(self, item=None, items=None):
        if item is not None:
            print('item: %s' % item.text())
            a2ctrl.list_select_items(self.ui.cfg_items, item)
            #item.setSelected(True)
        if items is None:
            items = a2ctrl.list_get_all_items_as_text(self.ui.cfg_items)
        self.cfg['items'] = items

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            self.delete_item()
        return a2ctrl.EditCtrl.keyPressEvent(self, event)
