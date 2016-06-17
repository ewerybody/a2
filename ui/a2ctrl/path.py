"""
a2 path control
"""
import a2ctrl
import logging
from functools import partial
from PySide import QtGui, QtCore
from a2ctrl import path_edit_ui


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Draw(a2ctrl.DrawCtrl):
    def __init__(self, main, cfg, mod):
        super(Draw, self).__init__(main, cfg, mod)
        self.value = self.get_user_value(str)
        self._setupUi()

    def _setupUi(self):
        self.layout = QtGui.QHBoxLayout(self)
        self.label_text = self.cfg.get('label', '')
        self.label = QtGui.QLabel(self.label_text, self)
        self.value_ctrl = QtGui.QLineEdit(self.value)
        if self.cfg.get('writable', False):
            self.value_ctrl.editingFinished.connect(self.delayed_check)
        else:
            self.value_ctrl.setReadOnly(True)
        self.browse_button = QtGui.QPushButton('Browse...')
        self.browse_button.clicked.connect(self.browse)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.value_ctrl)
        self.layout.addWidget(self.browse_button)
        self.setLayout(self.layout)

    def check(self, value=None):
        if value is None:
            value = self.value_ctrl.text()

        # prevent being called double
        if self.value == value:
            return

        self.value = value
        self.set_user_value(value)
        self.change('variables')

    def browse(self):
        save_mode = self.cfg.get('save_mode', False)

        if save_mode:
            filepath = QtGui.QFileDialog.getSaveFileName(self, caption=self.label_text, dir=self.value)
        else:
            filepath = QtGui.QFileDialog.getOpenFileName(self, caption=self.label_text, dir=self.value)

        if filepath[0]:
            self.value_ctrl.setText(filepath[0])
            self.check(filepath[0])


class Edit(a2ctrl.EditCtrl):
    def __init__(self, cfg, main, parentCfg):
        self.ctrlType = 'Path'
        super(Edit, self).__init__(cfg, main, parentCfg, addLayout=False)
        self.helpUrl = self.a2.urls.help_path

        self.ui = path_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)

        self.ui.internalNameLabel.setMinimumWidth(a2ctrl.labelW)

        self.check_new_name()
        self.connect_cfg_controls()

        self.mainWidget.setLayout(self.ui.editLayout)
