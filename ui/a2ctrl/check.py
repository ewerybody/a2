'''
Created on Dec 28, 2015

@author: eRiC
'''
import a2ctrl
import logging
from PySide import QtGui
from a2ctrl import checkbox_edit_ui, getCfgValue


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
        self.layout = QtGui.QVBoxLayout(self)
        #self.ctrllayout.setContentsMargins(0, 0, 0, 0)
        state = getCfgValue(self.cfg, userCfg, 'enabled')
        self.checkbox = QtGui.QCheckBox(self.cfg.get('label') or '', self)
        self.checkbox.setChecked(state)
        self.checkbox.clicked.connect(self.check)
        #self.checkbox.setWordWrap(True)
        self.layout.addWidget(self.checkbox)
        #self.checkbox.setMinimumHeight(lenM)
        self.setLayout(self.layout)
        
    def check(self):
        state = self.checkbox.isChecked()
        self.mod.setUserCfg(self.cfg, 'enabled', state)
        self.mod.change()


class Edit(a2ctrl.EditCtrl):
    """
    Checkbox to control boolean values for the a2 runtime.
    We might put them to the db and get and fetch from there or first: just write them into
    code directly and start with the variables include.
    """
    def __init__(self, cfg, main):
        self.ctrlType = 'Checkbox'
        super(Edit, self).__init__(cfg, main, addLayout=False)
        self.helpUrl = self.main.urls.helpCheckbox
        self.cfg = cfg
        
        self.ui = checkbox_edit_ui.Ui_checkbox_edit()
        self.ui.setupUi(self.mainWidget)

        for label in [self.ui.internalNameLabel, self.ui.displayLabelLabel, self.ui.label]:
            label.setMinimumWidth(a2ctrl.labelW)
        
        self.connectCfgCtrls(self.ui)
        self.mainWidget.setLayout(self.ui.verticalLayout)
