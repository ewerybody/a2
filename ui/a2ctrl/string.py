'''
Created on Feb 28, 2016

@author: eRiC
'''
import a2ctrl
import logging
from PySide import QtGui
from a2ctrl import string_edit_ui


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Draw(a2ctrl.DrawCtrl):
    def __init__(self, main, cfg, mod):
        super(Draw, self).__init__(main, cfg, mod)
        self.value = a2ctrl.get_cfg_value(self.cfg, self.userCfg, 'value', str)
        self._setupUi()

    def _setupUi(self):
        self.layout = QtGui.QHBoxLayout(self)
        self.label_text = self.cfg.get('label', '')
        self.label = QtGui.QLabel(self.label_text, self)
        self.value_ctrl = QtGui.QLineEdit(self.value)
        #self.valueCtrl.returnPressed.connect(self.check)
        self.value_ctrl.editingFinished.connect(self.delayed_check)
        #self.valueCtrl.leaveEvent = self.lineLeaveEvent
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.value_ctrl)
        self.setLayout(self.layout)

    def check(self, value=None):
        if value is None:
            value = self.value_ctrl.text()
        
        # prevent being called double
        if self.value == value:
            return

        self.value = value
        self.mod.set_user_cfg(self.cfg, 'value', value)
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
        self.helpUrl = self.a2.urls.help_string
        
        self.ui = string_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)

        self.ui.internalNameLabel.setMinimumWidth(a2ctrl.labelW)
        
        self.check_new_name()
        self.connect_cfg_controls(self.ui)
        self.mainWidget.setLayout(self.ui.editLayout)
