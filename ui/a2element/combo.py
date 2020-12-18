from PySide6 import QtCore, QtWidgets

import a2ctrl
import a2util
from a2element import combo_edit_ui, DrawCtrl, EditCtrl


_FLAGS = (
    QtCore.Qt.ItemIsSelectable
    | QtCore.Qt.ItemIsEditable
    | QtCore.Qt.ItemIsDragEnabled
    | QtCore.Qt.ItemIsEnabled
)
_NEW_ITEM_NAME = 'new_item'


class Draw(DrawCtrl):
    def __init__(self, *args):
        super(Draw, self).__init__(*args)
        self.value = self.get_user_value(str)
        self.user_edit = self.cfg.get('user_edit', False)
        self._setup_ui()

    def _setup_ui(self):
        self.layout = QtWidgets.QHBoxLayout(self)
        self.label_text = self.cfg.get('label', '')
        self.label = QtWidgets.QLabel(self.label_text, self)
        self.layout.addWidget(self.label)

        self.value_ctrl = QtWidgets.QComboBox()
        if self.user_edit:
            items = self.get_user_value(list, 'items')
            self.value_ctrl.setEditable(True)
            self.value_ctrl.editTextChanged.connect(self.check_user_items)
        else:
            items = self.cfg.get('items', [])
        self.value_ctrl.addItems(items)
        self.value_ctrl.currentIndexChanged.connect(self.delayed_check)
        self.layout.addWidget(self.value_ctrl)

        if self.value in items:
            index = items.index(self.value)
            self.value_ctrl.setCurrentIndex(index)

    def check(self, *args):
        value = args[0]

        # prevent being called double
        if self.value == value:
            return

        if self.user_edit:
            items = [self.value_ctrl.itemText(i) for i in range(self.value_ctrl.count())]
            self.set_user_value(items, 'items')

        self.value = value
        self.set_user_value(value)
        self.change('variables')

    def check_user_items(self, *args):
        raise NotImplementedError('Ohoh! I thought this was done already! :(')


class Edit(EditCtrl):
    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg, add_layout=False)
        self.helpUrl = self.a2.urls.help_number

        a2ctrl.check_ui_module(combo_edit_ui)
        self.ui = combo_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)

        self.ui.plus_button.clicked.connect(self.add_item)
        self.ui.minus_button.clicked.connect(self.ui.cfg_items.remove_selected)

        self.check_new_name()
        a2ctrl.connect.cfg_controls(self.cfg, self.ui)

        for item in self.ui.cfg_items.iter_items():
            item.setFlags(_FLAGS)

        self.ui.cfg_items.itemChanged.connect(self.update_items)

    def add_item(self):
        self.ui.cfg_items.blockSignals(True)
        new_name = a2util.get_next_free_number(_NEW_ITEM_NAME, self.ui.cfg_items.get_names())
        item = self.ui.cfg_items.add(new_name)
        if item is None:
            return

        item.setFlags(_FLAGS)
        self.ui.cfg_items.blockSignals(False)
        self.update_items()
        self.ui.cfg_items.editItem(item)

    def update_items(self, item=None, items=None):
        if item is not None:
            if isinstance(item, QtWidgets.QListWidgetItem):
                self.ui.cfg_items.select_items([item])
            else:
                self.ui.cfg_items.select_names(item)
        if items is None:
            items = self.ui.cfg_items.get_names()
        self.cfg['items'] = items

    @staticmethod
    def element_name():
        return 'ComboBox'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().combo


def get_settings(_module_key, cfg, db_dict, user_cfg):
    db_dict.setdefault('variables', {})
    value = a2ctrl.get_cfg_value(cfg, user_cfg, typ=str, default='')
    # user values might been stuck in the db only save if allowed.
    if cfg.get('user_edit', False) or value in cfg.get('items', []):
        db_dict['variables'][cfg['name']] = value
