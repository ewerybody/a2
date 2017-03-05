"""
a2element.include

@created: Sep 3, 2016
@author: eRiC
"""
import os
import subprocess
from os.path import exists

from PySide import QtGui, QtCore

import a2ctrl
import a2core
from a2element import EditCtrl


log = a2core.get_logger(__name__)


class Edit(EditCtrl):
    """
    User-invisible control that you only setup in edit-mode for
    unconditional autohotkey script include. If the parent element is
    enabled: it gets included in (enabled group or module).
    """
    def __init__(self, cfg, main, parent_cfg):
        super(Edit, self).__init__(cfg, main, parent_cfg, add_layout=False)
        self.main = main
        self.layout = QtGui.QHBoxLayout(self.mainWidget)
        self.layout.setSpacing(5)
        self.labelCtrl = QtGui.QLabel('script file:')
        self.labelCtrl.setAlignment(QtCore.Qt.AlignRight)
        self.layout.addWidget(self.labelCtrl)
        self.button = QtGui.QPushButton(self.cfg['file'])
        self.buttonMenu = a2ctrl.BrowseScriptsMenu(self.main, self.set_script)
        self.button.setMenu(self.buttonMenu)
        self.layout.addWidget(self.button)

        self.editButton = QtGui.QPushButton('edit script')
        self.editButton.pressed.connect(self.edit_script)
        self.layout.addWidget(self.editButton)

        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.layout.addItem(spacerItem)
        self.mainWidget.setLayout(self.layout)

    def set_script(self, typ, name):
        self.cfg['file'] = name
        self.button.setText(name)

    def edit_script(self):
        if exists(self.main.devset.code_editor):
            subprocess.Popen([self.main.devset.code_editor,
                              os.path.join(self.main.mod.path, self.cfg['file'])])
        else:
            log.error('No code_editor found! Set it up in settings!')

    @staticmethod
    def element_name():
        return 'Include'

    @staticmethod
    def element_icon():
        return a2ctrl.Icons.inst().code


def get_settings(module_key, cfg, db_dict, user_cfg):
    db_dict.setdefault('includes', []).append(cfg['file'])
