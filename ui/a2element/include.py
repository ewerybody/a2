"""
a2element.include

@created: Sep 3, 2016
@author: eRiC
"""
import os

from PySide import QtGui, QtCore

import a2ctrl
import a2core
from a2element import EditCtrl
from a2element.common import BrowseScriptsMenu


log = a2core.get_logger(__name__)


class Edit(EditCtrl):
    """
    User-invisible control that you only setup in edit-mode for
    unconditional autohotkey script include. If the parent element is
    enabled: it gets included in (enabled group or module).
    """
    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg, add_layout=False)
        self.base_layout = QtGui.QHBoxLayout(self.mainWidget)
        self.base_layout.setSpacing(5)
        self.labelCtrl = QtGui.QLabel('script file:')
        self.labelCtrl.setAlignment(QtCore.Qt.AlignRight)
        self.base_layout.addWidget(self.labelCtrl)
        self.button = QtGui.QPushButton(self.cfg['file'])
        self.button_menu = BrowseScriptsMenu(self.main, self.set_script)
        self.button.setMenu(self.button_menu)
        self.base_layout.addWidget(self.button)

        self.edit_button = QtGui.QPushButton('edit script')
        self.edit_button.clicked.connect(self.edit_script)
        self.edit_button.setIcon(a2ctrl.Icons.inst().edit)
        self.base_layout.addWidget(self.edit_button)

        self.base_layout.addItem(QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum))
        self.mainWidget.setLayout(self.base_layout)

    def set_script(self, typ, name):
        self.cfg['file'] = name
        self.button.setText(name)

    def edit_script(self):
        script_path = os.path.join(self.main.mod.path, self.cfg['file'])
        self.main.edit_code(script_path)

    @staticmethod
    def element_name():
        return 'Include'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().code


def get_settings(module_key, cfg, db_dict, user_cfg):
    db_dict.setdefault('includes', []).append(cfg['file'])
