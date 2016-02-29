'''
Created on Feb 28, 2016

@author: eRiC
'''
import a2ctrl
import logging
from PySide import QtGui
from a2ctrl import string_edit_ui, getCfgValue


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Draw(QtGui.QWidget):
    def __init__(self, cfg, mod):
        super(Draw, self).__init__()
        self.cfg = cfg
        self.mod = mod
        self._setupUi()

    def _setupUi(self):
        userCfg = self.mod.db.get(self.cfg['name'], self.mod.name)
        self.layout = QtGui.QHBoxLayout(self)
        self.label = QtGui.QLabel(self.cfg.get('label', ''), self)
        self.valueCtrl = QtGui.QLineEdit(getCfgValue(self.cfg, userCfg, 'value') or '')
        self.valueCtrl.returnPressed.connect(self.check)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.valueCtrl)
        #self.checkbox.setWordWrap(True)
        #self.checkbox.setMinimumHeight(lenM)
        self.setLayout(self.layout)
        
    def check(self, value=None):
        if value is None:
            value = self.valueCtrl.text()
        self.mod.setUserCfg(self.cfg, 'value', value)
        self.mod.change(True)


class Edit(a2ctrl.EditCtrl):
    """
    Checkbox to control boolean values for the a2 runtime.
    We might put them to the db and get and fetch from there or first: just write them into
    code directly and start with the variables include.
    """
    def __init__(self, cfg, main, parentCfg):
        self.ctrlType = 'String'
        super(Edit, self).__init__(cfg, main, parentCfg, addLayout=False)
        self.helpUrl = self.main.urls.helpCheckbox
        self.cfg = cfg
        
        self.ui = string_edit_ui.Ui_string_edit()
        self.ui.setupUi(self.mainWidget)

        self.ui.internalNameLabel.setMinimumWidth(a2ctrl.labelW)
        
        self.connectCfgCtrls(self.ui)
        self.mainWidget.setLayout(self.ui.stringLayout)
