'''
Created on Feb 28, 2016

@author: eRiC
'''
import a2ctrl
import logging
import threading
from PySide import QtGui, QtCore
from a2ctrl import string_edit_ui, getCfgValue
import time


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Draw(QtGui.QWidget):
    def __init__(self, cfg, mod):
        super(Draw, self).__init__()
        self.cfg = cfg
        self.mod = mod
        self.userCfg = self.mod.db.get(self.cfg['name'], self.mod.name)
        self.value = getCfgValue(self.cfg, self.userCfg, 'value') or ''
        self._setupUi()

    def _setupUi(self):
        self.layout = QtGui.QHBoxLayout(self)
        self.labelText = self.cfg.get('label', '')
        self.label = QtGui.QLabel(self.labelText, self)
        self.valueCtrl = QtGui.QLineEdit(getCfgValue(self.cfg, self.userCfg, 'value') or '')
        #self.valueCtrl.returnPressed.connect(self.check)
        self.valueCtrl.editingFinished.connect(self.lineLeaveEvent)
        #self.valueCtrl.leaveEvent = self.lineLeaveEvent
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.valueCtrl)
        self.setLayout(self.layout)

    def lineLeaveEvent(self, event=None):
        QtCore.QTimer().singleShot(150, self.check)
    
    def check(self, value=None):
        if value is None:
            value = self.valueCtrl.text()
        
        # prevent being called double
        if self.value == value:
            return

        self.value = value
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
