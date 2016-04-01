'''
Created on Apr 1, 2016

@author: eRiC
'''
import a2ctrl
import logging
from PySide import QtGui, QtCore
from a2ctrl import combo_edit_ui
from functools import partial


class Draw(a2ctrl.DrawCtrl):
    def __init__(self, main, cfg, mod):
        super(Draw, self).__init__(main, cfg, mod)
        self.value = a2ctrl.get_cfg_value(self.cfg, self.userCfg, 'value') or ''
        self._setupUi()

    def _setupUi(self):
        self.layout = QtGui.QHBoxLayout(self)
        self.label_text = self.cfg.get('label', '')
        self.label = QtGui.QLabel(self.label_text, self)
        self.layout.addWidget(self.label)
        
        self.value_ctrl = QtGui.QComboBox()
        self.value_ctrl.setEditable(self.cfg.get('cfg_user_edit', False))

        self.value_ctrl.currentIndexChanged.connect(self.check)

    def check(self, value=None):
        print('value: %s' % value)
        if value is None:
            value = self.value_ctrl.currentText()
        
        # prevent being called double
        if self.value == value:
            return

        self.value = value
        self.mod.setUserCfg(self.cfg, 'value', value)
        self.change('variables')


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
        
        self.connectCfgCtrls(self.ui)
        self.mainWidget.setLayout(self.ui.editLayout)
