'''
Created on Dec 28, 2015

@author: eRiC
'''
import a2ctrl
import logging
from PySide import QtGui
from a2ctrl import check_edit_ui


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Draw(a2ctrl.DrawCtrl):
    def __init__(self, main, cfg, mod):
        super(Draw, self).__init__(main, cfg, mod)
        self._setupUi()

    def _setupUi(self):
        self.layout = QtGui.QVBoxLayout(self)
        self.checkbox = QtGui.QCheckBox(self.cfg.get('label', ''), self)
        value = a2ctrl.get_cfg_value(self.cfg, self.userCfg, 'value', bool)
        self.checkbox.setChecked(value)
        self.checkbox.clicked[bool].connect(self.delayed_check)
        self.layout.addWidget(self.checkbox)
        self.setLayout(self.layout)

    def check(self, state):
        self.mod.set_user_cfg(self.cfg, 'value', state)
        self.change('variables')


class Edit(a2ctrl.EditCtrl):
    """
    Checkbox to control boolean values for the a2 runtime.
    We might put them to the db and get and fetch from there or first: just write them into
    code directly and start with the variables include.
    """
    def __init__(self, cfg, main, parentCfg):
        self.ctrlType = 'Checkbox'
        super(Edit, self).__init__(cfg, main, parentCfg, addLayout=False)
        self.helpUrl = self.a2.urls.helpCheckbox
        
        self.ui = check_edit_ui.Ui_edit()
        self.ui.setupUi(self.mainWidget)

        for label in [self.ui.internalNameLabel, self.ui.displayLabelLabel]:
            label.setMinimumWidth(a2ctrl.labelW)
        
        self.check_new_name()
        self.connect_cfg_controls(self.ui)
        self.mainWidget.setLayout(self.ui.editLayout)
