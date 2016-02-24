'''
Created on Dec 28, 2015

@author: eRiC
'''
import a2ctrl
import logging
from PySide import QtCore, QtGui
from a2ctrl import group_edit_ui


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Draw(QtGui.QGroupBox):
    """
    Group box to bundle multiple other controls or includes that can be
    enabled/disables all at once.
    """
    def __init__(self, cfg, mod):
        super(Draw, self).__init__()
        self.cfg = cfg
        self.mod = mod
        
        userCfg = self.mod.db.get(self.cfg['name'], self.mod.name)
        self.setTitle(self.cfg.get('label', ''))
        self.setCheckable(self.cfg.get('disablable', True))
        self.setChecked(a2ctrl.getCfgValue(self.cfg, userCfg, 'enabled'))
        self.clicked[bool].connect(self.check)

        self.layout = QtGui.QVBoxLayout(self)
        for child in self.cfg.get('children', []):
            self.layout.addWidget(a2ctrl.draw(child, self.mod))

    def check(self, state):
        self.mod.setUserCfg(self.cfg, 'enabled', state)
        self.mod.change(True)


class Edit(a2ctrl.EditCtrl):
    """
    Group box to bundle multiple other controls or includes that can be
    enabled/disables all at once.
    These also use the draw()/edit() functions to create the sub-controls.
    Each EditGroup has its own 'add...' button to create sub controls for itself
    but just without the option to create further groups within. (Although if
        properly implemented it would probably work very well, we will
        not go deeper than this to keep complexity under the lid)
    """
    def __init__(self, cfg, main):
        self.ctrlType = 'Groupbox'
        super(Edit, self).__init__(cfg, main, addLayout=False)
        if 'children' not in self.cfg:
            self.cfg['children'] = []
        
        self.ui = group_edit_ui.Ui_group_edit()
        self.ui.setupUi(self.mainWidget)
        
        controls = []
        for child in self.cfg['children']:
            controls.append(a2ctrl.edit(child, self.main))
        
        controls.append(a2ctrl.EditAddElem(self.main, self.cfg['children']))
        for ctrl in controls:
            self.ui.groupLayout.addWidget(ctrl)
        
        self.connectCfgCtrls(self.ui)
        self.mainWidget.setLayout(self.ui.groupLayout)


if __name__ == '__main__':
    import a2app
    a2app.main()
