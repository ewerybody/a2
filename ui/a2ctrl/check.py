'''
Created on Dec 28, 2015

@author: eRiC
'''
import a2core
import a2ctrl
import logging
from PySide import QtGui
from a2ctrl import checkbox_edit_ui

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
        self.checkbox.setChecked(a2ctrl.get_cfg_value(self.cfg, self.userCfg, 'value') or False)
        self.checkbox.clicked[bool].connect(self.check)
        #self.checkbox.setWordWrap(True)
        self.layout.addWidget(self.checkbox)
        #self.checkbox.setMinimumHeight(lenM)
        self.setLayout(self.layout)
        
    def check(self, state):
        self.mod.setUserCfg(self.cfg, 'value', state)
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
        
        self.ui = a2ctrl.checkbox_edit_ui.Ui_checkbox_edit()
        self.ui.setupUi(self.mainWidget)

        for label in [self.ui.internalNameLabel, self.ui.displayLabelLabel, self.ui.label]:
            label.setMinimumWidth(a2ctrl.labelW)
        
        self.connectCfgCtrls(self.ui)
        self.mainWidget.setLayout(self.ui.verticalLayout)
